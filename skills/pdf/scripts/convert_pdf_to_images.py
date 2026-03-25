import os
import sys

from pdf2image import convert_from_path


def convert(pdf_path: str, output_dir: str, max_dim: int = 1000) -> None:
    """Converts a PDF file into a set of PNG images, one per page.

    Args:
        pdf_path: Path to the input PDF file.
        output_dir: Directory where the output images will be saved.
        max_dim: Maximum dimension (width or height) for the output images.
            Images larger than this will be resized proportionally.
    """
    images = convert_from_path(pdf_path, dpi=200)

    for i, image in enumerate(images):
        width, height = image.size
        if width > max_dim or height > max_dim:
            scale_factor = min(max_dim / width, max_dim / height)
            new_width = int(width * scale_factor)
            new_height = int(height * scale_factor)
            image = image.resize((new_width, new_height))

        image_path = os.path.join(output_dir, f"page_{i + 1}.png")
        image.save(image_path)
        print(f"Saved page {i + 1} as {image_path} (size: {image.size})")

    print(f"Converted {len(images)} pages to PNG images")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: convert_pdf_to_images.py [input pdf] [output directory]")
        sys.exit(1)
    pdf_path = sys.argv[1]
    output_directory = sys.argv[2]
    convert(pdf_path, output_directory)
