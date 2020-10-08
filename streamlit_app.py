import streamlit as st
from PIL import Image
import numpy as np
import base64
from io import BytesIO
import yaml
import textwrap
import streamlit.components.v1 as components

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

def base64_img_html(im, width):
    io_buffer = BytesIO()
    st.experimental_show(type(im))
    im.save(io_buffer, format="JPEG")
    img_str = base64.b64encode(io_buffer.getvalue()).decode("utf-8")
    st.experimental_show(type(img_str))
    img_tag = f'<img style="border: 1px solid #ddd" src="data:image/jpeg;base64,{img_str}" />'
    # img_tag = f'<img style="width:{width}px" src="https://raw.githubusercontent.com/treuille/img-to-base64/main/screenshot-1-face-gan.png"/>' 
    return img_tag

def captioned_img_html(app_num, base64_img, name, live_url, git_url, width):
    return textwrap.dedent(f'''
        <div style="width:{width}px; margin-right:20px; margin-bottom:20px">
           {base64_img}
           <div style="width:{width}px; text-align:center; margin-top:3px; font-family: Sans-Serif; font-size: 10px">
              ({app_num})
              <a href="{live_url}">Live App</a> |
              <a href="{git_url}">Github Source</a>
           </div>
        </div>
    ''')
# st.code(img_tag, language='html')


# Remove the file uploader deprecation warning.
st.set_option('deprecation.showfileUploaderEncoding', False)

"# Grid Figure Creator"

# Sidebar configuration
show_config = st.sidebar.checkbox('Show raw config', True)

# Load the config information from the user.
config = yaml.load(open('table_config.yaml'))
new_img_width = config['img-width']
remove_top_pixels = config['remove-top-pixels']

st.experimental_show(new_img_width)
st.experimental_show(remove_top_pixels)

# Create the images
figure_html = ""
for img_num, img_info in enumerate(config['imgs']):
    image = load_image(img_info['filename'], new_img_width, remove_top_pixels)
    st.image(image)
    st.experimental_show(type(image))
    base64_img = base64_img_html(image, new_img_width)
    captioned_img = captioned_img_html(img_num + 1,
            base64_img, img_info['name'],
            img_info['live-url'], img_info['git-url'],
            new_img_width)
    figure_html += captioned_img + '\n'

# Wrap everything in a giant div
figure_html = textwrap.dedent(f'''
<div style="display: flex; flex-wrap: wrap; justify-content: center">
{textwrap.indent(figure_html, prefix="  ")}
</div>
''')

components.html(figure_html, height=400)
st.code(figure_html, language='html')


# Show the raw configuration data at the bottom.
if show_config:
    st.write('## Raw config', config)

st.stop()

# "## Input"
# 
# IMAGE_FORMATS = ['png', 'jpg', 'jpeg']
# file = st.file_uploader('Select an image file.', type=IMAGE_FORMATS)
# 
# 
# st.experimental_show(remove_top_pixels)
# st.experimental_show(new_img_width)
# 
# if st.checkbox('Show help.'):
#     st.help(st.file_uploader)
# 
# if not file:
#     st.warning("Please upload an image file.")
#     st.stop()
# 
# "## Output"
# 
