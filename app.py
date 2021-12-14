import json
import os
from enum import Enum

import streamlit as st
import streamlit.components.v1 as components
import wget
from bs4 import BeautifulSoup as bs

st.set_page_config(page_title="HTML parser", layout="wide")
st.title("html parser viewer")

col_button_1, col_button_2, col_button_3 = st.columns(3)
col1, col2, col3 = st.columns(3)

data_id = "data_100"
extraction_method = "extraction-method-1"


class HtmlRendering(Enum):
    browser = 1
    raw = 2


options = [
    "data_100",
    "data_124",
    "data_143",
    "data_192",
    "data_33",
    "data_39",
    "data_81",
    "data_102",
    "data_130",
    "data_182",
    "data_200",
    "data_36",
    "data_73",
]

with col_button_1:
    data_id = st.selectbox(
        "data", options
    )  # , index=0, format_func=special_internal_function, key=None, help=None, on_change=None, args=None, kwargs=None)


with col_button_2:
    extraction_method = st.selectbox(
        "extraction method", ["extraction-method-1", "extraction-method-2", "extraction-method-3"]
    )

with col_button_3:
    html_rendering = st.selectbox(
        "Html rendering", [HtmlRendering.browser.name, HtmlRendering.raw.name]
    )

output_directory = "out_dir"
os.makedirs(output_directory, exist_ok=True)


def build_url(data_id, filename, branch_name="main"):
    url = f"https://raw.githubusercontent.com/SaulLu/comparison-c4-C4-web-pages/{branch_name}/{data_id}/{filename}"
    print(url)
    return url


with col1:
    st.subheader("Metadata")
    file_name = "metadata.json"
    path_file_dir = os.path.join(output_directory, data_id, extraction_method)
    path_file = os.path.join(path_file_dir, file_name)
    if not os.path.isfile(path_file):
        os.makedirs(path_file_dir, exist_ok=True)

        url = build_url(data_id, file_name, extraction_method)
        wget.download(url, out=path_file_dir)

    with open(path_file, "r") as f:
        content = f.read()

    metadata = json.loads(content)
    st.write(metadata)

with col2:
    st.subheader("HTML")

    file_name = "html.html"
    path_file_dir = os.path.join(output_directory, data_id, extraction_method)
    path_file = os.path.join(path_file_dir, file_name)
    if not os.path.isfile(path_file):
        os.makedirs(path_file_dir, exist_ok=True)

        url = build_url(data_id, file_name, extraction_method)
        wget.download(url, out=path_file_dir)

    with open(path_file, "r") as f:
        html = f.read()
    if html_rendering == HtmlRendering.browser.name:
        components.html(html, height=2000, scrolling=True)
    else:
        soup = bs(html)  # make BeautifulSoup
        prettry_html = soup.prettify()  # prettify the html
        st.code(prettry_html)

with col3:
    st.subheader("Text")
    file_name = "text.txt"
    path_file_dir = os.path.join(output_directory, data_id, extraction_method)
    path_file = os.path.join(path_file_dir, file_name)
    if not os.path.isfile(path_file):
        os.makedirs(path_file_dir, exist_ok=True)

        url = build_url(data_id, file_name, extraction_method)
        wget.download(url, out=path_file_dir)

    with open(path_file, "r") as f:
        text = f.read()
    st.text(text)
