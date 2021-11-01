try:
	import PIL
	import numpy as np
	import tensorflow as tf
	from tensorflow import keras
	from tensorflow.keras.optimizers import Nadam
	from tensorflow.keras.preprocessing.image import ImageDataGenerator
except ModuleNotFoundError:
	print('ERROR: Some modules are missing')
	exit()

def build(output_types, activation, loss, optimizer):
	data = tf.keras.Input(shape=(120, 120, 3))
	inputs = tf.keras.layers.Conv2D(16, 3, padding='same', activation='relu')(data)
	inputs = tf.keras.layers.MaxPooling2D(strides=2)(inputs)
	inputs = tf.keras.layers.Conv2D(32, 3, padding='same', activation='relu')(inputs)
	inputs = tf.keras.layers.MaxPooling2D(strides=2)(inputs)
	inputs = tf.keras.layers.Conv2D(64, 3, padding='same', activation='relu')(inputs)
	inputs = tf.keras.layers.MaxPooling2D(strides=2)(inputs)
	inputs = tf.keras.layers.Flatten()(inputs)
	inputs = tf.keras.layers.Dense(128, activation='relu')(inputs)
	outputs = tf.keras.layers.Dense(output_types, activation=activation)(inputs)

	model = tf.keras.Model(inputs=data, outputs=outputs)
	model.compile(optimizer=optimizer, loss=loss, metrics=['accuracy'])

	return model

try:
	data_path = ',,/possible-tiles'
	generator = ImageDataGenerator(rescale=1./255, shear_range=0.3, zoom_range=0.3, horizontal_flip=True)
	data = generator.flow_from_directory(data_path, target_size=(120,120), batch_size=32, class_mode='categorical')
	print('SUCCESS: Generator set up success')
except FileNotFoundError:
	print('ERROR: Cannot find data files')
	exit()

cnn_model = build(output_types=13, activation='softmax', loss='log_cosh', optimizer=Nadam(learning_rate=0.0003))
cnn_model.summary()
cnn_model.fit(x=data, epochs=3)
cnn_model.save('figures_recognition.h5')
