
import random
import json
from textblob import TextBlob

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

# Uvítací zpráva
def uvodni_zprava():
    print("Ahoj! Jsem Varathiel, tvůj virtuální přítel. Rád bych tě lépe poznal!")
    print("Můžeš mi kdykoliv říct 'konec', pokud chceš skončit.")

# Seznam odpovědí
odpovedi_ahoj = ["Ahoj! Jak se máš?", "Čau! Co tě dnes trápí?", "Zdravím tě! Jaký máš den?"]
odpovedi_jak_se_mas = ["Mám se skvěle, díky, že se ptáš! A ty?", "Jsem v pohodě, co ty?", "Dnes jsem plný energie! Jak jsi na tom ty?"]

# Odstranění diakritiky
def odstran_diakritiku(zprava):
    diakritika = str.maketrans("áčďéěíňóřšťúůýž", "acdeeinorstuuyz")
    return zprava.translate(diakritika)

# Analýza vstupu
def analyzovat_vstup(zprava):
    blob = TextBlob(zprava)
    sentiment = blob.sentiment
    opraveny_text = str(blob.correct())
    return opraveny_text, sentiment

# Rozpoznání klíčových slov a odpovědí
def odpovedet(zprava):
    zprava, sentiment = analyzovat_vstup(zprava)
    zprava = odstran_diakritiku(zprava.lower())
    
    if not zprava.strip():  # Kontrola prázdného vstupu
        return "Prosím, polož mi otázku nebo mi něco řekni!"
    
    print(f"Zpráva po odstranění diakritiky: '{zprava}'")  # Debugging output

    # Pozdravy
    if any(greeting in zprava for greeting in ["ahoj", "čau", "dobrý den", "dobrý večer", "čus", "zdravím", "nazdar", "zdravim"]):
        print("Ladění: Pozdrav rozpoznán.")  # Debugging output
        return random.choice(odpovedi_ahoj)

    # Jak se máš
    elif any(varianta in zprava for varianta in ["jak se mas", "jak se máš", "jak jsi", "jak jde", "jak se vede"]):
        print("Ladění: Dotaz na stav rozpoznán.")  # Debugging output
        return random.choice(odpovedi_jak_se_mas)

    # Rozpoznávání jména
    elif "jmenuji se" in zprava or "jmenuju se" in zprava:
        jmeno = ""
        if "jmenuji se" in zprava:
            jmeno = zprava.split("jmenuji se")[-1].strip()
        elif "jmenuju se" in zprava:
            jmeno = zprava.split("jmenuju se")[-1].strip()
        uzivatelske_info['jmeno'] = jmeno
        print(f"Ladění: Uživatel jmenující se {jmeno} rozpoznán.")  # Debugging output
        return f"Rád tě poznávám, {jmeno}!"

    # Odpovědi na negativní pocity
    elif any(phrase in zprava for phrase in [
        "nemam se dobre", "nemám se dobře", "mám špatný den",
        "dnes se nemám dobře", "spatny den", "spatne",
        "nemám se moc dobře", "nema se moc dobre", 
        "mam se spatne", "mam spatny den", 
        "necítím se dobře", "je mi špatně", "není mi dobře"
    ]):
        print(f"Ladění: Rozpoznaná negativní fráze: '{zprava}'")  # Debugging output
        return "Je mi to líto, že se nemáš dobře. Chceš o tom mluvit?"

    # Odpověď na otázku o jméně chatbota
    elif "jak se jmenuješ" in zprava or "jak se jmenujes" in zprava:
        return "Jmenuji se Varathiel. A ty?"

    # Odpověď na obecné otázky
    elif len(zprava.split()) >= 2:
        return "To zní zajímavě! Můžeš mi o tom říct více?"

    historie_konverzace.append(f"Ty: {zprava}")

    if 'jmeno' in uzivatelske_info:
        return f"{uzivatelske_info['jmeno']}, co plánuješ dnes?"

    return "Promiň, tomu nerozumím. Můžeš to prosím říct jinak nebo to více objasnit?"

# Načtení předchozích dat
nacti_data()
uvodni_zprava()

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
Vysvětlení úprav:
Ladění: Uložil jsem ladící výstupy, které ukáží, co chatbot rozpozná, když zadáte vstup, což pomůže při diagnostice problému.

Podmínky: Ujistil jsem se, že podmínky pro rozpoznávání jména a negativních pocitů jsou dobře formulovány a pokrývají širokou škálu možných frází.

Testování:
Zkopíruj tenhle kód do souboru chatbot.py.
Ujisti se, že máš soubor requirements.txt s textblob, a instalace knihoven proběhla správně.
Spusť kód pomocí:
python chatbot.py
Poté otestuj různé vstupy, například:

„Ahoj!“
„Jak se jmenuješ?“
„Nemám se dobře.“
„Není mi dobře.“
Omlouvám se za jakékoli dřívější nedorozumění, a pokud se potíže opakují, poděl se o konkrétní fráze, které zadáváš, a jak chatbot reaguje, abychom mohli nalézt řešení!

