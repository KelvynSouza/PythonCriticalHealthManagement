from flask_restx import fields
import numpy as np
from entities.model import Model


class CriticalPredictModel(Model):
    def __init__(self, name, predict_status):
        self.name = name
        self.prediction_result = predict_status

    @classmethod
    def build_definition(cls, ns_critical):
        return ns_critical.model('PredictionResult', {
            'name': fields.String(description='Status crítico previsto'),
            'prediction_result': fields.Integer(description='Status crítico previsto')
        })


class CriticalPayload(Model):
    def __init__(self, name, temperature, heart_beats_rate):
        self.__name = name
        self.__temperature = float(temperature)
        self.__heart_beats_rate = float(heart_beats_rate)

    def get_name(self):
        return self.__name

    def get_payload(self):
        return np.array([[self.__temperature, self.__heart_beats_rate]])

    @classmethod
    def build_definition(cls, ns_classifier):
        return ns_classifier.model('PredictionPayload', {
            'name': fields.String(description='Nome do Paciente'),
            'temperature': fields.Float(description='Temperatura Corporal'),
            'heart_beats_rate': fields.Float(description='Batimento Cardíaco'),
        })
