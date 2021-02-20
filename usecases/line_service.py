from data.line_repository import LineRepository
from entities.treatment_model import AttendedPatientModel, LineToAttendModel

from enum import IntEnum


class Situation(IntEnum):
    worse = 0
    better = 1


class LineService:
    def __init__(self):
        self.better_line = []
        self.worse_line = []
        self.attended = 0
        self.__attend_worse_line_limit = 5
        self.db = LineRepository()
        self.__init_lists()
        self.__init_attended_number()

    def __init_lists(self):
        line = self.db.get_line()
        if len(line) != 0:
            self.better_line = [x[1] for x in line if x[2] == Situation.better]
            self.worse_line = [x[1] for x in line if x[2] == Situation.worse]

    def __init_attended_number(self):
        self.attended = self.db.get_patients_attended()[0]

    def attend(self):
        patient_attend = ''
        exist_patient_better = len(self.better_line) != 0
        exist_patient_worse = len(self.worse_line) != 0
        exist_patient = exist_patient_better or exist_patient_worse
        limit_worse_not_attended = self.attended < self.__attend_worse_line_limit

        if exist_patient:
            if exist_patient_worse and (limit_worse_not_attended or not exist_patient_better):
                patient_attend = self.worse_line[0]
                self.worse_line.pop(0)
            elif exist_patient_better:
                patient_attend = self.better_line[0]
                self.better_line.pop(0)

            if limit_worse_not_attended:
                self.attended += 1
            else:
                self.attended = 0

        self.__update_database()
        return AttendedPatientModel(patient_attend).to_json()

    def lineup_patient(self, patient):
        self.__update_line(patient)
        self.__update_database()

    def __update_line(self, patient):
        exist = self.__verify_existence_in_line(patient)
        if exist:
            self.__update_patient_in_line(self.__verify_better_line, self.__verify_worse_name, patient)
        else:
            self.__put_patient_in_line(patient)

    def __verify_existence_in_line(self, patient):
        self.__verify_better_line = any(x == patient['name'] for x in self.better_line)
        self.__verify_worse_name = any(x == patient['name'] for x in self.worse_line)
        return self.__verify_better_line or self.__verify_worse_name

    def __update_patient_in_line(self, better_line_verification, worse_line_verification, patient):
        if better_line_verification:
            if patient['prediction_result'] == Situation.worse:
                self.better_line.remove(patient['name'])
                self.worse_line.append(patient['name'])
        elif worse_line_verification:
            if patient['prediction_result'] == Situation.better:
                self.worse_line.remove(patient['name'])
                self.better_line.insert(0, patient['name'])

    def __put_patient_in_line(self, patient):
        if patient['prediction_result'] == Situation.better:
            self.better_line.append(patient['name'])
        else:
            self.worse_line.append(patient['name'])

    def __update_database(self):
        self.db.delete_all_patients()
        for patient in self.worse_line:
            self.db.add_patient(patient, 0)
        for patient in self.better_line:
            self.db.add_patient(patient, 1)
        self.db.update_patients_attended(self.attended)

    def get_full_line(self):
        return LineToAttendModel(self.worse_line + self.better_line).to_json()

    def delete_full_line(self):
        self.db.delete_all_patients()
        self.db.update_patients_attended(0)
