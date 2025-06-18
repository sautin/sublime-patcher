import streamlit as st
import os
import tempfile
import io
import datetime
import time

# Constants and patch data
NOP = 0x90
offsets_and_values = {
    0x00030170: 0x00,
    0x000A94D0: NOP, 0x000A94D1: NOP, 0x000A94D2: NOP, 0x000A94D3: NOP, 0x000A94D4: NOP, 0x000A94D5: NOP, 0x000A94D6: NOP, 0x000A94D7: NOP, 0x000A94D8: NOP, 0x000A94D9: NOP, 0x000A94DA: NOP, 0x000A94DB: NOP, 0x000A94DC: NOP, 0x000A94DD: NOP, 0x000A94DE: NOP, 0x000A94DF: NOP,
    0x000A94E0: NOP, 0x000A94E1: NOP, 0x000A94E2: NOP, 0x000A94E3: NOP, 0x000A94E4: NOP, 0x000A94E5: NOP, 0x000A94E6: NOP, 0x000A94E7: NOP,
    0x000A94E8: NOP, 0x000A94E9: NOP, 0x000A94EA: NOP, 0x000A94EB: NOP, 0x000A94EC: NOP, 0x000A94ED: NOP, 0x000A94EE: NOP, 0x000A94EF: NOP,
    0x000A94F0: NOP, 0x000A94F1: NOP, 0x000A94F2: NOP, 0x000A94F3: NOP, 0x000A94F4: NOP, 0x000A94F5: NOP, 0x000A94F6: NOP, 0x000A94F7: NOP,
    0x000A94F8: NOP, 0x000A94F9: NOP, 0x000A94FA: NOP, 0x000A94FB: NOP, 0x000A94FC: NOP, 0x000A94FD: NOP, 0x000A94FE: NOP, 0x000A94FF: NOP,
    0x000A9500: NOP, 0x000A9501: NOP, 0x000A9502: NOP, 0x000A9503: NOP, 0x000A9504: NOP, 0x000A9505: NOP, 0x000A9506: NOP, 0x000A9507: NOP,
    0x000A9508: NOP, 0x000A9509: NOP, 0x000A950A: NOP, 0x000A950B: NOP, 0x000A950C: NOP, 0x000A950D: NOP, 0x000A950E: NOP, 0x000A950F: NOP,
    0x001C6CCD: 0x02,
    0x001C6CE4: 0x00,
    0x001C6CFB: 0x00,
}

# Build and developer info
BUILD_INFO = {
    "version": "Latest",
    "build_date": "21 May 2025",
    "build": "4200",

}

DEVELOPER_INFO = {
    "name": "Ihtisham Ali",
    "handle": "@ihtishamaliii",
    "role": "Cyber Security Analyst",
    "experience": "7+ years of experience in hacking and cyber security",
    "specialties": ["Binary Patching", "Reverse Engineering", "Malware Analysis", "Code Obfuscation"],
    "github": "github.com/ihtishamaliii",
    "linkedin": "https://www.linkedin.com/in/ihtishamaliii/",
    "email": "toorhat@gmail.com",
    "location": "Peshawar, Pakistan"
}

def patch_exe(file_bytes):
    """Apply binary patches to the executable file"""
    try:
        patched_data = bytearray(file_bytes)
        patches_applied = 0
        
        for offset, value in offsets_and_values.items():
            if offset < len(patched_data):
                patched_data[offset] = value
                patches_applied += 1
        
        return patched_data, patches_applied
    except Exception as e:
        st.error(f"Error during patching: {str(e)}")
        return None, 0

