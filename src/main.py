from transport import *


def main():
    trans = TransportSystem()

    trans.add_parking(Parking())

    trans.add_consumer(Consumer({'Сникерс': 20}))
    trans.add_consumer(Consumer({'Сникерс': 10, 'Хлеб': 5}))

    trans.add_warehouse(Warehouse({'Сникерс': 40, 'Хлеб': 10}))


if __name__ == '__main__':
    main()
