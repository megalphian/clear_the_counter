import sys
import os
import io

import cv2
import boto3

s3 = boto3.client('s3')
rekt = boto3.client('rekognition')
bucket_name = 'hacked2018'

filename = 'buffer.jpg'
min_confidence = 70

is_food=False
is_dishes=False

food_list = ['Food', 'Banana', 'Pasta']
dish_list = ['Pot', 'Cup', 'Dish']

def upload_to_s3():
    try:
        s3.upload_file(filename, bucket_name, filename)
    except Exception as ex:
        print('wtf s3')

def run_recognition(img):
    try:
        response = rekt.detect_labels(Image={
        "S3Object":{
        "Bucket": bucket_name,
        "Name": filename
        }
        }, MinConfidence=min_confidence)
        return response
    except:
        print('wtf rek')

def reset_state():
    is_food = False
    is_dishes = False

if __name__=="__main__":
    cam = cv2.VideoCapture(0)
    # while True:
    try:
        ret_val, img = cam.read()
        cv2.imwrite(filename, img)
        upload_to_s3()
        # cv2.imshow('my webcam', img)
        response = run_recognition(img)
        print(len(response['Labels']))
        for i in range(len(response['Labels'])):
            if (response['Labels'][i]['Name'] in food_list) and (is_food == False):
                is_food = True
                print('FOOOOOD')
            if (response['Labels'][i]['Name'] in dish_list) and (is_dishes == False):
                is_dishes = True
                print
        reset_state()
    except Exception as ex:
        print('wtf')
        print(ex)
