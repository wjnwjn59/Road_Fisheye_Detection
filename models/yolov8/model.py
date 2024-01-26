import os
import yaml
import json

from pathlib import Path
from ultralytics import YOLO

class YOLOv8:
    def __init__(self, model_name: str, dataset_root_dir: str) -> None:
        self.model_name = self.get_model_path(model_name)
        self.model = YOLO(self.model_name)
        self.id_to_cls = {
            0: 'Bus',
            1: 'Bike',
            2: 'Car',
            3: 'Pedestrian',
            4: 'Truck'
        }
        self.config = self.load_config()
        self.dataset_root_dir = dataset_root_dir
        self.yolo_yaml_path = os.path.join(
            self.dataset_root_dir, 'fisheye8k_data.yaml'
        )

    def get_model_path(self, model_name):
        current_dir = Path(__file__).parent
        model_path = current_dir / 'weights' / f'{model_name}.pt'

        return model_path

    def load_config(self) -> dict:
        current_dir = Path(__file__).parent
        config_file_path = current_dir / 'config.json'

        with open(config_file_path, 'r') as file:
            config = json.load(file)

        return config
    
    def create_yaml_file(self) -> None:
        data_yaml = {
            'path': os.path.abspath(self.dataset_root_dir),
            'train': 'train/images',
            'val': 'test/images',
            'nc': len(self.id_to_cls.keys()),
            'names': self.id_to_cls 
        }

        with open(self.yolo_yaml_path, 'w') as f:
            yaml.dump(data_yaml, f, default_flow_style=False)

    def check_yaml_file(self) -> None:
        self.create_yaml_file()

    def train(self) -> None:
        self.check_yaml_file()

        self.model.train(
            data=self.yolo_yaml_path,
            **self.config
        )

    def detect(self, src_img) -> dict:
        results = self.model.predict(src_img, verbose=False)[0]

        return results

    def eval(self, is_save: bool=False) -> dict:
        project_name = os.path.join(
            self.config['project'],
            self.config['name']
        )
        results = self.model.val(
            name='evaluation',
            save_json=is_save
        )

        return results