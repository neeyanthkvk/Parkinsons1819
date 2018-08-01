import keras
import numpy as np
import keras.backend as K
from sklearn.model_selection import train_test_split

# Data Loading
y = np.zeros((466+148, 2))
x = np.concatenate([np.load("/data2/3D/PD.npy"), np.load("/data2/3D/Control.npy")])
print("LOADED")
for i in range(466):
    y[i][0] = 1
for i in range(466, 466+148):
    y[i][1] = 1
print("MADE Y")
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, random_state=42)
x = 0
y = 0

# Model Creation
from keras.models import Sequential
from keras.layers import Conv3D, MaxPooling3D, GlobalMaxPooling3D, GlobalAveragePooling3D
from keras.layers import Conv2D, MaxPooling2D, GlobalMaxPooling2D, GlobalAveragePooling2D
from keras.layers import Flatten, Dropout, Dense, Reshape, BatchNormalization
from keras.layers.advanced_activations import LeakyReLU
from keras.optimizers import Adam
from keras.losses import binary_crossentropy

model = Sequential()
model.add(Conv3D(32, kernel_size=(3, 3, 3), input_shape=(176, 256, 240, 1), padding="same"))
model.add(LeakyReLU())
model.add(Conv3D(32, padding="same", kernel_size=(3, 3, 3)))
model.add(LeakyReLU())
model.add(MaxPooling3D(pool_size=(3, 3, 3), padding="same"))
model.add(Dropout(0.25))

model.add(Conv3D(64, padding="same", kernel_size=(3, 3, 3)))
model.add(LeakyReLU())
model.add(Conv3D(64, padding="same", kernel_size=(3, 3, 3)))
model.add(LeakyReLU())
model.add(MaxPooling3D(pool_size=(3, 3, 3), padding="same"))
model.add(Dropout(0.25))

model.add(Conv3D(64, padding="same", kernel_size=(3, 3, 3)))
model.add(LeakyReLU())
model.add(Conv3D(64, padding="same", kernel_size=(3, 3, 3)))
model.add(LeakyReLU())
model.add(MaxPooling3D(pool_size=(3, 3, 3), padding="same"))
model.add(Dropout(0.25))

model.add(Flatten())
model.add(Dense(512, activation='relu'))
model.add(BatchNormalization())
model.add(Dropout(0.5))
model.add(Dense(2, activation='softmax'))
model.compile(loss=binary_crossentropy, optimizer=Adam, metrics=['accuracy'])
model.summary()

# Model Testing
history = model.fit(x_train, y_train, validation_data = (x_test, y_test), batch_size=16, epochs = 25, verbose = 1, shuffle = True)
import pickle
pickle.dump(history, open("history.pkl", "wb"))
model.save_weights("7312018.h5")
