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
    def test_1(self):
        tsys = TransportSystem.Loader.load('./configs/test1.json')

        route_builder = RouteBuilder(tsys)
        routes = route_builder.calc_routes()

        self.assertEqual(len(routes), 1)

    def test_2(self):
        tsys = TransportSystem.Loader.load('./configs/test2.json')

        route_builder = RouteBuilder(tsys)
        routes = route_builder.calc_routes()

        self.assertEqual(len(routes), 3)

    def test_3(self):
        tsys = TransportSystem.Loader.load('./configs/test3.json')

        route_builder = RouteBuilder(tsys)
        routes = route_builder.calc_routes()

        self.assertEqual(len(routes), 1)

    def test_4(self):
        tsys = TransportSystem.Loader.load('./configs/test4.json')

        route_builder = RouteBuilder(tsys)
        routes = route_builder.calc_routes()

        self.assertEqual(len(routes), 2)


if __name__ == '__main__':
    unittest.main()
