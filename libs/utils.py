import streamlit as st
import os
from streamlit_ace import st_ace
from libs.logger import logger

def initialize_session_state():
    if "code_language" not in st.session_state:
        st.session_state.code_language = "Python"
    if "compiler_mode" not in st.session_state:
        st.session_state.compiler_mode = "Offline"
    if "generated_code" not in st.session_state:
        st.session_state.generated_code = ""
    if "ai_option" not in st.session_state:
        st.session_state.ai_option = "Open AI"
    if "output" not in st.session_state:
        st.session_state.output = ""
    if "vertex_ai_loaded" not in st.session_state:
        st.session_state.vertex_ai_loaded = False
    if "uploaded_file" not in st.session_state:
        st.session_state.uploaded_file = None
    if "project" not in st.session_state:
        st.session_state.project = ""
    if "region" not in st.session_state:
        st.session_state.region = ""
    if "vertexai_langchain" not in st.session_state:
        st.session_state.vertexai_langchain= None
    if "openai_langchain" not in st.session_state:
        st.session_state.openai_langchain = None
    if "code_prompt" not in st.session_state:
        st.session_state.code_prompt = ""
    if "display_cost" not in st.session_state:
        st.session_state.display_cost = False
    if "download_link" not in st.session_state:
        st.session_state.download_link = None
    if "download_logs" not in st.session_state:
        st.session_state.download_logs = False
    if "auto_debug_chain" not in st.session_state:
        st.session_state.auto_debug_chain = False
    if "code_input" not in st.session_state:
        st.session_state.code_input = None
    if "code_output" not in st.session_state:
        st.session_state.code_output = None
    if "palm_langchain" not in st.session_state:
        st.session_state.palm_langchain = None
    if "gemini_langchain" not in st.session_state:
        st.session_state.gemini_langchain = None
    if "code_fix_instructions" not in st.session_state:
        st.session_state.code_fix_instructions = None
    if "sequential_chain" not in st.session_state:
        st.session_state.sequential_chain = None
    if "stderr" not in st.session_state:
        st.session_state.stderr = None
    if "compiler_offline_privacy_shown" not in st.session_state:
        st.session_state.compiler_offline_privacy_shown = True
    if "compiler_online_privacy_shown" not in st.session_state:
        st.session_state.compiler_online_privacy_shown = True
    if "compiler_offline_privacy_accepted" not in st.session_state:
        st.session_state.compiler_offline_privacy_accepted = None
    if "compiler_online_privacy_accepted" not in st.session_state:
        st.session_state.compiler_online_privacy_accepted = None

    # Initialize session state for Vertex AI
    if "vertexai" not in st.session_state:
        st.session_state["vertexai"] = {
            "model_name": "code-bison",
            "temperature": 0.1,
            "max_tokens": 2048
        }
    
    # Initialize session state for Open AI
    if "openai" not in st.session_state:
        st.session_state["openai"] = {
            "model_name": "text-davinci-003",
            "temperature": 0.1,
            "max_tokens": 2048
        }
        
    # Initialize session state for Palm AI
    if "palm" not in st.session_state:
        st.session_state["palm"] = {
            "model_name": "text-bison-001",
            "temperature": 0.1,
            "max_tokens": 2048
        }

    # Initialize session state for Palm AI
    if "gemini" not in st.session_state:
        st.session_state["gemini"] = {
            "model_name": "gemini-pro",
            "temperature": 0.1,
            "max_tokens": 2048
        }
    
    if "coding_guidelines" not in st.session_state:
        st.session_state["coding_guidelines"] = {
            "modular_code": False,
            "exception_handling": False,
            "error_handling": False,
            "logs": False,
            "comments": False,
            "efficient_code": False,
            "robust_code": False,
            "memory_efficiency": False,
            "speed_efficiency": False,
            "naming_conventions": False
        }

