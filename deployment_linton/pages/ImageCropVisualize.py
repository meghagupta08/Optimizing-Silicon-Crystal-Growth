from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st  # 🎈 data web app development
from pprint import pprint
import sys
from pathlib import Path

FILE = Path(__file__).resolve()
ROOT = FILE.parents[1]  # YOLOv5 root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH

pprint(sys.path)

import config_loader as conf_loader
import APIAccess as api


options = conf_loader.load_options()


arg_dict = {}
arg_dict['source'] = options['api_source']
arg_dict['width'] = 250
arg_dict['height'] = 350
arg_dict['number'] = -1
stream_images = api.get_API_stream_images(arg_dict) #API Call
placeholder = st.empty()

def get_api_image():
    frame_number = 0
    PIL_image = None
    for single_frame in stream_images:
        frame_number=frame_number+1
        with placeholder.container():
            PIL_image = Image.fromarray(np.uint8(single_frame)).convert('RGB')
            if frame_number == 1:
                break
            break
    return PIL_image



def show_image(image, x1, y1, x2, y2):
    fig, ax = plt.subplots()
    ax.imshow(image)
    rect = plt.Rectangle((x1, y1), x2-x1, y2-y1, linewidth=1, edgecolor='r', facecolor='none')
    ax.add_patch(rect)
    plt.axis('on')
    st.pyplot(fig)

def crop_image(image, left, top, width, height):
    pil_image = Image.fromarray(image)
    cropped_img = pil_image.crop((left, top, width, height))
    cropped_img_np = np.array(cropped_img)
    return cropped_img_np


st.title("Image Cropper")
api_image = get_api_image()


if __name__ == '__main__':
    if api_image is not None:
        api_image = np.array(api_image)
        h, w = api_image.shape[:2]
        x1 = st.text_input("Enter the x-coordinate of the top-left corner (0 to {})".format(w-1), "0")
        y1 = st.text_input("Enter the y-coordinate of the top-left corner (0 to {})".format(h-1), "0")
        x2 = st.text_input("Enter the x-coordinate of the bottom-right corner (0 to {})".format(w-1), str(w))
        y2 = st.text_input("Enter the y-coordinate of the bottom-right corner (0 to {})".format(h-1), str(h))
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        # if x1 >= x2 or y1 >= y2 or x1 < 0 or y1 < 0 or x2 > w or y2 > h:
        #     st.error("Invalid coordinates. Please enter valid coordinates.")
        # else:
        cropped_image = crop_image(api_image, x1, y1, x2, y2)
        st.subheader("Original Image")
        show_image(api_image, x1, y1, x2, y2)
        st.subheader("Cropped Image")
        st.image(cropped_image, use_column_width=True)