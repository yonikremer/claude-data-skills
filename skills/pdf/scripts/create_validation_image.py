import json
import sys

from PIL import Image, ImageDraw


def create_validation_image(
    page_number: int, fields_json_path: str, input_path: str, output_path: str
) -> None:
    """Creates a validation image with bounding boxes drawn over it.

    Draws red rectangles for entry boxes and blue rectangles for label boxes
    defined in a fields JSON file for a specific page.

    Args:
        page_number: The page number to process.
        fields_json_path: Path to the JSON file containing form field definitions.
        input_path: Path to the input image (e.g., a page from the PDF).
        output_path: Path where the validation image will be saved.
    """
    with open(fields_json_path, "r") as f:
        data = json.load(f)

        img = Image.open(input_path)
        draw = ImageDraw.Draw(img)
        num_boxes = 0

        for field in data["form_fields"]:
            if field["page_number"] == page_number:
                entry_box = field["entry_bounding_box"]
                label_box = field["label_bounding_box"]
                draw.rectangle(entry_box, outline="red", width=2)
                draw.rectangle(label_box, outline="blue", width=2)
                num_boxes += 2

        img.save(output_path)
        print(
            f"Created validation image at {output_path} with {num_boxes} bounding boxes"
        )


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print(
            "Usage: create_validation_image.py [page number] [fields.json file] [input image path] [output image path]"
        )
        sys.exit(1)
    page_number_arg = int(sys.argv[1])
    fields_json_path_arg = sys.argv[2]
    input_image_path_arg = sys.argv[3]
    output_image_path_arg = sys.argv[4]
    create_validation_image(
        page_number_arg,
        fields_json_path_arg,
        input_image_path_arg,
        output_image_path_arg,
    )
