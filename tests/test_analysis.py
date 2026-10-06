import pytest

def test_code_input_presence():
    code_sample = "SELECT * FROM users;"
    assert len(code_sample) > 0
