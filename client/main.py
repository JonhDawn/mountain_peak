import sys

import requests

ipaddress = sys.argv[1]
BASE_URL = f'http://{ipaddress}:8000'


def create_peak(name: str, lat: float, lon: float, altitude: float) -> dict:
    data = {'name': name, 'lat': lat, 'lon': lon, 'altitude': altitude}
    request = requests.post(f'{BASE_URL}/peak/', data=data)
    return request.json() if request.ok else {}


def upload_peak(name: str, lat: float, lon: float, altitude: float) -> dict:
    data = {'name': name, 'lat': lat, 'lon': lon, 'altitude': altitude}
    request = requests.put(f'{BASE_URL}/peak/', data=data)
    return request.json() if request.ok else {}


def read_peak(name: str) -> dict:
    request = requests.get(f'{BASE_URL}/peak/?name={name}')
    return request.json() if request.ok else {}


def delete_peak(name: str) -> dict:
    data = {'name': name}
    request = requests.delete(f'{BASE_URL}/peak/', data=data)
    return request.json() if request.ok else {}


def get_peaks_in_box(lat_ne: float, lat_sw: float, lon_ne: float, lon_sw: float) -> dict:
    request = requests.get(f'{BASE_URL}/zone/?lat_ne={lat_ne}&lat_sw={lat_sw}&lon_ne={lon_ne}&lon_sw={lon_sw}')
    return request.json() if request.ok else {}


if __name__ == '__main__':
    create_peak('Everest', lat=27.988, lon=86.925, altitude=8849.0)
    create_peak('K2', lat=35.881, lon=76.514, altitude=8611.0)
    print(get_peaks_in_box(lat_ne=40, lat_sw=20, lon_ne=90, lon_sw=80))
