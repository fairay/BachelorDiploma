import datetime as dt
from typing import List, Optional, Tuple, Dict

from .nodes import *
from .route import Route, RouteList
from .system import TransportSystem
from .transport import Transport


def is_intersect(from1: dt.timedelta, to1: dt.timedelta, from2: dt.timedelta, to2: dt.timedelta) -> bool:
    return (from1 <= from2 <= to1) or (from2 <= from1 <= to2)


def required_offset(from1: dt.timedelta, to1: dt.timedelta, from2: dt.timedelta, to2: dt.timedelta) -> dt.timedelta:
    # 1 shifts 2 to the future
    if not is_intersect(from1, to1, from2, to2):
        return dt.timedelta(0)
    else:
        return to1 - from2


class RouteSchedule(Route):
    _begin: dt.timedelta
    _arrival: List[dt.timedelta]
    _departure: List[dt.timedelta]
    intervals = {
        Parking: dt.timedelta(minutes=2),
        Warehouse: dt.timedelta(minutes=10),
        Consumer: dt.timedelta(minutes=12),
        GeoNode: dt.timedelta(minutes=0)
    }

    def __init__(self, route: Route, begin: dt.timedelta):
        super(RouteSchedule, self).__init__(*route.nodes)
        self.track = None
        self.loads = route.loads

        self._begin = begin
        self.schedule()

    def schedule(self):
        self._arrival = []
        self._departure = []
        current_time = self._begin

        last_node: Optional[GeoNode] = None
        for node, load, i in zip(self.nodes, self.loads, range(len(self.nodes))):
            if last_node:
                current_time += dt.timedelta(minutes=last_node.linked[node].time)

            if load.amount or i in (0, len(self.nodes) - 1):
                interval = self.intervals[type(node)]
            else:
                interval = dt.timedelta(0)
            self._arrival.append(current_time)
            current_time += interval
            self._departure.append(current_time)

            last_node = node

    def shove(self, other: 'RouteSchedule') -> bool:
        """
        :rtype: bool
        True if postpone was made
        """
        self_stops = self.stops
        for node in self_stops:
            if node not in other.stops or isinstance(node, Parking):
                continue

            self_stop = self_stops[node]
            other_stop = other.stops[node]
            offset = required_offset(self_stop[0], self_stop[1], other_stop[0], other_stop[1])
            if offset.total_seconds() > 1e-5:
                other.postpone_by(offset)
                return self.shove(other) or True  # Hope this doesn't exceed the call stack limit
        return False

    def postpone_by(self, delta: dt.timedelta):
        self.begin = self._begin + delta

    @property
    def begin(self) -> dt.timedelta:
        return self._begin

    @begin.setter
    def begin(self, value: dt.timedelta):
        self._begin = value
        self.schedule()

    @property
    def end(self):
        return self._departure[-1]

    @property
    def nodes_schedule(self):
        # node, load, arrival, departure
        return zip(self.nodes, self.loads, self._arrival, self._departure)

    @property
    def stops(self) -> Dict[GeoNode, Tuple[dt.timedelta, dt.timedelta]]:
        stops: Dict[GeoNode, Tuple[dt.timedelta, dt.timedelta]] = {}
        for node, arrival, departure in zip(self.nodes, self._arrival, self._departure):
            if arrival == departure:
                continue

            stops[node] = (arrival, departure)
        return stops


class RouteScheduleList(list[RouteSchedule]):
    pass


class TransportAssignment(dict[Transport, RouteScheduleList]):
    def __init__(self, dict):
        super(TransportAssignment, self).__init__(dict)
        self.routes = RouteScheduleList()

    @property
    def earliest_start(self) -> (dt.timedelta | None, Transport):
        start = dt.timedelta(1000)
        start_truck = None
        for track, routes in self.items():
            if not routes:
                return None, track

            if routes[-1].end < start:
                start = routes[-1].end
                start_truck = track
        return start, start_truck

    def set(self, truck: Transport, route: RouteSchedule):
        route.track = truck
        self[truck].append(route)
        self.routes.append(route)

    def try_attach(self, route: RouteSchedule) -> bool:
        start, truck = self.earliest_start
        if start is not None and start > route.begin:
            route.begin = start

        routes = list(filter(lambda r: r.end > route.begin, self.routes))

        for other in routes:
            if other.shove(route):
                return False

        self.set(truck, route)
        return True


class ScheduleBuilder(object):
    sys: TransportSystem

    def __init__(self, sys: TransportSystem):
        self.sys = sys

    def _init_schedule(self, routes: RouteList, begin: dt.timedelta) -> RouteScheduleList:
        schedule = RouteScheduleList()
        for route in routes:
            schedule.append(RouteSchedule(route, begin))
        return schedule

    def build_schedule(self, routes: RouteList,
                       begin: dt.timedelta = dt.timedelta(hours=9),
                       end: dt.timedelta = dt.timedelta(hours=18)
                       ) -> RouteScheduleList:
        schedule = self._init_schedule(routes, begin)

        unallocated = RouteScheduleList(schedule)
        assignment = TransportAssignment({t: RouteScheduleList() for t in self.sys.transport})

        while len(unallocated):
            unallocated.sort(key=lambda r: r.begin)
            route = unallocated.pop(0)
            if not assignment.try_attach(route):
                unallocated.append(route)

        return schedule
