import sqlite3
import random
conn = sqlite3.connect(
    "C:\\Users\\hovor\\Desktop\\kody\\Investicni_appka\\databaze.db")
c = conn.cursor()

# Tato funkce ověřuje, zda se jméno zadané uživatelem náhodou již nenachází v databázi. Pokud se v ní nachází, funkce vrátí False.


def overeni_jmena(jmeno):
    conn = sqlite3.connect(
        "C:\\Users\\hovor\\Desktop\\kody\\Investicni_appka\\databaze.db")
    c = conn.cursor()

    # Pokud se jméno v databázi již nachází, funkce vrátí false, a uživateli se vypíše chybová hláška.
    if c.execute('SELECT EXISTS(SELECT * FROM uzivatele WHERE login_uzivatele =?)', (jmeno,)).fetchone() == (1,):
        conn.commit()
        conn.close()
        return False

# Tato funkce zajišťuje registraci, a zapsání přihlašovacích údajů nového uživatele do systému.


def registrace(jmeno, heslo):
    conn = sqlite3.connect(
        "C:\\Users\\hovor\\Desktop\\kody\\Investicni_appka\\databaze.db")
    c = conn.cursor()

    # Vloží hodnoty zadané uživatelem do tablu uzivatele.
    c.execute("INSERT INTO uzivatele VALUES(?,?,?)", (jmeno, heslo, 100))
    # Přiřadí defaultní/prázdné hodnoty ze všech fondů do portfolia uživatele.
    for i in c.execute("SELECT nazev_fondu FROM fondy").fetchall():
        c.execute("INSERT INTO portfolio VALUES(?,?,?,?,?)",
                  (jmeno, i[0], 0, 0, 0))
        conn.commit()
    conn.commit()
    conn.close()

# Tato funkce ověří, zda-li jsou zadané údaje v databázi, a zda jméno, a heslo souhlasí.


def login(jmeno, heslo):
    conn = sqlite3.connect(
        "C:\\Users\\hovor\\Desktop\\kody\\Investicni_appka\\databaze.db")
    c = conn.cursor()

    # Funkce SELECT EXISTS zjistí, jestli vybraná věc existuje, a funkce .fetchone() vrátí výsledek funkce SELECT EXISTS(vrátí (1,) pokud vybraná věc existuje , a (0,) pokud ne.
    if c.execute('SELECT EXISTS(SELECT * FROM uzivatele WHERE heslo_uzivatele =? AND login_uzivatele =?)', (heslo, jmeno)).fetchone() == (1,):
        conn.commit()
        conn.close()
        return True
    else:
        conn.commit()
        conn.close()
        return False

# Funkce pro výpis portfolia.


def vypis_portfolia(jmeno):
    conn = sqlite3.connect(
        "C:\\Users\\hovor\\Desktop\\kody\\Investicni_appka\\databaze.db")
    c = conn.cursor()

    # Stav_uctu vypíše stav finančních prostředků uživatele z table uzivatele, defaultní stav účtu je 100 Kč.
    stav_uctu = c.execute(
        "SELECT stav_uctu FROM uzivatele WHERE login_uzivatele = ?", (jmeno,)).fetchone()[0]
    print("\nStav vašich finančích prostředku: ", round(stav_uctu, 4), "Kč")
    # Pokud je jméno v table portfolio AND celkové množství akcií je větší než 0, vypíše portfolio přiřazené ke jménu uživatele.
    # Pokud uživatel nevlastní žádné akcie, vypíše hlášku Portfolio je přázdné.
    if c.execute("SELECT EXISTS(SELECT * FROM portfolio WHERE majitel_portfolia = ? AND mnozstvi_akcii > 0)", (jmeno,)).fetchall()[0] == (1,):
        # Smyčka postupně vypíše všechny fondy ve kterých má uživatel alespoň 1 akcii.
        for i in c.execute('SELECT * FROM portfolio WHERE majitel_portfolia = ? AND mnozstvi_akcii > 0', (jmeno,)).fetchall():
            print("Název Fondu: ", i[1])
            print("Množství akcií: ", i[2])
            print("Průměrná cena nákupu: ", round(i[3], 4))
            print("Aktuální cena za akcii: ", c.execute(
                "SELECT aktualni_hodnota FROM fondy WHERE nazev_fondu = ?", (i[1],)).fetchall()[0][0])
            zisk_ztrata = (i[2] * c.execute('SELECT aktualni_hodnota FROM fondy WHERE nazev_fondu = ?',
                           (i[1],)).fetchall()[0][0]) - (i[2] * i[3])
            if zisk_ztrata > 0:
                print("Zisk: ", round(zisk_ztrata, 4), "Kč\n")
            elif zisk_ztrata < 0:
                print("Ztráta: ", round(zisk_ztrata, 4), "Kč\n")
            else:
                print("Zisk/ztráta: ", zisk_ztrata, "Kč\n")

    else:
        print("V tuto chvíli je vaše portfolio prázdné.")

