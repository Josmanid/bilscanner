from dataclasses import dataclass
from .peak import Peak


@dataclass
class EngineEstimate:
    """
    Holds the engine estimate: firing frequency, revolutions per minute
    and the peaks that matched the harmonic comb.
    """
    firing_frequency: float
    revolutions_per_minute: float
    matched_peaks: list[Peak]

