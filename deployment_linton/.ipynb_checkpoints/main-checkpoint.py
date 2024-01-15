import time  # to simulate a real time data, time loop
import streamlit as st  # 🎈 data web app development

import time
import yolov5.detect as yolo_detect
from pathlib import Path
import os
import sys
from PIL import Image
import numpy as np


FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # YOLOv5 root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative
ROOT = ROOT / 'yolov5'

print(ROOT)
options = {
    #'weights': ['yolov5_ws/yolov5/runs/train/exp/weights/best.pt'],
           'weights': [ROOT / 'runs/train/exp6/weights/best.pt'],
 'source': 'C:/Users/mxggis/Documents/PythonScripts/Linton_ImageAnalysis/yolov5_ws/CroppedImages/FulllengthImages',
 #'source': 'Z:/Data/Image Data/Video/project.avi',
 'data': ROOT / 'data/dataset.yaml',
 'imgsz': [640,640],
 'conf_thres': 0.50,
 'iou_thres': 0.45,
 'max_det': 1000,
 'device': '',
 'view_img': False,
 'save_txt': False,
 'save_conf': False,
 'save_crop': False,
 'nosave': False,
 'classes': None,
 'agnostic_nms': False,
 'augment': True,
 'visualize': False,
 'update': False,
 'project': ROOT / 'runs/detect',
 'name': 'exp',
 'exist_ok': False,
 'line_thickness': 2 ,
 'hide_labels': False,
 'hide_conf': False,
 'half': False,
 'dnn': False,
 'vid_stride': 1
  #,'fileName': ""
}

st.set_page_config(
    page_title="Real-Time facet detection dashboard",
    page_icon="✅",
    layout="wide",
)

# dashboard title
st.title("Real-Time facet detection")

# creating a single-element container
placeholder = st.empty()


for detection in yolo_detect.main(options):

    with placeholder.container():

        st.markdown("### Facet detection")

        PIL_image = Image.fromarray(np.uint8(detection)).convert('RGB')

        st.image(PIL_image)

        #time.sleep(5)