def show_privacy_policy(mode) -> bool:
    if mode == 'offline':
        st.markdown("""
        ## Code Execution License - OFFLINE:
        - You are solely responsible for the code that you write, compile, and run using the Platform.
        - You agree not to write, compile, or run any code that is *illegal*, *harmful*, *malicious*, *offensive*, *infringing*, or otherwise violates any laws, rights, or policies. 
        - You agree not to write, compile, or run any code that may *damage*, *interfere with*, or *compromise* the Platform, the JDoodle Compiler API, or any other systems or services. 
        - You agree not to write, compile, or run any code that may *access* or *disclose* any *confidential* or *sensitive* information.
        """)
        agree = st.radio('I agree to the Code Execution License - OFFLINE', ('Not Sure','Yes', 'No'), index=0)
        if agree == 'Yes':
            return True
        elif agree == 'No':
            return False
        else :
            return None
            
    elif mode == 'online':
        st.markdown("""
        ## Code Execution License - ONLINE:
        - **The platform uses the [JDoodle Compiler](https://www.jdoodle.com/) to compile and run your code.** 
          - *The JDoodle Compiler is a third-party service that provides online code execution for various programming languages.*
          - *The JDoodle Compiler may collect and use your code and other information in accordance with their own [terms and conditions](https://www.jdoodle.com/terms) and [privacy policy](https://www.jdoodle.com/privacy).*
        """)
        agree = st.radio('I agree to the Code Execution License - ONLINE', ('Not Sure','Yes', 'No'), index=0)
        if agree == 'Yes':
            return True
        elif agree == 'No':
            return False
        else :
            return None

# Load the CSS files
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def display_code_editor(font_size, tab_size, theme, keybinding, show_gutter, show_print_margin, wrap, auto_update, readonly, language):
    if st.session_state.generated_code and st.session_state.compiler_mode == "Offline":
        st.session_state.generated_code = st_ace(
            language=language.lower(),
            theme=theme,
            keybinding=keybinding,
            height=400,
            value=st.session_state.generated_code,
            font_size=font_size,
            tab_size=tab_size,
            show_gutter=show_gutter,
            show_print_margin=show_print_margin,
            wrap=wrap,
            auto_update=auto_update,
            readonly=readonly
        )
    elif st.session_state.generated_code and st.session_state.compiler_mode == "Online":
        st.components.v1.html(st.session_state.output,width=720, height=800, scrolling=True)

def display_support():
    st.markdown("<div style='text-align: center;'>Share and Support</div>", unsafe_allow_html=True)
    
    st.write("""
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center;">
            <ul style="list-style-type: none; margin: 0; padding: 0; display: flex;">
                <li style="margin-right: 10px;"><a href="https://twitter.com/haseeb_heaven" target="_blank"><img src="https://img.icons8.com/color/32/000000/twitter--v1.png"/></a></li>
                <li style="margin-right: 10px;"><a href="https://www.buymeacoffee.com/haseebheaven" target="_blank"><img src="https://img.icons8.com/color/32/000000/coffee-to-go--v1.png"/></a></li>
                <li style="margin-right: 10px;"><a href="https://www.youtube.com/@HaseebHeaven/videos" target="_blank"><img src="https://img.icons8.com/color/32/000000/youtube-play.png"/></a></li>
                <li><a href="https://github.com/haseeb-heaven/LangChain-Coder" target="_blank"><img src="https://img.icons8.com/color/32/000000/github--v1.png"/></a></li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

# create method to upgrade the pip packages and pip
def upgrade_pip_packages():
    try:
        # upgrade pip
        os.system("python -m pip install --upgrade pip")
        # upgrade pip packages
        os.system("pip install -r requirements.txt --upgrade")
    except Exception as e:
        print(f"Error upgrading pip packages: {e}")

def handle_privacy_policy(compiler_mode):
    privacy_shown_key = f'compiler_{compiler_mode.lower()}_privacy_shown'
    privacy_accepted_key = f'compiler_{compiler_mode.lower()}_privacy_accepted'

    if st.session_state[privacy_shown_key]:
        # Display the privacy policy for the selected compiler mode.
        st.session_state[privacy_accepted_key] = show_privacy_policy(compiler_mode.lower())            

    else:
        logger.info(f"Privacy shown state {st.session_state[privacy_shown_key]} for {compiler_mode.lower()} compiler mode.")
    
    if st.session_state[privacy_shown_key]:
        if st.button(f"Accept Privacy"):

            if st.session_state[privacy_accepted_key] == True:
                st.toast(f"Privacy policy accepted for {compiler_mode.lower()} compiler mode.", icon="✅")
            elif st.session_state[privacy_accepted_key] == False:
                st.toast(f"Privacy policy not accepted for {compiler_mode.lower()} compiler mode.", icon="❌")
            else:
                st.toast(f"Please select the privacy policy for {compiler_mode.lower()} compiler mode.", icon="❌")

            if st.session_state[privacy_accepted_key] in [True, False]:
                st.session_state[privacy_shown_key] = False