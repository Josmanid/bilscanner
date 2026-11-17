from dataclasses import dataclass


@dataclass 
class Peak:
    """Holds one peak in the spectrum"""
    frequency: float       # toppens frekvens i Hz
    amplitude: float       # toppens amplitude i spektret
    above_floor_db: float  # hvor mange dB toppen ligger over gulvet    
