import tensorflow as tf
import cv2
import numpy as np
from p5 import *
import random
import threading
import time

# TensorFlow Lite 모델 load
interpreter = tf.lite.Interpreter(model_path="quant_model.tflite")
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# 웹캠 load
camera = cv2.VideoCapture(0)
camera.set(3, 320)  # width - lower resolution
camera.set(4, 240)  # height - lower resolution

class ImageGetter(threading.Thread):
    def __init__(self):
        super(ImageGetter, self).__init__()
        self.image = None

    def get_image(self):
        return self.image

    def run(self):
        global camera
        while True:
            ret, frame = camera.read()
            frame = cv2.resize(frame, (224, 224))  # resize
            frame = np.asarray(frame)  # to numpy array
            frame = (frame.astype(np.float32) / 127.0) - 1  # normalize
            frame = np.expand_dims(frame, axis=0)  # expand dimension
            self.image = frame
            time.sleep(0.01)  # sleep for a while to reduce CPU usage

class ModelInferencer(threading.Thread):
    def __init__(self):
        super(ModelInferencer, self).__init__()
        self.prediction = None
        self.image = None
        self.new_prediction = False

    def set_image(self, image):
        self.image = image

    def get_prediction(self):
        self.new_prediction = False
        return self.prediction

    def run(self):
        global interpreter, input_details, output_details
        while True:
            if self.image is not None:
                interpreter.set_tensor(input_details[0]['index'], self.image)
                interpreter.invoke()
                self.prediction = interpreter.get_tensor(output_details[0]['index'])
                self.new_prediction = True
                self.image = None
            time.sleep(0.01)  # sleep for a while to reduce CPU usage

image_getter = ImageGetter()
image_getter.start()

model_inferencer = ModelInferencer()
model_inferencer.start()


class Circle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.targetX = self.x
        self.targetY = self.y
        self.easing = 0.05
        self.size = random.uniform(20, 80)  
        # 동그라미의 크기 랜덤 설정

    def move(self):
        dx = self.targetX - self.x
        dy = self.targetY - self.y
        self.x += dx * self.easing
        self.y += dy * self.easing

    def display(self):
        circle((self.x, self.y), self.size)

circles = []
circleCount = 20  # 동그라미 개수 설정
status = 1

def setup():
    size(1280, 720)
    for _ in range(circleCount):
        x = random.uniform(0, width)
        y = random.uniform(0, height)
        circle = Circle(x, y)
        circles.append(circle)

def draw():
    global circles, status

    background(255)
    for circle in circles:
        circle.move()
        circle.display()

    image = image_getter.get_image()  # 웹캠 이미지 가져오기
    if image is not None:
        model_inferencer.set_image(image)

    if model_inferencer.new_prediction:
        prediction = model_inferencer.get_prediction()

        # 주먹 - 모임
        if np.argmax(prediction) == 0: 
            if status == 1:
                status = 0
                targetX = width / 2
                targetY = height / 2
                for circle in circles:
                    circle.targetX = targetX
                    circle.targetY = targetY

        # 보자기 - 퍼짐
        elif np.argmax(prediction) == 1:
            if status == 0:
                status = 1
                for circle in circles:
                    circle.targetX = random.uniform(0, width)
                    circle.targetY = random.uniform(0, height)

run()

