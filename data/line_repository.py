import sqlite3


class LineRepository:
    def __init__(self):
        self.conn = sqlite3.connect("line.db")
        self.__init_tables()
        self.__init_attended_number()

    def __init_tables(self):
        cursor = self.conn.cursor()
        self.conn.execute("""
        create table if not exists line_status (
            id_patient integer primary key autoincrement,
            name text UNIQUE,
            status integer
        )
        """)
        self.conn.execute("""
                create table if not exists line_queue (                    
                    name text UNIQUE,
                    seq integer
                )
                """)

    def __init_attended_number(self):
        self.conn.execute("insert or ignore into line_queue (name, seq) values('patient_attended', 0)")
        self.conn.commit()

    def add_patient(self, patient_name: str, patient_status: int):
        self.conn.execute("insert into line_status (name, status) values (?, ?)",
                          (patient_name, patient_status))
        self.conn.commit()

    def add_patients(self, patients):
        self.conn.execute("insert into line_status (name, status) values (?, ?)",
                          patients)
        self.conn.commit()

    def get_patient(self, patient_name: str):
        return self.conn.execute("select id_patient, name, status from line_status where name = ?", patient_name)

    def delete_patient(self, patient_name: str):
        self.conn.execute("delete from line_status where name = ?", patient_name)
        self.conn.commit()

    def update_status(self, patient_name: str, patient_status: int):
        self.conn.execute("update line_status set status = ? where name = ?",
                          (patient_status, patient_name))
        self.conn.commit()

    def get_line(self):
        return self.conn.execute("select id_patient, name, status from line_status").fetchall()

    def get_patients_attended(self):
        return self.conn.execute("select seq from line_queue where name = 'patient_attended'").fetchone()

    def update_patients_attended(self, number_attended: int):
        self.conn.execute("update line_queue set seq = ? where name = 'patient_attended'", (number_attended,))
        self.conn.commit()

    def delete_patients_attended(self):
        self.conn.execute("update line_queue set seq = 0 where name = 'patient_attended'")
        self.conn.commit()

    def delete_all_patients(self):
        self.conn.execute("update line_queue set seq = 0")
        self.conn.commit()
        self.conn.execute("delete from line_status")
        self.conn.commit()
