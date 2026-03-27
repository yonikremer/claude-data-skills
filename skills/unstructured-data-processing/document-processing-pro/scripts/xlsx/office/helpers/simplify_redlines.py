"""Simplify tracked changes by merging adjacent w:ins or w:del elements.

Merges adjacent <w:ins> elements from the same author into a single element.
Same for <w:del> elements. This makes heavily-redlined documents easier to
work with by reducing the number of tracked change wrappers.

Rules:
- Only merges w:ins with w:ins, w:del with w:del (same element type)
- Only merges if same author (ignores timestamp differences)
- Only merges if truly adjacent (only whitespace between them)
"""

import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

import defusedxml.minidom

WORD_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"


def simplify_redlines(input_dir: str) -> tuple[int, str]:
    """Simplifies tracked changes by merging adjacent w:ins or w:del elements.

    Args:
        input_dir (str): The directory containing the unpacked DOCX files.

    Returns:
        tuple[int, str]: A tuple containing the number of merged changes and a status message.
    """
    doc_xml = Path(input_dir) / "word" / "document.xml"

    if not doc_xml.exists():
        return 0, f"Error: {doc_xml} not found"

    try:
        dom = defusedxml.minidom.parseString(doc_xml.read_text(encoding="utf-8"))
        root = dom.documentElement

        merge_count = 0

        containers = _find_elements(root, "p") + _find_elements(root, "tc")

        for container in containers:
            merge_count += _merge_tracked_changes_in(container, "ins")
            merge_count += _merge_tracked_changes_in(container, "del")

        doc_xml.write_bytes(dom.toxml(encoding="UTF-8"))
        return merge_count, f"Simplified {merge_count} tracked changes"

    except Exception as e:
        return 0, f"Error: {e}"


def _merge_tracked_changes_in(container: defusedxml.minidom.Element, tag: str) -> int:
    """Merges adjacent compatible tracked changes within a container element.

    Args:
        container (defusedxml.minidom.Element): The container element (e.g., paragraph or table cell).
        tag (str): The tag name of the tracked changes to merge ('ins' or 'del').

    Returns:
        int: The number of merges performed.
    """
    merge_count = 0

    tracked = [
        child
        for child in container.childNodes
        if child.nodeType == child.ELEMENT_NODE and _is_element(child, tag)
    ]

    if len(tracked) < 2:
        return 0

    i = 0
    while i < len(tracked) - 1:
        curr = tracked[i]
        next_elem = tracked[i + 1]

        if _can_merge_tracked(curr, next_elem):
            _merge_tracked_content(curr, next_elem)
            container.removeChild(next_elem)
            tracked.pop(i + 1)
            merge_count += 1
        else:
            i += 1

    return merge_count


def _is_element(node: defusedxml.minidom.Node, tag: str) -> bool:
    """Checks if a node is an element with the given tag name.

    Args:
        node (defusedxml.minidom.Node): The node to check.
        tag (str): The tag name to match.

    Returns:
        bool: True if it matches, False otherwise.
    """
    if node.nodeType != node.ELEMENT_NODE:
        return False
    name = node.localName or node.tagName
    return name == tag or name.endswith(f":{tag}")


def _get_author(elem: defusedxml.minidom.Element) -> str:
    """Gets the author of a tracked change element.

    Args:
        elem (defusedxml.minidom.Element): The tracked change element.

    Returns:
        str: The author name, or an empty string if not found.
    """
    author = elem.getAttribute("w:author")
    if not author:
        for attr in elem.attributes.values():
            if attr.localName == "author" or attr.name.endswith(":author"):
                return attr.value
    return author


def _can_merge_tracked(
    elem1: defusedxml.minidom.Element, elem2: defusedxml.minidom.Element
) -> bool:
    """Checks if two tracked change elements can be merged.

    Args:
        elem1 (defusedxml.minidom.Element): The first element.
        elem2 (defusedxml.minidom.Element): The second element.

    Returns:
        bool: True if they can be merged, False otherwise.
    """
    if _get_author(elem1) != _get_author(elem2):
        return False

    node = elem1.nextSibling
    while node and node != elem2:
        if node.nodeType == node.ELEMENT_NODE:
            return False
        if node.nodeType == node.TEXT_NODE and node.data.strip():
            return False
        node = node.nextSibling

    return True


