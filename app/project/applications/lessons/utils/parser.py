import requests


def get_data():
    sample_url = 'https://sample.fitnesskit-admin.ru/schedule/get_v3/?club_id=1'
    orange_url = 'https://orange.fitnesskit-admin.ru/schedule/get_v3/?club_id=1'
    data = requests.get(sample_url)
    if data.status_code == 504:
        data = requests.get(orange_url)
    lesson_data = data.json()['lessons']
    return lesson_data
