# Architecture Documentation

## System Overview
The Agentic AI Code Auditor is an autonomous multi-agent orchestration engine that performs static code analysis, security vulnerability detection, and automated refactoring recommendations.

### Components
1. **Frontend**: Streamlit interactive dashboard with real-time status indicators and downloadable Markdown reports.
2. **Backend**: Multi-Agent Engine powered by Google Gemini API.
3. **Analysis Modules**: Architectural SOLID review, OWASP Top 10 security scanning, and code smell analysis.
4. **Synthesis Module**: Executive report generation with code health scoring.

### Data Flow
1. **Input Phase**: Source code (`.py`, `.js`, `.cpp`, `.java`, `.sql`) is uploaded or chosen from pre-loaded samples.
2. **Orchestration Phase**: The orchestrator triggers specialized agents sequentially:
   - **Architectural Agent**: Evaluates structural patterns and SOLID principles.
   - **Security Agent**: Scans for OWASP vulnerabilities and hardcoded secrets.
3. **Synthesis Phase**: The Lead Reviewer Agent aggregates feedback, computes a code health score (0–100), and outputs structured Markdown.
4. **Export Phase**: Users view interactive visual breakdowns and download the final audit report (`.md`).

### Agent Roles

#### SOLID Review Agent
- Checks Single Responsibility Principle (SRP)
- Validates Open/Closed Principle (OCP)
- Reviews Liskov Substitution Principle (LSP)
- Ensures Interface Segregation Principle (ISP)
- Analyzes Dependency Inversion Principle (DIP)

#### OWASP Security Agent
- Injection vulnerabilities (SQL, Command Injection)
- Cross-Site Scripting (XSS)
- Broken Authentication & Access Control
- Sensitive Data Exposure & Hardcoded Keys
- Security Misconfigurations & Logging Issues

#### Code Quality Agent
- Performance optimization & algorithmic complexity
- Code smell detection & modularity
- Documentation completeness & naming conventions
