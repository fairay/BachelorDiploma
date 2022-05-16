from copy import copy
from typing import List

from .geonode import GeoNode
from ..transport import Transport


class Parking(GeoNode):
    def __init__(self, name='Стоянка'):
        super(Parking, self).__init__(name)
        self.transport: List[Transport] = []

    def __copy__(self) -> 'Parking':
        new = Parking(self.name)
        new.linked = copy(self.linked)
        new.transport = copy(self.transport)
        return new

    def clear_transport(self):
        self.transport: List[Transport] = []

    def del_transport(self, track: Transport):
        for i, t in enumerate(self.transport):
            if track.name == t.name:
                del self.transport[i]

    def add_transport(self, track: Transport):
        self.transport.append(track)

    def update(self, other: 'Parking'):
        super(Parking, self).update(other)

        self.transport = []
        for track in other.transport:
            self.add_transport(track)
