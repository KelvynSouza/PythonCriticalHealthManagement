import pandas as pd
import os
from keras.models import Sequential  # Modelo Sequencial
from keras.layers import Dense, Dropout  # Fully Connected

dataset = pd.read_csv(os.path.join(os.getcwd(), '..', 'dataset.csv'))
previsores = dataset.iloc[:, 0:2]
classes = dataset.iloc[:, 2]

ESTRUTURA_JSON_FILE_PATH = os.path.join(os.getcwd(), '..', 'classificador.json')
WEIGHTS_FILE_PATH = os.path.join(os.getcwd(), '..', 'weights.h5')


def criar_rede() -> Sequential:
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


if __name__ == '__main__':
    rede = criar_rede()
    rede.fit(previsores, classes, batch_size=15, epochs=10000)
    estrutura_json = rede.to_json()
    with open(ESTRUTURA_JSON_FILE_PATH, 'w') as arquivo_json:
        arquivo_json.write(estrutura_json)
        arquivo_json.close()

    rede.save_weights(WEIGHTS_FILE_PATH)


