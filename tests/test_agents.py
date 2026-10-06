import pytest

def test_sample_code_loading():
    sample_py = "def login_user(username, password): pass"
    assert "login_user" in sample_py

def test_score_parser():
    import re
    lead_res = "Code Health Score: 85/100"
    score_match = re.search(r'(\d{1,3})/100', lead_res)
    assert score_match is not None
    assert score_match.group(1) == "85"
