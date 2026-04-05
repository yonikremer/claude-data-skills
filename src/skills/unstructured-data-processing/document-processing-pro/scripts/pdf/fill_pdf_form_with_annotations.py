import json
import sys
from typing import List, Tuple

from pypdf import PdfReader, PdfWriter
from pypdf.annotations import FreeText


def transform_from_image_coords(
        bbox: List[float],
        image_width: float,
        image_height: float,
        pdf_width: float,
        pdf_height: float,
) -> Tuple[float, float, float, float]:
    """Transforms bounding box coordinates from image space to PDF space.

    Args:
        bbox: Bounding box in image coordinates [x0, y0, x1, y1].
        image_width: Width of the image the bbox was defined on.
        image_height: Height of the image the bbox was defined on.
        pdf_width: Width of the PDF page.
        pdf_height: Height of the PDF page.

    Returns:
        A tuple of (left, bottom, right, top) in PDF points.
    """
    x_scale = pdf_width / image_width
    y_scale = pdf_height / image_height

    left = bbox[0] * x_scale
    right = bbox[2] * x_scale

    top = pdf_height - (bbox[1] * y_scale)
    bottom = pdf_height - (bbox[3] * y_scale)

    return left, bottom, right, top


def transform_from_pdf_coords(
        bbox: List[float], pdf_height: float
) -> Tuple[float, float, float, float]:
    """Transforms bounding box coordinates within PDF space (y-inversion).

    Args:
        bbox: Bounding box in PDF-relative coordinates [x0, y0, x1, y1].
        pdf_height: Height of the PDF page.

    Returns:
        A tuple of (left, bottom, right, top) in pypdf's expected coordinate system.
    """
    left = bbox[0]
    right = bbox[2]

    pypdf_top = pdf_height - bbox[1]
    pypdf_bottom = pdf_height - bbox[3]

    return left, pypdf_bottom, right, pypdf_top


def fill_pdf_form(
        input_pdf_path: str, fields_json_path: str, output_pdf_path: str
) -> None:
    """Fills a PDF form by adding FreeText annotations.

    Reads field definitions and text values from a JSON file and overlays
    them onto the PDF at specified coordinates.

    Args:
        input_pdf_path: Path to the input PDF file.
        fields_json_path: Path to the JSON file with field definitions and text.
        output_pdf_path: Path where the resulting PDF will be saved.
    """

    with open(fields_json_path, "r") as f:
        fields_data = json.load(f)

    reader = PdfReader(input_pdf_path)
    writer = PdfWriter()

    writer.append(reader)

    pdf_dimensions = {}
    for i, page in enumerate(reader.pages):
        mediabox = page.mediabox
        pdf_dimensions[i + 1] = [mediabox.width, mediabox.height]

    annotations = []
    for field in fields_data["form_fields"]:
        page_num = field["page_number"]

        page_info = next(
            p for p in fields_data["pages"] if p["page_number"] == page_num
        )
        pdf_width, pdf_height = pdf_dimensions[page_num]

        if "pdf_width" in page_info:
            transformed_entry_box = transform_from_pdf_coords(
                field["entry_bounding_box"], float(pdf_height)
            )
        else:
            image_width = page_info["image_width"]
            image_height = page_info["image_height"]
            transformed_entry_box = transform_from_image_coords(
                field["entry_bounding_box"],
                image_width,
                image_height,
                float(pdf_width),
                float(pdf_height),
            )

        if "entry_text" not in field or "text" not in field["entry_text"]:
            continue
        entry_text = field["entry_text"]
        text = entry_text["text"]
        if not text:
            continue

        font_name = entry_text.get("font", "Arial")
        font_size = str(entry_text.get("font_size", 14)) + "pt"
        font_color = entry_text.get("font_color", "000000")

        annotation = FreeText(
            text=text,
            rect=transformed_entry_box,
            font=font_name,
            font_size=font_size,
            font_color=font_color,
            border_color=None,
            background_color=None,
        )
        annotations.append(annotation)
        writer.add_annotation(page_number=page_num - 1, annotation=annotation)

    with open(output_pdf_path, "wb") as output:
        writer.write(output)

    print(f"Successfully filled PDF form and saved to {output_pdf_path}")
    print(f"Added {len(annotations)} text annotations")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(
            "Usage: fill_pdf_form_with_annotations.py [input pdf] [fields.json] [output pdf]"
        )
        sys.exit(1)
    input_pdf_arg = sys.argv[1]
    fields_json_arg = sys.argv[2]
    output_pdf_arg = sys.argv[3]

    fill_pdf_form(input_pdf_arg, fields_json_arg, output_pdf_arg)
