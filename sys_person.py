import mysql.connector
from mysql.connector import errorcode

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


class My_DB_Connector(object):
    """
    pack the toll of mysql_connector
    """

    _dbconfig = {
        'host': "localhost",
        'user': "ifka",
        'passwd': "123456",
        'database': "student"
    }

    mydb = None

    def connect(self):
        """

        :return: mydb
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
            print("Database connect successfully")
            return mydb

    def close(self):
        if self.mydb is not None:
            self.mydb.commit()
            self.mydb.close()

    def query_db_read(self, name_list, table, where=None):
        """
        :param where: where clause
        :param table: table in db
        :param name_list: query
        :return:
        """
        mydb = self.connect()
        if mydb is None:
            print("Database does not exist")
        else:
            db_cursor = mydb.cursor()
        query = f"SELECT {','.join(name_list)} FROM {table} "
        if where is not None:
            query = query + where
        db_cursor.execute(query)
        result = db_cursor.fetchall()
        output = []
        if result is False or len(result) == 0:
            return output
        for res in result:
            output.append({x: y for x, y in zip(name_list, res)})
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
        input_type = 'teacher'
        query = ['tea_name', 'tea_subject']
        # query = ['tea_id', 'tea_name', 'tea_subject']
        table = 'tea'
        where = None
        DB_Connector = My_DB_Connector()
        row = DB_Connector.query_db_read(query, table)
        print(row)
        key = ['name', 'subject']
        # key = ['person_id', 'name', 'subject']
        person_data = []
        for item in range(0, len(row)):
            person_data.append(dict(zip(key, row[item])))
        self.append_data(person_data, input_type)

    def load_manual(self, input_type):
        person_data = []

        if input_type == 'teacher':
            name = input('please input your name: ')
            subject = input('please input your subject: ')
            teacher = {'name': name, 'subject': subject}
            person_data.append(teacher)

        if input_type == 'student':  # input move out of class
            name = input('please input your name: ')
            student_number = input('please input your student number: ')
            subject = input('please input your subject: ')
            score = input('please input your score: ')
            student = {'name': name, 'number': student_number, 'subject': subject, 'score': score}
            person_data.append(student)

            self.append_data(person_data, input_type)

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


class System:
    data = HR()

    def __init__(self):
        Person.person_id = self.data.max_id + 1

    def run(self):
        """
        thread of the process
        :return:
        """
        # 1. db is loaded in to data (HR class)
        self.data.read_db()
        # 2. MANAL INPUT
        trrp = input("data")
        self.data.load_data(trrp)
        # 3. write backe to db
        success = self.export_db_tea(self.data)
        if success:
            print('save sucessfully')

    def show_max_person_id_tea(self):
        max_id = self.query_db_fun(['MAX(tea_id)'], 'tea')
        print(max_id)

    def show_all_teachers(self):
        for teacher in self.teachers:
            print(teacher.name, teacher.subject)

    def show_all_students(self):
        for student in self.student:
            print(student.name, student.person_id)

    def find_student_score(self):
        find_stu = True
        while find_stu:
            name = input('please input the name that you want to search for his/her score:')
            flag = False
            for student in self.student:
                if name == student.name:
                    flag = True
                    for subject in student.score:
                        print(subject, student.score[subject])
            if flag is False:
                print('there is no {} in classroom {}'.format(name, student.classroom))

            target_student = [x for x in self.data["student"] if x.name == name]  # check
            if len(target_student) == 0:
                print("no")
            else:
                for subject in target_student[0].score:
                    print(subject, target_student[0].score[subject])
            op = input('do you want to search the other person y/n: ')
            if op == 'n':
                find_stu = False
