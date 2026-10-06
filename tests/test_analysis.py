import pytest
from src.analyzers.code_analyzer import analyze_code

def test_python_file_analysis():
    code = "def hello(): print('world')"
    result = analyze_code(code, "python")
    assert result is not None
    assert "analysis" in result
