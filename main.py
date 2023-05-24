import tensorflow as tf
import cv2
import numpy as np
from p5 import *
import random
import threading
import time

width = 1280
height = 720

# TensorFlow Lite 모델 load
interpreter = tf.lite.Interpreter(model_path="quant_model.tflite")
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# 웹캠 load
camera = cv2.VideoCapture(0)
camera.set(3, 224)  # width - 해상도 낮춤
camera.set(4, 224)  # height - 해상도 낮춤

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
            frame = cv2.resize(frame, (224, 224)) 
            frame = np.asarray(frame)
            frame = (frame.astype(np.float32) / 127.0) - 1 
            frame = np.expand_dims(frame, axis=0) 
            self.image = frame
            time.sleep(0.01)  # CPU 부담을 줄이기 위해 적용

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
            time.sleep(0.01)  # CPU 부담을 줄이기 위해 적용

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
        self.easing = 0.02 #애니메이션 부드러움 조절
        self.size = random.uniform(10, 50)  
        # 동그라미 랜덤 크기 설정

    def move(self):
        dx = self.targetX - self.x
        dy = self.targetY - self.y
        self.x += dx * self.easing  
        self.y += dy * self.easing

    def display(self):
        fill(255)
        ellipse(self.x, self.y, self.size, self.size)


circles = []
circleCount = 30  # 동그라미 개수 설정
status = 1

def setup():
    size(width, height)
    for _ in range(circleCount):
        x = random.uniform(0, width)
        y = random.uniform(0, height)
        circle = Circle(x, y)
        circles.append(circle)

def draw():
    global circles, status

    fill(0, 30)
    rect(0, 0, width, height)

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

