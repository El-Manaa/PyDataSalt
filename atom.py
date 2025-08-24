from dataclasses import dataclass


@dataclass(frozen=True)
class Atom:
    number: int | None
    symbol: str
    name: str
    group: str
    atomicMass: float | None
    standardState: str
    meltingPoint: float | None
    electronegativity: float | None
    density: float | None
    yeardiscovered: int | None
