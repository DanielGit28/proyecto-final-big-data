# config.py
API_BASE_URL = "https://power.larc.nasa.gov/api/temporal"
LATITUDE = "51.5074"
LONGITUDE = "-0.1278"
START_DATE = "20230101"
END_DATE = "20231231"

INPUT_FOLDER = "./data/nasa_power"
OUTPUT_FOLDER = "./data/processed"

# 'daily' or 'hourly'
TEMPORALITY = "daily"
COMMUNITY = "RE"  # AG: Agriculture, RE: Renewable energy, etc.


VARIABLES = [
    "T2M",                # Temperature at 2 meters (°C)
    "RH2M",               # Relative Humidity (%)
    "PRECTOTCORR",        # Precipitation (mm)
    "ALLSKY_SFC_SW_DWN"   # Solar Radiation (W/m^2)
]
