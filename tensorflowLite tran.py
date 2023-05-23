# 티쳐블머신 모델 경량화 파일
import tensorflow as tf

# Teachable Machine에서 내보낸 모델 파일의 경로를 입력합니다.
saved_model_dir = 'keras_model.h5'

# 모델을 불러옵니다.
model = tf.keras.models.load_model(saved_model_dir)

# 모델을 TensorFlow Lite 형식으로 양자화하여 변환합니다.
converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]
tflite_quant_model = converter.convert()

# 변환된 모델을 파일로 저장합니다.
with open('quant_model.tflite', 'wb') as f:
  f.write(tflite_quant_model)