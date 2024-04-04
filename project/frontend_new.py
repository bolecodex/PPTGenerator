import streamlit as st
import streamlit.components.v1 as components
from cg_utils import *
from rag_documents import *
import os
from pathlib import Path, PurePath
from upload_ppt_to_google_drive import upload_ppt_to_google_drive


# Directories
UPLOAD_DIR = Path(__file__).resolve().parent.joinpath('', 'upload')
INPUT_DIR = Path(__file__).resolve().parent.joinpath('', 'input')
TEMPLATE_DIR = Path(__file__).resolve().parent.joinpath('', 'template')
OUTPUT_DIR = Path(__file__).resolve().parent.joinpath('', 'output')
VECTOR_STORE_DIR = Path(__file__).resolve().parent.joinpath('', 'vector_store')
if not os.path.exists(UPLOAD_DIR):
   os.makedirs(UPLOAD_DIR)
if not os.path.exists(INPUT_DIR):
   os.makedirs(INPUT_DIR)   
if not os.path.exists(VECTOR_STORE_DIR):
   os.makedirs(VECTOR_STORE_DIR)


# Get text-to-text FMs
t2t_fms = get_t2t_fms(fm_vendors)





# if __name__ == "__main__":
#     st.set_page_config(page_title="PPTGPT", page_icon="📖", layout="wide")
#     main()
#     with st.sidebar:
#         st.markdown("---")
#         st.markdown(
#             '<h6>Made in &nbsp<img src="https://streamlit.io/images/brand/streamlit-mark-color.png" alt="Streamlit logo" height="16">&nbsp by <a href="https://twitter.com/andfanilo">@weibo</a></h6>',
#             unsafe_allow_html=True,
#         )
        
def save_uploaded_file(directory, file):
    st.session_state.clicked = True
    if not os.path.exists(directory):
        os.makedirs(directory)  # create the directory if it does not exist
    file_path = os.path.join(directory, file.name)
    with open(file_path, "wb") as f:
        f.write(file.getbuffer())  # write the file to the specified directory
    
    
