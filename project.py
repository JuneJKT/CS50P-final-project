from datetime import date, datetime
from geopy.geocoders import Nominatim
from astropy.coordinates import SkyCoord, EarthLocation, AltAz
from astropy import units as u
from astropy.time import Time
from astropy.coordinates import get_sun, get_body
from fpdf import FPDF


class PDF(FPDF):
    def __init__(self):
        super().__init__(orientation="P", unit="mm", format=(88.9, 50.8))


def main():
    # Get birthdate and birthtime
    while True:
        birthdate = input("Enter your birthdate (YYYY-MM-DD): ").strip()
        birthtime = input("Enter your birth time (HH:MM in 24-hr format): ").strip()
        try:
            bd, birthtime = get_date(birthdate, birthtime)
            break
        except (ValueError, TypeError):
            pass

    # Get birth location
    while True:
        location_name = input("Enter your birth place (e.g. New York City): ").strip()
        try:
            latitude, longitude = get_coordinates(location_name)
            break
        except (ValueError, TypeError):
            pass

    # Make items into correct format
    observing_time = Time(f"{bd} {birthtime}:00")
    observing_location = EarthLocation(lat=latitude*u.deg, lon=longitude*u.deg, height=0*u.m)

    # Get part of luck
    luckysign, ascending_sign = get_poluck(observing_time, observing_location)

    # Get a prophecy
    prophecy = get_prophecy(luckysign)

    # Printing
    print("\n")
    print(f"Birthdate: {bd}, Birth time {birthtime}")
    print(f"Latitude: {latitude}, Longitude: {longitude}")
    print(f"Ascendant: {ascending_sign}")
    print(f"Lucky pathway is in {luckysign}", end="\n \n")
    print(f"Advice for you: {prophecy}", end="\n \n")
    print(f"Remember, these prophecies are symbolic and open to interpretation. They aim to provide guidance and inspiration rather than a deterministic outlook. Trust in your unique journey and intuition as you navigate the path toward your fortune.", end="\n \n")

    # Make a card
    ask = input("Do you want a prophecy card in PDF? (Y/N): ").strip().upper()
    if ask == "Y":
        prophet = prophecy
        get_pic(prophet)
    else:
        pass


def get_date(birthdate, birthtime):
    bd = date.fromisoformat(birthdate)
    # Check actual date
    if bd <= date.today():
        # Validate time format
        datetime.strptime(birthtime, "%H:%M")
        return bd, birthtime
    else:
        raise ValueError


def get_coordinates(location_name):
    geolocator = Nominatim(user_agent="my_geocoder")
    location = geolocator.geocode(location_name)
    if location:
        latitude = location.latitude
        longitude = location.longitude
        return latitude, longitude
    else:
        raise ValueError


def get_poluck(observing_time, observing_location):
    # Get the position of the Sun at the specified time and location
    sun_position = get_sun(observing_time)
    moon_position = get_body("moon", observing_time, location=observing_location)

    # Get the position of the Moon at the specified time and location
    moon_position = get_body("moon", observing_time, location=observing_location)

    # Get the coordinates of the Moon
    moon_coord = SkyCoord(moon_position.ra, moon_position.dec, frame='icrs')

    # Calculate the difference between the Sun and Moon longitudes
    diff_longitude = (sun_position.ra - moon_position.ra).degree
    if diff_longitude < 0:
        diff_longitude += 360  # Adjust if negative

    # Calculate the Ascendant using the Sun's position
    ascendant_lon = (sun_position.ra + 180 * u.deg) % (360 * u.deg)

    # Calculate moon degree
    moon_sign = moon_coord.transform_to('geocentrictrueecliptic').lon
    moon_sign_deg = moon_sign.degree % 360

    # Define the zodiac signs
    zodiac_signs = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']

    # Calculate the ascending zodiac sign
    ascending_sign_index = int(ascendant_lon.degree / 30)
    ascending_sign = zodiac_signs[ascending_sign_index]

    # Calculate the altitude of the Sun at the specified time and location
    sun_altitude = get_sun(observing_time).transform_to(AltAz(obstime=observing_time, location=observing_location)).alt

    # Check if the Sun is above or below the horizon (day or night chart)
    is_day_chart = sun_altitude > 0  # Sun is above horizon for day chart, below for night

    # Calculate the Part of Fortune based on day or night chart
    if is_day_chart:
        partoffortune = int(ascending_sign_index + moon_sign_deg - sun_position.ra.degree)
    else:
        partoffortune = int(ascending_sign_index + sun_position.ra.degree - moon_sign_deg)

    # Define the zodiac signs in order
    zodiac_signs_ordered = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']

    # Calculate the luck sign
    luck_sign_index = int(partoffortune /30)
    luck_sign = zodiac_signs_ordered[luck_sign_index]

    # Find the index of the Ascendant's sign in the zodiac_signs_ordered list
    ascendant_index = zodiac_signs_ordered.index(ascending_sign)

    luck_index = zodiac_signs_ordered.index(luck_sign)

    # Reorder the zodiac_signs_ordered list to start from the Ascendant's sign
    reordered_signs = zodiac_signs_ordered[ascendant_index:] + zodiac_signs_ordered[:ascendant_index]

    # Calculate the position of the lucky sign after reordering
    lucky_sign_position = (luck_index - ascendant_index) % 12  # Ensure it wraps around the zodiac cycle

    # Find the lucky sign after reordering
    luckysign = reordered_signs[lucky_sign_position]

    return luckysign, ascending_sign


def get_prophecy(luckysign):
     prophecies = {
            'Aries': "Your fortune shines through bold actions and initiative. Seize the moment and trust in your instincts to unlock prosperity.",
            'Taurus': "Stability and patience are your keys to fortune. Embrace the steady path, and abundance will find its way to you.",
            'Gemini': "Versatility and communication hold the power to enhance your fortune. Embrace change and adaptability for success.",
            'Cancer': "Your fortune lies in nurturing and emotional connections. Trust your intuition, and home and family will bring blessings.",
            'Leo': "Creative expression and self-confidence pave the way to your fortune. Shine brightly, and abundance will follow.",
            'Virgo': "Attention to detail and practicality bring forth your fortune. Organize and refine, and prosperity will come naturally.",
            'Libra': "Harmony and balance are your keys to fortune. Seek equilibrium in all things, and prosperity will flow effortlessly.",
            'Scorpio': "Transformation and intensity lead to your fortune. Embrace change fearlessly, and hidden treasures will be revealed.",
            'Sagittarius': "Adventure and optimism drive your fortune. Explore new horizons, and abundance will be found in the journey.",
            'Capricorn': "Discipline and perseverance shape your fortune. Climb steadily, and success will crown your efforts.",
            'Aquarius': "Innovation and originality hold the key to your fortune. Embrace uniqueness, and prosperity will follow your vision.",
            'Pisces': "Imagination and intuition guide your fortune. Trust your dreams, and let compassion lead you to abundance."
        }
     return prophecies.get(luckysign)


def get_pic(prophet):
    pdf = PDF()
    pdf.set_auto_page_break(0)
    pdf.set_margins(0,0,0)
    pdf.add_page()
    pdf.image("bgpic.png", w=88.9, h=50.8)
    pdf.set_font("times", "B", 8.5)
    pdf.set_text_color(255, 64, 129)
    pdf.set_xy(2.5, 19.5)
    pdf.multi_cell(85, 4, f"{prophet}", align="C")
    pdf.output("prophecycard.pdf")


if __name__ == "__main__":
    main()
