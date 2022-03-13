from connector import Connector
from itertools import groupby
from operator import itemgetter


class Employee(Connector):

    def find_ees(self):
        """
            Нахождение всех сотрудников из офиса заданного сотрудника
        :return:
        """

        while True:
            ee_id = 0
            print("Введите идентификатор сотрудника:")
            try:
                ee_id = int(input())
            except ValueError:
                print("Проверьте правильность введённых данных, идентификатор сотрудника - число.")

            if ee_id and ee_id > 0:
                query = f'''SELECT * FROM \"{self.schema}\".{self.table} WHERE id = {ee_id}'''
                self.cur = self.conn.cursor()
                self.cur.execute(query)
                ee_info = self.cur.fetchall()
                if not ee_info:
                    print('Сотрудник не найден')
                elif not ee_info[0][1] or ee_info[0][3] == 2:
                    print('Введенные данные - не идентификатор сотрудника')
                else:
                    query = f'''
                                WITH RECURSIVE tree(id, parent) AS (
                                    SELECT *
                                    FROM \"{self.schema}\".{self.table} WHERE id = {ee_id}
                                    UNION
                                        SELECT \"{self.schema}\".{self.table}.*
                                        FROM tree t, \"{self.schema}\".{self.table}
                                        WHERE \"{self.schema}\".{self.table}.id = t.parent
                                            or \"{self.schema}\".{self.table}.parent = t.id
                                )
                                SELECT * FROM tree ORDER BY name;
                            '''
                    self.cur = self.conn.cursor()
                    self.cur.execute(query)
                    ees = self.cur.fetchall()
                    ees.sort(key=itemgetter(3))
                    info = {"office" if r_type == 1 else "ees": [value for value in values] for r_type, values in
                            groupby(ees, key=itemgetter(3)) if r_type != 2}

                    print(info["office"][0][2])
                    print("Сотрудники: " + ", ".join([ee[2] for ee in info['ees']]))
            else:
                print("Задан неверный идентификатор")


if __name__ == '__main__':
    with Employee() as ee:
        ee.find_ees()
