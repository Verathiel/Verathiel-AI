import random
import re
import logging
from datetime import datetime
import json

with open("responses.json", "r", encoding="utf-8") as f:
    responses = json.load(f)

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

uzivatelske_info = {}
prazdne_vstupy = 0

odpovedi_ahoj = responses["pozdrav"]
odpovedi_jak_se_mas = responses["jak_se_mas"]
odpovedi_emoce_negative = responses["negativni_emoce"]
odpovedi_emoce_positive = responses["pozitivni_emoce"]

def odstran_diakritiku(zprava):
    diakritika = str.maketrans("áčďéěíňóřšťúůýž", "acdeeinorstuuyz")
    return zprava.translate(diakritika)

def odpovedet(zprava):
    global prazdne_vstupy
    zprava = odstran_diakritiku(zprava.lower()).strip()

    if not zprava:
        prazdne_vstupy += 1
        if prazdne_vstupy >= 3:
            return "Hej, jsi tam ještě? Napiš něco, ať pokračujeme!"
        return "Prosím, polož mi otázku nebo mi něco řekni!"

    prazdne_vstupy = 0
    logging.debug(f"Zpráva po odstranění diakritiky: '{zprava}'")

    if any(p in zprava for p in ["jsem smutna", "jsem smutny"]):
        return random.choice(odpovedi_emoce_negative)
    elif any(p in zprava for p in ["jsem stastna", "jsem stastny", "jsem vesela", "jsem rad", "jsem rada"]):
        return random.choice(odpovedi_emoce_positive)

    pozdravy = ["ahoj", "cau", "cus", "nazdar", "zdravim", "dobry den", "dobry vecer", "cauky", "caves", "servus"]
    if any(pozdrav in zprava for pozdrav in pozdravy):
        logging.debug("Rozpoznán pozdrav")
        return random.choice(odpovedi_ahoj)

    if any(varianta in zprava for varianta in ["jak se mas", "jak jsi", "jak jde", "jak se vede"]):
        logging.debug("Rozpoznána otázka 'jak se máš'")
        return random.choice(odpovedi_jak_se_mas)

    match_jmeno = re.search(r"jmenuji\s+se\s+(\w+)", zprava)
    if match_jmeno:
        jmeno = match_jmeno.group(1)
        uzivatelske_info['jmeno'] = jmeno
        logging.debug(f"Rozpoznáno jméno: {jmeno}")
        return f"Rád tě poznávám, {jmeno}!"

    match_preference = re.search(r"mam\s+rad\s+(.+)", zprava)
    if match_preference:
        preference = match_preference.group(1)
        uzivatelske_info['preference'] = preference
        logging.debug(f"Rozpoznána preference: {preference}")
        return f"Skvělé, že máš rád {preference}! To je zajímavé."

    if any(otazka in zprava for otazka in ["kolik je hodin", "jaky je cas"]):
        logging.debug("Rozpoznána otázka na čas")
        aktualni_cas = datetime.now().strftime("%H:%M")
        return f"Je {aktualni_cas}. Co teď plánuješ?"

    if len(zprava.split()) >= 2:
        logging.debug("Použita fallback odpověď pro dlouhou zprávu")
        return "To zní zajímavě! Můžeš mi o tom říct více?"

    if 'jmeno' in uzivatelske_info:
        logging.debug("Použita odpověď s jménem uživatele")
        return f"{uzivatelske_info['jmeno']}, co plánuješ dnes?"

    logging.debug("Není rozpoznána žádná specifická podmínka")
    return "Promiň, tomu nerozumím. Můžeš to prosím říct jinak nebo to více objasnit?"
