import streamlit as st  # 🎈 data web app development
from PIL import Image
import numpy as np
import os
import config_loader as conf_loader
import yolov5.detect as yolo_detect

os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
options = {}

st.set_page_config(
    page_title="Real-Time facet detection dashboard",
    page_icon="✅",
    layout="wide",
)

# dashboard title
st.title("Real-Time facet detection")

# creating a single-element container
placeholder = st.empty()

options = conf_loader.load_options()

print("\n ------ ENVRIONMENT VARIBALES -------------------\n\n")
print(options)

try:
    for detection in yolo_detect.main(options):

        with placeholder.container():

            st.markdown("### Facet detection")

            PIL_image = Image.fromarray(np.uint8(detection)).convert('RGB')

            st.image(PIL_image)
except StopIteration as e:
    st.markdown("End of images.")

        #time.sleep(5)



