# -*- coding: utf-8 -*-
import cv2
from keras.models import load_model
import numpy as np
import cv2

model = load_model('keras_model.h5')

image = cv2.VideoCapture(0)   
#fourcc = cv2.VideoWriter_fourcc(*'DIVX') # Codec info
# cv2.VideoWriter(outputFile, fourcc, frame, size)
#writer = cv2.VideoWriter('Output.avi', fourcc, 30.0, (640, 480))

image.set(3,600)       
image.set(4,500)
image.set(5, 30)  #set frame

image.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('M', 'J', 'P', 'G'))

while ( image.isOpened() ):
    ret, frame = image.read()
    
    size = (224, 224)
    image2 = cv2.resize(frame, size)
    #turn the image into a numpy array
    image_array = np.asarray(image2)
# Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
# Load the image into the array
    data = np.array([normalized_image_array])

# run the inference
    prediction = model.predict(data)

    if(np.argmax(prediction) == 0):
        cv2.putText(frame, "Rock", (50,50), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 255, 0), 1, cv2.LINE_AA)
    elif(np.argmax(prediction) == 1):
        cv2.putText(frame, "Paper", (50,50), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 255), 1, cv2.LINE_AA)
    
    cv2.imshow('Pose Monitoring', frame)
#    writer.write(frame)
    
    if cv2.waitKey(1) == ord('q'):
        break

image.release()  
#writer.release()
cv2.destroyAllWindows()