def main():
        
    """Main function for RAG"""
    st.set_page_config(page_title="Retrieval Augmented Generation - Similarity Search", layout="wide")
    css = '''
        <style>   
            .block-container {
                padding-top: 1rem;
                padding-bottom: 0rem;
                # padding-left: 5rem;
                # padding-right: 5rem;
            }
            button[kind="primary"] {
                background-color: #FF9900;
                border: none;
            }                  
            #divshell {
                border-top-right-radius: 7px;
                border-top-left-radius: 7px;
                border-bottom-right-radius: 7px;
                border-bottom-left-radius: 7px;
            }                      
        </style>
    '''
    st.write(css, unsafe_allow_html=True)
    # st.header("Retrieval Augmented Generation (RAG) - PDF Documents")
    # st.markdown("**Select** a foundation model, **upload** and **submit** your document(s), **enter** a question or instruction to retrieve information from your document(s) and click **Ask**. " \
    #              "You will see results with and without using RAG. " \
    #              "Refer the [Demo Overview](Solutions%20Overview) for a description of the solution.")

    with st.sidebar:
        st.header("Configuration")
        rag_fm = st.selectbox('Select Foundation Model',t2t_fms, key="rag_fm_key")
        rag_docs = st.file_uploader(label="Upload Documents", type="pdf", accept_multiple_files=True, key="rag_docs_key")
        if st.session_state.rag_docs_key is not None:
            st.button("Submit Documents", type="primary", on_click=process_docs, args=(UPLOAD_DIR, INPUT_DIR))
        files = st.empty()
        with files.container():
            list_files(INPUT_DIR)
        if len(os.listdir(INPUT_DIR)) > 0:
            if st.button("Delete Documents", type="primary"):
                empty_dir(INPUT_DIR)
                empty_dir(VECTOR_STORE_DIR)
                with files.container():
                    list_files(INPUT_DIR)
                st.rerun()
                
        ppt_template = st.file_uploader(
            "Upload a PPT template",
            type=["pptx", "ppt"],
            key="ppt_template"
        )
        if 'clicked' not in st.session_state:
            st.session_state.clicked = False
        if st.session_state.ppt_template is not None:
            st.button("Generate PPT based on Template", type="primary", on_click=save_uploaded_file, args=(TEMPLATE_DIR, ppt_template))
        files = st.empty()
        with files.container():
            list_files(TEMPLATE_DIR)
        if len(os.listdir(TEMPLATE_DIR)) > 0:
            if st.button("Delete Template", type="primary"):
                empty_dir(TEMPLATE_DIR)
                with files.container():
                    list_files(TEMPLATE_DIR)
                st.rerun()
                
    st.header("📖PPTGPT")
    # st.title("Intelligent PPT Generator")

                
    col1, col2 = st.columns([1.75,0.25])
    with col1:
        rag_fm_prompt = st.text_input('Enter your question or instruction for information from the uploaded document(s)', key="rag_fm_prompt_key",label_visibility="visible")
        rag_fm_prompt_validation = st.empty()
        rag_enabled_response = st.empty()

    with col2:
        st.markdown("<br />", unsafe_allow_html=True)
        if st.button("Ask!", type="primary"):
            if rag_fm_prompt is not None:
                if 'faiss_vector_db' not in st.session_state:
                    st.session_state.faiss_vector_db = None
                with rag_fm_prompt_validation.container():
                    if len(rag_fm_prompt) < 10:
                        st.error('Your question or instruction must contain at least 10 characters.', icon="🚨")
                    elif len(os.listdir(INPUT_DIR)) == 0 and len(os.listdir(VECTOR_STORE_DIR)) == 0:
                        st.session_state.faiss_vector_db = None
                        st.error('There are no PDF documents for RAG. Pleasse upload at least one document.', icon="🚨")
                    elif len(os.listdir(INPUT_DIR)) == 0 and len(os.listdir(VECTOR_STORE_DIR)) > 0:
                        empty_dir(VECTOR_STORE_DIR)
                        st.session_state.faiss_vector_db = None
                    elif len(os.listdir(INPUT_DIR)) > 0 and len(os.listdir(VECTOR_STORE_DIR)) == 0:
                        pdf_chunks = split_pdfs(INPUT_DIR)
                        st.session_state.faiss_vector_db = embeddings_faiss(pdf_chunks,VECTOR_STORE_DIR, bedrock_embeddings)
                    elif len(os.listdir(INPUT_DIR)) > 0 and len(os.listdir(VECTOR_STORE_DIR)) > 0:
                        st.session_state.faiss_vector_db = embeddings_faiss([],VECTOR_STORE_DIR, bedrock_embeddings)
                        # with rag_disabled_response.container():
                        #     st.markdown(f"<div id='divshell' style='background-color: #fdf1f2;'><p style='text-align: center;font-weight: bold;'>Without RAG ( {rag_fm} )</p>{ask_fm_rag_off(rag_fm_prompt, rag_fm)}</div>", unsafe_allow_html=True)
                        with rag_enabled_response.container():
                            st.markdown(f"<div id='divshell' style='background-color: #f1fdf1;'><p style='text-align: center;font-weight: bold;'>With RAG ( {rag_fm} )</p>{ask_fm_rag_on(rag_fm_prompt, rag_fm, st.session_state.faiss_vector_db)}</div>", unsafe_allow_html=True)
    
    if st.session_state.clicked:
        read_prompt_from_ppt_template(os.path.join(TEMPLATE_DIR, ppt_template.name), os.path.join(OUTPUT_DIR, "output.ppt"), rag_fm, st.session_state.faiss_vector_db)
        webViewLink = upload_ppt_to_google_drive('service-account-credentials.json',os.path.join(OUTPUT_DIR, "output.ppt"),"output.ppt")

    else:    
        webViewLink="https://docs.google.com/presentation/d/1woR2iiRAH_1Xu6aJQPGZcgxd0fQuopGf/edit?usp=drivesdk&ouid=109567901216249287883&rtpof=true&sd=true"
    components.iframe(webViewLink, height=700)
    
# Main  
if __name__ == "__main__":
    main()