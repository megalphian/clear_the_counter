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

if __name__=="__main__":
    cam = cv2.VideoCapture(0)
    # while True:
    try:
        ret_val, img = cam.read()
        cv2.imwrite(filename, img)
        upload_to_s3()
        # cv2.imshow('my webcam', img)
        response = run_recognition(img)
        type(response)
    except Exception as ex:
        print('wtf')
        print(ex)
