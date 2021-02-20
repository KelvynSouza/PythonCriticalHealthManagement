# REST-RISK-CLASSIFIER

### Resum
MCC-REST is an Flask-Restx based API with an Artificial Neural Network for predict critical health state based on 
beat heart and temperature.

### Project structure
```
project/
├── app.py
├── dataset.csv
├── classificador.json
├── weigths.h5
├── requiriments.txt
└── controllers
    ├── critical_controller.py
└── models
	├── critical_model.py
	├── model.py
└── service
	├── classifier_service.py.py
```

### Instructions
On root path

 1. **Install dependencies**
```
	pip install -r requiriments.txt
```
 2. **Execute application**
```
	python app.py
```
The application will expose a swagger based documentation on root path.
