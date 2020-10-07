import streamlit as st
from PIL import Image
import numpy as np
import base64
from io import BytesIO
import yaml
import textwrap

@st.cache
def load_image(filename, new_img_width, remove_top_pixels):
    # Shave off some pixels from the top
    im = Image.open(open(filename, 'rb'))
    im = np.array(im)[remove_top_pixels:,:,:]
    im = Image.fromarray(im)

    # Downsample the image
    old_img_width, old_img_height = im.size
    new_img_height = (old_img_height * new_img_width) // old_img_width
    im = im.resize((new_img_width, new_img_height), Image.LANCZOS)

    # All done!
    return im

def base64_img_html(im):
    io_buffer = BytesIO()
    st.experimental_show(type(im))
    im.save(io_buffer, format="JPEG")
    img_str = base64.b64encode(io_buffer.getvalue()).decode("utf-8")
    st.experimental_show(type(img_str))
    img_tag = f'<img src="data:image/jpeg;base64,{img_str}" />'
    return img_tag

def captioned_img_html(base64_img, name, live_url, git_url):
    return textwrap.dedent(f'''
        <span>
           {base64_img}
        </span>
    ''')
# st.code(img_tag, language='html')


# Remove the file uploader deprecation warning.
st.set_option('deprecation.showfileUploaderEncoding', False)

"# Grid Figure Creator"

# Sidebar configuration
show_config = st.sidebar.checkbox('Show raw config', True)
remove_top_pixels = st.sidebar.slider('Remove pixels from top.', 0, 100, 10)
new_img_width = st.sidebar.slider('Image width', 1, 1000, 100)

# Load the config information from the user.
config = yaml.load(open('table_config.yaml'))

# Create the images
for img_num, img_info in enumerate(config['imgs']):
    image = load_image(img_info['filename'], new_img_width, remove_top_pixels)
    st.image(image)
    st.experimental_show(type(image))
    base64_img = base64_img_html(image)
    captioned_img = captioned_img_html(base64_img, img_info['name'],
            img_info['live-url'], img_info['git-url'])
    st.code(captioned_img, language='html')



# Show the raw configuration data at the bottom.
if show_config:
    st.write('## Raw config', config)

st.stop()

"## Input"

IMAGE_FORMATS = ['png', 'jpg', 'jpeg']
file = st.file_uploader('Select an image file.', type=IMAGE_FORMATS)


st.experimental_show(remove_top_pixels)
st.experimental_show(new_img_width)

if st.checkbox('Show help.'):
    st.help(st.file_uploader)

if not file:
    st.warning("Please upload an image file.")
    st.stop()

"## Output"

