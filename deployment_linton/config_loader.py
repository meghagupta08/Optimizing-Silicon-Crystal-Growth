from pathlib import Path
import os
import sys

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # YOLOv5 root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative
ROOT = ROOT / 'yolov5'

print(ROOT)
options = {
    # 'weights': ['yolov5_ws/yolov5/runs/train/exp/weights/best.pt'],
    'weights': [ROOT / 'runs/train/exp3/weights/best.pt'],
    'source': 'C:/Users/mxggis/Documents/PythonScripts/Linton_ImageAnalysis/yolov5_ws/CroppedImages/FulllengthImages',
    'data': ROOT / 'data/dataset.yaml',
    'imgsz': [640, 640],
    'conf_thres': 0.50,
    'iou_thres': 0.35,
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
    'line_thickness': 2,
    'hide_labels': False,
    'hide_conf': False,
    'half': False,
    'dnn': False,
    'vid_stride': 1
    , 'fileName': ''
    , 'resize': False
    , 'resize_image_val': 299
    , 'crop': False
    , 'crop_val': [360,260,410,290] #[375,265,30,30]
    ,'api_source':'aipngstream_endpoint.dat'

}



def load_options():
    for key, value in options.items():
        env_key_value = None
        if os.environ.get(key.upper()):
            env_key_value = os.environ.get(key.upper())
        elif os.environ.get(key.lower()):
            env_key_value = os.environ.get(key.lower())
        if env_key_value:
            if key.strip() == 'api_source':
                options[key] = env_key_value
            elif key.strip() == 'crop':
                if env_key_value == "True":
                    options[key] = True
                else:
                    options[key] = False
            elif key.strip() == 'crop_val':
                options[key] = [int(val) for val in env_key_value.strip().split(",")]
            elif key.strip() == 'conf_thres':
                options[key] = float(env_key_value)
            elif key.strip() == 'iou_thres':
                options[key] = float(env_key_value)
            elif key.strip() == 'source':
                options[key] = env_key_value
            elif key.strip() == 'resize':
                if env_key_value == "True":
                    options[key] = True
                else:
                    options[key] = False
            elif key.strip() == 'resize_image_val':
                options[key] = int(env_key_value)
            elif key.strip() == 'view_img':
                if env_key_value == "True":
                    options[key] = True
                else:
                    options[key] = False
    return options