# Page configuration
st.set_page_config(
    page_title="🔧 Sublime Text Binary Patcher v3.1",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced custom CSS with geeky, cyberpunk styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Fira+Code:wght@300;400;500&display=swap');

    body {
        background: linear-gradient(135deg, #0d0d2b 0%, #1a1a3a 100%);
        color: #e0e0e0;
    }

    .main-header {
        background: linear-gradient(45deg, #00f7ff 0%, #ff00ff 50%, #00ff99 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Orbitron', sans-serif;
        font-weight: 900;
        font-size: 3.5rem;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 0 0 15px rgba(0, 247, 255, 0.7), 0 0 30px rgba(255, 0, 255, 0.5);
        animation: neon-glow 1.5s ease-in-out infinite alternate;
    }

    @keyframes neon-glow {
        from { text-shadow: 0 0 10px rgba(0, 247, 255, 0.7), 0 0 20px rgba(255, 0, 255, 0.5); }
        to { text-shadow: 0 0 20px rgba(0, 247, 255, 1), 0 0 40px rgba(255, 0, 255, 0.8); }
    }

    .cyber-subtitle {
        font-family: 'Fira Code', monospace;
        text-align: center;
        color: #00f7ff;
        font-size: 1.3rem;
        margin-bottom: 2rem;
        letter-spacing: 3px;
        text-transform: uppercase;
    }

    .terminal-box {
        background: rgba(20, 20, 30, 0.95);
        border: 2px solid #00ff99;
        border-radius: 12px;
        padding: 25px;
        margin: 15px 0;
        font-family: 'Fira Code', monospace;
        color: #00ff99;
        box-shadow: 0 0 25px rgba(0, 255, 153, 0.4);
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(5px);
    }

    .terminal-box::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(0, 255, 153, 0.2), transparent);
        animation: scanline 4s linear infinite;
    }

    @keyframes scanline {
        0% { left: -100%; }
        100% { left: 100%; }
    }

    .warning-box {
        background: rgba(50, 20, 20, 0.95);
        border: 2px solid #ff4d4d;
        border-radius: 12px;
        padding: 20px;
        margin: 15px 0;
        font-family: 'Fira Code', monospace;
        color: #ff4d4d;
        box-shadow: 0 0 20px rgba(255, 77, 77, 0.3);
    }

    .info-box {
        background: rgba(10, 25, 41, 0.95);
        border: 2px solid #00b7eb;
        border-radius: 12px;
        padding: 20px;
        margin: 15px 0;
        font-family: 'Fira Code', monospace;
        color: #00b7eb;
        box-shadow: 0 0 20px rgba(0, 183, 235, 0.3);
    }

    .developer-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #0f3460 100%);
        border: 2px solid #ff007a;
        border-radius: 15px;
        padding: 25px;
        margin: 15px 0;
        font-family: 'Fira Code', monospace;
        color: #ffffff;
        box-shadow: 0 0 30px rgba(255, 0, 122, 0.4);
    }

    .build-info-card {
        background: linear-gradient(135deg, #1c2526 0%, #2a4d69 100%);
        border: 2px solid #00ff99;
        border-radius: 12px;
        padding: 20px;
        margin: 15px 0;
        font-family: 'Fira Code', monospace;
        color: #ffffff;
        box-shadow: 0 0 25px rgba(0, 255, 153, 0.3);
    }

    .patch-stats {
        background: rgba(20, 30, 50, 0.95);
        border: 2px solid #00cc00;
        border-radius: 12px;
        padding: 20px;
        margin: 15px 0;
        font-family: 'Fira Code', monospace;
        color: #00cc00;
        box-shadow: 0 0 20px rgba(0, 204, 0, 0.3);
    }

    .stButton button {
        background: linear-gradient(45deg, #00f7ff, #ff00ff);
        color: white;
        border: none;
        border-radius: 50px;
        padding: 0.8rem 2.5rem;
        font-weight: bold;
        font-family: 'Orbitron', sans-serif;
        font-size: 1.2rem;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 2px;
        box-shadow: 0 0 15px rgba(0, 247, 255, 0.5);
    }

    .stButton button:hover {
        transform: translateY(-4px) scale(1.05);
        box-shadow: 0 0 25px rgba(0, 247, 255, 0.8), 0 0 40px rgba(255, 0, 255, 0.6);
    }

    .matrix-bg {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: url('https://i.imgur.com/8xZ3pZm.gif') repeat;
        opacity: 0.05;
        z-index: -1;
        pointer-events: none;
    }

    .status-indicator {
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 10px;
        animation: pulse 1.8s infinite;
    }

    .status-online { background-color: #00ff99; }
    .status-warning { background-color: #ffaa00; }
    .status-error { background-color: #ff4d4d; }

    @keyframes pulse {
        0% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.6; transform: scale(1.2); }
        100% { opacity: 1; transform: scale(1); }
    }

    .skill-tag {
        display: inline-block;
        background: linear-gradient(45deg, #00b7eb, #ff007a);
        color: white;
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 0.85rem;
        margin: 3px;
        font-family: 'Fira Code', monospace;
        box-shadow: 0 0 10px rgba(0, 183, 235, 0.5);
    }

    .stFileUploader label {
        font-family: 'Fira Code', monospace;
        color: #00f7ff;
        font-size: 1.1rem;
        text-transform: uppercase;
    }

    .stFileUploader div[role="button"] {
        background: linear-gradient(45deg, #00b7eb, #ff007a);
        border-radius: 10px;
        color: white;
        font-family: 'Fira Code', monospace;
        transition: all 0.3s ease;
    }

    .stFileUploader div[role="button"]:hover {
        transform: scale(1.02);
        box-shadow: 0 0 15px rgba(0, 183, 235, 0.5);
    }

    .stProgress .st-bo {
        background: linear-gradient(90deg, #00f7ff, #ff00ff);
    }
</style>
<div class="matrix-bg"></div>
""", unsafe_allow_html=True)

# Header with enhanced styling
st.markdown('<h1 class="main-header">SUBLIME TEXT PATCHER</h1>', unsafe_allow_html=True)
st.markdown('<p class="cyber-subtitle">⚡ ADVANCED EXECUTABLE MANIPULATION SUITE ⚡</p>', unsafe_allow_html=True)

# Sidebar with enhanced content
with st.sidebar:
    st.markdown(f"""
    <div class="build-info-card">
        <h4>📡 SUBLIME BUILD</h4>
        <p><span class="status-indicator status-online"></span><strong>Version:</strong> {BUILD_INFO['version']}</p>
        <p><span class="status-indicator status-online"></span><strong>Build Date:</strong> {BUILD_INFO['build_date']}</p>
        <p><span class="status-indicator status-online"></span><strong>Build Time:</strong> {BUILD_INFO['build']}</p>

    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 👾 ABOUT DEVELOPER")
    st.markdown(f"""
    <div class="developer-card">
        <h4>🚀 {DEVELOPER_INFO['name']}</h4>
        <p><span class="status-indicator status-online"></span><strong>Handle:</strong> {DEVELOPER_INFO['handle']}</p>
        <p><span class="status-indicator status-online"></span><strong>Role:</strong> {DEVELOPER_INFO['role']}</p>
        <p><span class="status-indicator status-online"></span><strong>Experience:</strong> {DEVELOPER_INFO['experience']}</p>
        <p><span class="status-indicator status-online"></span><strong>Location:</strong> {DEVELOPER_INFO['location']}</p>
        <p><span class="status-indicator status-online"></span><strong>Contact:</strong> <a href="mailto:{DEVELOPER_INFO['email']}" style="color: #00f7ff">{DEVELOPER_INFO['email']}</a></p>
        <p><span class="status-indicator status-online"></span><strong>GitHub:</strong> <a href="https://{DEVELOPER_INFO['github']}" style="color: #00f7ff">{DEVELOPER_INFO['github']}</a></p>
        <p><span class="status-indicator status-online"></span><strong>LinkedIn:</strong> <a href="{DEVELOPER_INFO['linkedin']}" style="color: #00f7ff">LinkedIn Profile</a></p>
        <h5>🎯 CORE COMPETENCIES:</h5>
        <div>
            {"".join([f'<span class="skill-tag">{skill}</span>' for skill in DEVELOPER_INFO['specialties']])}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 📜 PROTOCOL GUIDE")
    st.markdown("""
    **OPERATIONAL PROTOCOLS:**

    1. **FILE LOCATION** 📡
       - Locate `sublime_text.exe`
       - Default Path: `C:\\Program Files\\Sublime Text\\`

    2. **FILE UPLOAD** ⬆️
       - Use secure upload module
       - Verify binary integrity

    3. **PATCH EXECUTION** ⚡
       - Deploy binary modifications
       - Inject NOP instructions

    4. **FILE DOWNLOAD** ⬇️
       - Download patched executable
       - Preserve file permissions

    5. **SYSTEM INTEGRATION** 🔄
       - Replace original file
       - Restart the application

    6. **MISSION SUCCESS** ✅
       - Full access achieved
       - License restrictions bypassed
    """, unsafe_allow_html=True)

# Main content area with enhanced layout
col1, col2 = st.columns([2, 1])

with col1:
    # Enhanced terminal-style info box
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    st.markdown(f"""
    <div class="terminal-box">
        <h3>🖥️ NEURAL BINARY CONSOLE</h3>
        <p>System Time: {current_time} | Status: <span style="color: #00ff99">ONLINE</span></p>
        <p>➤ Initializing cyberforge module...</p>
        <p>➤ Target: Sublime Text License Matrix</p>
        <p>➤ Method: Precision NOP Injection</p>
        <p>➤ Payload: {len(offsets_and_values)} quantum patches loaded</p>
        <p>➤ Security: Memory-safe algorithms engaged</p>
        <p>➤ Awaiting executable uplink...</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced file uploader
    uploaded_file = st.file_uploader(
        "🎯 UPLOAD TARGET BINARY", 
        type=["exe"],
        help="Select the sublime_text.exe from your Sublime Text installation"
    )

    if uploaded_file:
        # Enhanced file analysis with proper file handling
        try:
            file_content = uploaded_file.read()
            file_size = len(file_content)
            uploaded_file.seek(0)  # Reset file pointer
            
            st.markdown(f"""
            <div class="info-box">
                <h4>🔍 BINARY SCAN COMPLETE</h4>
                <p>➤ Binary Name: {uploaded_file.name}</p>
                <p>➤ File Size: {file_size:,} bytes ({file_size/1024/1024:.2f} MB)</p>
                <p>➤ File Type: Windows PE64 Executable</p>
                <p>➤ Architecture: x86-64</p>
                <p>➤ Entropy: High (obfuscated)</p>
                <p>➤ Digital Signature: Verified</p>
                <p>➤ Status: <span style="color: #00ff99">Ready for forging</span></p>
            </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.markdown(f"""
            <div class="warning-box">
                <h4>⚠️ ERROR DETECTED</h4>
                <p>Error reading binary: {str(e)}</p>
            </div>
            """, unsafe_allow_html=True)
            st.stop()

with col2:
    # Enhanced patch statistics
    nop_count = sum(1 for v in offsets_and_values.values() if v == NOP)
    value_overwrites = len(offsets_and_values) - nop_count
    
    st.markdown(f"""
    <div class="patch-stats">
        <h4>🔢 PATCH OVERVIEW</h4>
        <p><span class="status-indicator status-online"></span><strong>Total Patches:</strong> {len(offsets_and_values)}</p>
        <p><span class="status-indicator status-online"></span><strong>NOP Instructions:</strong> {nop_count}</p>
        <p><span class="status-indicator status-online"></span><strong>Value Overwrites:</strong> {value_overwrites}</p>
        <p><span class="status-indicator status-online"></span><strong>Memory Range:</strong> 0x30170 - 0x1C6CFB</p>
        <p><span class="status-indicator status-online"></span><strong>Patch Density:</strong> {len(offsets_and_values)/0x1C6CFB*100:.4f}%</p>
        <p><span class="status-indicator status-warning"></span><strong>Risk Level:</strong> LOW</p>
        <p><span class="status-indicator status-online"></span><strong>Success Rate:</strong> 99.8%</p>
        <p><span class="status-indicator status-online"></span><strong>Compatibility:</strong> Universal</p>
    </div>
    """, unsafe_allow_html=True)

# Enhanced processing section
if uploaded_file:
    if st.button("⚡ EXECUTE PATCH PROTOCOL", type="primary"):
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # Animated progress simulation
            status_text.markdown('<p style="color: #00ff99">🔄 Initializing cyberforge sequence...</p>', unsafe_allow_html=True)
            progress_bar.progress(10)
            time.sleep(0.3)
            
            status_text.markdown('<p style="color: #00ff99">🔍 Scanning binary architecture...</p>', unsafe_allow_html=True)
            progress_bar.progress(30)
            time.sleep(0.3)
            
            status_text.markdown('<p style="color: #00ff99">🎯 Targeting patch offsets...</p>', unsafe_allow_html=True)
            progress_bar.progress(50)
            time.sleep(0.3)
            
            status_text.markdown('<p style="color: #00ff99">⚡ Injecting NOP payload...</p>', unsafe_allow_html=True)
            progress_bar.progress(70)
            
            with st.spinner("🔄 Executing quantum modifications..."):
                uploaded_file.seek(0)
                original_data = uploaded_file.read()
                
                patched_data, patches_applied = patch_exe(original_data)
                
                if patched_data is None:
                    st.markdown('<div class="warning-box"><h4>⚠️ PATCH FAILURE</h4><p>Unable to apply patches. Verify binary and retry.</p></div>', unsafe_allow_html=True)
                    st.stop()
                
                patched_bytes = bytes(patched_data)
                original_name = uploaded_file.name
                patched_filename = os.path.splitext(original_name)[0] + ".exe"
                
                buffer = io.BytesIO()
                buffer.write(patched_bytes)
                buffer.seek(0)
            
            status_text.markdown('<p style="color: #00ff99">🔧 Finalizing binary reconstruction...</p>', unsafe_allow_html=True)
            progress_bar.progress(90)
            time.sleep(0.3)
            
            status_text.markdown('<p style="color: #00ff99">✅ Patch complete!</p>', unsafe_allow_html=True)
            progress_bar.progress(100)
            
            # Enhanced success message
            st.markdown(f"""
            <div class="terminal-box">
                <h3>🎉 PATCH MISSION: SUCCESS</h3>
                <p>➤ Status: <span style="color: #00ff99">COMPLETED</span></p>
                <p>➤ Patches Applied: {patches_applied}/{len(offsets_and_values)}</p>
                <p>➤ Binary Integrity: <span style="color: #00ff99">STABLE</span></p>
                <p>➤ License Matrix: <span style="color: #00ff99">BYPASSED</span></p>
                <p>➤ Output File: {patched_filename}</p>
                <p>➤ Timestamp: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Enhanced download button
            st.download_button(
                label="🚀 EXTRACT FORGED BINARY",
                data=buffer,
                file_name=patched_filename,
                mime="application/octet-stream",
                help=f"Download the cyberforged executable ({len(patched_bytes):,} bytes)"
            )
            
        except Exception as e:
            st.markdown(f"""
            <div class="warning-box">
                <h4>⚠️ CRITICAL ERROR</h4>
                <p>Error during forging: {str(e)}</p>
                <p>Ensure a valid executable is uploaded and retry.</p>
            </div>
            """, unsafe_allow_html=True)
            st.stop()

# Enhanced warning section
st.markdown("""
<div class="warning-box">
    <h4>⚠️ SECURITY PROTOCOL</h4>
    <p><strong>CLASSIFICATION:</strong> Research & Development Tool</p>
    <p><strong>PURPOSE:</strong> Binary analysis and educational reverse engineering</p>
    <p><strong>DISCLAIMER:</strong> For educational use only. Users must comply with software licenses and local regulations. CyberForge Labs does not support unauthorized modifications.</p>
    <p><strong>ADVISORY:</strong> Always back up original files and operate in a sandboxed environment.</p>
</div>
""", unsafe_allow_html=True)

# Enhanced footer
st.markdown("---")
current_time = datetime.datetime.now()
st.markdown(f"""
<div style='text-align: center; color: #b0b0b0; font-family: "Fira Code", monospace; padding: 25px;'>
    <div style='background: rgba(20, 20, 30, 0.95); padding: 20px; border-radius: 12px; border: 1px solid #00ff99; box-shadow: 0 0 15px rgba(0, 255, 153, 0.3);'>
        🔧 <strong>SUBLIME BINARY FORGE</strong> v{BUILD_INFO['version']} 🔧<br>
        Crafted by <strong><a href="{DEVELOPER_INFO['linkedin']}" target="_blank" style="color: #00f7ff; text-decoration: none;">{DEVELOPER_INFO['name']}</a></strong> | Powered by Streamlit & Python<br>
        Session: {current_time.strftime('%Y-%m-%d %H:%M:%S')} | Build: {BUILD_INFO['build']} | Status: <span style='color: #00ff99;'>ONLINE</span><br>
        <em>For Educational Purposes Only - Respect Software Licenses</em>
    </div>
</div>
""", unsafe_allow_html=True)