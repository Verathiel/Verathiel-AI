import json
import logging

uzivatelske_info = {}
historie_konverzace = []

def uloz_data():
    data = {
        'uzivatelske_info': uzivatelske_info,
        'historie_konverzace': historie_konverzace
    }
    try:
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        logging.error(f"Chyba při ukládání dat: {e}")

def nacti_data():
    global uzivatelske_info, historie_konverzace
    try:
        with open('data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            uzivatelske_info = data.get('uzivatelske_info', {})
            historie_konverzace = data.get('historie_konverzace', [])
    except FileNotFoundError:
        uzivatelske_info = {}
        historie_konverzace = []
    except Exception as e:
        logging.error(f"Chyba při načítání dat: {e}")
