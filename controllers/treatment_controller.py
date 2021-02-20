from flask_restx import Namespace, Resource
from usecases.classifier_service import ClassifierService
from usecases.line_service import LineService

from entities.treatment_model import AttendedPatientModel, LineToAttendModel

print('\033[1;36m*' * 70)
print('*', '\t' * 4, 'Starting Treatment Controller', '\t' * 4, '*')
print('\033[1;36m*\033[m' * 70)
classifier_service = ClassifierService()

ns_treatment = Namespace('treatment')


@ns_treatment.route('/attend')
class Attend(Resource):

    @ns_treatment.doc('treatment')
    @ns_treatment.marshal_with(AttendedPatientModel.build_definition(ns_treatment))
    def get(self):
        line_service = LineService()
        result = line_service.attend()
        return result


@ns_treatment.route('/line')
class GetLine(Resource):

    @ns_treatment.doc('treatment')
    def get(self):
        line_service = LineService()
        result = line_service.get_full_line()
        return result

    @ns_treatment.doc('treatment')
    def delete(self):
        line_service = LineService()
        line_service.delete_full_line()