import requests

if __name__ == '__main__':
    r = requests.get('http://127.0.0.1:8000/events/from/2022-01-12T15:06:00/to/12/')
    print(r.json())