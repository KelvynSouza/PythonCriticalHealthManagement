from tensorflow.python.keras.models import Sequential, model_from_json
from entities.critical_model import CriticalPredictModel, CriticalPayload
from pathlib import Path


class ClassifierService:

    def __init__(self):
        self.ESTRUTURA_JSON_FILE_PATH = Path(__file__).parent.parent.joinpath('classificador.json')
        self.WEIGHTS_FILE_PATH = Path(__file__).parent.parent.joinpath('weights.h5')
        print(self.ESTRUTURA_JSON_FILE_PATH)
        self.__try_to_load_model()

    def predict(self, predict_payload: CriticalPayload):
        prediction = self.__classifier.predict(predict_payload.get_payload())
        prediction = (prediction > 0.5)
        prediction = prediction[0]

        critical_result = CriticalPredictModel(predict_payload.get_name(), prediction)
        return critical_result.to_json()

    def __load_model(self) -> Sequential:
        print('\033[1;36m*' * 50)
        print('*', '\t' * 4, 'Loading the Model', '\t' * 4, '*')
        print('\033[1;36m*\033[m' * 50)

        arquivo_json = open(self.ESTRUTURA_JSON_FILE_PATH, 'r')
        estrutura = arquivo_json.read()
        arquivo_json.close()

        classificador = model_from_json(estrutura)
        classificador.load_weights(self.WEIGHTS_FILE_PATH)

        return classificador

    def __try_to_load_model(self):
        try:
            self.__classifier = self.__load_model()
        except FileNotFoundError:
            raise Exception('Os arquivos da rede neural não foram encontrados!')