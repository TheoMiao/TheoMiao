import mysql.connector
from mysql.connector import errorcode



import csv
from csv import reader


def get_data(file):
    """
    get data from csv
    """
    # ='Grade.csv' Name,Number,Subject,Grade
    # 1. change the list into dict
    # with语句来自动帮我们调用close()
    with open(file, 'r', encoding='utf-8') as csv_file:  # delimiter = {str} ','
        csv_reader = reader(csv_file)
        data_csv= list(csv_reader)
    return data_csv


class Person:
    # person_id = 0 --> person_id = max(person_id)+1
    classroom = 'IFKA'

    # num = 0

    def __init__(self, name, subject):  # per = Person(name, subject) -> call __init__
        self.name = name
        self.subject = subject

        # Person.person_id = self.person_id + 1
        # self.person_id = Person.person_id

    def tell_me_subject(self):
        return self.subject
    @property # what is it
    def num(self):
        pass

    @staticmethod
    # 静态方法无需实力化，装饰器
    # 将该被装饰的函数与该类没有关系，该函数不能用self传参，需要和普通函数一样传参
   # cls?
    def count():
        # what is decoration?
        print('the total amount of people is {}'.format(Person.person_id))


class Student(Person):
    # student_id = 0

    def __init__(self, name, number, subject, score, person_id):
        super().__init__(name, subject, person_id)
        self.student_number = number
        self.score = {subject: score}


class Teacher(Person):
    # teacher_id = 0

    def __init__(self, name, subject, person_id):
        super().__init__(name, subject, person_id)

    def tell_me_subject(self):
        return '{} responsible for {}'.format(self.name, self.subject)


# def test2(input):
#     input = input +2
#     return input
class My_DB_Connector:
    """

    """
    db_config = {}
    mydb = None

    def connect(self):


        pass

    def close(self):
        if self.mydb is not None:
            self.mydb.commit()
            self.mydb.close()

    def query_db_fun(self, name_list):
        """

        :param name_list:
        :return:
        """
        self.connect()

        output = []
        self.close()
        return output


class HR(list):
    _type = {'teacher': Teacher,
             'student': Student}
    db = My_DB_Connector()

    def load_db(self):
        # students = self.db.query_db_fun('tea_id', 'tea')
        # self.append(Student('a', '2', '2', 3, 4))
        # self.append(Teacher('a', '2', '2', ))
        pass

    def load_manual(self, input):
        pass


    @property
    def students(self):
        return [x for x in self if type(x) is Student]

    @property
    def teachers(self):
        return [x for x in self if type(x) is Teacher]

    @property
    def max_id(self):
        if len(self) == 0:
            self.load_db()
        _max_id = max([x.id for x in self.students])
        return _max_id