def _merge_tracked_content(
    target: defusedxml.minidom.Element, source: defusedxml.minidom.Element
) -> None:
    """Moves content from a source tracked change to a target tracked change.

    Args:
        target (defusedxml.minidom.Element): The element to merge content into.
        source (defusedxml.minidom.Element): The element to move content from.
    """
    while source.firstChild:
        child = source.firstChild
        source.removeChild(child)
        target.appendChild(child)


def _find_elements(
    root: defusedxml.minidom.Element, tag: str
) -> list[defusedxml.minidom.Element]:
    """Recursively finds all elements with the given tag name.

    Args:
        root (defusedxml.minidom.Element): The root element to start the search from.
        tag (str): The tag name to search for.

    Returns:
        list[defusedxml.minidom.Element]: A list of matching elements.
    """
    results = []

    def traverse(node):
        if node.nodeType == node.ELEMENT_NODE:
            name = node.localName or node.tagName
            if name == tag or name.endswith(f":{tag}"):
                results.append(node)
            for child in node.childNodes:
                traverse(child)

    traverse(root)
    return results


def get_tracked_change_authors(doc_xml_path: Path) -> dict[str, int]:
    """Gets the count of tracked changes per author in a DOCX XML file.

    Args:
        doc_xml_path (Path): The path to the document.xml file.

    Returns:
        dict[str, int]: A dictionary mapping author names to change counts.
    """
    if not doc_xml_path.exists():
        return {}

    try:
        tree = ET.parse(doc_xml_path)
        root = tree.getroot()
    except ET.ParseError:
        return {}

    namespaces = {"w": WORD_NS}
    author_attr = f"{{{WORD_NS}}}author"

    authors: dict[str, int] = {}
    for tag in ["ins", "del"]:
        for elem in root.findall(f".//w:{tag}", namespaces):
            author = elem.get(author_attr)
            if author:
                authors[author] = authors.get(author, 0) + 1

    return authors


def _get_authors_from_docx(docx_path: Path) -> dict[str, int]:
    """Gets the count of tracked changes per author from a packed DOCX file.

    Args:
        docx_path (Path): The path to the DOCX file.

    Returns:
        dict[str, int]: A dictionary mapping author names to change counts.
    """
    try:
        with zipfile.ZipFile(docx_path, "r") as zf:
            if "word/document.xml" not in zf.namelist():
                return {}
            with zf.open("word/document.xml") as f:
                tree = ET.parse(f)
                root = tree.getroot()

                namespaces = {"w": WORD_NS}
                author_attr = f"{{{WORD_NS}}}author"

                authors: dict[str, int] = {}
                for tag in ["ins", "del"]:
                    for elem in root.findall(f".//w:{tag}", namespaces):
                        author = elem.get(author_attr)
                        if author:
                            authors[author] = authors.get(author, 0) + 1
                return authors
    except (zipfile.BadZipFile, ET.ParseError):
        return {}


def infer_author(
    modified_dir: Path, original_docx: Path, default: str = "Claude"
) -> str:
    """Infers which author added new changes to a document.

    Args:
        modified_dir (Path): The directory containing the modified (unpacked) files.
        original_docx (Path): The path to the original DOCX file.
        default (str, optional): The default author name to use if none found. Defaults to "Claude".

    Returns:
        str: The inferred author name.

    Raises:
        ValueError: If multiple authors added new changes.
    """
    modified_xml = modified_dir / "word" / "document.xml"
    modified_authors = get_tracked_change_authors(modified_xml)

    if not modified_authors:
        return default

    original_authors = _get_authors_from_docx(original_docx)

    new_changes: dict[str, int] = {}
    for author, count in modified_authors.items():
        original_count = original_authors.get(author, 0)
        diff = count - original_count
        if diff > 0:
            new_changes[author] = diff

    if not new_changes:
        return default

    if len(new_changes) == 1:
        return next(iter(new_changes))

    raise ValueError(
        f"Multiple authors added new changes: {new_changes}. "
        "Cannot infer which author to validate."
    )
