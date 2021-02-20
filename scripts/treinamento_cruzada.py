import pandas as pd
import os
from keras.models import Sequential  # Modelo Sequencial
from keras.layers import Dense, Dropout  # Fully Connected
from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.model_selection import cross_val_score

dataset = pd.read_csv(os.path.join(os.getcwd(), '..', 'dataset.csv'))
previsores = dataset.iloc[:, 0:2]
classes = dataset.iloc[:, 2]
print(previsores)
print(classes)

def criar_rede():
    classificador = Sequential()
    classificador.add(Dense(units=6,
                            activation='relu',
                            kernel_initializer='normal',
                            input_dim=2))
    classificador.add(Dense(units=1, activation='sigmoid'))
    classificador.compile(optimizer='adam',
                          loss='binary_crossentropy',
                          metrics=['binary_accuracy'])
    return classificador


classificador = KerasClassifier(build_fn=criar_rede, epochs=10000, batch_size=15)
resultados = cross_val_score(estimator=classificador,
                             X=previsores,
                             y=classes,
                             cv=10,
                             scoring='accuracy')

media = resultados.mean()
desvio = resultados.std()

print(f'Media {media}')
print(f'Desvio {desvio}')
