import json
from pathlib import Path

from connector import Connector


class DB(Connector):
    def init_db(self):
        """
            Инициализация БД
        :return:
        """
        self._drop_schema()
        self._create_schema()
        self._import_records()

    def _drop_schema(self):
        """
            Сброс тестовой схемы
        :return:
        """
        self.cur.execute(f"DROP SCHEMA IF EXISTS \"{self.schema}\"  CASCADE;")
        print("Очищение тестовой базы прошло успешно")
        self.conn.commit()

    def _create_schema(self):
        """
            Создание тестовой схемы и таблицы
        :return:
        """
        self.cur = self.conn.cursor()
        self.cur.execute(f"CREATE SCHEMA \"{self.schema}\";")
        self.cur.execute(f'''CREATE TABLE \"{self.schema}\".{self.table}(
                                id INT PRIMARY KEY NOT NULL,
                                parent INT REFERENCES \"{self.schema}\".{self.table},
                                name VARCHAR NOT NULL,
                                type INT NOT NULL);
                                CREATE INDEX ON \"{self.schema}\".{self.table}(parent);
                          ''')
        self.conn.commit()
        print(f"Создание тестовой схемы {self.schema} прошло успешно")
        print(f"Создание тестовой таблицы {self.table} прошло успешно")

    def _import_records(self):
        """
            Запись тестовых данных в таблицу
        :return:
        """
        with open(f'{Path(__file__).parent}/test_data.json') as test_file:
            records = json.load(test_file)
            values = [
                f"({record['id']}, {record['ParentId'] if record['ParentId'] else 'null'}, '{record['Name']}', {record['Type']})"
                for record in records]
            self.cur.execute(f'''INSERT INTO \"{self.schema}\".{self.table} (id, parent, name, type)
                                    VALUES {", ".join(values)};
                              ''')
            self.conn.commit()
            print(f"Тестовые данные были успешно загружены в БД")


if __name__ == '__main__':
    with DB() as db:
        db.init_db()
