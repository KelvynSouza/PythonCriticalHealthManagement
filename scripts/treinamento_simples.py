import pandas as pd
import os
from sklearn.model_selection import train_test_split
from keras.models import Sequential #Modelo Sequencial
from keras.layers import Dense #Fully Connected
from sklearn.metrics import confusion_matrix, accuracy_score

dataset = pd.read_csv(os.path.join(os.getcwd(), '..', 'dataset.csv'))
previsores = dataset.iloc[:, 0:2]
classes = dataset.iloc[:, 2]

previsores_treinamento, previsores_teste, classes_treinamento, classes_teste \
    = train_test_split(previsores, classes, test_size=0.25)

classificador = Sequential()
# (2 entradas + 1 saida) / 2 = 1.5 (Arredonda pra cima) = 2
classificador.add(Dense(units=2,
                        activation='relu',
                        kernel_initializer='random_uniform',
                        input_dim=2))
classificador.add(Dense(units=2,
                        activation='relu',
                        kernel_initializer='random_uniform'))
classificador.add(Dense(units=1, activation='sigmoid'))
classificador.compile(optimizer='adam',
                      loss='binary_crossentropy',
                      metrics=['binary_accuracy'])

classificador.fit(previsores_treinamento, classes_treinamento,
                  batch_size=10, epochs=20000)

previsoes = classificador.predict(previsores_teste)
previsoes = (previsoes > 0.5)

precisao = accuracy_score(classes_teste, previsoes)
print(f'A precisão é de {precisao}')

