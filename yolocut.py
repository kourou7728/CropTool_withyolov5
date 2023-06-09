import os
import cv2
import glob
import numpy as np
import torch
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--size', type=int, default=416, help='size to crop the image')
args = parser.parse_args()


model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
count = 0
error_list = []
input_dir = 'input'
output_dir = 'output'



if not os.path.exists(input_dir):
    os.makedirs(input_dir)

if not os.path.exists(output_dir):
    os.makedirs(output_dir)


for filename in glob.glob(os.path.join(input_dir, '*.*')):
    try:
        count += 1
        print('正在處理:', os.path.basename(filename))
        img = cv2.imread(filename)
        results = model(img)

        
        pred_boxes = results.xyxy[0][:, :4] 

        # crop&save
        for box in pred_boxes:
            x1, y1, x2, y2 = box.tolist() 
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

            width = x2 - x1
            height = y2 - y1
            center_x = (x1 + x2) // 2
            center_y = (y1 + y2) // 2
            side_length = max(width, height)

            square_x1 = center_x - side_length // 2
            square_y1 = center_y - side_length // 2
            square_x2 = square_x1 + side_length
            square_y2 = square_y1 + side_length

            square_x1 = max(square_x1, 0)
            square_y1 = max(square_y1, 0)
            square_x2 = min(square_x2, img.shape[1])
            square_y2 = min(square_y2, img.shape[0]) 

            obj_img = img[square_y1:square_y2, square_x1:square_x2]
            resized_img = cv2.resize(obj_img, (args.size, args.size), interpolation=cv2.INTER_AREA)
            
            
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, f'{os.path.basename(filename)}_{count}.jpg')
            cv2.imwrite(output_path, resized_img)
    except Exception as e:
        error_list.append(filename)
        print(f"Error processing {filename}: {e}")

print(f'Processed {count} images, {len(error_list)} images have errors:', [os.path.basename(file) for file in error_list])
