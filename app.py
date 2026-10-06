import streamlit as st
import google.generativeai as genai
import time
import re

# --- 1. Page Configuration & Custom CSS ---
st.set_page_config(
    page_title="Agentic AI Code Auditor",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# High-Contrast Modern Custom Styling
st.markdown("""
<style>
    /* Global Text Contrast Overrides */
    .stApp {
        background-color: #0F172A;
        color: #F8FAFC;
    }
    
    /* Hero Header */
    .hero-container {
        background: linear-gradient(135deg, #1E1B4B 0%, #312E81 50%, #4338CA 100%);
        padding: 2rem;
        border-radius: 16px;
        border: 1px solid #6366F1;
        box-shadow: 0 10px 25px -5px rgba(99, 102, 241, 0.3);
        margin-bottom: 2rem;
    }
    .hero-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #FFFFFF !important;
        margin-bottom: 0.5rem;
    }
    .hero-subtitle {
        font-size: 1.05rem;
        color: #C7D2FE !important;
        margin-bottom: 0;
    }
    
    /* Section Titles with explicit contrast */
    .section-header {
        font-size: 1.4rem;
        font-weight: 700;
        color: #38BDF8 !important;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Tab & Card Styling */
    .agent-card-arch {
        background-color: #1E293B;
        border-left: 5px solid #38BDF8;
        padding: 1.2rem;
        border-radius: 8px;
        color: #F1F5F9;
    }
    .agent-card-sec {
        background-color: #1E293B;
        border-left: 5px solid #F59E0B;
        padding: 1.2rem;
        border-radius: 8px;
        color: #F1F5F9;
    }
    .agent-card-lead {
        background-color: #1E293B;
        border-left: 5px solid #10B981;
        padding: 1.2rem;
        border-radius: 8px;
        color: #F1F5F9;
    }
</style>
""", unsafe_allow_html=True)

# --- Hero Header ---
st.markdown("""
<div class="hero-container">
    <div class="hero-title">🛡️ Agentic AI Code Auditor & Security Engine</div>
    <div class="hero-subtitle">Autonomous multi-agent orchestration for static code review, OWASP security scanning, and automated refactoring powered by Google Gemini.</div>
</div>
""", unsafe_allow_html=True)

# --- Sidebar Configuration ---
with st.sidebar:
    st.header("⚙️ Configuration")
    api_key = st.text_input("Enter Gemini API Key", type="password", help="Get your free key from Google AI Studio")
    
    st.markdown("---")
    st.subheader("📌 Pre-loaded Samples")
    sample_choice = st.selectbox(
        "Select a test script:",
        ["None", "Vulnerable Python (Security Flaws)", "Messy JavaScript (Code Smells)", "Clean SQL Query"]
    )
    
    st.markdown("---")
    st.markdown("### 🤖 Engine Capabilities")
    st.caption("• Architectural SOLID Review")
    st.caption("• OWASP Security Vulnerability Scan")
    st.caption("• Multi-Agent Lead Review Synthesis")

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

# --- Main Dashboard ---
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown('<div class="section-header">📄 Source Code Input</div>', unsafe_allow_html=True)
    
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
    st.markdown('<div class="section-header">🤖 Multi-Agent Analysis</div>', unsafe_allow_html=True)
    
    run_button = st.button("⚡ Run Multi-Agent Audit", type="primary", use_container_width=True)
    
    if run_button:
        if not api_key:
            st.error("⚠️ Please enter your Gemini API Key in the sidebar.")
        elif not code_content:
            st.warning("⚠️️ Please upload a file or select a pre-loaded sample script.")
        else:
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel("gemini-2.5-flash")
                
                with st.status("🔍 Orchestrating AI Agents...", expanded=True) as status:
                    # Agent 1
                    st.write("🏗️ **Architectural Agent:** Evaluating design patterns, modularity, and readability...")
                    arch_prompt = f"Analyze code architecture, design patterns, and readability. Use clear bullet points:\n\n```\n{code_content}\n```"
                    arch_res = model.generate_content(arch_prompt).text
                    time.sleep(0.3)
                    
                    # Agent 2
                    st.write("🛡️ **Security Agent:** Scanning for OWASP vulnerabilities, injection risks, and secret exposure...")
                    sec_prompt = f"Analyze security vulnerabilities, injection risks, and key leaks. Use clear bullet points:\n\n```\n{code_content}\n```"
                    sec_res = model.generate_content(sec_prompt).text
                    time.sleep(0.3)
                    
                    # Agent 3
                    st.write("👨‍💻 **Lead Reviewer Agent:** Synthesizing final findings and assigning code health score...")
                    lead_prompt = f"""Synthesize these agent reviews into a comprehensive summary report.
                    Architecture Review: {arch_res}
                    Security Audit: {sec_res}
                    
                    Format output clearly with:
                    1. Health Score: Provide numeric score X/100
                    2. Key Executive Summary
                    3. Recommended Refactoring Actions
                    """
                    lead_res = model.generate_content(lead_prompt).text
                    status.update(label="✅ Audit Completed Successfully!", state="complete", expanded=False)
                
                # Parse numeric score
                score_match = re.search(r'(\d{1,3})/100', lead_res)
                score_val = score_match.group(1) if score_match else "80"
                score_int = int(score_val) if score_val.isdigit() else 80
                
                # Metrics Dashboard
                st.markdown("### 📊 Audit Summary Dashboard")
                m1, m2, m3 = st.columns(3)
                m1.metric("Code Health Score", f"{score_int}/100")
                m2.metric("OWASP Security", "Scanned")
                m3.metric("Architecture", "Audited")
                
                st.progress(score_int / 100, text=f"Overall Code Health: {score_int}%")
                st.markdown("---")
                
                # Tabbed Output Section
                st.markdown("### 🔍 Agent Detailed Outputs")
                tab1, tab2, tab3 = st.tabs(["🏗️ Architectural Review", "🛡️ Security Audit", "👨‍💻 Lead Reviewer Report"])
                
                with tab1:
                    st.markdown('<div class="agent-card-arch">', unsafe_allow_html=True)
                    st.markdown(arch_res)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                with tab2:
                    st.markdown('<div class="agent-card-sec">', unsafe_allow_html=True)
                    st.markdown(sec_res)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                with tab3:
                    st.markdown('<div class="agent-card-lead">', unsafe_allow_html=True)
                    st.markdown(lead_res)
                    st.markdown('</div>', unsafe_allow_html=True)
                
                st.markdown("---")
                
                # Download Report Button
                full_report = f"# Multi-Agent Code Audit Report\n\nHealth Score: {score_val}/100\n\n## 🏗️ Architectural Review\n{arch_res}\n\n## 🛡️ Security Review\n{sec_res}\n\n## 👨‍💻 Lead Reviewer Summary\n{lead_res}"
                st.download_button(
                    label="📥 Download Complete Audit Report (.md)",
                    data=full_report,
                    file_name="audit_report.md",
                    mime="text/markdown",
                    use_container_width=True
                )
                
            except Exception as e:
                st.error(f"Execution Error: {e}")
