import pytest
import os
from graph_sieve.extractor import extract_all
from graph_sieve.hebrew_utils import normalize_rtl_text

def test_extract_windows_1255_hebrew():
    # Create a temporary file with Windows-1255 encoding
    test_file = "tests/data/hebrew_1255.txt"
    os.makedirs(os.path.dirname(test_file), exist_ok=True)
    
    # "פרויקט מיקום" in windows-1255
    hebrew_text = "פרויקט מיקום"
    
    # Write as windows-1255
    with open(test_file, "wb") as f:
        f.write(hebrew_text.encode('windows-1255'))
        
    # Extract using the new logic
    extracted = extract_all(test_file)
    
    # It should correctly decode the Windows-1255 text 
    # and then bidi normalize it. The bidi normalization 
    # of "פרויקט מיקום" will reverse the string for display.
    # In normalized form, the words appear reversed.
    expected = normalize_rtl_text(hebrew_text)
    
    assert expected in extracted

def test_rtl_normalization():
    # Test that bidi algorithm works
    original = "פרויקט"
    normalized = normalize_rtl_text(original)
    
    # The string should be reversed
    assert normalized == original[::-1]
