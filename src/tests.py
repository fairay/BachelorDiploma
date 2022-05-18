import unittest

from entities import TransportSystem, RouteBuilder


class MyTestCase(unittest.TestCase):
    def test_1(self):
        tsys = TransportSystem.Loader.load('./configs/test1.json')

        route_builder = RouteBuilder(tsys)
        routes = route_builder.calc_routes()

        self.assertEqual(len(routes), 1)


if __name__ == '__main__':
    unittest.main()
