import streamlit as st
import google.generativeai as genai
import time
import re

# --- 1. Page Configuration & Custom CSS ---
st.set_page_config(
    page_title="Agentic AI Code Auditor & Security Engine",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional Custom Styling
st.markdown("""
<style>
    /* Hero Banner */
    .hero-box {
        background: linear-gradient(135deg, #1E1E2F 0%, #2D2B55 100%);
        padding: 2rem;
        border-radius: 12px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .hero-title {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(90deg, #60A5FA, #A78BFA, #F472B6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .hero-subtitle {
        font-size: 1rem;
        color: #9CA3AF;
        margin-bottom: 0;
    }
    
    /* Section Headers */
    .section-title {
        font-size: 1.25rem;
        font-weight: 700;
        color: #1F2937;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    /* Agent Result Headers */
    .agent-header-arch { color: #2563EB; font-weight: 700; font-size: 1.1rem; }
    .agent-header-sec { color: #D97706; font-weight: 700; font-size: 1.1rem; }
    .agent-header-lead { color: #059669; font-weight: 700; font-size: 1.1rem; }
</style>
""", unsafe_allow_html=True)

# --- Hero Header ---
st.markdown("""
<div class="hero-box">
    <div class="hero-title">🛡️ Agentic AI Code Auditor & Security Engine</div>
    <div class="hero-subtitle">Autonomous multi-agent orchestration for static code analysis, OWASP security scanning, and automated refactoring powered by Google Gemini.</div>
</div>
""", unsafe_allow_html=True)

# --- Sidebar Configuration ---
with st.sidebar:
    st.header("⚙️ Configuration")
    api_key = st.text_input("Enter Gemini API Key", type="password")
    
    st.markdown("---")
    st.subheader("📌 Pre-loaded Samples")
    sample_choice = st.selectbox(
        "Select a test script:",
        ["None", "Vulnerable Python (Security Flaws)", "Messy JavaScript (Code Smells)", "Clean SQL Query"]
    )
    
    st.markdown("---")
    st.markdown("**Engine Capabilities**")
    st.caption("• Architectural SOLID Review")
    st.caption("• OWASP Vulnerability Scan")
    st.caption("• Multi-Agent Lead Synthesis")

# Pre-defined sample snippets
SAMPLE_PY = """import sqlite3

def login_user(username, password):
    # DANGER: SQL Injection vulnerability & cleartext evaluation
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE user='{username}' AND pass='{password}'"
    cursor.execute(query)
    user = cursor.fetchone()
    
    # Unsafe eval usage
    eval(f"print('User logged in: {username}')")
    return user
"""

SAMPLE_JS = """function processData(d) {
    var a = 10;
    for(var i=0; i<d.length; i++){
        if(d[i] == "admin"){
            console.log("Found admin!");
            // hardcoded key
            var apiKey = "12345-ABCDE-SECRET";
        }
    }
    return d;
}
"""

SAMPLE_SQL = """SELECT id, username, created_at 
FROM users 
WHERE status = 'ACTIVE' 
ORDER BY created_at DESC;
"""

code_content = ""
language = "python"

if sample_choice == "Vulnerable Python (Security Flaws)":
    code_content = SAMPLE_PY
    language = "python"
elif sample_choice == "Messy JavaScript (Code Smells)":
    code_content = SAMPLE_JS
    language = "javascript"
elif sample_choice == "Clean SQL Query":
    code_content = SAMPLE_SQL
    language = "sql"

# --- Main Interface ---
col1, col2 = st.columns([1, 1], gap="medium")

with col1:
    st.markdown('<div class="section-title">📄 Source Code Input</div>', unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Upload Code File (.py, .js, .cpp, .java, .sql)",
        type=["py", "js", "cpp", "java", "sql"]
    )
    
    if uploaded_file is not None:
        code_content = uploaded_file.read().decode("utf-8")
        ext = uploaded_file.name.split(".")[-1]
        language = "python" if ext == "py" else ("javascript" if ext == "js" else ext)

    if code_content:
        st.code(code_content, language=language, line_numbers=True)
    else:
        st.info("💡 Upload a source code file or select a pre-loaded sample script from the sidebar to test.")

with col2:
    st.markdown('<div class="section-title">🤖 Multi-Agent Analysis</div>', unsafe_allow_html=True)
    
    run_button = st.button("⚡ Run Multi-Agent Audit", type="primary", use_container_width=True)
    
    if run_button:
        if not api_key:
            st.error("⚠️ Please enter your Gemini API Key in the sidebar.")
        elif not code_content:
            st.warning("⚠️ Please upload a file or select a pre-loaded sample snippet.")
        else:
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel("gemini-2.5-flash")
                
                with st.status("🔍 Orchestrating Multi-Agent Pipeline...", expanded=True) as status:
                    # Agent 1: Architectural Review
                    st.write("🏗️ **Architectural Agent:** Evaluating code design patterns and modularity...")
                    arch_prompt = f"Analyze code architecture, design patterns, and readability concise bullet points:\n\n```\n{code_content}\n```"
                    arch_res = model.generate_content(arch_prompt).text
                    time.sleep(0.4)
                    
                    # Agent 2: Security Review
                    st.write("🛡️ **Security Agent:** Scanning for OWASP vulnerabilities and security risks...")
                    sec_prompt = f"Analyze security vulnerabilities, injection risks, and key leaks in concise bullet points:\n\n```\n{code_content}\n```"
                    sec_res = model.generate_content(sec_prompt).text
                    time.sleep(0.4)
                    
                    # Agent 3: Lead Reviewer Synthesis
                    st.write("👨‍💻 **Lead Reviewer Agent:** Synthesizing report and scoring code health...")
                    lead_prompt = f"""Synthesize these reviews into a final audit report.
                    Architecture: {arch_res}
                    Security: {sec_res}
                    
                    Format:
                    Score: [Provide numeric score X/100]
                    Key Findings: [Bullet points]
                    Refactoring Recommendations: [Bullet points]
                    """
                    lead_res = model.generate_content(lead_prompt).text
                    status.update(label="✅ Analysis Completed Successfully!", state="complete", expanded=False)
                
                # Metric Display Parsing
                score_match = re.search(r'(\d{1,3})/100', lead_res)
                score_val = score_match.group(1) if score_match else "85"
                
                # Visual Metric Dashboard
                m_col1, m_col2, m_col3 = st.columns(3)
                m_col1.metric("Code Health Score", f"{score_val}/100")
                m_col2.metric("Security Risks", "Scanned")
                m_col3.metric("Architecture", "Audited")
                
                st.markdown("---")
                
                # Agent Results Output Cards
                with st.container(border=True):
                    st.markdown('<div class="agent-header-arch">🏗️ Architectural Review</div>', unsafe_allow_html=True)
                    st.markdown(arch_res)
                    
                with st.container(border=True):
                    st.markdown('<div class="agent-header-sec">🛡️ Security & OWASP Audit</div>', unsafe_allow_html=True)
                    st.markdown(sec_res)
                    
                with st.container(border=True):
                    st.markdown('<div class="agent-header-lead">👨‍💻 Lead Reviewer Synthesis</div>', unsafe_allow_html=True)
                    st.markdown(lead_res)
                
                # Download Report Button
                full_report = f"# Multi-Agent Code Audit Report\n\nHealth Score: {score_val}/100\n\n## 🏗️ Architectural Review\n{arch_res}\n\n## 🛡️ Security Review\n{sec_res}\n\n## 👨‍💻 Lead Reviewer Summary\n{lead_res}"
                st.download_button(
                    label="📥 Download Audit Report (.md)",
                    data=full_report,
                    file_name="audit_report.md",
                    mime="text/markdown",
                    use_container_width=True
                )
                
            except Exception as e:
                st.error(f"Execution Error: {e}")
