from pymongo import MongoClient

# Connection String
finn = "mongodb://localhost:27017"

#Neuen Client erstellen
client = MongoClient(finn)

#Definieren der Datenbase die benutzt wird
db = client.Spiele

#Definieren der Collection die benutzt wird
collection = db.pcgames

# Ausgeben der Daten eines Spiels
def print_game_details(game):
    print("\nSpiel Details:")
    print(f"Titel: {game['Titel']}")
    print(f"Erscheinungsjahr: {game['Erscheinungsjahr']}")
    print(f"Anzahl Downloads: {game['AnzahlDownloads']}")
    print(f"Altersgrenze: {game['Altersgrenze']}")
    print(f"Art(en): {', '.join(game['Art'])}")
    print(f"Wertung: {game['Wertung']}")

# Einfügen eines neuen Spiels
def insert_game():
    # Abfragen der Daten für das Spiel
    titel = input("Geben Sie den Titel des Spiels ein: ")
    try:
        jahr = int(input("Geben Sie das Erscheinungsjahr des Spiels ein: "))
        if jahr < 0:
            print("Fehler: Das Erscheinungsjahr kann nicht kleiner als 0 sein.")
            return
        downloads = int(input("Geben Sie die Anzahl der Downloads ein: "))
        if downloads < 0:
            print("Fehler: Die Anzahl Downloads kann nicht kleiner als 0 sein")
            return
        altersgrenze = int(input("Geben Sie die Altersgrenze des Spiels ein: "))
        wertung = float(input("Geben Sie die Bewertung des Spiels ein (0-10): "))
        if wertung < 0 or wertung > 10:
            print("Fehler: Die Bewertung muss im Bereich von 0 bis 10 liegen.")
            return
        art = input("Geben Sie die Art(en) des Spiels (kommagetrennt) ein: ").split(',')
    except ValueError:
        print("Fehler: Ungültiger Datentyp. Stellen Sie sicher, dass Sie eine ganze Zahl für Jahr, Downloads und Altersgrenze eingeben und eine Dezimalzahl für die Bewertung (0-10).")
        return
    
    # Einfügen in die Database
    new_game = {
        "Titel": titel,
        "Erscheinungsjahr": jahr,
        "AnzahlDownloads": downloads,
        "Altersgrenze": altersgrenze,
        "Art": art,
        "Wertung": wertung
    }
    collection.insert_one(new_game)
    print(f"{titel} wurde zur Sammlung hinzugefügt.")

# Aktualisieren eines Spiels
def update_game():
    # Auswählen eines Spiels
    titel = input("Geben Sie den Titel des zu aktualisierenden Spiels ein: ")
    game = collection.find_one({"Titel": titel})
    if game:
        print_game_details(game)
        print("\nLassen Sie Felder leer, die Sie nicht aktualisieren möchten.")

        # Eingeben der Daten die man aktualisieren will
        wertung = input("Geben Sie die neue Bewertung für das Spiel ein: ")
        downloads = input("Geben Sie die neue Anzahl Downloads für das Spiel ein: ")
        altersgrenze = input("Geben Sie die neue Altersgrenze für das Spiel ein: ")
        art = input("Geben Sie die neue Art(en) des Spiels (kommagetrennt) ein: ")

        try:
            new_rating = None if wertung == "" else float(wertung)
            new_downloads = None if downloads == "" else int(downloads)
            new_altersgrenze = None if altersgrenze == "" else int(altersgrenze)
        except ValueError:
            print("Fehler: Ungültiger Datentyp. Stellen Sie sicher, dass Sie eine ganze Zahl für Downloads und Altersgrenze und eine Dezimalzahl für die Bewertung (0-10) eingeben.")
            return

        new_art = art.split(',') if art else game['Art']

        # Aufrufen von updategame mit den richtigen Argumenten
        updategame(titel, new_rating, new_downloads, new_altersgrenze, new_art, game)

    else:
        print(f"{titel} wurde nicht gefunden.")

