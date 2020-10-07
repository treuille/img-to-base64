import streamlit as st
from PIL import Image
import numpy as np
import base64
from io import BytesIO

# Remove the file uploader deprecation warning.
st.set_option('deprecation.showfileUploaderEncoding', False)

"# Base 64 Image Encoder"

"## Input"

IMAGE_FORMATS = ['png', 'jpg', 'jpeg']
file = st.file_uploader('Select an image file.', type=IMAGE_FORMATS)

remove_top_pixels = st.slider('Remove pixels from top.', 0, 100, 10)
new_img_width = st.slider('Image width', 1, 1000, 100)

st.experimental_show(remove_top_pixels)
st.experimental_show(new_img_width)

if st.checkbox('Show help.'):
    st.help(st.file_uploader)

if not file:
    st.warning("Please upload an image file.")
    st.stop()

"## Output"

im = Image.open(file)
old_img_width, old_img_height = im.size
new_img_height = (old_img_height * new_img_width) // old_img_width
st.experimental_show(im)
im = im.resize((new_img_width, new_img_height), Image.LANCZOS)
st.image(im)
im = np.array(im)
st.image(im[remove_top_pixels:,:,:])
st.experimental_show((im.shape, im.dtype))

im = Image.fromarray(im)
io_buffer = BytesIO()
im.save(io_buffer, format="JPEG")
img_str = base64.b64encode(io_buffer.getvalue()).decode("utf-8")
st.experimental_show(type(img_str))
st.help(st.code)
img_tag = f'<img src="data:image/jpeg;base64,{img_str}" />'
st.code(img_tag, language='html')