# Funkce pro nákup akcií.


def nakup_akcii(jmeno):
    conn = sqlite3.connect(
        "C:\\Users\\hovor\\Desktop\\kody\\Investicni_appka\\databaze.db")
    c = conn.cursor()

    # Tato proměnná, a list zaznamenává počet cyklů pro kontrolu, zda-li user nezadal číslo fondu který se v seznamu nenachází.
    pocet_cyklu = 0
    pocet_cyklu_list = []
    # Smyčka která vypíše všechny fondy, a aktualizuje aktuální hodnotu akcie na náhodnou částku.
    for i in c.execute("SELECT rowid, * FROM fondy").fetchall():
        # Přičte číslo 1 k proměné pocet_cyklu při každém cyklu smyčky for. Číslo se následně přiřadí do listu jako string, protože rowid se udává ve stringu, a díky tomu můžeme vyhodit
        # pomocí if chybovou hlášku, když user zadá cokoliv jiného než číslo fondu, který se nachází v listu.
        pocet_cyklu += 1
        pocet_cyklu_list.append(str(pocet_cyklu))
        # Vypíše název fondu
        nazev_fondu = i[1]
        print("\nČíslo fondu: ", i[0])
        print(nazev_fondu)
        # Vytvoří náhodné číslo v rozmezí min/max ceny určené v table fondy u jednotlivých fondů.
        hodnota = round(random.uniform(i[2], i[3]), 4)
        print("Předchozí cena fondu: ", i[5])
        print("Aktuální cena fondu je: ", hodnota, "Kč")
        # Tato proměnná nese hodnotu průmerné ceny nákupu akcie uživatele ve fondu který je zrovna vypisován.
        prumerna_cena_v_ptf = c.execute(
            "SELECT prumerna_cena_nakupu FROM portfolio WHERE majitel_portfolia = ? AND nazev_fondu = ?", (jmeno, nazev_fondu)).fetchall()[0][0]
        # Proměnná na výpis stavu účtu
        stav_uctu = c.execute(
            "SELECT stav_uctu FROM uzivatele WHERE login_uzivatele = ?", (jmeno,)).fetchone()[0]
        # Zde pomocí if určujeme zda cena od minulé změny vzrostla, klesla, a nebo zůstala stejná.
        if hodnota > i[5]:
            rozdil = hodnota - i[5]
            print("Cena vzrostla o", round(rozdil, 3), "Kč za akcii.")
        elif hodnota < i[5]:
            rozdil = i[5] - hodnota
            print("Cena klesla o", round(rozdil, 3), "Kč za akcii.")
        elif hodnota == i[5]:
            print("Cena se nezměnila.")
        # Výpis kolik akcií si uživatel může s aktuálním zůstatkem pořídit.
        print("S vaším aktuálním zůstatkem na účtu si můžete koupit",
              round((stav_uctu / hodnota), 4), "ks akcií tohoto fondu.")
        # Zde pomocí if zjistíme, zda má uživatel nějaké akcie z fondu který je aktuálně vypisován. Pokud ano, vypíše se zda je aktuální cena lepší/horší než jeho průměrná nákupní cena.
        if c.execute("SELECT mnozstvi_akcii FROM portfolio WHERE majitel_portfolia = ? AND nazev_fondu = ?", (jmeno, nazev_fondu)).fetchall()[0][0] > 0:
            if (prumerna_cena_v_ptf - hodnota) > 0:
                print("Aktuální cena za akcii je nižší o ", round((prumerna_cena_v_ptf - hodnota),
                      4), "Kč za kus, než je vaše průměrná nákupní cena akcie tohoto fondu.")
            elif (prumerna_cena_v_ptf - hodnota) < 0:
                print("Aktuální cena za akcii je vyšší o ", round((hodnota - prumerna_cena_v_ptf),
                      4), "Kč za kus, než je vaše průměrná nákupní cena akcie tohoto fondu.")
            else:
                print(
                    "Aktuální cena za kus této akcie je stejná jako vaše průměrná nákupní cena v tomto fondu.")

        # Zde aktualizujeme aktuální cenu jednotlivých fondů, a zároveň uložíme aktuální hodnotu jako předchozí, pro porovnání v dalším výpisu.
        c.execute('UPDATE fondy SET aktualni_hodnota = ?,posledni_hodnota = ? WHERE nazev_fondu = ?',
                  (hodnota, hodnota, nazev_fondu))
        conn.commit()

    # Zde uživatel určuje parametry pro provedení nákupu.
    print("\nStav vašich finančích prostředku: ", round(stav_uctu, 4), "Kč")
    if input("Chcete provést nákup akcii?(a/n)") == "a":
        # Proměnná fond určuje rowid fondu, do kterého chceme investovat.
        fond = input("Vlož číslo fondu do kterého chceš investovat: ")
        # Pokud uživatel zadá cokoliv co se nenachází v listu pocet_cyklu_list, vyhodí chybovou hlášku, a user se vrátí do menu.
        if (fond not in pocet_cyklu_list) == False:
            # Proměnná množství určuje množství akcií které chceme zakoupit.
            mnozstvi = float(
                input("Zadej množství akcii které chceš koupit: "))
            # Tato proměnná nese název fondu do kterého chceme investovat. Slouží pro lepší přehled v kódu.
            nazev_kupovaneho_fondu = c.execute(
                "SELECT * FROM fondy WHERE rowid = ?", (fond,)).fetchall()[0][0]
            # Tato proměnná nese aktuální cenu za 1 akcii fondu do kterého chceme investovat. Slouží pro lepší přehled v kódu.
            akt_cena_kup_akc = c.execute(
                "SELECT aktualni_hodnota FROM fondy WHERE nazev_fondu = ?", (nazev_kupovaneho_fondu,)).fetchall()[0][0]
            # Zde pomocí if zkontrolujeme, zda-li není hodnota nákupu větší než množství peněz na účtu.
            if (akt_cena_kup_akc * mnozstvi) < stav_uctu:
                # Zde odečteme z účtu peníze v hodnotě celkové transakce.
                stav_uctu -= (c.execute("SELECT * FROM fondy WHERE rowid = ?",
                              (fond,)).fetchall()[0][3] * mnozstvi)
                # Tato proměnná nese hodnotu celkové transakce nákupu. Slouží pro lepší přehled v kódu.
                celkova_cena = c.execute(
                    "SELECT * FROM fondy WHERE rowid = ?", (fond,)).fetchall()[0][3] * mnozstvi
                # Tato proměnná v sobě nese list s tuplem všech údajů z portfolia. Slouží pro lepší přehled v kódu.
                vypis_portfolio = c.execute(
                    "SELECT * FROM portfolio WHERE majitel_portfolia =? AND nazev_fondu =?", (jmeno, nazev_kupovaneho_fondu)).fetchall()
                # Tato proměnná slouží pro lepší přehled v kódu. Nese aktuální množství akcií + počet akcií nakoupených v této transakci, a slouží k aktualizaci parametru množství v table portfolio.
                mnozstvi_nakup = mnozstvi + vypis_portfolio[0][2]
                # Tato proměnná slouží pro lepší přehled v kódu. Slouží k aktualizaci parametru průměrná cena nákupu v table portfolio.
                prumerna_cena = (
                    (vypis_portfolio[0][3] * vypis_portfolio[0][2])+celkova_cena) / (vypis_portfolio[0][2]+mnozstvi)
                # Zde aktualizujeme účetní zůstatek uživatele po provedení této transakce.
                c.execute(
                    'UPDATE uzivatele SET stav_uctu = ? WHERE login_uzivatele = ?', (stav_uctu, jmeno))
                # Zde ukládáme transakci do historie transakcí.
                c.execute("INSERT INTO nakupy VALUES(?,?,?,?)",
                          (nazev_kupovaneho_fondu, jmeno, celkova_cena, mnozstvi))
                # Zde aktualizujeme hodnoty v table portfolio po provedeném nákupu.
                c.execute('UPDATE portfolio SET mnozstvi_akcii = ?, prumerna_cena_nakupu = ? WHERE majitel_portfolia = ? AND nazev_fondu = ?',
                          (mnozstvi_nakup, prumerna_cena, jmeno, nazev_kupovaneho_fondu))
                # Výpis potvrzení transakce, a její detaily.
                print(
                    f"Potvrzujeme vaši koupi {mnozstvi}ks cenných papírů fondu {nazev_kupovaneho_fondu}, ve výši {akt_cena_kup_akc}Kč za kus, v celkové hodnotě {round(celkova_cena,4)}Kč.")
            else:
                print("Na tuto transakci nemáte dostatečné finanční prostředky.")
        else:
            print("Fond číslo", fond, "neexistuje.")
        conn.commit()
    conn.commit()
    conn.close()

