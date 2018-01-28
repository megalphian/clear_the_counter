import sys
import os
import time

import cv2
import boto3
import json

import slack_handler

s3 = boto3.client('s3')
rekt = boto3.client('rekognition')
bucket_name = 'hacked2018'

filename = 'buffer.jpg'
min_confidence = 70

is_food=False
is_dishes=False

food_list = ['Food', 'Banana', 'Pasta', 'Bottle', 'Beverage']
dish_list = ['Pot', 'Pottery', 'Cup', 'Cutlery', 'Dish', 'Plate', 'Fork', 'Spoon', 'Knife']

def upload_to_s3():
    try:
        s3.upload_file(filename, bucket_name, filename)
    except Exception as ex:
        print('wtf s3')

def run_recognition():
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

def reset_state(wait_time=20):
    global is_food, is_dishes
    is_food = False
    is_dishes = False
    print('Waiting for the next check')
    time.sleep(wait_time)

if __name__=="__main__":
    cam = cv2.VideoCapture(0)
    while True:
        try:
            ret_val, img = cam.read()
            cv2.imwrite(filename, img)
            upload_to_s3()
            response = run_recognition()
            print(response['Labels'])
            for i in range(len(response['Labels'])):
                if (response['Labels'][i]['Name'] in food_list) and (is_food == False):
                    is_food = True
                    is_dishes = False
                elif (response['Labels'][i]['Name'] in dish_list) and (is_dishes == False) and (is_food == False):
                    is_dishes = True
                    is_food = False

            if (is_food==True) or (is_dishes==True):
                if is_food:
                    slack_handler.upload_file('FREE FOOOD', 'Get what you need', filename)
                elif is_dishes:
                    slack_handler.upload_file('SHAME SHAME SHAME', 'Please clear the mess up', filename)
                print('Sleep')
                reset_state(wait_time=60)
            else:
                reset_state()
        except Exception as ex:
            print('wtf')
            print(ex)
