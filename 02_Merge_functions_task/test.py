from p5 import *

previous_mouse_x = 0

def setup():
    size(800, 800)

def draw():
    global previous_mouse_x

    if abs(mouse_x - previous_mouse_x) > 1:
        background(255)  # background는 draw 함수 내에서 호출되어야 합니다.
        create_and_draw_shape()
        previous_mouse_x = mouse_x

def create_and_draw_shape():
    translate(width/2, height/2)

    start_angle = map_value(mouse_x, 0, width, 0, 360)
    num_lines = 720

    for angle in range(num_lines):
        adjusted_angle = (angle + start_angle) % num_lines
        r = map_value(adjusted_angle, 0, num_lines - 1, 255, 105)
        stroke(r, 105, 180)
        stroke_weight(3)

        x = cos(radians(adjusted_angle)) * (width/4)
        y = sin(radians(adjusted_angle)) * (width/4)

        line(0, 0, x, y)

def map_value(value, leftMin, leftMax, rightMin, rightMax):
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    valueScaled = float(value - leftMin) / float(leftSpan)
    return rightMin + (valueScaled * rightSpan)

run()
