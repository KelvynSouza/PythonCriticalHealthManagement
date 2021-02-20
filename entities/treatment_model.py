from flask_restx import fields, Model
import numpy as np
from entities.model import Model


class AttendedPatientModel(Model):
    def __init__(self, name):
        self.name = name

    @classmethod
    def build_definition(cls, ns_attended):
        return ns_attended.model('Attended', {
            'name': fields.String(description='Paciente a ser atendido.')
        })


class LineToAttendModel(Model):
    def __init__(self, line):
        self.line = line
