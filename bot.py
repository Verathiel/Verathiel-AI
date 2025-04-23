import random
import re
import logging
from datetime import datetime

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

uzivatelske_info = {}
prazdne_vstupy = 0

odpovedi_ahoj = ["Ahoj! Jak se máš?", "Čau! Co tě dnes trápí?", "Zdravím tě! Jaký máš den?"]
odpovedi_jak_se_mas = ["Mám se skvěle, díky, že se ptáš! A ty?", "Jsem v pohodě, co ty?", "Dnes jsem plný energie! Jak jsi na tom ty?"]
odpovedi_emoce = ["To mě mrzí, co se stalo? Řekni mi víc.", "Hej, to zní těžce. Chceš o tom mluvit?", "Proč jsi smutný? Třeba tě rozveselím!"]

def odstran_diakritiku(zprava):
    diakritika = str.maketrans("áčďéěíňóřšťúůýž", "acdeeinorstuuyz")
    return zprava.translate(diakritika)

def odpovedet(zprava):
    global prazdne_vstupy
    zprava = odstran_diakritiku(zprava.lower())

    if not zprava.strip():
        prazdne_vstupy += 1
        if prazdne_vstupy >= 3:
            return "Hej, jsi tam ještě? Napiš něco, ať pokračujeme!"
        return "Prosím, polož mi otázku nebo mi něco řekni!"

    prazdne_vstupy = 0
    logging.debug(f"Zpráva po odstranění diakritiky: {zprava}")

    pozdravy = ["ahoj", "cau", "cus", "nazdar", "zdravim", "dobry den", "dobry vecer", "cauky", "caves", "servus"]
    if any(pozdrav in zprava for pozdrav in pozdravy):
        return random.choice(odpovedi_ahoj)

    elif any(varianta in zprava for varianta in ["jak se mas", "jak jsi", "jak jde", "jak se vede"]):
        return random.choice(odpovedi_jak_se_mas)

    elif re.search(r"jmenuji\s+se\s+(\w+)", zprava):
        jmeno = re.search(r"jmenuji\s+se\s+(\w+)", zprava).group(1)
        uzivatelske_info['jmeno'] = jmeno
        return f"Rád tě poznávám, {jmeno}!"

    elif re.search(r"mam\s+rad\s+(.+)", zprava):
        preference = re.search(r"mam\s+rad\s+(.+)", zprava).group(1)
        uzivatelske_info['preference'] = preference
        return f"Skvělé, že máš rád {preference}! To je zajímavé."

    elif any(emoce in zprava for emoce in ["jsem smutny", "jsem smutna", "jsem spatne", "je mi blbe"]):
        return random.choice(odpovedi_emoce)

    elif any(otazka in zprava for otazka in ["kolik je hodin", "jaky je cas"]):
        aktualni_cas = datetime.now().strftime("%H:%M")
        return f"Je {aktualni_cas}. Co těď plánuješ?"

    elif len(zprava.split()) >= 2:
        return "To zní zajímavě! Můžeš mi o tom říct více?"

    if 'jmeno' in uzivatelske_info:
        return f"{uzivatelske_info['jmeno']}, co plánuješ dnes?"
    return "Promiň, tomu nerozumím. Můžeš to prosím říct jinak nebo to více objasnit?"
