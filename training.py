import matplotlib.pyplot as plt
import numpy as np
import os
from pathlib import Path
import imghdr
import PIL
import tensorflow as tf
from tensorflow import keras
from keras import layers
from keras.models import Sequential
from keras import datasets, layers, models
from settings import *
import cv2

# (train_images, train_labels), (test_images, test_labels) = datasets.cifar10.load_data()

# data_dir = "C:\\Users\\User\\Desktop\\frogs\\data"
# image_extensions = [".png", ".jpg"]  # add there all your images file extensions
#
# img_type_accepted_by_tf = ["bmp", "gif", "jpeg", "png"]
# for filepath in Path(data_dir).rglob("*"):
#     if filepath.suffix.lower() in image_extensions:
#         img_type = imghdr.what(filepath)
#         if img_type is None:
#             print(f"{filepath} is not an image")
#             os.remove(filepath)
#         elif img_type not in img_type_accepted_by_tf:
#             print(f"{filepath} is a {img_type}, not accepted by TensorFlow")
#             os.remove(filepath)

batch_size = 64
data_root = ""
train_ds = tf.keras.utils.image_dataset_from_directory(
    str("C:\\Users\\User\\Desktop\\frogs\\data"),
    labels='inferred',
    validation_split=0.2,
    subset="training",
    color_mode="rgb",
    seed=123,
    image_size=(INPUT_SIZE[0], INPUT_SIZE[1]),
    batch_size=batch_size)

normalization_layer = layers.Rescaling(1./255)
train_ds = train_ds.map(lambda x, y: (normalization_layer(x), y))

validation_dataset = tf.keras.utils.image_dataset_from_directory(
    str("C:\\Users\\User\\Desktop\\frogs\\data"),
    labels='inferred',
    shuffle=True,
    validation_split=0.2,
    subset="validation",
    seed=123,
    image_size=(INPUT_SIZE[0], INPUT_SIZE[1]),
    batch_size=batch_size)

validation_dataset = validation_dataset.map(lambda x, y: (normalization_layer(x), y))
# image_batch, labels_batch = next(iter(normalized_ds))
# first_image = image_batch[0]


# for test in normalized_ds.as_numpy_iterator():
#     for i in range(test[1].size):
#         cv2.imshow(train_ds.class_names[test[1][i]],test[0][i])
#         cv2.waitKey(0)



# train_images, test_images = train_images / 255.0, test_images / 255.0
# class_names = ['airplane', 'automobile', 'bird', 'cat', 'deer',
#                'dog', 'frog', 'horse', 'ship', 'truck']


model = create_model()


# test_loss, test_acc = model.evaluate(test_images,  test_labels, verbose=2)


checkpoint_path = "training_1/cp.ckpt"
checkpoint_dir = os.path.dirname(checkpoint_path)
cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_path,
                                                 save_weights_only=True,
                                                 verbose=1)
history = model.fit(train_ds,
                    epochs=2,
                    validation_data=validation_dataset,
                    callbacks=[cp_callback])


# plt.plot(history.history['accuracy'], label='accuracy')
# plt.plot(history.history['val_accuracy'], label = 'val_accuracy')
# plt.xlabel('Epoch')
# plt.ylabel('Accuracy')
# plt.ylim([0.5, 1])
# plt.legend(loc='lower right')
# plt.waitforbuttonpress()
