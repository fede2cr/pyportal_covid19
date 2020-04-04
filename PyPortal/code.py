import sys
import time
import board
from adafruit_pyportal import PyPortal
cwd = ("/"+__file__).rsplit('/', 1)[0] # the current working directory (where this file is)
sys.path.append(cwd)
import covid_graphics  # pylint: disable=wrong-import-position

# Get wifi details and more from a secrets.py file
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

# Use cityname, country code where countrycode is ISO3166 format.
# E.g. "New York, US" or "London, GB"
LOCATION = "CRI"

# Set up where we'll be fetching data from

DATE="2020-04-03"  # TODO: Si data está vació, pedir el día anterior
DATA_SOURCE = "https://covid-api.com/api/reports?date="+DATE+"&iso="+LOCATION

DATA_LOCATION = []

# Initialize the pyportal object and let us know what data to fetch and where
# to display it
pyportal = PyPortal(url=DATA_SOURCE,
                    json_path=DATA_LOCATION,
                    status_neopixel=board.NEOPIXEL,
                    default_bg=0x000000)

gfx = covid_graphics.Covid_Graphics(pyportal.splash, am_pm=True)

pyportal.get_local_time()
now = time.localtime()

year = now[0]
month = now[1]
day = now[2] -1
date_format_str = "%d-%02d-%02d"
DATE = date_format_str % (year, month, day)
print(dir(pyportal))

localtile_refresh = None
weather_refresh = None
while True:
    # only query the online time once per hour (and on first run)
    if (not localtile_refresh) or (time.monotonic() - localtile_refresh) > 3600:
        try:
            print("Getting time from internet!")
            pyportal.get_local_time()
            localtile_refresh = time.monotonic()
        except RuntimeError as e:
            print("Some error occured, retrying! -", e)
            continue

    # only query the weather every 10 minutes (and on first run)
    if (not weather_refresh) or (time.monotonic() - weather_refresh) > 3600:
        try:
            value = pyportal.fetch()
            print("Response is", value)
            gfx.display_cases(value)
            weather_refresh = time.monotonic()
        except RuntimeError as e:
            print("Some error occured, retrying! -", e)
            continue

    gfx.update_time()

    time.sleep(30)  # wait 30 seconds before updating anything again