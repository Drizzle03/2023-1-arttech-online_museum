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
camera.set(3, 160)  # width
camera.set(4, 120)  # height

class ImageGetter(threading.Thread):
    def __init__(self, condition):
        super(ImageGetter, self).__init__()
        self.image = None
        self.condition = condition

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
            with self.condition:
                self.image = frame
                self.condition.notify()  # Notify the inferencer that a new image is ready
            time.sleep(0.01)  # To reduce CPU usage

class ModelInferencer(threading.Thread):
    def __init__(self, condition):
        super(ModelInferencer, self).__init__()
        self.prediction = None
        self.image = None
        self.new_prediction = False
        self.condition = condition

    def set_image(self, image):
        self.image = image

    def get_prediction(self):
        self.new_prediction = False
        return self.prediction

    def run(self):
        global interpreter, input_details, output_details
        while True:
            with self.condition:
                self.condition.wait()  # Wait for a new image to be ready
                if self.image is not None:
                    interpreter.set_tensor(input_details[0]['index'], self.image)
                    interpreter.invoke()
                    self.prediction = interpreter.get_tensor(output_details[0]['index'])
                    self.new_prediction = True
                    self.image = None
                time.sleep(0.01)  # To reduce CPU usage

condition = threading.Condition()

# Pass it to each thread
image_getter = ImageGetter(condition)
image_getter.start()

model_inferencer = ModelInferencer(condition)
model_inferencer.start()


class Circle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.targetX = self.x
        self.targetY = self.y
        self.easing = 0.033 #애니메이션 부드러움 조절
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
circleCount = 40  # 동그라미 개수 설정
status = 1

def setup():
    size(width, height)
    noStroke()
    for _ in range(circleCount):
        x = random.uniform(0, width)
        y = random.uniform(0, height)
        circle = Circle(x, y)
        circles.append(circle)

def draw():
    global circles, status
    fill(0, 10)
    rect(0, 0, width, height)

    for circle in circles:
        circle.move()
        circle.display()

    image = image_getter.get_image()  # 웹캠 이미지 가져오기
    if image is not None:
        model_inferencer.set_image(image)

    if model_inferencer.new_prediction:
        prediction = model_inferencer.get_prediction()

        max_prediction_index = np.argmax(prediction)  # Save the result of np.argmax()

        # 주먹 - 모임
        if max_prediction_index == 0: 
            if status == 1:
                status = 0
                targetX = width / 2
                targetY = height / 2
                for circle in circles:
                    circle.targetX = targetX
                    circle.targetY = targetY

        # 보자기 - 퍼짐
        elif max_prediction_index == 1:
            if status == 0:
                status = 1
                for circle in circles:
                    circle.targetX = random.uniform(0, width)
                    circle.targetY = random.uniform(0, height)
    fill(0, 10)
    rect(0, 0, width, height)

run()

