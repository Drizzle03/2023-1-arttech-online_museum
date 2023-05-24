# 캠 없이 인터랙션만 테스트 하고 싶을 떄 실행
# key 1를 누를 때 - 주먹 효과 대체, 구체가 모임
# key 2를 누를 때 - 보자기 효과 대체, 구체가 퍼짐

from p5 import *
import random

width = 1280
height = 720

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
    noStroke()
    size(width, height)
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

def key_pressed(event):
    global circles, status

    # 주먹 - 모임
    if event.key == '1':
        if status == 1:
                status = 0
                targetX = width / 2
                targetY = height / 2
                for circle in circles:
                    circle.targetX = targetX
                    circle.targetY = targetY

    # 보자기 - 퍼짐
    elif event.key == '2':
        if status == 0:
                status = 1
                for circle in circles:
                    circle.targetX = random.uniform(0, width)
                    circle.targetY = random.uniform(0, height)

run()