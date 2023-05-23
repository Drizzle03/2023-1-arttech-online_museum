# 필요한 라이브러리를 불러옵니다.
import cv2
import numpy as np
from p5 import *
import tensorflow as tf

# TensorFlow Lite 모델을 불러옵니다.
interpreter = tf.lite.Interpreter(model_path="quant_model.tflite")
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

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

def setup():
    size(640, 480)

def draw():
    background(255)

    # 이미지 로드
    image = get_image()

    # 이미지를 모델의 입력 텐서에 설정
    interpreter.set_tensor(input_details[0]['index'], image)
    # 모델 실행
    interpreter.invoke()
    # 예측 결과 도출
    prediction = interpreter.get_tensor(output_details[0]['index'])

    if np.argmax(prediction) == 0:  # 주먹일 경우
        fill(255, 0, 0)
        circle((320, 240), 100)  # 원 그림

    elif np.argmax(prediction) == 1:  # 보자기일 경우
        fill(0, 255, 0)
        rect((260, 190), 120, 100)  # 사각형 그림

run()
