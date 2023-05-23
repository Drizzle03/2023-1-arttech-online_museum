# 필요한 라이브러리를 불러옵니다.
from keras.models import load_model
import cv2
import numpy as np
from p5 import *
import random

# Keras 모델을 불러옵니다.
model = load_model('keras_model.h5')

# 웹캠을 불러옵니다.
camera = cv2.VideoCapture(0)
camera.set(3, 640)  # width
camera.set(4, 480)  # height

# 웹캠에서 이미지를 가져오는 함수입니다.
def get_image():
    ret, frame = camera.read()
    frame = cv2.resize(frame, (224, 224))  # resize
    frame = np.asarray(frame)  # to numpy array
    frame = (frame.astype(np.float32) / 127.0) - 1  # normalize
    frame = np.expand_dims(frame, axis=0)  # expand dimension
    return frame

class Circle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.targetX = self.x
        self.targetY = self.y
        self.easing = 0.05
        self.size = random.uniform(20, 80)  # 동그라미의 크기를 무작위로 설정

    def move(self):
        dx = self.targetX - self.x
        dy = self.targetY - self.y
        self.x += dx * self.easing
        self.y += dy * self.easing

    def display(self):
        circle((self.x, self.y), self.size)

circles = []
circleCount = 20  # 동그라미 개수 설정



def setup():
    size(1280, 720)
    for _ in range(circleCount):
        x = random.uniform(0, width)
        y = random.uniform(0, height)
        circle = Circle(x, y)
        circles.append(circle)

def draw():
    global circles
    background(255)
    for circle in circles:
        circle.move()
        circle.display()

    # 이미지 로드
    image = get_image()

    # 예측 결과 도출
    prediction = model.predict(image)

    if np.argmax(prediction) == 0:  # 주먹일 경우
        targetX = width / 2
        targetY = height / 2
        for circle in circles:
            circle.targetX = targetX
            circle.targetY = targetY

    elif np.argmax(prediction) == 1:  # 보자기일 경우
        for circle in circles:
            circle.targetX = random.uniform(0, width)
            circle.targetY = random.uniform(0, height)

run()
