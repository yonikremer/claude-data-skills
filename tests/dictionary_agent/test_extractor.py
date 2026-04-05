from unittest.mock import MagicMock, patch

from src.dictionary_agent.extractor import extract_text_from_pdf, extract_text_from_pptx


@patch("pdfplumber.open")
def test_extract_text_from_pdf(mock_open, tmp_path):
    # Mock PDF structure
    mock_pdf = mock_open.return_value.__enter__.return_value
    mock_page = MagicMock()
    mock_page.extract_text.return_value = "Extracted Text"
    mock_pdf.pages = [mock_page]

    # Create dummy file path
    dummy_pdf = tmp_path / "dummy.pdf"
    dummy_pdf.write_text("dummy content")

    result = extract_text_from_pdf(str(dummy_pdf))
    assert "Extracted Text" in result


@patch("src.dictionary_agent.extractor.Presentation")
def test_extract_text_from_pptx(mock_presentation, tmp_path):
    # Mock PPTX structure
    mock_prs = mock_presentation.return_value
    mock_slide = MagicMock()
    mock_shape = MagicMock()
    mock_shape.text = "Slide Text"
    mock_slide.shapes = [mock_shape]
    mock_slide.has_notes_slide = True
    mock_slide.notes_slide.notes_text_frame.text = "Notes Text"
    mock_prs.slides = [mock_slide]

    # Create dummy file path
    dummy_pptx = tmp_path / "dummy.pptx"
    dummy_pptx.write_text("dummy content")

    result = extract_text_from_pptx(str(dummy_pptx))
    assert "Slide Text" in result
    assert "Notes Text" in result
