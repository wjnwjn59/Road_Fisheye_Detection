import argparse

from models.yolov8.model import YOLOv8

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', type=str, required=True)
    parser.add_argument('--root_dir', type=str, default='../../datasets/Fisheye8K')
    parser.add_argument('--is_eval', type=bool, default=True)
    args = parser.parse_args()

    if 'yolov8' in args.model:
        model = YOLOv8(
            model_name=args.model,
            dataset_root_dir=args.root_dir
        )
    else:
        raise RuntimeError
    
    model.train()
    model.eval()

if __name__ == '__main__':
    main()