from assets import human
from assets import suits as asu
from monster import suits as msu


class LabAssistant(human.Human):
    """In the wrong place at the wrong time."""
    team = "lab_crew"
    suits = [msu.lab_coat, msu.scalpel]

class GuardL1(human.Human):
    """Protect and imprison."""
    team = "lab_crew"
    suits = [msu.guardsuit, msu.taser]
