from p5 import *

button_images = []  
active_buttons = []  

num = 60

save_deactive_images = ''
save_button = 'deactive'
frame = True

# 색상 리스트
color_list = ["#F2EEE5", "#E5C1C5", "#C3E2DD", "#6ECEDA"]
color_index = 0

class Spin:
    def __init__(self, xpos, ypos, s):
        self.x = xpos
        self.y = ypos
        self.speed = s
        self.angle = 0.0

    def update(self):
        self.angle += self.speed


class SpinSpots(Spin):
    def __init__(self, x, y, s, d):
        super().__init__(x, y, s)
        self.dim = d

    def display(self):
        no_stroke()
        push_matrix()
        translate(mouse_x, mouse_y)  # 변경된 부분
        self.angle += self.speed
        rotate(self.angle)
        ellipse(-self.dim/2, 0, self.dim, self.dim)
        ellipse(self.dim/2, 0, self.dim, self.dim)
        pop_matrix()


spots = None
arm = None

def setup():
    global spots, arm
    size(1280, 720)  
    no_stroke()
    load_button_images()
    spots = SpinSpots(width/2, height/2, -0.02, 90.0)

def draw():
    global save_button, frame, spots, arm, color_list, color_index
    if frame:
        background(255)
        frame = False

    fill("#E6E6E6")
    rect(0, 613, 1280, 108)

    # btn1가 활성화되었을 경우
    if 0 in active_buttons:
        fill(color_list[color_index])
        spots.update()
        spots.display()

    # btn2가 활성화되었을 경우
    if 1 in active_buttons: 
        which = frame_count % num
        mousey = min(600, mouse_y)  # 마우스의 y 좌표가 613 이상이면 613으로 고정

        fill(color_list[color_index])
        ellipse(mouse_x, mousey, 30, 30)
            
    # 색상 인덱스 갱신
    color_index = (color_index + 1) % len(color_list)



    if 5 in active_buttons: 
        frame = True

    draw_button()

def draw_button():
    global save_button
    for i in range(len(button_images)):
        if i in active_buttons:
            active_image = load_image(f"source/btn{i+1}-active.png")
            image(active_image, 355+(i*99), 627, 75, 75)  
        else:
            image(button_images[i], 355+(i*99), 627, 75, 75)  

    if save_button == 'deactive':
        image(save_deactive_images, 1175, 628, 75, 75)
    else:
        save_active_image = load_image("source/save-active.png")
        image(save_active_image, 1175, 628, 75, 75)

def load_button_images():
    global save_deactive_images
    save_deactive_images = load_image('source/save-deactive.png')

    for i in range(6):
        button_image = load_image(f"source/btn{i+1}-deactive.png")
        button_images.append(button_image)

def mouse_pressed():
    global save_button

    for i in range(len(button_images)):
        button_x = 355 + (i * 99)
        button_y = 613
        button_width = 75
        button_height = 75

        if button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_height:
            if i in active_buttons:
                active_buttons.remove(i)
            else:
                active_buttons.append(i)

    save_btn_x = 1175
    save_btn_y = 628

    if save_btn_x <= mouse_x <= save_btn_x + button_width and save_btn_y <= mouse_y <= save_btn_y + button_height:
        if save_button == 'deactive':
            save_button = 'active'
        else:
            save_button = 'deactive'

run()
