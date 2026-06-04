import math

def gps_to_ecef(lat_deg, lon_deg, alt_m=0.0):
    a = 6378137.0
    f = 1.0 / 298.257223563
    b = a * (1 - f)
    e2 = 1 - (b**2 / a**2)
    lat = math.radians(lat_deg)
    lon = math.radians(lon_deg)
    sin_lat = math.sin(lat)
    N = a / math.sqrt(1 - e2 * sin_lat**2)
    X = (N + alt_m) * math.cos(lat) * math.cos(lon)
    Y = (N + alt_m) * math.cos(lat) * math.sin(lon)
    Z = (N * (1 - e2) + alt_m) * math.sin(lat)
    return X, Y, Z

print("GPS to ECEF ready. Example usage in tests.")