# Funkce pro prodej akcií.


def prodej_akcii(jmeno):
    conn = sqlite3.connect(
        "C:\\Users\\hovor\\Desktop\\kody\\Investicni_appka\\databaze.db")
    c = conn.cursor()

    # Zde pomocí if ověřujeme, zda-li už uživatel vlastní akcie v nějakém fondu. Pokud ne, vypíšeme hlášku prázdné portfolio.
    if c.execute("SELECT EXISTS(SELECT * FROM portfolio WHERE majitel_portfolia = ? AND mnozstvi_akcii > 0)", (jmeno,)).fetchall()[0] == (1,):
        # Proměnná prazdne zabrání funkci aby pokračovala k prodeji akcií, pokud má uživatel prázdné portfolio(prazdne = 1).
        prazdne = 0
        # Proměnná stav účtu uživatele
        stav_uctu = c.execute(
            "SELECT stav_uctu FROM uzivatele WHERE login_uzivatele = ?", (jmeno,)).fetchone()[0]
        # Proměnné pocitadlo, a fond_list slouží k řazení fondů od čísla 1, a následnému výběru požadovaného fondu uživatelem.
        pocitadlo = 0
        fond_list = []
        # Smyčka for projíždí fondy v portfoliu uživatele, a přiřazuje jejich jména do listu.
        # Počítadlo pak zaznamenává jejich pořadí v listu, a díky tomu uživateli stačí pro výběr fondu pro prodej napsat jen číslo fondu.
        # Smyčka vypíše všechny fondy kde má uživatel alespoň 1 akcii.
        for i in c.execute('SELECT * FROM portfolio WHERE majitel_portfolia = ? AND mnozstvi_akcii > 0', (jmeno,)).fetchall():
            # Přiřazení jména do listu fond_list.
            fond_list.append(i[1])
            # Při každém cyklu se k proměnné pocitadlo přičte 1.
            pocitadlo += 1
            print("Číslo fondu: ", pocitadlo)
            print("Název Fondu: ", i[1])
            print("Množství akcií: ", i[2])
            print("Průměrná cena nákupu: ", round(i[3], 4))
            print("Aktuální cena za akcii: ", c.execute(
                "SELECT aktualni_hodnota FROM fondy WHERE nazev_fondu = ?", (i[1],)).fetchall()[0][0])
            zisk_ztrata = (i[2] * c.execute('SELECT aktualni_hodnota FROM fondy WHERE nazev_fondu = ?',
                           (i[1],)).fetchall()[0][0]) - (i[2] * i[3])
            if zisk_ztrata > 0:
                print("Zisk: ", round(zisk_ztrata, 4), "Kč\n")
            elif zisk_ztrata < 0:
                print("Ztráta: ", round(zisk_ztrata, 4), "Kč\n")
            else:
                print("Zisk/ztráta: ", zisk_ztrata, "Kč\n")
    else:
        print("V tuto chvíli je vaše portfolio prázdné.")
        # prazdne = 1, funkce se ukončí.
        prazdne = 1
        return

    # prazdne = 0, uživatel vlastní nějaké akcie, a může uskutečnit prodej.
    if prazdne == 0:
        # V této proměnné uživatel zadá číslo fondu od kterého chce odprodat akcie.
        fond = int(input("Vlož číslo fondu kterého akcie chceš odprodat: "))
        if (fond-1) < pocitadlo:
            # V této proměnné uživatel určí počet akcií které chce odprodat.
            mnozstvi = float(
                input("Zadej množství akcii které chceš odprodat: "))
            # V této proměnné se určí název fondu (fond - 1, protože pořadí listu začíná od nuly.)
            nazev_prodavaneho_fondu = fond_list[fond-1]
            # Tato proměnná nese hodnotu aktuální kupní ceny akcie.
            akt_cena_kup_akc = c.execute(
                "SELECT aktualni_hodnota FROM fondy WHERE nazev_fondu = ?", (nazev_prodavaneho_fondu,)).fetchall()[0][0]
            # Tato proměnná v sobě nese list s tuplem všech údajů z portfolia. Slouží pro lepší přehled v kódu.
            vypis_portfolia = c.execute(
                'SELECT * FROM portfolio WHERE majitel_portfolia = ? AND nazev_fondu = ?', (jmeno, nazev_prodavaneho_fondu)).fetchall()
            # Pomocí if zjistíme, zda-li požadované množství akcií na prodej není větší než množství akcií které uživatel vlastní.
            if c.execute('SELECT * FROM portfolio WHERE majitel_portfolia = ? AND nazev_fondu = ?', (jmeno, nazev_prodavaneho_fondu)).fetchall()[0][2] >= mnozstvi:
                # Zde se peníze za prodej přičtou na účet uživatele.
                stav_uctu += (mnozstvi * akt_cena_kup_akc)
                # Aktualizace stavu účtu uživatele.
                c.execute(
                    'UPDATE uzivatele SET stav_uctu = ? WHERE login_uzivatele = ?', (stav_uctu, jmeno))
                # Aktualizace hodnot parametrů v portfoliu uživatele
                c.execute('UPDATE portfolio SET mnozstvi_akcii = ? WHERE majitel_portfolia = ? AND nazev_fondu = ?', ((
                    vypis_portfolia[0][2] - mnozstvi), jmeno, nazev_prodavaneho_fondu))
                # Uložení transakce do historie transakcí.
                c.execute("INSERT INTO prodeje VALUES(?,?,?,?)",
                          (nazev_prodavaneho_fondu, jmeno, akt_cena_kup_akc, mnozstvi))
                # Vynulování průměrné ceny nákupu v portfoliu uživatele pokud je množství akcii v konrkétním fondu 0.
                if (vypis_portfolia[0][2] - mnozstvi) == 0:
                    c.execute('UPDATE portfolio SET prumerna_cena_nakupu = ? WHERE majitel_portfolia = ? AND nazev_fondu = ?', (
                        0, jmeno, nazev_prodavaneho_fondu))
                    conn.commit()
                conn.commit()
                # Potvrzení transakce výpisem uživateli.
                print(
                    f"Prodal jste {round(mnozstvi,3)}ks akcií fondu {nazev_prodavaneho_fondu} za {round(mnozstvi * akt_cena_kup_akc,3)}Kč.")
                conn.close()
            else:
                print(
                    "Zadal jste k prodeji větší množství akcií než vlastníte. Operace byla zrušena.")
        else:
            print("Fond číslo", fond, "neexistuje.")

