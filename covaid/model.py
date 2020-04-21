#Dependencies
import numpy as np
import pandas as pd

#dataset import
dataset = pd.read_csv("covaid_train_scaled.csv")
X = dataset.iloc[:,:3].values
y = dataset.iloc[:,3:4].values
X = np.array(X)
y = np.array(y)
#Normalizing the data
#from sklearn.preprocessing import StandardScaler
#sc = StandardScaler()
#X = sc.fit_transform(X)
from sklearn.preprocessing import OneHotEncoder
ohe = OneHotEncoder()
y = ohe.fit_transform(y).toarray()
from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size = 0.2)
import keras
from keras.models import Sequential
from keras.layers import Dense
# Neural network
model = Sequential()
model.add(Dense(64, input_dim=3, activation="relu"))
model.add(Dense(32, activation="relu"))
model.add(Dense(16, activation="relu"))
model.add(Dense(5, activation="softmax"))
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
history = model.fit(X_train, y_train, epochs=150, batch_size=4)
y_pred = model.predict(X_test)
model.save('my_model.hdf5')

#Converting predictions to label
pred = list()
for i in range(len(y_pred)):
    pred.append(np.argmax(y_pred[i]))
#Converting one hot encoded test label to label
test = list()
for i in range(len(y_test)):
    test.append(np.argmax(y_test[i]))
from sklearn.metrics import accuracy_score
a = accuracy_score(pred,test)
print(pred)
print('Accuracy is:', a*100)
#history = model.fit(X_train, y_train,validation_data = (X_test,y_test), epochs=100, batch_size=64)