import pytest

from astropy.coordinates import EarthLocation
from astropy.time import Time
from astropy import units as u

from project import get_date, get_coordinates, get_poluck, get_prophecy


def main():
    test_get_date()
    test_get_coordinates()
    test_get_poluck()
    test_get_prophecy()
    test_get_pic()


def test_get_date():
    with pytest.raises(ValueError):
        assert get_date("2025-06-08", "12:12")
    with pytest.raises(ValueError):
        assert get_date("1987-06-05", "25:30")


def test_get_coordinates():
    assert get_coordinates("Bangkok") == (13.8245796, 100.6224463)
    assert get_coordinates("London") == (51.5074456, -0.1277653)
    assert get_coordinates("New York City") == (40.7127281, -74.0060152)


def test_get_poluck():
    observing_time = Time("1987-06-05 21:46:00")
    observing_location = EarthLocation(lat=13.1857117*u.deg, lon=101.1210777*u.deg, height=0*u.m)
    assert get_poluck(observing_time, observing_location) == ("Capricorn", "Sagittarius")


def test_get_prophecy():
    assert get_prophecy("Taurus") == "Stability and patience are your keys to fortune. Embrace the steady path, and abundance will find its way to you."
    assert get_prophecy("Pisces") == "Imagination and intuition guide your fortune. Trust your dreams, and let compassion lead you to abundance."
    assert get_prophecy("Leo") == "Creative expression and self-confidence pave the way to your fortune. Shine brightly, and abundance will follow."


if __name__ == "__main__":
    main()
