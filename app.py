from flask import Flask
from flask_restx import Api
from controllers.critical_controller import ns_critical
from controllers.treatment_controller import ns_treatment

import os

app = Flask(__name__)
api = Api(app=app, version='1.0', title='MCC-REST', description='A critical corporal monitor on REST-API')

api.add_namespace(ns_critical)
api.add_namespace(ns_treatment)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 1256))
    print(f'App is running on {port}')
    app.run(host="0.0.0.0", port=port)
