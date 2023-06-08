from p5 import *

button_images = []  
active_buttons = []  

mx = [0]*60  # 마우스의 x좌표를 저장할 리스트
my = [0]*60  # 마우스의 y좌표를 저장할 리스트
num = 60

save_deactive_images = ''
save_button = 'deactive'
frame = True

def setup():
    size(1280, 720)  
    no_stroke()
    load_button_images()

def draw():
    global save_button, frame

    if frame:
        background(255)
        frame = False

    fill("#E6E6E6")
    rect(0, 613, 1280, 108)

    if 1 in active_buttons:  # btn2가 활성화되었을 경우
        which = frame_count % num
        mx[which] = mouse_x
        my[which] = min(613, mouse_y)  # 마우스의 y 좌표가 613 이상이면 613으로 고정

        for i in range(num):
            index = (which + 1 + i) % num
            ellipse(mx[index], my[index], i, i)

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
