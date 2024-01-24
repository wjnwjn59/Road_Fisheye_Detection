import os
import importlib.util
import json

class Detector:
    def __init__(self, model_name):
        self.model_name = model_name
        self.model = None
        self.config = None
        self.cls_to_id = {
            'Bus': 0,
            'Bike': 1,
            'Car': 2,
            'Pedestrian': 3,
            'Truck': 4
        }
        self.load_model()

    def load_model(self):
        model_path = f"models/{self.model_name}/model.py"
        config_path = f"models/{self.model_name}/config.json"

        # Dynamically import the model module
        spec = importlib.util.spec_from_file_location("model", model_path)
        model_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(model_module)

        # Load model
        self.model = model_module.Model()

        # Load config
        with open(config_path, 'r') as file:
            self.config = json.load(file)

    def train(self):
        # Implement training logic using self.model and self.config
        pass
