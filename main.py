import databaze
# SEKVENCE LOGIN/REGISTRACE
print("""Vítejte v investničním dotazníku MaJa.
Pro registraci nového účtu, napište 1
Pro přihlášení k existujícímu účtu stisněte Enter.
""")
# Uživatel si zvolí zda-li se chce zaregistrovat, nebo přihlásit.
# Pokud se chce zaregistrovat, zadá jméno, a heslo. Ve funkci databaze.overeni_jmena proběhne ověření, zda-li se zadané jméno již nenachází v databázi.
# Pokud oveření proběhne bez problému. Data se zapíšou do databáze pomocí funkce databaze.registrace, a uživatel se s nimi může přihlásit.
while True:
    while True:
        # Proměnná pokracovat slouží pro ukončení celé smyčky, ve které běží sekvence Login/registrace. Hodnota True je jen placeholder.
        # Smyčka se ukončí až níže pomocí funkce if, pokud pokracovat = False.
        pokracovat = True
        if input("Zvolte 1 pro registraci, a nebo zmačkněte Enter pro přihlášení: ") == "1":
            while True:
                registrace_jmeno = input(
                    "Zadejte jméno kterým se budete přihlašovat. Jméno nerozlišuje velká/malá písmena: ")
                # Pokud jméno již je v databázi, vypíše se hláška, a nabídka s možnostmi.
                if databaze.overeni_jmena(registrace_jmeno.lower()) == False:
                    print(
                        "Zadané jméno již existuje. Chcete si zvolit jiné nebo pokračovat na login?")
                    if input("Zadejte 1 pro vyzkoušení jiného jména nebo 2 pro pokračování na login.") == "2":
                        break
                else:
                    # Pokud se jméno v databázi nenachází, pomocí funkce databaze.registrace se zadané údaje vloží do databáze.
                    registrace_heslo = input(
                        "Zadejte heslo pod kterým se budete přihlašovat: ")
                    databaze.registrace(
                        registrace_jmeno.lower(), registrace_heslo)
                    print(
                        "Gratulujeme, nyní jste zaregistrováni v našem dotazníku. Pro pokračování se přihlašte vámi zadanými údaji.")
                    break

        # Následně zadá své jméno, a heslo, a přihlásí se do systému. Funkce .login prověří, zda se zadané údaje nacházejí v databázi, a zda jméno, a heslo souhlasí.
        while True:
            login_jmeno = input("Zadejte vaše přihlašovací jméno: ")
            login_heslo = input("Zadejte vaše heslo: ")
            # Pokud se jméno neshoduje s heslem, nebo zadané údaje nejsou v databázi, vypíše se chybová hláška, a nabídka s možnostmi.
            if databaze.login(login_jmeno.lower(), login_heslo) == False:
                print("Zadal jste špatné jméno nebo heslo.")
                if input("Zadejte 1 pokud to chcete zkusit znovu nebo 2 pro navrácení k registraci: ") == "2":
                    break
            else:
                # Při úspěšném zadání údajů se ukončí smyčka while ve které běží login.
                print("Vítejte", login_jmeno.lower(), ".")
                # Do proměnné pokracovat se uloží hodnota False
                pokracovat = False
                break
        # Protože proměnná pokracovat je False, ukončí se celá smyčka while, ve které běží sekvence login/registrace.
        break
    # Tato podmínka zajišťuje, že program neskončí hned po přihlášení.
    if pokracovat == False:
        while True:
            print("""Operace:
    1. Zobrazit vaše portfolio.
    2. Nákup cenných papírů.
    3. Prodej vašich cenných papírů
    4. Historie transakcí
    5. Vrátit se k loginu/registraci
    6. Ukončí program
            """)
            operace = input("Zadejte číslo operace kterou chcete provést: ")
            if operace == "1":
                databaze.vypis_portfolia(login_jmeno.lower())
            elif operace == "2":
                databaze.nakup_akcii(login_jmeno.lower())
            elif operace == "3":
                databaze.prodej_akcii(login_jmeno.lower())
            elif operace == "4":
                databaze.historie_transakci(login_jmeno.lower())
            elif operace == "5":
                break
            elif operace == "6":
                break
            else:
                print("Tato možnost se v seznamu nenachází.\n")
        if operace == "6":
            print("Na viděnou příště.")
            break
