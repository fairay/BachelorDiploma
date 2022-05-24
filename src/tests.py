import unittest

from entities import TransportSystem, RouteBuilder, Parking, Warehouse, Product, Consumer, Road, Transport


def small_sys() -> TransportSystem:
    tsys = TransportSystem()
    tsys.vol = 0.1
    tsys.add_parking(Parking('Стоянка'))
    tsys.add_warehouse(Warehouse('Склад №1', Product('шоколад', 10, tsys.vol)), Road())
    tsys.add_consumer(Consumer('Магазин №1', Product('шоколад', 4, tsys.vol)))
    tsys.add_consumer(Consumer('Магазин №2', Product('шоколад', 4, tsys.vol)))
    tsys.add_link(1, 2)
    tsys.add_link(1, 3)
    tsys.add_link(2, 3)
    tsys.add_transport(Transport('ГАЗель NEXT', 1.0))
    return tsys


class MyTestCase(unittest.TestCase):
    def case(self, filename: str, want_route_n: int):
        tsys = TransportSystem.Loader.load(f'./configs/{filename}.json')

        route_builder = RouteBuilder(tsys)
        routes = route_builder.calc_routes()

        self.assertEqual(len(routes), want_route_n)

    def test_files(self):
        cases = {
            'test1': 1,
            'test2': 3,
            'test3': 1,
            'test4': 2,
            'test5': 2,
            'test6': 1,
            'test7': 2,
            'test8': 2,
            'test9': 1,
            'test10': 2,
            'test11': 1,
            'test12': 3,
        }

        for filename, want in cases.items():
            with self.subTest(filename=filename, want=want):
                self.case(filename, want)


if __name__ == '__main__':
    unittest.main()
