import streamlit as st

# Remove the file uploader deprecation warning.
st.set_option('deprecation.showfileUploaderEncoding', False)

"# Base 64 Image Encoder"

"## Input"

IMAGE_FORMATS = ['png', 'jpg', 'jpeg']
file = st.file_uploader('Select an image file.', type=IMAGE_FORMATS)

remove_top_pixels = st.slider('Remove pixels from top.', 0, 100, 10)
image_width = st.slider('Image width', 1, 1000, 100)

st.experimental_show(remove_top_pixels)
st.experimental_show(image_width)

st.help(st.file_uploader)
assert file, "Please upload an image file."