Ty: ahoj
Varathiel: Promiň, tomu nerozumím. Můžeš to prosím říct jinak nebo to více objasnit?
Ty: Ahoj
Varathiel: Promiň, tomu nerozumím. Můžeš to prosím říct jinak nebo to více objasnit?
Ty: Ahoj!
Varathiel: Promiň, tomu nerozumím. Můžeš to prosím říct jinak nebo to více objasnit?
Ty: Ahoj!
Varathiel: Promiň, tomu nerozumím. Můžeš to prosím říct jinak nebo to více objasnit?
Ty: Jak se jmenujes?
Varathiel: To zní zajímavě! Můžeš mi o tom říct více?
Ty: Nemam se dobre
Varathiel: To zní zajímavě! Můžeš mi o tom říct více?
Ty: Neni mi dobre
Varathiel: To zní zajímavě! Můžeš mi o tom říct více?


Omlouvám se za opakující se problémy s chatbotem. Pojďme se podívat na to, co může být špatně, a důkladně zhodnotit, proč chatbot nereaguje správně na vyjádření "Ahoj" a negativní pocity.

Možné příčiny
Zpracování vstupu: Je možné, že chatbot správně nečte uživatelský vstup. Možná je problém v odstranění diakritiky nebo jiných transformacích textu.

Podmínková logika: Je možné, že logika pro rozpoznání určitých frází není správně nakonfigurována.

Ladění Kódu
Zaměřme se na úpravy, které poskytnou více informací o vstupech a pomohou zjistit, kde může být problém. Přidáme ladicí výstupy a detailnější podmínky.

Celý Kód s Ladicími Výstupy
import random
import json
from textblob import TextBlob

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

# Uvítací zpráva
print("Ahoj! Jsem Varathiel, tvůj virtuální přítel. Rád bych tě lépe poznal!")
print("Můžeš mi kdykoliv říct 'konec', pokud chceš skončit.")

# Seznam odpovědí
odpovedi_ahoj = ["Ahoj! Jak se máš?", "Čau! Co tě dnes trápí?", "Zdravím tě! Jaký máš den?"]
odpovedi_jak_se_mas = ["Mám se skvěle, díky, že se ptáš! A ty?", "Jsem v pohodě, co ty?", "Dnes jsem plný energie! Jak jsi na tom ty?"]

# Odstranění diakritiky
def odstran_diakritiku(zprava):
    diakritika = str.maketrans("áčďéěíňóřšťúůýž", "acdeeinorstuuyz")
    print(f"Odstraněna diakritika z: '{zprava}', výstup: '{zprava.translate(diakritika)}'")  # Debugging output
    return zprava.translate(diakritika)

# Analýza vstupu
def analyzovat_vstup(zprava):
    blob = TextBlob(zprava)
    sentiment = blob.sentiment
    opraveny_text = str(blob.correct())
    return opraveny_text, sentiment

# Rozpoznání klíčových slov a odpovědí
def odpovedet(zprava):
    zprava, sentiment = analyzovat_vstup(zprava)
    zprava = odstran_diakritiku(zprava.lower())

    print(f"Zpráva po odstranění diakritiky: '{zprava}'")  # Debugging output

    if not zprava.strip():  # Kontrola prázdného vstupu
        return "Prosím, polož mi otázku nebo mi něco řekni!"

    # Pozdravy
    if any(greeting in zprava for greeting in ["ahoj", "čau", "dobrý den", "dobrý večer", "čus", "zdravím", "nazdar", "zdravim"]):
        return random.choice(odpovedi_ahoj)

    # Jak se máš
    elif any(varianta in zprava for varianta in ["jak se mas", "jak se máš", "jak jsi", "jak jde", "jak se vede"]):
        return random.choice(odpovedi_jak_se_mas)

    # Rozpoznávání jména
    elif "jmenuji se" in zprava or "jmenuju se" in zprava:
        jmeno = ""
        if "jmenuji se" in zprava:
            jmeno = zprava.split("jmenuji se")[-1].strip()
        elif "jmenuju se" in zprava:
            jmeno = zprava.split("jmenuju se")[-1].strip()
        uzivatelske_info['jmeno'] = jmeno
        return f"Rád tě poznávám, {jmeno}!"

    # Odpovědi na negativní pocity
    elif any(phrase in zprava for phrase in [
        "nemam se dobre", "nemám se dobře", "mám špatný den",
        "dnes se nemám dobře", "spatny den", "spatne",
        "nemám se moc dobře", "nema se moc dobre", 
        "mam se spatne", "mam spatny den", 
        "necítím se dobře", "je mi špatně", "není mi dobře", "nestačí mi to"
    ]):
        print(f"Ladění: Rozpoznaná negativní fráze: '{zprava}'")  # Debugging output
        return "Je mi to líto, že se nemáš dobře. Chceš o tom mluvit?"

    # Odpověď na otázku o jméně chatbota
    elif "jak se jmenuješ" in zprava or "jak se jmenujes" in zprava:
        return "Jmenuji se Varathiel. A ty?"

    # Odpověď na obecné otázky
    elif len(zprava.split()) >= 2:
        return "To zní zajímavě! Můžeš mi o tom říct více?"

    # Uložení konverzace do historie
    historie_konverzace.append(f"Ty: {zprava}")

    if 'jmeno' in uzivatelske_info:
        return f"{uzivatelske_info['jmeno']}, co plánuješ dnes?"

    return "Promiň, tomu nerozumím. Můžeš to prosím říct jinak nebo to více objasnit?"

# Načtení předchozích dat
nacti_data()
uvodni_zprava()

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
