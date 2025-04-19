import random
import json
import re
import logging
from datetime import datetime

# Nastavení logování
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Inicializace proměnných
uzivatelske_info = {}
historie_konverzace = []
prazdne_vstupy = 0  # Počítadlo prázdných vstupů

# Uložení dat
def uloz_data():
    """Uloží uživatelská data a historii konverzace do JSON souboru."""
    data = {
        'uzivatelske_info': uzivatelske_info,
        'historie_konverzace': historie_konverzace
    }
    try:
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        logging.error(f"Chyba při ukládání dat: {e}")

# Načtení dat
def nacti_data():
    """Načte uživatelská data a historii konverzace z JSON souboru."""
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

# Uvítací zpráva od Varathiela
print("Ahoj! Jsem Varathiel, tvůj virtuální přítel. Rád bych tě lépe poznal!")
print("Můžeš mi kdykoliv říct 'konec', pokud chceš skončit.")

# Seznam odpovědí pro různé situace
odpovedi_ahoj = ["Ahoj! Jak se máš?", "Čau! Co tě dnes trápí?", "Zdravím tě! Jaký máš den?"]
odpovedi_jak_se_mas = ["Mám se skvěle, díky, že se ptáš! A ty?", "Jsem v pohodě, co ty?", "Dnes jsem plný energie! Jak jsi na tom ty?"]
odpovedi_emoce = ["To mě mrzí, co se stalo? Řekni mi víc.", "Hej, to zní těžce. Chceš o tom mluvit?", "Proč jsi smutný? Třeba tě rozveselím!"]

# Funkce pro zjednodušení vstupu bez diakritiky
def odstran_diakritiku(zprava):
    """Odstraní diakritiku z textu pro snadnější zpracování."""
    diakritika = str.maketrans("áčďéěíňóřšťúůýž", "acdeeinorstuuyz")
    return zprava.translate(diakritika)

# Funkce pro rozpoznání klíčových slov a odpovědí
def odpovedet(zprava):
    """Zpracuje uživatelský vstup a vrátí odpověď bota na základě klíčových slov."""
    global prazdne_vstupy
    zprava = odstran_diakritiku(zprava.lower())

    # Kontrola prázdného vstupu
    if not zprava.strip():
        prazdne_vstupy += 1
        if prazdne_vstupy >= 3:
            return "Hej, jsi tam ještě? Napiš něco, ať pokračujeme!"
        return "Prosím, polož mi otázku nebo mi něco řekni!"

    prazdne_vstupy = 0  # Reset počítadla prázdných vstupů
    logging.debug(f"Zpráva po odstranění diakritiky: {zprava}")

    # Pozdravy
    pozdravy = ["ahoj", "cau", "cus", "nazdar", "zdravim", "dobry den", "dobry vecer", "cauky", "caves", "servus"]
    if any(pozdrav in zprava for pozdrav in pozdravy):
        return random.choice(odpovedi_ahoj)

    # Jak se máš
    elif any(varianta in zprava for varianta in ["jak se mas", "jak jsi", "jak jde", "jak se vede"]):
        return random.choice(odpovedi_jak_se_mas)

    # Rozpoznání jména
    elif re.search(r"jmenuji\s+se\s+(\w+)", zprava):
        jmeno = re.search(r"jmenuji\s+se\s+(\w+)", zprava).group(1)
        uzivatelske_info['jmeno'] = jmeno
        return f"Rád tě poznávám, {jmeno}!"

    # Rozpoznání preference
    elif re.search(r"mam\s+rad\s+(.+)", zprava):
        preference = re.search(r"mam\s+rad\s+(.+)", zprava).group(1)
        uzivatelske_info['preference'] = preference
        return f"Skvělé, že máš rád {preference}! To je zajímavé."

    # Reakce na emoce
    elif any(emoce in zprava for emoce in ["jsem smutny", "jsem smutna", "jsem spatne", "je mi blbe"]):
        return random.choice(odpovedi_emoce)

    # Otázka na čas
    elif any(otazka in zprava for otazka in ["kolik je hodin", "jaky je cas"]):
        aktualni_cas = datetime.now().strftime("%H:%M")
        return f"Je {aktualni_cas}. Co teď plánuješ?"

    # Reakce na neznámá slova
    elif len(zprava.split()) >= 2:
        return "To zní zajímavě! Můžeš mi o tom říct více?"

    # Výchozí odpověď s kontextem
    if 'jmeno' in uzivatelske_info:
        return f"{uzivatelske_info['jmeno']}, co plánuješ dnes?"
    return "Promiň, tomu nerozumím. Můžeš to prosím říct jinak nebo to více objasnit?"

# Načtení předchozích dat
nacti_data()

# Hlavní smyčka programu
while True:
    uzivatelsky_vstup = input("Ty: ")

    # Zkontrolování pro ukončení
    if "konec" in uzivatelsky_vstup.lower() or "sbohem" in uzivatelsky_vstup.lower():
        uloz_data()  # Uložení dat při ukončení
        print("Sbohem! Doufám, že se brzy zase uvidíme.")
        break

    # Získání odpovědi od Varathiela a uložení konverzace
    historie_konverzace.append(f"Ty: {uzivatelsky_vstup}")
    odpoved = odpovedet(uzivatelsky_vstup)
    historie_konverzace.append(f"Varathiel: {odpoved}")

    # Vypsání odpovědi
    print(f"Varathiel: {odpoved}")
