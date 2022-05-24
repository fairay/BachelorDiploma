import datetime as dt
import random

import plotly as py
import plotly.figure_factory as ff

from entities import TransportSystem, Parking, Warehouse, Consumer
from entities.route_shedule import RouteScheduleList


def schedule_dict(sys: TransportSystem, routes: RouteScheduleList):
    df = []
    today = dt.datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
    for route in routes:
        truck = route.track
        truck_index = sys.transport.index(truck)
        for node, load, arrival, departure in route.nodes_schedule:
            operation = {}
            operation['Task'] = f'[{truck_index}] {truck.name}'

            t1 = today + arrival
            t2 = today + departure
            if t1 == t2:
                t2 += dt.timedelta(seconds=15)
            operation['Start'] = t1
            operation['Finish'] = t2
            operation['Node'] = node.name
            df.append(operation)
    df.sort(key=lambda x: x["Node"])
    return df


r = lambda: random.randint(0, 255)
rng = lambda low, high: random.randint(low, high)
color_scheme = {
    Parking: lambda: '#%02X%02X%02X' % (255, 0, 0),
    Warehouse: lambda: '#%02X%02X%02X' % (0, rng(0, 170), rng(220, 255)),
    Consumer: lambda: '#%02X%02X%02X' % (rng(0, 170), rng(220, 255), 0)
}


def draw_schedule(sys: TransportSystem, routes: RouteScheduleList):
    df = schedule_dict(sys, routes)

    colors = {node.name: color_scheme[type(node)]() for node in sys.nodes}

    return ff.create_gantt(df, index_col='Node', colors=colors,
                           title='График маршрутов', show_colorbar=True,
                           group_tasks=True,
                           showgrid_x=True, showgrid_y=True)


def draw_grant(sys: TransportSystem, routes: RouteScheduleList):
    fig = draw_schedule(sys, routes)
    py.offline.plot(fig, filename='gantt.html')
