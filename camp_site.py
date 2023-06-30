import dataclasses

@dataclasses.dataclass(frozen=True)
class CampSite:
    name: str
    url: str
    tel: str