class System:

    # def __init__(self):
    #     self.data = {}
    #     self.data_list = []


    data_list = []

    _dbconfig = {
        'host': "localhost",
        'user': "ifka",
        'passwd': "123456",
        'database': "student"
    }

    data = HR()

    def __init__(self):
        Person.person_id = self.data.max_id + 1


    # def test1(self, input):
    #     """
    #
    #     :param input: here we input ....
    #     :return: a number
    #     """
    #
    #     self.data_list.append(11)
    #
    # def runcode(self):
    #     self.test1(10)
    #     input = test2(10)
    #     self.data_list.append(input)

    def read_db_stu(self, input_type='student'):
        # import mysql.connector
        # from mysql.connector import errorcode

        # dbconfig = {
        #     'host': "localhost",
        #     'user': "ifka",
        #     'passwd': "123456",
        #     'database': "student"
        # }

        try:
            mydb = mysql.connector.connect(**self._dbconfig)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        else:
            print("Database student_stu load ok")
            db_cursor = mydb.cursor()
            name = "stu_name"
            number = "stu_number"
            subject = "stu_subject"
            score = "stu_score"
            db_cursor.execute(f"SELECT DISTINCT {name}, {number}, {subject}, {score} FROM stu")
            stu_row = db_cursor.fetchall()
            key = ['name', 'number', 'subject', 'score']
            person_data = []
            for item in range(1, len(stu_row)):
                person_data.append(dict(zip(key, stu_row[item])))
            self.append_data(person_data, input_type)

            mydb.close()


        # from db to classes


    def read_db_tea(self, input_type='teacher'):
        tea_row = self.query_db_fun(['tea_id','tea_name','tea_subject'],'tea')
        print(tea_row)

        # try:
        #     mydb = mysql.connector.connect(**self._dbconfig)
        # except mysql.connector.Error as err:
        #     if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        #         print("Something is wrong with your user name or password")
        #     elif err.errno == errorcode.ER_BAD_DB_ERROR:
        #         print("Database does not exist")
        #     else:
        #         print(err)
        # else:
        #     print("Database student_tea load ok")
        #     db_cursor = mydb.cursor()
        #     person_id = "tea_id"
        #     name = "tea_name"
        #     subject = "tea_subject"
        #     # for result in db_cursor.execute(f"SELECT DISTINCT, {person_id}, {name}, {subject} FROM tea", multi=True):
        #     #
        #     #     if result.with_rows:
        #     #         print('result:', result.fetchall())
        #     #     else:
        #     #         print('cursor:', result)
        #     db_cursor.execute(f"SELECT  {person_id}, {name}, {subject} FROM tea")
        #     tea_row = db_cursor.fetchall()
        #     print(tea_row)
        # #     key = ['person_id', 'name', 'subject']
        #     person_data = []
        #
        #     for item in range(0, len(tea_row)):
        #         person_data.append(dict(zip(key, tea_row[item])))
        #     self.append_data(person_data, input_type)
        #
        #
        #     mydb.close()


        # from db to classes

    def connect_db(self):
        try:
            mydb = mysql.connector.connect(**self._dbconfig)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
            return None
        else:
            print("Database load ok")

            return mydb
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

    def export_db_tea(self, data: list):## add manual input
        """
        this is to export list of teachers to database
        self.data is mandatry!
        :param: data is a list of teachers
        :return: True is epx successfully
        """

        mydb = self.connect_db()

        if mydb is None:
            print('there is no database')
        else:


            db_cursor = mydb.cursor()
            sql = "DELETE FROM tea2"

            try:
                # Execute the SQL command
                db_cursor.execute(sql)

                # Commit your changes in the database
                mydb.commit()
            except:
                # Roll back in case there is any error
                mydb.rollback()

            # With the executemany() method, it is not possible to specify multiple statements to execute in the operation argument.
            # Doing so raises an InternalError exception.
            # Consider using execute() with multi=True instead.
            # for result in db_cursor.executemany(stmt, mydata_modified, multi=True):
            #     print('cursor:', result)
            #     if result.with_rows:
            #         print('result:', result.fetchall())

            mydata_modified = []
            for item in self.data['teacher']:
                mydata_modified.append((item.name, item.subject))
            print(mydata_modified)

            stmt = "INSERT INTO tea2(tea_name, tea_subject) VALUES (%s, %s)"

            db_cursor.executemany(stmt, mydata_modified)

            mydb.commit()
            mydb.close()
        # def read_db_tea2(self, input_type='teacher'):
        #     try:
        #         mydb = mysql.connector.connect(**self._dbconfig)
        #     except mysql.connector.Error as err:
        #         if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        #             print("Something is wrong with your user name or password")
        #         elif err.errno == errorcode.ER_BAD_DB_ERROR:
        #             print("Database does not exist")
        #         else:
        #             print(err)
        #     else:
        #         print("Database student_tea load ok")
        #         db_cursor = mydb.cursor()
        #         name = "tea_name"
        #         subject = "tea_subject"
        #         db_cursor.execute(f"SELECT DISTINCT {name}, {subject} FROM tea2")
        #         tea_row = db_cursor.fetchall()
        #         key = ['name', 'subject']
        #         person_data = []
        #         for item in range(1, len(tea_row)):
        #             person_data.append(dict(zip(key, tea_row[item])))
        #         print(person_data)

    def query_in_db(self, query):
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
            print("Database load ok")
            db_cursor = mydb.cursor()
            db_cursor.execute(query)
            person_id_max = db_cursor.fetchall()
            print(person_id_max)
            print(type(person_id_max))
            mydb.close()
            return person_id_max

    def query_db_fun(self, name_list: list, table: str, where=None):
        query = f"SELECT {','.join(name_list)} FROM {table} "
        if where is not None:
            query = query + where
        result = self.query_in_db(query)
        output = []
        if result is False or len(result) == 0:
            return output
        for res in result:
            output.append({x: y for x, y in zip(name_list, res)})
        return output

    def show_max_person_id_tea(self):
        max_id = self.query_db_fun(['MAX(tea_id)'], 'tea')
        print(max_id)
            #Persion.person_id ...


    def show_min_score_stu(self):
        try:
            mydb = mysql.connector.connect(**self._dbconfig)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        else:
            print("Database load ok")
            db_cursor = mydb.cursor()
            name = "stu_name"
            number = "stu_number"
            subject = "stu_subject"
            score = "stu_score"
            db_cursor.execute(f"SELECT stu_name, stu_subject, stu_score FROM stu WHERE(stu_score, stu_name) in ( "
                              f"SELECT MIN(stu_score) AS min_s, stu_name FROM stu GROUP BY stu_name);")
            all_row = db_cursor.fetchall()
            for item in all_row:
                print(item)
            mydb.close()


    def show_avg_score_tea(self):
        try:
            mydb = mysql.connector.connect(**self._dbconfig)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        else:
            print("Database load ok")
            db_cursor = mydb.cursor()
            db_cursor.execute(f"SELECT tea_name,tea_subject, AVG(stu_score) AS score_avg "
                              f"FROM tea LEFT JOIN stu ON tea.tea_subject = stu.stu_subject "
                              f"GROUP BY tea_name,tea_subject "
                              f"ORDER BY score_avg DESC;")
            all_row = db_cursor.fetchall()
            for item in all_row:
                print(item)
            mydb.close()


    def append_data(self, person_data, input_type):


        # 无所谓老师/学生， 同一输入
        # input： 1。信息（数据形式同一， dict or list）
        #        2。type
        # function：　1. find the person if exists in the list 2. student(**data) or teacher(**data)
        # return self.data.append(person)

        if input_type not in self.data:  # 'a' in {'a':2}->true or 'a' in {}->false
            self.data[input_type] = []  # -> {'a': []}

        for item in person_data:
            person_id = item["person_id"]
            person_name = item["name"]
            person_subject = item["subject"]
            new_obj_needed = True
            if input_type == 'student':
                person_score = item["score"]
                # new_obj_needed = True
                for p in self.data[input_type]:
                    if person_name == p.name:
                        p.score[person_subject] = person_score
                        new_obj_needed = False
                        break
            if new_obj_needed:
                # student is a new instance in each loop
                person = self._type[input_type](**item)  # self._type[input_type] -> Teacher(**item) *item
                #person.person_id
                self.data[input_type].append(person)

            # 模块对象有一个秘密的只读属性 __dict__，它返回用于实现模块命名空间的字典；
            # __dict__ 是属性但不是全局名称。 显然，使用这个将违反命名空间实现的抽象，应当仅被用于事后调试器之类的场合。
            # if 'data_list' not in self.__dict__:
            #     self.data_list = []
            self.data_list.append(person)

    def load_csv(self, file, input_type):
        # input file, input_type
        # function: read file -> a list of data and input_type
        # self.append_data(...)
        # input_type = input('please input type:')
        csv_data = get_data(file)
        key = csv_data[0]
        person_data = []
        for item in range(1, len(csv_data)):
            person_data.append(dict(zip(key, csv_data[item])))
        self.append_data(person_data, input_type)

    def manual_input(self, input_type):
        # if input_type not in self.data:
        #     self.data[input_type] = []
        person_data = []

        if input_type == 'teacher':
            name = input('please input your name: ')
            subject = input('please input your subject: ')
            teacher = {'name': name, 'subject': subject}
            person_data.append(teacher)

        if input_type == 'student': # input move out of class
            name = input('please input your name: ')
            student_number = input('please input your student number: ')
            subject = input('please input your subject: ')
            score = input('please input your score: ')
            student = {'name': name, 'number': student_number, 'subject': subject, 'score': score}
            person_data.append(student)

            self.append_data(person_data, input_type)

    def show_all_teachers(self):
        for teacher in self.data.teachers:
            print(teacher.name, teacher.subject)

    def show_all_students(self):
        for student in self.data.students:
            print(student.name, student.person_id)

    def find_student_score(self):
        find_stu = True
        while find_stu:
            name = input('please input the name that you want to search for his/her score:')
            flag = False
            for student in self.data['student']:
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


if __name__ == '__main__':

    IFKA_list = System()
    # IFKA_list.read_db_stu()
    IFKA_list.run()

    # IFKA_list.show_avg_score_tea()
    # IFKA_list.show_min_score_stu()
    # IFKA_list.load_csv('student')
    # IFKA_list.load_csv('tea.csv', 'teacher')

    # op = input('add teacher y/n: ')
    # while op == 'y':
    #     IFKA_list.manual_input('teacher')
    #     op = input('add teacher y/n: ')
    #
    # op = input('add student y/n: ')
    # while op == 'y':
    #     IFKA_list.manual_input('student')
    #     op = input('add student y/n: ')
    #
    # Person.count()
    # IFKA_list.find_student_score()
    # # find = True
    # if find:
    #     name = input('please input the name that you want to search for his/her score:')
    #     IFKA_list.find_student_score(name)
    #     op = input('do you want to search the other person y/n: ')
    #     if op == 'n':
    #         find = False

    # IFKA_list.show_all_teachers()
    # IFKA_list.show_all_students()


