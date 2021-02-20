from flask_restx import Namespace, Resource
from usecases.classifier_service import ClassifierService
from usecases.line_service import LineService

from entities.critical_model import CriticalPayload, CriticalPredictModel

print('\033[1;36m*' * 70)
print('*', '\t' * 4, 'Starting Classifier Controller', '\t' * 4, '*')
print('\033[1;36m*\033[m' * 70)
classifier_service = ClassifierService()

ns_critical = Namespace('critical')


@ns_critical.route('/classifier')
class Classifier(Resource):

    @ns_critical.doc('Classifier')
    @ns_critical.expect(CriticalPayload.build_definition(ns_critical))
    @ns_critical.marshal_with(CriticalPredictModel.build_definition(ns_critical))
    def post(self):
        payload = CriticalPayload(**self.api.payload)
        result = classifier_service.predict(payload)
        line_service = LineService()
        line_service.lineup_patient(result)
        return result


