import pandas as pd
import os
from keras.models import Sequential  # Modelo Sequencial
from keras.layers import Dense, Dropout  # Fully Connected
from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.model_selection import GridSearchCV

dataset = pd.read_csv(os.path.join(os.getcwd(), '..', 'dataset.csv'))
previsores = dataset.iloc[:, 0:2]
classes = dataset.iloc[:, 2]

def criar_rede(optimizer, loss, kernel_initializer, activation, neurons):
    classificador = Sequential()
    classificador.add(Dense(units=neurons,
                            activation=activation,
                            kernel_initializer=kernel_initializer,
                            input_dim=2))
    classificador.add(Dense(units=1, activation='sigmoid'))
    classificador.compile(optimizer=optimizer,
                          loss=loss,
                          metrics=['binary_accuracy'])
    return classificador


classficiador = KerasClassifier(build_fn=criar_rede)
parametros = {
    'batch_size': [5, 10],
    'epochs': [1000, 2000],
    'optimizer': ['adam', 'sgd'],
    'loss': ['binary_crossentropy', 'hinge'],
    'kernel_initializer': ['random_uniform', 'normal'],
    'activation': ['relu', 'tahn'],
    'neurons': [2, 4]
}

grid_search = GridSearchCV(estimator=classficiador,
                           param_grid=parametros,
                           scoring='accuracy',
                           cv=5)

grid_search = grid_search.fit(previsores, classes)
melhores_parametros = grid_search.best_params_
melhor_precisao = grid_search.best_score_


print(f'melhores_parametros {melhores_parametros}')
print(f'melhor_precisao {melhor_precisao}')