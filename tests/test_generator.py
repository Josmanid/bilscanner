import pytest

from carscanner.sources.signalGenerator import SignalGenerator

# naming is like this CLassName_MethodName_WhatWeWantToHappen
def test_signalGenerator_sine_returns_correct_length_and_duration():
    # Arrange
    generator = SignalGenerator()

    # Act
    signal = generator.sine(frequency=18.75, amplitude=1, duration=5, fs=48000)

    # Assert: N = T * f_s og T = N / f_s (formel 7.2)
    assert len(signal.samples) == 240000
    assert signal.duration() == 5.0


def test_signalGenerator_sine_peak_equals_amplitude():
    # Arrange
    generator = SignalGenerator()

    # Act: amplitude 2 i stedet for 1, så vi tester at parameteren virker
    signal = generator.sine(frequency=18.75, amplitude=2, duration=5, fs=48000)

    # Assert: f(n) = A sin(2 pi f n T_s) svinger mellem -A og A.
    # pytest.approx, fordi toppen ikke altid rammer præcis en sample,
    # og computeren afrunder decimaltal.
    assert signal.samples.max() == pytest.approx(2.0)
    assert signal.samples.min() == pytest.approx(-2.0)