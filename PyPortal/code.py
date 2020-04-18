import sys
import time
import board
from adafruit_pyportal import PyPortal
cwd = ("/"+__file__).rsplit('/', 1)[0] # the current working directory (where this file is)
sys.path.append(cwd)
import covid_graphics  # pylint: disable=wrong-import-position

# Optional, to take a screenshot to SD card
#from adafruit_bitmapsaver import save_pixels
#import storage
#import busio

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

DATA_SOURCE = "https://covid-api.com/api/reports?iso="+LOCATION

DATA_LOCATION = []

# Initialize the pyportal object and let us know what data to fetch and where
# to display it
pyportal = PyPortal(url=DATA_SOURCE,
                    json_path=DATA_LOCATION,
                    status_neopixel=board.NEOPIXEL,
                    default_bg=0x000000)

gfx = covid_graphics.Covid_Graphics(pyportal.splash, am_pm=True)

display_refresh = None
while True:
    # only query the online time once per hour (and on first run)
    if (not display_refresh) or (time.monotonic() - display_refresh) > 3600:
        try:
            print("Getting time from internet!")
            pyportal.get_local_time()
            display_refresh = time.monotonic()
        except RuntimeError as e:
            print("Some error occured, retrying! -", e)
            continue

        try:
            value = pyportal.fetch()
            print("Response is", value)
            gfx.display_cases(value)
        except RuntimeError as e:
            print("Some error occured, retrying! -", e)
            continue

    gfx.update_time()
    # Optional: to take screenshot to SD card
    #storage.remount("/", False)
    #print('Taking Screenshot...')
    #save_pixels('/screenshot.bmp')
    #print('Screenshot taken')

    time.sleep(60)  # wait 60 seconds before updating anything again