# Funkce zaznamenávající transakce


def historie_transakci(jmeno):
    conn = sqlite3.connect(
        "C:\\Users\\hovor\\Desktop\\kody\\Investicni_appka\\databaze.db")
    c = conn.cursor()

    # Proměnná pro řazení transakcí nákupu od čísla 1
    cislo_transakce_nakup = 0
    # Pokud se v table nákupy nachází nějaké transakce, vypiš je za pomocí loopy for, jinak vypiš Žádné nákupní transakce.
    if c.execute('SELECT EXISTS(SELECT * FROM nakupy WHERE kupec =?)', (jmeno,)).fetchone() == (1,):
        print("\nToto je seznam všech vašich nákupních transakcí: ")
        for i in c.execute('SELECT rowid,* FROM nakupy WHERE kupec =?', (jmeno,)).fetchall():
            cislo_transakce_nakup += 1
            print(
                f"{cislo_transakce_nakup}. Nakoupil jste {round(i[4],3)}ks akcií fondu {i[1]}. Cena 1ks akcie byla {round(i[3],3)}Kč. Celková cena transakce byla {round(i[4]*i[3],3)}Kč.")
        else:
            print("Zatím jste neprovedl žádné nákupní transakce.\n")
    # Proměnná pro řazení transakcí prodeje od čísla 1
    cislo_transakce_prodej = 0
    # Pokud se v table prodeje nachází nějaké transakce, vypiš je za pomocí loopy for, jinak vypiš Žádné prodejní transakce.
    if c.execute('SELECT EXISTS(SELECT * FROM prodeje WHERE prodejce =?)', (jmeno,)).fetchone() == (1,):
        print("\nToto je seznam všech vašich prodejních transakcí: ")
        for i in c.execute('SELECT rowid,* FROM prodeje WHERE prodejce =?', (jmeno,)).fetchall():
            cislo_transakce_prodej += 1
            print(
                f"{cislo_transakce_prodej}. Prodal jste {round(i[4],3)}ks akcií fondu {i[1]}. Cena 1ks akcie byla {round(i[3],3)}Kč. Celková cena transakce byla {round(i[4]*i[3],3)}Kč.")
    else:
        print("Zatím jste neprovedl žádné prodejní transakce.\n")
    conn.commit()
    conn.close()


conn.commit()
conn.close()
