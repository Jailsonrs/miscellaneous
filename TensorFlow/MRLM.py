import pandas as pd
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

column_names = ['MPG','Cylinders','Displacement','Horsepower','Weight',
                'Acceleration', 'Model Year', 'Origin']

dataset_path = keras.utils.get_file("auto-mpg.data", "http://archive.ics.uci.edu/ml/machine-learning-databases/auto-mpg/auto-mpg.data")                
raw_dataset = pd.read_csv(dataset_path, names=column_names,
                      na_values = "?", comment='\t',
                      sep=" ", skipinitialspace=True)


dataset = raw_dataset.copy()
dataset.tail()

dataset.isna().sum()

dataset = dataset.dropna()

origin = dataset.pop('Origin')

dataset['USA'] = (origin == 1)*1.0
dataset['Europe'] = (origin == 2)*1.0
dataset['Japan'] = (origin == 3)*1.0

dataset.tail()

train_dataset = dataset.sample(frac=0.8, random_state=0)
test_dataset = dataset.drop(train_dataset.index)

train_stats = train_dataset.describe()
train_stats.pop("MPG")
train_stats = train_stats.transpose()
train_stats

train_labels = train_dataset.pop('MPG')
test_labels = test_dataset.pop('MPG')

def norm(x):
  return (x - train_stats['mean']) / train_stats['std']

normed_train_data = norm(train_dataset)
normed_test_data = norm(test_dataset)

model.summary()
example_batch = normed_train_data[:10]
example_result = model.predict(example_batch)
example_result

## input -> relu(xTb) -> output

class MyDense2(keras.layers.Layer):
	def __init__(self, features_n):
		super(MyDense2, self).__init__()
		
		init_w = tf.random_normal_initializer()
		self.w = tf.Variable(
			initial_value = init_w( shape = (features_n-1,), dtype = "float32"),
			trainable = True)

		init_b = tf.random_normal_initializer()
		self.b = tf.Variable(
			initial_value = init_b(shape = (1, ), dtype = "float32"), 
			trainable = True)		

		def call(self, input):
			self.x = tf.matmul(self.input,self.w)+self.b
			return(self.x)



model = keras.Sequential([
		MyDense2(33),
		MyDense2(1)
	])
optimizer = tf.keras.optimizers.RMSprop(0.001)


model.compile(loss='mse',
              optimizer=optimizer,
              metrics=['mae', 'mse'])

model.fit()































