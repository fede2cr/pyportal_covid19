# pyportal_covid19
Using and Adafruit PyPortal to receive daily stats about the progress of Covid19 infections in your country

![PyPortal](imgs/PyPortal.JPG)

## How to install

This will hopefully land on a Learn guide, so it will have detailed installation instructions. For the moment:

1. Follow the steps in the PyPortal Weather Station guide, except for the API key
2. Now, overwrite the files in the PyPortal/ folder, to the CIRCUITPY drive


## API

https://covid-19-apis.postman.com/
https://covid-api.com/api/reports?iso=CRI


## Bugs

[ ] I doesn't seem to download the JSON file from the API site from the PyPortal. I had to open the link with Firefox, and save it as ```local.txt```. The user agent for ``wget`` might be blocked, so the same could be happening with Python

## Attribution

Heavily based on the PyPortal Weather Station from the [Learn Guide](https://learn.adafruit.com/pyportal-weather-station) from Adafruit.
