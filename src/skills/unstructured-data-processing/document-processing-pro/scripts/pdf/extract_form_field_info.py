import json
import sys
from typing import Any, Dict, List, Optional, Set

from pypdf import PdfReader


def get_full_annotation_field_id(annotation: Any) -> Optional[str]:
    """Recursively constructs the full field ID for a PDF annotation.

    Args:
        annotation: The PDF annotation object (from pypdf).

    Returns:
        The full dot-separated field ID, or None if no name is found.
    """
    components = []
    while annotation:
        field_name = annotation.get("/T")
        if field_name:
            components.append(field_name)
        annotation = annotation.get("/Parent")
    return ".".join(reversed(components)) if components else None


def make_field_dict(field: Any, field_id: str) -> Dict[str, Any]:
    """Creates a dictionary representation of a PDF form field.

    Args:
        field: The PDF field object (from pypdf).
        field_id: The unique identifier for the field.

    Returns:
        A dictionary containing field metadata (ID, type, options, etc.).
    """
    field_dict = {"field_id": field_id}
    ft = field.get("/FT")
    if ft == "/Tx":
        field_dict["type"] = "text"
    elif ft == "/Btn":
        field_dict["type"] = "checkbox"
        states = field.get("/_States_", [])
        if len(states) == 2:
            if "/Off" in states:
                field_dict["checked_value"] = (
                    states[0] if states[0] != "/Off" else states[1]
                )
                field_dict["unchecked_value"] = "/Off"
            else:
                print(
                    f"Unexpected state values for checkbox `${field_id}`. Its checked and unchecked values may not be correct; if you're trying to check it, visually verify the results."
                )
                field_dict["checked_value"] = states[0]
                field_dict["unchecked_value"] = states[1]
    elif ft == "/Ch":
        field_dict["type"] = "choice"
        states = field.get("/_States_", [])
        field_dict["choice_options"] = [
            {
                "value": state[0],
                "text": state[1],
            }
            for state in states
        ]
    else:
        field_dict["type"] = f"unknown ({ft})"
    return field_dict


def get_field_info(reader: PdfReader) -> List[Dict[str, Any]]:
    """Extracts information about all form fields from a PDF.

    Args:
        reader: A pypdf PdfReader instance.

    Returns:
        A list of dictionaries, each describing a form field and its location.
    """
    fields = reader.get_fields()

    field_info_by_id = {}
    possible_radio_names: Set[str] = set()

    if fields:
        for field_id, field in fields.items():
            if field.get("/Kids"):
                if field.get("/FT") == "/Btn":
                    possible_radio_names.add(field_id)
                continue
            field_info_by_id[field_id] = make_field_dict(field, field_id)

    radio_fields_by_id = {}

    for page_index, page in enumerate(reader.pages):
        annotations = page.get("/Annots", [])
        for ann in annotations:
            field_id = get_full_annotation_field_id(ann)
            if field_id in field_info_by_id:
                field_info_by_id[field_id]["page"] = page_index + 1
                field_info_by_id[field_id]["rect"] = ann.get("/Rect")
            elif field_id in possible_radio_names:
                try:
                    on_values = [v for v in ann["/AP"]["/N"] if v != "/Off"]
                except KeyError:
                    continue
                if len(on_values) == 1:
                    rect = ann.get("/Rect")
                    if field_id not in radio_fields_by_id:
                        radio_fields_by_id[field_id] = {
                            "field_id": field_id,
                            "type": "radio_group",
                            "page": page_index + 1,
                            "radio_options": [],
                        }
                    radio_fields_by_id[field_id]["radio_options"].append(
                        {
                            "value": on_values[0],
                            "rect": rect,
                        }
                    )

    fields_with_location = []
    for field_info in field_info_by_id.values():
        if "page" in field_info:
            fields_with_location.append(field_info)
        else:
            print(
                f"Unable to determine location for field id: {field_info.get('field_id')}, ignoring"
            )

    def sort_key(f: Dict[str, Any]) -> List[Any]:
        """Generates a sort key based on page number and position.

        Args:
            f: Field dictionary.

        Returns:
            A list containing page number and adjusted coordinates.
        """
        if "radio_options" in f:
            rect = f["radio_options"][0]["rect"] or [0, 0, 0, 0]
        else:
            rect = f.get("rect") or [0, 0, 0, 0]
        adjusted_position = [-rect[1], rect[0]]
        return [f.get("page"), adjusted_position]

    sorted_fields = fields_with_location + list(radio_fields_by_id.values())
    sorted_fields.sort(key=sort_key)

    return sorted_fields


def write_field_info(pdf_path: str, json_output_path: str) -> None:
    """Extracts field info from a PDF and writes it to a JSON file.

    Args:
        pdf_path: Path to the input PDF file.
        json_output_path: Path where the JSON output will be saved.
    """
    reader = PdfReader(pdf_path)
    field_info = get_field_info(reader)
    with open(json_output_path, "w") as f:
        json.dump(field_info, f, indent=2)
    print(f"Wrote {len(field_info)} fields to {json_output_path}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: extract_form_field_info.py [input pdf] [output json]")
        sys.exit(1)
    write_field_info(sys.argv[1], sys.argv[2])
