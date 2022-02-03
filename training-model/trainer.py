''' TRAINING AN IMAGE CLASSIFIER - by JOAO ESTEVES'''

''' IMPORTING LIBRARIES '''

print('Importing Libraries...')
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
from tensorflow.keras.utils import image_dataset_from_directory
from tensorflow.data import AUTOTUNE
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Activation, Dense, Flatten, BatchNormalization, Conv2D, MaxPool2D, Rescaling, MaxPooling2D
from tensorflow.keras.losses import SparseCategoricalCrossentropy


'''HYPERPARAMETERS & DIMENSIONS'''
# To increase the accuracy, tune the hyperparameters
batch_size = 40
img_height = 64
img_width = 64
epochs = 8


'''DATA PREPARATION'''

print('Preprocessing data...')
# Directory
data_dir_train = 'data/train'
data_dir_test = 'data/test'

# Generating validation dataset from images in directory
val_ds = image_dataset_from_directory(
  data_dir_train,
  labels='inferred',                                                            # labels generated from directory structure
  validation_split=1/6,                                                         # fraction of data to reserve for validation
  subset='validation',                                                          # one of "training" or "validation"
  seed=123,                                                                     # random seed for shuffling
  image_size=(img_height, img_width),                                           # size to resize image (default 256, 256)
  batch_size=batch_size)                                                        # size of batches of data (default 32)

# Generating training dataset from images in directory
train_ds = image_dataset_from_directory(
  data_dir_train,
  labels='inferred',                                                            # labels generated from directory structure
  validation_split=1/6,                                                         # fraction of data to reserve for validation
  subset='training',                                                            # one of "training" or "validation"
  seed=123,                                                                     # random seed for shuffling
  image_size=(img_height, img_width),                                           # size to resize image (default 256, 256)
  batch_size=batch_size)                                                        # size of batches of data (default 32)

test_ds = image_dataset_from_directory(
  data_dir_test,
  labels='inferred',                                                            # labels generated from directory structure
  image_size=(img_height, img_width),                                           # size to resize image (default 256, 256)
  batch_size=batch_size)                                                        # size of batches of data (default 32)

# Assessing number of classes and their labels [folder titles]
class_names = train_ds.class_names
no_classes = len(class_names)
print('The dataset has {} classes'.format(no_classes))


''' IMPROVING PERFORMANCE '''

# Pre-fetch: load next picture while training
# Cache: prevent reopening same picture in the next epoch
train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)


''' BUILDING CNN MODEL ARCHITECTURE '''

print('Building CNN architecture...')
# Use Sequential API [One input - One output]
model = Sequential([
  Rescaling(1./255, input_shape=(img_height, img_width, 3)),                    # Rescaling: [pixel values between 0 and 1]
  Conv2D(16, (3,3), padding='same', activation='relu'),                         # Creates a convolution kernel
  MaxPooling2D(),                                                               # Downsamples the input along its spatial dimensions [2,2]
  Conv2D(32, (3,3), padding='same', activation='relu'),
  MaxPooling2D(),
  Conv2D(64, (3,3), padding='same', activation='relu'),
  MaxPooling2D(),
  Flatten(),
  Dense(128, activation='relu'),
  Dense(no_classes)
])

# Configure model for training
# Computes the crossentropy loss between the labels and predictions.
model.compile(optimizer='adam',
              loss=SparseCategoricalCrossentropy(from_logits=True),             # Softmax has not been applied to output
              metrics=['accuracy'])


''' TRAINING THE MODEL '''

print('Training the Model...')
history = model.fit(train_ds, validation_data=val_ds, epochs=epochs)

# Final Accuracy
acc = history.history['accuracy'][-1]
val_acc = history.history['val_accuracy'][-1]

# Final Loss
loss = history.history['loss'][-1]
val_loss = history.history['val_loss'][-1]


''' EVALUATING MODEL ON TEST DATA '''

print("Evaluate on test data...")
results = model.evaluate(test_ds)


''' PRINTING RESULTS'''
# Printing results
print('Results: Train Accuracy: {} - Train Loss: {} '.format(acc,loss))
print('Results: Valid Accuracy: {} - Valid Loss: {} '.format(val_acc,val_loss))
print('Results: Test Accuracy: {} - Test Loss: {} '.format(results[1],results[0]))


'''SAVING MODEL'''

model.save('trained_model')
print('Model Saved!')
print('To test this model on new data, go to the google-cloud-files folder.')