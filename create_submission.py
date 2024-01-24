import os
import argparse
import json

class SubmissionCreator:
    def __init__(self) -> None:
        self.save_dir = ''
    
    def get_image_Id(self, img_name):
        img_name = img_name.split('.png')[0]
        sceneList = ['M', 'A', 'E', 'N']
        cameraIndx = int(img_name.split('_')[0].split('camera')[1])
        sceneIndx = sceneList.index(img_name.split('_')[1])
        frameIndx = int(img_name.split('_')[2])
        imageId = int(str(cameraIndx)+str(sceneIndx)+str(frameIndx))
        
        return imageId
    
