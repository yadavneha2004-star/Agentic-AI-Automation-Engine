import pytest
from src.agents.solid_agent import SOLIDAgent
from src.agents.owasp_agent import OWASPAgent

class TestSOLIDAgent:
    def test_initialization(self):
        agent = SOLIDAgent()
        assert agent is not None

    def test_single_responsibility_check(self):
        agent = SOLIDAgent()
        code = """
        class UserManager:
            def create_user(self): pass
            def send_email(self): pass  # Violation!
        """
        result = agent.check_srp(code)
        assert "violation" in result.lower()

class TestOWASPAgent:
    def test_sql_injection_detection(self):
        code = "query = f'SELECT * FROM users WHERE id = {user_id}'"
        result = OWASPAgent().scan(code)
        assert "SQL Injection" in result["vulnerabilities"]
