from p5 import *
import random

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
    background(255)
    for circle in circles:
        circle.move()
        circle.display()

def key_pressed(event):
    global circles
    if event.key == '1':
        targetX = width / 2
        targetY = height / 2
        for circle in circles:
            circle.targetX = targetX
            circle.targetY = targetY
    elif event.key == '2':
        for circle in circles:
            circle.targetX = random.uniform(0, width)
            circle.targetY = random.uniform(0, height)

run()