# Basis für die update_game Funktion
def updategame(game_title, new_rating, new_downloads=None, new_altersgrenze=None, new_art=None, game=None):
    if game is None:
        game = collection.find_one({"Titel": game_title})
        if game is None:
            print(f"{game_title} wurde nicht gefunden.")
            return

    # Aktualisieren der Daten mit den zuvor eingegebenen Daten
    filter_criteria = {"Titel": game_title}
    update_data = {"$set": {}}

    if new_rating is not None:
        update_data["$set"]["Wertung"] = new_rating

    if new_downloads is not None:
        update_data["$set"]["AnzahlDownloads"] = new_downloads

    if new_altersgrenze is not None:
        update_data["$set"]["Altersgrenze"] = new_altersgrenze

    if new_art is not None:
        update_data["$set"]["Art"] = new_art

    result = collection.update_one(filter_criteria, update_data)
    if result.modified_count > 0:
        print(f"{result.modified_count} Dokument(e) aktualisiert.")
    else:
        print(f"{game_title} wurde nicht gefunden.")

# Löschen eines Spiels
def delete_game():
    titel = input("Geben Sie den Titel des zu löschenden Spiels ein:")
    # Löschen des Spiels nach Titel
    filter_criteria = {"Titel": titel}
    result = collection.delete_one(filter_criteria)

    if result.deleted_count > 0:
        print(f"{result.deleted_count} Dokument(e) gelöscht.")
    else:
        print(f"{titel} wurde nicht gefunden.")

# Anzeigen eines Spiels
def show_game():
    titel = input("Geben Sie den Titel des Spiels ein, dessen Details Sie anzeigen möchten: ")
    game = collection.find_one({"Titel": titel})
    if game:
        # Aufrufen von print_game_details
        print_game_details(game)
    else:
        print(f"{titel} wurde nicht gefunden.")

# Suchen eines Spiels anhand von Kriterien
def search_game():
    print("Geben Sie die Suchkriterien ein:")
    search_criteria = {}
    # Hier eingegebene Daten werden zu search_criteria hinzugefügt
    titel = input("Titel (Leer lassen, um zu überspringen): ")
    if titel:
        search_criteria["Titel"] = titel

    jahr = input("Erscheinungsjahr (Leer lassen, um zu überspringen): ")
    if jahr:
        try:
            search_criteria["Erscheinungsjahr"] = int(jahr)
        except ValueError:
            print("Fehler: Ungültiger Datentyp. Das Erscheinungsjahr muss eine ganze Zahl sein.")
            return

    downloads = input("Anzahl Downloads (Leer lassen, um zu überspringen): ")
    if downloads:
        try:
            search_criteria["AnzahlDownloads"] = int(downloads)
        except ValueError:
            print("Fehler: Ungültiger Datentyp. Die Anzahl der Downloads muss eine ganze Zahl sein.")
            return

    altersgrenze = input("Altersgrenze (Leer lassen, um zu überspringen): ")
    if altersgrenze:
        try:
            search_criteria["Altersgrenze"] = int(altersgrenze)
        except ValueError:
            print("Fehler: Ungültiger Datentyp. Die Altersgrenze muss eine ganze Zahl sein.")
            return

    art = input("Art(en) (kommagetrennt, Leer lassen, um zu überspringen): ")
    if art:
        search_criteria["Art"] = {"$in": art.split(',')}

    wertung = input("Wertung (0-10, Leer lassen, um zu überspringen): ")
    if wertung:
        try:
            wertung_float = float(wertung)
            if 0 <= wertung_float <= 10:
                search_criteria["Wertung"] = wertung_float
            else:
                print("Fehler: Ungültiger Wertungsbereich. Die Wertung muss im Bereich von 0 bis 10 liegen.")
                return
        except ValueError:
            print("Fehler: Ungültiger Datentyp. Die Wertung muss eine Dezimalzahl sein.")
            return
    # Suchen in der Datenbank mit searcg_criteria
    games = collection.find(search_criteria)
    games_list = list(games)
    if len(games_list) > 0:
        print("\nGefundene Spiele:")
        for game in games_list:
            print_game_details(game)
    else:
        print("Keine Spiele gefunden")

# Auswahl von verfügbaren Aktionen
while True:
    print("\nVerfügbare Aktionen:")
    print("1. Spiel hinzufügen")
    print("2. Spiel aktualisieren")
    print("3. Spiel löschen")
    print("4. Spiel anzeigen")
    print("5. Spiel suchen")
    print("6. Beenden")

    choice = input("Wählen Sie eine Aktion (1/2/3/4/5/6): ")

    if choice == "1":
        insert_game()

    elif choice == "2":
        update_game()

    elif choice == "3":
        delete_game()

    elif choice == "4":
        show_game()

    elif choice == "5":
        search_game()

    elif choice == "6":
        break

client.close()
print("Client wurde geschlossen.")