class Transport:
    def __init__(self, name="", volume=10.0, cons=1.0):
        self.name: str = name
        self.volume: float = volume

    def __repr__(self) -> str:
        return f'{self.name} (📦:{self.volume})'
