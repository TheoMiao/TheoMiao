import mysql.connector
from mysql.connector import errorcode

import csv
from csv import reader


class Person:
    person_id = 0
    classroom = 'IFKA'

    def __init__(self, name, subject):
        self.name = name
        self.subject = subject

    @staticmethod
    def count():
        print('the total amount of people is {}'.format(Person.person_id))


class Student(Person):
    def __init__(self, name, number, score, subject):
        super().__init__(name, subject)
        self.student_number = number
        self.score = {subject: score}


class Teacher(Person):
    def __init__(self, name, subject):
        super().__init__(name, subject)

class My_DB_Connector:
    """
    pack the toll of mysql_connector
    """
    _dbconfig = {
        'host': "localhost",
        'user': "ifka",
        'passwd': "123456",
        'database': "student"
    }

    def connect(self):
        """

        :return: db_cursor
        """
        try:
            mydb = mysql.connector.connect(**self._dbconfig)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
            return False
        else:
            print("Database load successfully")
            db_cursor = mydb.cursor()
            return db_cursor

    def close(self):
        if self.mydb is not None:
            self.mydb.commit()
            self.mydb.close()

    def query_db_fun(self, name_list, table, where = None):
        """

        :param name_list:
        :return:
        """
        db_cursor = self.connect()
        db_cursor.execute(f"SELECT DISTINCT {name}, {number}, {subject}, {score} FROM stu")
        stu_row = db_cursor.fetchall()

        output = []
        self.close()
        return output

class HR(list):
    _type = {'teacher': Teacher,
             'student': Student}

    def load_csv(self, file, input_type):
        """
        this is to import file of csv as a list of dictionary

        :param: input_type, [str] 'student' or 'teacher'
        :param: file, the first line contents key information
        :return: list of each person_data(dict) from csv
        """

        with open(file, 'r', encoding='utf-8') as csv_file:
            csv_reader = reader(csv_file)
            csv_data = list(csv_reader)
            key = csv_data[0]
            person_data = []
            for item in range(1, len(csv_data)):
                person_data.append(dict(zip(key, csv_data[item])))
            self.append_data(person_data, input_type)

        def check_duplicate_name(self, person_data):
            """
            check if name already exit,
            assume there is no person has the same name
            :return: no append_data
                     yes update subject
            """
        pass

        def update_data(self):
            """
            wenn there is duplicate name,
            update subject, score
            :return:
            """
        pass

    def load_db(self):
        pass

    def load_manual(self,input):
        pass

    def append_data(self, person_data, input_type):
        """
        this data could be teachers and students from
        load_scv, load_db, load_manual
        :param person_data: read data from load_scv, load_db, load_manual
        :param input_type: students/teacher
        :return: list of person
        """
        # if input_type not in self:
        #     self._type[input_type] = []

        # for item in person_data:
        #     person_name = item["name"]
        #     person_subject = item["subject"]
        #     new_obj_needed = True
        #
        #     if input_type == 'student':
        #         person_score = item["score"]
        #         # new_obj_needed = True
        #         for p in self:
        #             if person_name == p.name:
        #                 p.score[person_subject] = person_score
        #                 new_obj_needed = False
        #                 break
        #     print(new_obj_needed)
        #     if new_obj_needed:
        #         # student is a new instance in each loop
        #         person = self._type[input_type](**item)
        #         print(person)
        #         # self._type[input_type] -> Teacher(**item) *item
        #         # person.person_id

        for item in person_data:
            new_obj_needed = True
            if input_type == 'student':
                for student in self:
                # for student in self_type[input_type]:
                    if item["name"] == student.name:
                        student.score[item['subject']] = item['score']
                        new_obj_needed = False
                        break
            if new_obj_needed:
                person = self._type[input_type](**item)

                self.append(person)

    @property
    def student(self):
        return [x for x in self if type(x) is Student]

    @property
    def teacher(self):
        return [x for x in self if type(x) is Teacher]
