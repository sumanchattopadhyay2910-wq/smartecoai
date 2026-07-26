from dataclasses import dataclass


@dataclass
class Violation:
    title: str
    description: str = ""
    severity: str = "medium"
