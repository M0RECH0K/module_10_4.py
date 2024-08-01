import threading
import time
from queue import Queue


class Table:
    def __init__(self, number):
        self.number = number
        self.is_busy = False


class Cafe:
    def __init__(self, tables):
        self.queue = Queue()
        self.tables = tables

    def customer_arrival(self):
        number_of_visitors = 20
        for num_vis in range(1, number_of_visitors + 1):
            print(f'Посетитель номер {num_vis} прибыл.')
            num_vis_thread = Customer(num_vis, self)
            num_vis_thread.start()
            time.sleep(1)

    def serve_customer(self, customer):
        check_table = False
        for table in self.tables:
            if not table.is_busy:
                table.is_busy = True
                print(f'Посетитель номер {customer.number} сел за стол {table.number}')
                time.sleep(5)
                table.is_busy = False
                print(f'Посетитель номер {customer.number} покушал и ушёл.')
                check_table = True
                break
        if not check_table:
            print(f'Посетитель номер {customer.number} ожидает свободный стол.')
            self.queue.put(customer)
            self.queue.get()


class Customer(threading.Thread):
    def __init__(self, number, cafe):
        super().__init__()
        self.number = number
        self.cafe = cafe

    def run(self):
        self.cafe.serve_customer(self)


# Создаем столики в кафе
table1 = Table(1)
table2 = Table(2)
table3 = Table(3)
tables1 = [table1, table2, table3]

# Инициализируем кафе
cafe1 = Cafe(tables1)

# Запускаем поток для прибытия посетителей
customer_arrival_thread = threading.Thread(target=cafe1.customer_arrival)
customer_arrival_thread.start()

# Ожидаем завершения работы прибытия посетителей
customer_arrival_thread.join()
