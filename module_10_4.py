import threading
import time
from queue import Queue


class Table:
    def __init__(self, number):
        self.number = number
        self.is_busy = False


class Cafe(threading.Thread):
    def __init__(self, tables, *args, **kwargs):
        super(Cafe, self).__init__(*args, **kwargs)
        self.table = Queue()
        self.tables = tables
        self.customer = Queue()
        for i, table in enumerate(self.tables):
            self.table.put(i + 1)

    def customer_arrival(self):
        for i in range(1, 21):
            customer = Customer(customer=i, table=0)
            self.customer.put(customer)
        while not self.customer.empty():
            customer = self.customer.get()
            print(f'Посетитель номер {customer.customer} прибыл', flush=True)
            self.serve_customer(customer=customer)
            time.sleep(1)

    def serve_customer(self, customer):
        if not self.table.empty():
            table = self.table.get()
            customer.table = table
            customer.start()
        else:
            print(f'Посетитель номер {customer.customer} ожидает свободный стол')
            while self.table.empty():
                time.sleep(1)
            if not self.table.empty():
                table = self.table.get()
                customer.table = table
                customer.start()


class Customer(threading.Thread):
    def __init__(self, customer, table, *args, **kwargs):
        super(Customer, self).__init__(*args, **kwargs)
        self.table = table
        self.customer = customer

    def run(self):
        print(f'Посетитель номер {self.customer} сел за стол {self.table}', flush=True)
        time.sleep(5)
        print(f'Посетитель номер {self.customer} покушал и ушёл.', flush=True)
        cafe1.table.task_done()
        cafe1.table.put(self.table)
        cafe1.customer.task_done()
        cafe1.customer.join()


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


