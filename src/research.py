import random
import time

from entities import TransportSystem, RouteBuilder
import matplotlib.pyplot as plt

from system_generator import random_system


def one_case(sys: TransportSystem):
    routes, stat = RouteBuilder(sys).stat_calc_routes()

    plt.subplot(221)
    plt.ylabel('стоимость плана')
    plt.xlabel('количество итераций')
    plt.plot([a['cost'] for a in stat])

    plt.subplot(222)
    plt.ylabel('количество маршрутов')
    plt.xlabel('количество итераций')
    plt.plot([a['len'] for a in stat])

    plt.subplot(223)
    plt.ylabel('средняя протяжённость маршрутов')
    plt.xlabel('количество итераций')
    plt.plot([a['avg_dist'] for a in stat])

    plt.subplot(224)
    plt.ylabel('средняя занятость транспорта (%)')
    plt.xlabel('количество итераций')
    plt.plot([a['avg_full'] for a in stat])

    plt.suptitle(f'Система из {len(sys.nodes)} пунктов')
    plt.show()

def cmp_optimize(sizes):
    repeat_n = 2
    init_cost = []
    end_cost = []

    for size in sizes:
        init_aver = 0.0
        end_aver = 0.0

        repeat_n = max(2, 100 // size) * 2
        for i in range(repeat_n):
            tsys = random_system(size, size // 10, seed=random.randint(0, 10000))
            init_routes = RouteBuilder(tsys).calc_routes(0)
            end_routes = RouteBuilder(tsys).calc_routes()

            init_aver += sum(r.cost for r in init_routes)
            end_aver += sum(r.cost for r in end_routes)
        init_cost.append(init_aver / repeat_n)
        end_cost.append(end_aver / repeat_n)
        print(f'{size} DONE')

    plt.plot(list(sizes), init_cost, label='начальный план')
    plt.plot(list(sizes), end_cost, label='оптимизированный план')
    plt.ylabel('стоимость плана')
    plt.xlabel('количество пунктов')
    plt.legend()
    plt.show()

def time_research(sizes):
    repeat_n = 1
    times = []
    for size in sizes:
        aver = 0.0
        for i in range(repeat_n):
            tsys = random_system(size, size // 10, seed=size)

            t_begin = time.process_time()
            routes, stat = RouteBuilder(tsys).stat_calc_routes()
            aver += time.process_time() - t_begin
        print(f'{size:} {aver:}')
        times.append(aver / repeat_n)

    plt.ylabel('время оптимизации (мс)')
    plt.xlabel('количество пунктов')
    plt.plot(list(sizes), times)
    plt.show()

def cmp_truck():
    repeat_n = 2
    end_cost = []

    size = 50
    con_list = list(con / 10 for con in range(4, 15, 1))
    con_list += list(con / 10 for con in range(15, 60, 4))
    for con in con_list:
        end_aver = 0.0
        for i in range(repeat_n):
            tsys = random_system(size, size // 10, seed=random.randint(0, 10000), con=con)
            end_routes = RouteBuilder(tsys).calc_routes()

            end_aver += sum(r.cost for r in end_routes)
        end_cost.append(end_aver / repeat_n)
        print(f'{con} DONE')

    plt.plot(con_list, end_cost)
    plt.ylabel('стоимость плана')
    plt.xlabel('вместительность грузовика')
    plt.show()


def cmp_prod():
    repeat_n = 1
    end_cost = []

    size = 50
    profit_list = list(con / 100 for con in range(105, 120, 1))
    for profit in profit_list:
        end_aver = 0.0
        for i in range(repeat_n):
            tsys = random_system(size, size // 10, seed=random.randint(0, 10000), profit=2)
            end_routes = RouteBuilder(tsys).calc_routes()

            end_aver += sum(r.cost for r in end_routes)
        end_cost.append(end_aver / repeat_n)
        print(f'{profit} DONE')

    plt.plot(profit_list, end_cost)
    plt.ylabel('стоимость плана')
    plt.xlabel('избыток продуктов')
    plt.show()

if __name__ == '__main__':
    # cmp_truck()
    # cmp_optimize(range(20, 86, 5))
    # time_research(list(range(20, 100, 5)) + list(range(100, 146, 15)))
    # tsys = random_system(100, 10)
    # one_case(tsys)
    cmp_prod()
