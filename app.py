import streamlit as st
import google.generativeai as genai
import time

# --- 1. Page Configuration & Custom CSS ---
st.set_page_config(
    page_title="Agentic AI Code Auditor & Security Engine",
    page_icon="🛡️",
    layout="wide"
)

# Custom Styling for a vibrant, modern aesthetic
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 800;
        background: -webkit-linear-gradient(45deg, #FF4B4B, #FF8C00, #4B6CB7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #555555;
        margin-bottom: 1.5rem;
    }
    .agent-card {
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 0.8rem;
        color: #111111;
        font-weight: 500;
    }
    .agent-arch { background-color: #E3F2FD; border-left: 5px solid #2196F3; }
    .agent-sec { background-color: #FFF3E0; border-left: 5px solid #FF9800; }
    .agent-lead { background-color: #E8F5E9; border-left: 5px solid #4CAF50; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">🛡️️ Agentic AI Code Auditor & Security Engine</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Multi-agent orchestration engine for static code analysis, OWASP security scanning, and automated refactoring powered by Google Gemini.</div>', unsafe_allow_html=True)

# --- Sidebar Configuration ---
st.sidebar.header("⚙️ Configuration")
api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

st.sidebar.markdown("---")
st.sidebar.subheader("📌 Pre-loaded Sample Code")
sample_choice = st.sidebar.selectbox(
    "Or select a sample file to test:",
    ["None", "Vulnerable Python (Security Flaws)", "Messy JavaScript (Code Smells)", "Clean SQL Query"]
)

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

# Determine code input content and language
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

# --- Main UI Layout ---
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📄 Input Source Code")
    uploaded_file = st.file_uploader(
        "Upload Code File (.py, .js, .cpp, .java, .sql)",
        type=["py", "js", "cpp", "java", "sql"]
    )
    
    if uploaded_file is not None:
        code_content = uploaded_file.read().decode("utf-8")
        ext = uploaded_file.name.split(".")[-1]
        language = "python" if ext == "py" else ("javascript" if ext == "js" else ext)

    if code_content:
        st.code(code_content, language=language)
    else:
        st.info("Upload a source code file or select a pre-loaded sample from the sidebar to get started.")

with col2:
    st.subheader("🤖 Multi-Agent Analysis")
    
    run_button = st.button("🚀 Run Multi-Agent Audit", type="primary", use_container_width=True)
    
    if run_button:
        if not api_key:
            st.error("Please enter your Gemini API Key in the sidebar.")
        elif not code_content:
            st.warning("Please upload a file or select a sample code snippet.")
        else:
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel("gemini-2.5-flash")
                
                with st.status(" Orchestrating AI Agents...", expanded=True) as status:
                    # Agent 1: Architectural Review
                    st.write("🏗️ **Architectural Agent:** Evaluating code structure, design patterns, and readability...")
                    arch_prompt = f"Analyze the following code for software architecture, readability, and design patterns. Keep response concise:\n\n```\n{code_content}\n```"
                    arch_res = model.generate_content(arch_prompt).text
                    time.sleep(0.5)
                    
                    # Agent 2: Security Review
                    st.write("🛡️ **Security Agent:** Scanning for OWASP vulnerabilities and security flaws...")
                    sec_prompt = f"Analyze the following code for security vulnerabilities, hardcoded secrets, and OWASP risks. Keep response concise:\n\n```\n{code_content}\n```"
                    sec_res = model.generate_content(sec_prompt).text
                    time.sleep(0.5)
                    
                    # Agent 3: Lead Reviewer Synthesis
                    st.write("👨‍💻 **Lead Reviewer Agent:** Synthesizing final report and calculating health score...")
                    lead_prompt = f"""Synthesize these two reviews into a final summary report:
                    Architectural Audit: {arch_res}
                    Security Audit: {sec_res}
                    
                    Format output clearly in Markdown with:
                    1. Code Health Score (0-100)
                    2. Top Key Findings (Bullet points)
                    3. Recommended Refactoring Fixes
                    """
                    lead_res = model.generate_content(lead_prompt).text
                    status.update(label="✅ Audit Complete!", state="complete", expanded=False)
                
                # Display Agent Outputs in Colorful Cards
                st.markdown('<div class="agent-card agent-arch"><b>🏗️ Architectural Agent Output</b><br>' + arch_res.replace('\n', '<br>') + '</div>', unsafe_allow_html=True)
                st.markdown('<div class="agent-card agent-sec"><b>🛡️ Security Agent Output</b><br>' + sec_res.replace('\n', '<br>') + '</div>', unsafe_allow_html=True)
                st.markdown('<div class="agent-card agent-lead"><b>👨‍💻 Lead Reviewer Synthesis</b><br>' + lead_res.replace('\n', '<br>') + '</div>', unsafe_allow_html=True)
                
                # Download Report Feature
                full_report = f"# Multi-Agent Code Audit Report\n\n## 🏗️ Architectural Review\n{arch_res}\n\n## 🛡️ Security Review\n{sec_res}\n\n## 👨‍💻 Lead Reviewer Summary\n{lead_res}"
                st.download_button(
                    label="📥 Download Audit Report (.md)",
                    data=full_report,
                    file_name="audit_report.md",
                    mime="text/markdown",
                    use_container_width=True
                )
                
            except Exception as e:
                st.error(f"An error occurred during execution: {e}")
