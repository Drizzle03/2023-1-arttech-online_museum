# 티쳐블머신 모델 경량화 파일
#
import tensorflow as tf

saved_model_dir = 'keras_model.h5'
model = tf.keras.models.load_model(saved_model_dir)

# 모델을 TensorFlow Lite 형식 양자화 변환
converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]
tflite_quant_model = converter.convert()

# 파일 저장
with open('quant_model.tflite', 'wb') as f:
  f.write(tflite_quant_model)