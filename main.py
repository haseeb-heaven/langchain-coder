import os
import tempfile
import streamlit as st
from libs.codey_lib import CodeyLib
from libs.general_utils import GeneralUtils
from libs.lang_codes import LangCodes
from libs.logger import logger
from streamlit_ace import st_ace

general_utils = None

def initialize_session_state():
    if "code_language" not in st.session_state:
        st.session_state.code_language = "Python"
    if "compiler_mode" not in st.session_state:
        st.session_state.compiler_mode = "Online"
    if "generated_code" not in st.session_state:
        st.session_state.generated_code = ""
    if "ai_option" not in st.session_state:
        st.session_state.ai_option = "Open AI"
    if "output" not in st.session_state:
        st.session_state.output = ""
        

def main():
    # initialize session state
    initialize_session_state()
    
    # Initialize classes
    code_language = st.session_state.get("code_language", "Python")
    lang_chain_coder = None # We'll initialize this after settings
    codey = None  # We'll initialize this after loading environment variables
    general_utils = GeneralUtils()
    
    # Streamlit UI
    st.title("LangChain Coder - AI 🦜🔗")
    logger.info("LangChain Coder - AI 🦜🔗")
    
    # Sidebar for settings
    with st.sidebar:
        # Session states for input options
        ai_option = st.session_state.get("ai_option", "Open AI")
        st.session_state.code_language = st.session_state.get("code_language", "Python")
        st.session_state.compiler_mode = st.session_state.get("compiler_mode", "Online")

        # Dropdown for selecting AI options
        st.selectbox("Select an AI option", ["Open AI", "Vertex AI"], key="ai_option")

        # Dropdown for selecting code language
        st.selectbox("Select a language", list(LangCodes().keys()), key="code_language")

        # Radio buttons for selecting compiler mode
        st.radio("Compiler Mode", ("Online", "Offline"), key="compiler_mode")
        credentials_file_path = None
        
        # Load environment variables for Vertex AI
        if ai_option == "Vertex AI":
            with st.expander("Vertex AI Settings"):
                project = st.text_input("Project name:", value="heavenllm")
                region = st.text_input("App region:", value="us-central1")
                logger.info(f"Vertex AI Project: {project} and Region: {region}")
                
                uploaded_file = st.file_uploader("Upload Service Account Key")
                if uploaded_file:
                    file_path = save_uploadedfile(uploaded_file)  # Save the uploaded file
                    if file_path:
                        credentials_file_path = file_path
                        st.toast(f"Credentials file uploaded {credentials_file_path}", icon="✅")
                    else:
                        st.toast("Failed to save the uploaded file.", icon="❌")
                
                if project and region and credentials_file_path:
                    try:
                        # Initialize CodeyLib
                        codey = CodeyLib(project=project, location=region, model_name="code-bison", max_output_tokens=1024, temperature=0.1, credentials_file_path=credentials_file_path)
                        codey.load_model()
                        st.toast("Vertex AI initialized successfully.", icon="✅")
                    except Exception as exception:
                        st.toast(f"Error loading Vertex AI: {str(exception)}", icon="❌")
                        logger.error(f"Error loading Vertex AI: {str(exception)}")
                else:
                    # Show error message
                    st.toast("Please select all settings for Vertex AI.", icon="❌")
                    logger.error("Please select all settings for Vertex AI.")


    code_prompt = st.text_area(" ", height=100,placeholder="Enter a prompt to generate the code")

    if st.button("Generate Code"):
        if ai_option == "Open AI":
            st.session_state.generated_code = lang_chain_coder.generate_code(code_prompt, code_language)
        elif ai_option == "Vertex AI" and codey:
            st.session_state.generated_code  = codey.generate_code(code_prompt,code_language)
        else:
            st.error("Please select a valid AI option and fill in the required details.")
            st.session_state.generated_code  = ""
    
    # Save and Run Code
    if st.session_state.generated_code:
        
        with st.sidebar.expander("Code Editor", expanded=False):
            # Sidebar for settings
            st.sidebar.title("Code Editor Settings")

            # Font size setting
            font_size = st.sidebar.slider("Font Size", min_value=8, max_value=30, value=14, step=1)

            # Tab size setting
            tab_size = st.sidebar.slider("Tab Size", min_value=2, max_value=8, value=4, step=1)

            # Theme setting
            themes = ["monokai", "github", "tomorrow", "kuroir", "twilight", "xcode", "textmate", "solarized_dark", "solarized_light", "terminal"]
            theme = st.sidebar.selectbox("Theme", options=themes, index=themes.index("monokai"))

            # Keybinding setting
            keybindings = ["emacs", "sublime", "vim", "vscode"]
            keybinding = st.sidebar.selectbox("Keybinding", options=keybindings, index=keybindings.index("emacs"))

            # Other settings
            show_gutter = st.sidebar.checkbox("Line Number", value=True)
            show_print_margin = st.sidebar.checkbox("Print Margin", value=True)
            wrap = st.sidebar.checkbox("Wrap", value=True)
            auto_update = st.sidebar.checkbox("Auto Update", value=False)
            readonly = st.sidebar.checkbox("Readonly", value=True)
            language = st.sidebar.selectbox("Language", options=list(LangCodes().keys()), index=list(LangCodes().keys()).index("Python"))
            # Display the st_ace code editor with the selected settings
        if st.session_state.generated_code:
            code_editor = st_ace(
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
        
        # Save Code
        code_file = st.text_input("File name:")
        if st.button("Save Code"):
            general_utils.save_code(code_file)

        # Run Code
        if st.button("Run Code") and st.session_state.generated_code :
            st.session_state.output = general_utils.execute_code(st.session_state.compiler_mode)

def save_uploadedfile(uploadedfile):
    try:
        # Check if tempDir exists, if not, create it
        if not os.path.exists("tempDir"):
            os.makedirs("tempDir")

        with open(os.path.join("tempDir", uploadedfile.name), "wb") as f:
            f.write(uploadedfile.getbuffer())
        return os.path.join("tempDir", uploadedfile.name)
    except Exception as e:
        st.error(f"Error saving uploaded file: {e}")
        return None

if __name__ == "__main__":
    main()
