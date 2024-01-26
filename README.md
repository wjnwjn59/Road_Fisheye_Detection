# Road Fisheye Detection
## Description
Source code for AI CITY 2024 Challenge Track 4: Road Object Detection in Fish-Eye Cameras.

## Datasets
Download Fisheye8K dataset at [here](https://scidm.nchc.org.tw/en/dataset/fisheye8k).

## Methods
- [x] Survey paper: [here](https://arxiv.org/pdf/2205.13281.pdf)
- [x] YOLOv8
- [] Co-DETR
- [] [FisheyeYOLO](https://ml4ad.github.io/files/papers2020/FisheyeYOLO:%20Object%20Detection%20on%20Fisheye%20Cameras%20for%20Autonomous%20Driving.pdf)


## Benchmarks

The table below reported models performance on Fishey8K test set.

| Model    | Version | Input Size | Precision | Recall | mAP0.5 | mAP0.5-0.95 | F1-score | APS  | APM  | APL  | Inference[ms] |
| -------- | ------- | ---------- | --------- | ------ | ------ | ----------- | -------- | ---- | ---- | ---- | ------------- |
| YOLOv8  | YOLOv8s     | 640x480    | 0.xx      | 0.xx   | 0.xx   | 0.xx        | 0.xx     | 0.xx | 0.xx | 0.xx | 0.xx          |
| YOLOv8  | YOLOv8m     | 640x480    | 0.xx      | 0.xx   | 0.xx   | 0.xx        | 0.xx     | 0.xx | 0.xx | 0.xx | 0.xx          |
| Co-DETR  |  x     | 640x480    | 0.xx      | 0.xx   | 0.xx   | 0.xx        | 0.xx     | 0.xx | 0.xx | 0.xx | 0.xx          |
