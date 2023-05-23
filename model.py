import cv2
import numpy as np
import tensorflow as tf

# TensorFlow Lite 모델 파일의 경로를 입력합니다.
model_path = 'keras_model.h5'

# TensorFlow Lite 모델을 로드합니다.
interpreter = tf.lite.Interpreter(model_path=model_path)
interpreter.allocate_tensors()

# 입력 및 출력 텐서에 대한 정보를 가져옵니다.
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# 웹캠을 초기화합니다.
cap = cv2.VideoCapture(0)

while True:
    # 프레임을 읽어옵니다.
    ret, frame = cap.read()

    # 프레임 크기를 조정하고 전처리합니다.

    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    # 프레임 크기를 조정하고 전처리합니다.
    frame_resized = cv2.resize(frame, (224, 224))
    frame_resized = np.expand_dims(frame_resized, axis=0)
    frame_resized = frame_resized / 255.0

    # TensorFlow Lite 모델로 예측을 수행합니다.
    interpreter.set_tensor(input_details[0]['index'], frame_resized.astype(np.float32))
    interpreter.invoke()
    prediction = interpreter.get_tensor(output_details[0]['index'])

    # 화면에 결과를 표시합니다.
    if(np.argmax(prediction) == 0):
        cv2.putText(frame, "Masked", (50,50), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 255, 0), 1, cv2.LINE_AA)
    elif(np.argmax(prediction) == 1):
        cv2.putText(frame, "No Masked", (50,50), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 255), 1, cv2.LINE_AA)

    cv2.imshow('Mask Monitoring', frame)

    # 'q' 키를 누르면 종료합니다.
    if cv2.waitKey(1) == ord('q'):
        break

# 웹캠과 창을 해제합니다.
cap.release()
cv2.destroyAllWindows()
