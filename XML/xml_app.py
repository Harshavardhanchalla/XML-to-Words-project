import streamlit as st
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import re
import joblib

# Function to strip HTML tags
def strip_html(text):
    soup = BeautifulSoup(text, "html.parser")
    return soup.get_text()

# Function to remove text between square brackets
def remove_between_square_brackets(text):
    return re.sub('\[[^]]*\]', '', text)

# Function to denoise text
def denoise_text(text):
    text = strip_html(text)
    text = remove_between_square_brackets(text)
    text = re.sub('  ', '', text)
    return text

# Streamlit app
st.set_page_config(page_title="XML File Denoising App", layout="wide")

st.title("XML File Denoising Application")
st.write("This application allows you to upload an XML file, view its content, and clean the data by removing HTML tags and text between square brackets.")

# Sidebar for file upload
st.sidebar.header("Upload XML File")
uploaded_file = st.sidebar.file_uploader("Choose an XML file", type="xml")

if uploaded_file is not None:
    with st.spinner('Parsing XML file...'):
        # Parse the XML file
        tree = ET.parse(uploaded_file)
        root = tree.getroot()
        
        # Convert XML root to string
        root_string = ET.tostring(root, encoding='utf8').decode('utf8')
    
    st.subheader("Original XML Content")
    st.code(root_string, language='xml')
    
    if st.sidebar.button("Clean Data"):
        with st.spinner('Cleaning data...'):
            # Clean the XML content
            denoised_text = denoise_text(root_string)
            
            # Save the denoised text using joblib
            joblib.dump(denoised_text, 'xml_to_data.pkl')
        
        st.subheader("Denoised Text")
        st.code(denoised_text, language='text')

else:
    st.info("Please upload an XML file to get started.")

st.sidebar.write("Once you upload the file, the original content will be displayed. Click the 'Clean Data' button to view the cleaned content.")
