import csv

def carica_da_file(file_path):
    album = {}

    try:
        with open(file_path, 'r', encoding='utf-8') as f1:
            reader = csv.DictReader(f1)

            for riga in reader:
                riga = {chiave.strip(): valore.strip() for chiave, valore in riga.items()}

                anno = int(riga["anno"])

                foto = {
                    "codice": riga["codice"],
                    "titolo": riga["titolo"],
                    "autore": riga["autore"],
                    "mese": int(riga["mese"]),
                    "anno": anno
                }

                if anno not in album:
                    album[anno] = []

                album[anno].append(foto)

        return album

    except FileNotFoundError:
        return None

def aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path):

    if mese < 1 or mese > 12:
        return None

    for anno_album in album:
        for foto in album[anno_album]:
            if foto["codice"] == codice:
                return None

    foto_nuova = {
        "codice": codice,
        "titolo": titolo,
        "autore": autore,
        "mese": mese,
        "anno": anno
    }

    if anno not in album:
        album[anno] = []

    album[anno].append(foto_nuova)

    try:
        with open(file_path, 'a', encoding='utf-8', newline='') as f1:
            writer = csv.writer(f1)
            writer.writerow([codice, titolo, autore, mese, anno])

    except FileNotFoundError:
        album[anno].remove(foto_nuova)

        if len(album[anno]) == 0:
            del album[anno]

        return None

    return foto_nuova


def cerca_foto(album, codice):
    """Cerca una foto nell'album dato il codice"""

    for anno in album:
        for foto in album[anno]:
            if foto["codice"] == codice:
                return f'{foto["codice"]}, {foto["titolo"]}, {foto["autore"]}, {foto["mese"]}, {foto["anno"]}'

    return None


def elenco_foto_anno_per_titolo(album, anno):
    """Ordina i titoli delle foto di un dato anno in ordine alfabetico"""

    if anno not in album:
        return None

    titoli = []

    for foto in album[anno]:
        titoli.append(foto["titolo"])

    titoli.sort()

    return titoli

def main():
    album = []
    file_path = "album_fotografico.csv"

    while True:
        print("\n--- MENU ALBUM FOTOGRAFICO ---")
        print("1. Carica album da file")
        print("2. Aggiungi una nuova foto")
        print("3. Cerca una foto per codice")
        print("4. Elenco foto di un anno (ordinato per titolo)")
        print("5. Esci")

        scelta = input("Scegli un'opzione >> ").strip()

        if scelta == "1":
            while True:
                file_path = input("Inserisci il path del file da caricare: ").strip()
                album = carica_da_file(file_path)
                if album is not None:
                    break

        elif scelta == "2":
            if not album:
                print("Prima carica l'album da file.")
                continue

            codice = input("Codice della foto: ").strip()
            titolo = input("Titolo: ").strip()
            autore = input("Autore: ").strip()
            try:
                mese = int(input("Mese (1-12): ").strip())
                anno = int(input("Anno: ").strip())
            except ValueError:
                print("Errore: inserire valori numerici validi per mese e anno.")
                continue

            foto = aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path)
            if foto:
                print(f"Foto aggiunta con successo!")
            else:
                print("Non è stato possibile aggiungere la foto.")

        elif scelta == "3":
            if not album:
                print("L'album è vuoto.")
                continue

            codice = input("Inserisci il codice della foto da cercare: ").strip()
            risultato = cerca_foto(album, codice)
            if risultato:
                print(f"Foto trovata: {risultato}")
            else:
                print("Foto non trovata.")

        elif scelta == "4":
            if not album:
                print("L'album è vuoto.")
                continue

            try:
                anno = int(input("Inserisci l'anno da consultare: ").strip())
            except ValueError:
                print("Errore: inserire un valore numerico valido.")
                continue

            titoli = elenco_foto_anno_per_titolo(album, anno)
            if titoli is not None:
                print(f'\nFoto del {anno}:')
                print("\n".join([f"- {titolo}" for titolo in titoli]))
            else:
                print(f"Nessuna foto trovata per l'anno {anno}.")

        elif scelta == "5":
            print("Uscita dal programma...")
            break
        else:
            print("Opzione non valida. Riprova.")


if __name__ == "__main__":
    main()
