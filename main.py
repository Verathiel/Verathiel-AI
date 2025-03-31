import random
import json

# Inicializace proměnných
uzivatelske_info = {}
historie_konverzace = []

# Uložení dat
def uloz_data():
    data = {
        'uzivatelske_info': uzivatelske_info,
        'historie_konverzace': historie_konverzace
    }
    with open('data.json', 'w') as f:
        json.dump(data, f)

# Načtení dat
def nacti_data():
    global uzivatelske_info, historie_konverzace
    try:
        with open('data.json', 'r') as f:
            data = json.load(f)
            uzivatelske_info = data.get('uzivatelske_info', {})
            historie_konverzace = data.get('historie_konverzace', [])
    except FileNotFoundError:
        uzivatelske_info = {}
        historie_konverzace = []

# Uvítací zpráva od Varathiela
print("Ahoj! Jsem Varathiel, tvůj virtuální přítel. Rád bych tě lépe poznal!")
print("Můžeš mi kdykoliv říct 'konec', pokud chceš skončit.")

# Seznam odpovědí pro různé situace
odpovedi_ahoj = ["Ahoj! Jak se máš?", "Čau! Co tě dnes trápí?", "Zdravím tě! Jaký máš den?"]
odpovedi_jak_se_mas = ["Mám se skvěle, díky, že se ptáš! A ty?", "Jsem v pohodě, co ty?", "Dnes jsem plný energie! Jak jsi na tom ty?"]

# Funkce pro zjednodušení vstupu bez diakritiky
def odstran_diakritiku(zprava):
    diakritika = str.maketrans("áčďéěíňóřšťúůýž", "acdeeinorstuuyz")
    return zprava.translate(diakritika)

# Funkce pro rozpoznání klíčových slov a odpovědí
def odpovedet(zprava):
    zprava = odstran_diakritiku(zprava.lower())
    if not zprava.strip():  # Kontrola prázdného vstupu
        return "Prosím, polož mi otázku nebo mi něco řekni!"

    print(f"Zpráva po odstranění diakritiky: {zprava}")  # Debug výstup

    # Pozdravy
    if any(greeting in zprava for greeting in ["ahoj", "čau", "dobrý den", "dobrý večer", "čus", "zdravím", "nazdar", "zdravim"]):
        return random.choice(odpovedi_ahoj)

    # Jak se máš
    elif any(varianta in zprava for varianta in ["jak se mas", "jak se máš", "jak jsi", "jak jde", "jak se vede"]):
        return random.choice(odpovedi_jak_se_mas)

    elif "jmenuji se" in zprava:
        jmeno = zprava.split("jmenuji se")[-1].strip()
        uzivatelske_info['jmeno'] = jmeno
        return f"Rád tě poznávám, {jmeno}!"

    elif "mám rád" in zprava:
        preference = zprava.split("mám rád")[-1].strip()
        uzivatelske_info['preference'] = preference
        return f"Skvělé, že máš rád {preference}! To je zajímavé."

    # Přidání reakce na neznámá slova
    elif len(zprava.split()) >= 2:
        return "To zní zajímavě! Můžeš mi o tom říct více?"

    # Přidání historie pro kontext
    historie_konverzace.append(f"Ty: {zprava}")

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

    # Získání odpovědi od Varathiela
    odpoved = odpovedet(uzivatelsky_vstup)

    # Uložení konverzace do historie
    historie_konverzace.append(f"Ty: {uzivatelsky_vstup}")
    historie_konverzace.append(f"Varathiel: {odpoved}")

    # Vypsání odpovědi
    print(f"Varathiel: {odpoved}")
