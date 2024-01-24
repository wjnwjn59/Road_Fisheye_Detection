import os
import yaml
import json

from ultralytics import YOLO

class YOLOv8:
    def __init__(self, model_name: str) -> None:
        self.model_name = model_name
        self.model = YOLO(model_name)
        self.cls_to_id = {
            'Bus': 0,
            'Bike': 1,
            'Car': 2,
            'Pedestrian': 3,
            'Truck': 4
        }
        self.config = self.load_config()
        self.data_root_dir = 'datasets/Fisheye8k'
        self.yolo_yaml_path = os.path.join(
            self.data_root_dir, 'fisheye8k_data.yaml'
        )

    def load_config(self) -> dict:
        config_file_path = 'config.json'

        with open(config_file_path, 'r') as file:
            config = json.load(file)

        return config
    
    def create_yaml_file(self) -> None:
        data_yaml = {
            'path': self.dataset_root_dir,
            'train': 'train/images/camera',
            'val': 'test/images/camera',
            'nc': len(self.cls_to_id.keys()),
            'names': self.cls_to_id 
        }

        with open(self.yolo_yaml_path, 'w') as f:
            yaml.dump(data_yaml, f, default_flow_style=False)

    def check_yaml_file(self) -> None:
        if not os.path.exists(self.yolo_yaml_path):
            self.create_yaml_file()

    def train(self) -> None:
        self.check_yaml_file()

        self.model.train(
            **self.config
        )

    def detect(self, src_img) -> dict:
        results = self.model.predict(src_img, verbose=False)[0]

        return results

    def eval(self) -> dict:
        results = self.model.eval(save=False)

        return results