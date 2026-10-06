import streamlit as st
import google.generativeai as genai
import time
import re

# --- 1. Page Configuration & Modern Glassmorphism CSS ---
st.set_page_config(
    page_title="Agentic AI Code Auditor",
    page_icon="🛡️️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom High-End Modern Styling
st.markdown("""
<style>
    /* Dark Glassmorphism App Background */
    .stApp {
        background: #0B0F19;
        color: #F3F4F6;
    }
    
    /* Hero Banner Styling */
    .hero-card {
        background: linear-gradient(135deg, rgba(30, 27, 75, 0.7) 0%, rgba(49, 46, 129, 0.7) 100%);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(99, 102, 241, 0.3);
        border-radius: 16px;
        padding: 2.5rem;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }
    .hero-title {
        font-size: 2.4rem;
        font-weight: 800;
        background: linear-gradient(90deg, #6366F1 0%, #A855F7 50%, #EC4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .hero-subtitle {
        font-size: 1.1rem;
        color: #9CA3AF !important;
        line-height: 1.5;
    }

    /* Section Headers */
    .section-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: #38BDF8 !important;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    /* Agent Output Cards */
    .agent-box {
        background: rgba(17, 24, 39, 0.8);
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
        margin-bottom: 1rem;
    }
    .agent-box-arch { border-top: 4px solid #38BDF8; }
    .agent-box-sec { border-top: 4px solid #F59E0B; }
    .agent-box-lead { border-top: 4px solid #10B981; }

    /* Custom Metric Badges */
    .metric-card {
        background: #111827;
        border: 1px solid #1F2937;
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 800;
        color: #6366F1;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #9CA3AF;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
</style>
""", unsafe_allow_html=True)

# --- Hero Banner ---
st.markdown("""
<div class="hero-card">
    <div class="hero-title">🛡️ Agentic AI Code Auditor & Security Engine</div>
    <div class="hero-subtitle">Autonomous multi-agent orchestration for static code analysis, OWASP security scanning, and automated refactoring powered by Google Gemini.</div>
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
    st.caption("• OWASP Vulnerability Scan")
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
            st.warning("⚠️ Please upload a file or select a pre-loaded sample script.")
        else:
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel("gemini-2.5-flash")
                
                with st.status("🔍 Orchestrating AI Agents...", expanded=True) as status:
                    # Agent 1
                    st.write("🏗️ **Architectural Agent:** Evaluating design patterns, modularity, and readability...")
                    arch_prompt = f"Analyze code architecture, design patterns, and readability concise bullet points:\n\n```\n{code_content}\n```"
                    arch_res = model.generate_content(arch_prompt).text
                    time.sleep(0.3)
                    
                    # Agent 2
                    st.write("🛡️ **Security Agent:** Scanning for OWASP vulnerabilities, injection risks, and key exposure...")
                    sec_prompt = f"Analyze security vulnerabilities, injection risks, and key leaks in concise bullet points:\n\n```\n{code_content}\n```"
                    sec_res = model.generate_content(sec_prompt).text
                    time.sleep(0.3)
                    
                    # Agent 3
                    st.write("👨‍💻 **Lead Reviewer Agent:** Synthesizing final findings and assigning code health score...")
                    lead_prompt = f"""Synthesize these reviews into a summary report.
                    Architecture: {arch_res}
                    Security: {sec_res}
                    
                    Format:
                    Score: [Provide numeric score X/100]
                    Key Findings: [Bullet points]
                    Recommendations: [Bullet points]
                    """
                    lead_res = model.generate_content(lead_prompt).text
                    status.update(label="✅ Audit Completed Successfully!", state="complete", expanded=False)
                
                # Parse numeric score
                score_match = re.search(r'(\d{1,3})/100', lead_res)
                score_val = score_match.group(1) if score_match else "80"
                score_int = int(score_val) if score_val.isdigit() else 80
                
                # Custom Metric Dashboard
                st.markdown("### 📊 Executive Metrics")
                m1, m2, m3 = st.columns(3)
                with m1:
                    st.markdown(f'<div class="metric-card"><div class="metric-value">{score_int}/100</div><div class="metric-label">Health Score</div></div>', unsafe_allow_html=True)
                with m2:
                    st.markdown('<div class="metric-card"><div class="metric-value">OWASP</div><div class="metric-label">Security Scan</div></div>', unsafe_allow_html=True)
                with m3:
                    st.markdown('<div class="metric-card"><div class="metric-value">SOLID</div><div class="metric-label">Architecture</div></div>', unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                st.progress(score_int / 100, text=f"Overall Code Health: {score_int}%")
                st.markdown("---")
                
                # Tabbed Detailed Findings
                st.markdown("### 🔍 Agent Detailed Outputs")
                tab1, tab2, tab3 = st.tabs(["🏗️️ Architectural Review", "🛡️ Security Audit", "👨‍💻 Lead Reviewer Report"])
                
                with tab1:
                    st.markdown('<div class="agent-box agent-box-arch">', unsafe_allow_html=True)
                    st.markdown(arch_res)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                with tab2:
                    st.markdown('<div class="agent-box agent-box-sec">', unsafe_allow_html=True)
                    st.markdown(sec_res)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                with tab3:
                    st.markdown('<div class="agent-box agent-box-lead">', unsafe_allow_html=True)
                    st.markdown(lead_res)
                    st.markdown('</div>', unsafe_allow_html=True)
                
                st.markdown("---")
                
                # Download Report Button
                full_report = f"# Multi-Agent Code Audit Report\n\nHealth Score: {score_val}/100\n\n## 🏗️ Architectural Review\n{arch_res}\n\n## 🛡️ Security Review\n{sec_res}\n\n## 👨‍‍💻 Lead Reviewer Summary\n{lead_res}"
                st.download_button(
                    label="📥 Download Complete Audit Report (.md)",
                    data=full_report,
                    file_name="audit_report.md",
                    mime="text/markdown",
                    use_container_width=True
                )
                
            except Exception as e:
                st.error(f"Execution Error: {e}")
