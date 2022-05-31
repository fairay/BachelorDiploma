import random
import time
from typing import List

import matplotlib.pyplot as plt

from entities import TransportSystem, RouteBuilder
from system_generator import random_system


def smooth(old: List[float]) -> List[float]:
    new = [old[0]]
    for i in range(1, len(old) - 1):
        # if i + 3 < len(old):
        #     old[i] = min(old[i], max(old[i+1:i+4]))
        # if i - 3 >= 0:
        #     old[i] = max(old[i], min(old[i-3:i]))

        val = old[i - 1] + 2 * old[i] + old[i + 1]
        new.append(val / 4)
    new.append(old[-1])
    return new


def one_case(sys: TransportSystem):
    routes, stat = RouteBuilder(sys).stat_calc_routes()
    label = f'{len(sys.nodes)} пунктов'

    plt.subplot(221)
    plt.ylabel('длительность маршрутов, км')
    plt.xlabel('количество итераций, шт')
    plt.plot([a['cost'] for a in stat], label=label)
    plt.legend()

    plt.subplot(222)
    plt.ylabel('количество маршрутов, шт')
    plt.xlabel('количество итераций, шт')
    plt.plot([a['len'] for a in stat], label=label)
    plt.legend()

    plt.subplot(223)
    plt.ylabel('средняя протяжённость маршрутов, км')
    plt.xlabel('количество итераций, шт')
    plt.plot([a['avg_dist'] for a in stat], label=label)
    plt.legend()

    plt.subplot(224)
    plt.ylabel('средняя занятость транспорта, %')
    plt.xlabel('количество итераций, шт')
    plt.plot([a['avg_full'] for a in stat], label=label)
    plt.legend()

    # plt.suptitle(f'Система из {len(sys.nodes)} пунктов')
    # plt.show()


def many_cases(sizes):
    for size in sizes:
        tsys = random_system(size, size // 10, seed=1)
        one_case(tsys)

    plt.show()


def cmp_parking_dist():
    size = 50

    dist = []
    cost = []
    for i in range(100):
        tsys = random_system(size, size // 10, seed=10)
        routes, stat = RouteBuilder(tsys).stat_calc_routes()
        dist.append(stat[0]['avg_parking_dist'])
        cost.append(stat[-1]['cost'])

    cost = [x for _, x in sorted(zip(dist, cost))]
    cost = smooth(smooth(cost))
    dist.sort()

    plt.plot(dist, cost)
    plt.ylabel('стоимость плана')
    plt.xlabel('среднее расстояние до парковки')
    plt.show()


def cmp_optimize(sizes):
    init_cost = []
    end_cost = []

    for size in sizes:
        init_aver = 0.0
        end_aver = 0.0

        repeat_n = max(2, 100 // size)
        for i in range(repeat_n):
            tsys = random_system(size, size // 10, seed=random.randint(0, 10000))
            init_routes = RouteBuilder(tsys).calc_routes(0)
            end_routes = RouteBuilder(tsys).calc_routes()

            init_aver += sum(r.cost for r in init_routes)
            end_aver += sum(r.cost for r in end_routes)
        init_cost.append(init_aver / repeat_n)
        end_cost.append(end_aver / repeat_n)
        print(f'{size} DONE')

    init_cost.sort()
    end_cost.sort()
    init_cost, end_cost = smooth(init_cost), smooth(end_cost)

    plt.plot(list(sizes), init_cost, label='начальный план', linestyle='dotted')
    plt.plot(list(sizes), end_cost, label='оптимизированный план')
    plt.ylabel('длительность маршрутов, км', fontsize=18)
    plt.xlabel('количество пунктов, шт', fontsize=18)
    plt.title('Сравнение длительности маршрутов\nдо и после оптимизации', fontsize=18)
    plt.legend(prop={'size': 14})
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

    plt.ylabel('время оптимизации, с', fontsize=18)
    plt.xlabel('количество пунктов, шт', fontsize=18)
    plt.title('Временные характеристики программы', fontsize=18)
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

    end_cost = smooth(end_cost)

    plt.plot(con_list, end_cost)
    plt.ylabel('длительность маршрутов, км')
    plt.xlabel('вместительность грузовика, м³')
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
    plt.ylabel('длительность маршрутов, км')
    plt.xlabel('избыток продуктов, разы')
    plt.show()

def main(case):
    match case:
        case 'many_cases':
            # Исследование работы алгоритма (характеристики системы по итерациям)
            many_cases([100, 200])
        case 'cmp_optimize_low':
            # Сравнение длительностей маршрутов
            cmp_optimize(range(20, 81, 5))
        case 'cmp_optimize_high':
            # Сравнение длительностей маршрутов
            cmp_optimize(range(80, 181, 15))
        case 'time_research':
            # Временные характеристики
            time_research(list(range(20, 100, 10)) + list(range(100, 251, 25)))
        case _:
            print(f'no {case} research')

if __name__ == '__main__':
    main('time_research')

    # cmp_parking_dist()
    # cmp_truck()

    # time_research(list(range(20, 100, 10)) + list(range(100, 251, 25)))
    # cmp_prod()
    # tsys = random_system(100, 10)
    # one_case(tsys)
