import sqlite3 as dbapi


BAZA = 'serije.db'


GLAVNI_MENI = ["Išči", "Žanri", "Top 10", "Zapri"]
ISCI_NE_OBSTAJA = ["Ponovno išči", "Glavni meni"]
PREGLED_EPIZOD = ["Najboljše epizode", "Vse epizode"]
ZACETEK = ["Glavni meni"]
ZANRI = ['Musical', 'Documentary', 'News', 'Talk-Show',
         'Family', 'Game-Show', 'Comedy', 'Music', 'Drama', 'Crime',
         'Mystery', 'Fantasy', 'Reality-TV', 'History', 'Sport', 'Action',
         'Adventure', 'Western', 'Horror', 'Sci-Fi', 'Romance', 'War',
         'Animation', 'Thriller', 'Biography', 'Short', 'Adult'] 


def glavniMeni():
    izbira = menu(GLAVNI_MENI)
    match izbira:
        case 1:
            isci()
        case 2:
            izberiZanr()
        case 3:
            top10()
        case 4:
            return




def isci():
    print(
        """
            Kaj iščeš?
        """
    )    
    vhod = input()
    izhod = conn.execute(
        """
            SELECT naslovi.id, naslov, ocena FROM naslovi
            JOIN ocene ON naslovi.id = ocene.id
            WHERE naslov LIKE ? AND tip = "tvSeries" AND stVolitev > 10000
            ORDER BY ocena DESC
            LIMIT 10;
        """,["%" + vhod + "%"]
    ).fetchall()

    if len(izhod) == 0:
        print(f"Naslov '{vhod}' ne obstaja \n")
        izbira = menu(ISCI_NE_OBSTAJA)
        match izbira:
            case 1:
                isci()
            case 2:
                glavniMeni()
    else:
        izpisiRezultat(izhod)

    







def menu(moznosti):
    while True:
        for i in range(len(moznosti)):
            print(str(i + 1) + ")" + moznosti[i])

        vhod = input()
        if (len(vhod) > 0) and (vhod.isdigit()) and (int(vhod) in range(1, len(moznosti) + 1)):
            return int(vhod)
        else:
            print("Napačen vhod \n")
    


def izpisiRezultat(rez):
    dolzina = len(rez)
    if dolzina == 0:
        print("Nič pametnega")
        return glavniMeni()
    while True:
        for i in range(min(dolzina, 10)):
            print(str(i + 1) + ")", end = " ")
            for e in rez[i][1:]:
                print(e, end = "   ")
            print()

        vhod = input()
        if (len(vhod) > 0) and (vhod.isdigit()) and (int(vhod) in range(1, dolzina + 1)):
            izberi(rez[int(vhod) - 1][0])
            return
        else:
            print("Napačen vhod \n")
    

def izberi(id):
    vrstica = conn.execute("SELECT * FROM naslovi WHERE id = ?;", [id]).fetchone()
    if vrstica[1] == "tvSeries":
        izpisiSerijo(vrstica)
        izbira = menu(PREGLED_EPIZOD)
        match izbira:
            case 1:
                najboljseEpizode(id)
            case 2:
                pregledEpzod(id)
    else:
        izpisiEpizodo(vrstica)
        izbira = menu(ZACETEK)
        match izbira:
            case 1:
                glavniMeni() #TODO

    
def izpisiSerijo(vrstica):
    id, _, naslov, zacetekLeto, konecLeto, __ = vrstica
    tabZanri = zanri(id)
    casSkupaj = vsotaCas(id)
    url = "https://www.imdb.com/title/" + id + "/"
    sezone, epizode = stSezonInEpizod(id)
    ocena, stVolitev = ocenaInVolitve(id)
    print(
        f"""
            id : {id}
            naslov : {naslov}
            čas [min] : {casSkupaj}
            sezone/epizode : {sezone} / {epizode}
            ocena/število volilcev : {ocena} / {stVolitev}
            začetek/konec : {zacetekLeto} / {konecLeto}
            spletna stran : {url}
            žanri : """, end = "")
    for zanr in tabZanri:
        print(zanr + " ", end = "")
    print()


def zanri(id):
    izhod = conn.execute(
        """
            SELECT zanr FROM zanr
            WHERE id = ?;
        """, [id]
    )
    z = []
    for zanr in izhod:
        z.append(zanr[0])

    return z


def vsotaCas(id):
    izhod = conn.execute(
        """
            SELECT SUM(n2.cas) FROM naslovi n1
            JOIN epizode ON epizode.serija = n1.id
            JOIN naslovi n2 ON epizode.id = n2.id
            WHERE n1.id = ?;
        """, [id]
    )
    return izhod.fetchone()[0]


def stSezonInEpizod(id):
    sezone = conn.execute(
        """
            SELECT COUNT(DISTINCT sezona) FROM epizode
            WHERE serija = ?;
        """, [id])
    epizode = conn.execute(
        """
            SELECT COUNT(epizoda) FROM epizode
            WHERE serija = ?;
        """, [id])
    return (sezone.fetchone()[0], epizode.fetchone()[0])



def ocenaInVolitve(id):
    izhod = conn.execute(
        """
            SELECT ocena, stVolitev FROM ocene
            WHERE id = ?;
        """, [id]).fetchall()
    ocena = izhod[0][0]
    stVolitev = izhod[0][1]
    return (ocena, stVolitev)




def izpisiEpizodo(vrstica):
    id, _, naslov, __, ___, cas = vrstica
    tabZanri = zanri(id)
    url = "https://www.imdb.com/title/" + id + "/"
    sezona, epizoda = sezonaInEpizoda(id)
    ocena, stVolitev = ocenaInVolitve(id)
    print(
        f"""
            id : {id}
            naslov : {naslov}
            čas [min] : {cas}
            sezona/epizoda : {sezona} / {epizoda}
            ocena/število volilcev : {ocena} / {stVolitev}
            spletna stran : {url}
            žanri : """, end = "")
    for zanr in tabZanri:
        print(zanr + " ", end = "")
    print()



def sezonaInEpizoda(id):
    izhod = conn.execute(
        """
            SELECT sezona, epizoda FROM epizode
            WHERE id = ?;
        """,[id]).fetchall()
    sezona = izhod[0][0]
    epizoda = izhod[0][1]
    return (sezona, epizoda)




def izberiZanr():
    stran = 1
    while True:
        print(f"stran: {stran} od 3")
        for i in range((stran - 1) * 9, stran * 9):
            print(str((i + 1) - (stran - 1) * 9) + ")" + ZANRI[i])
        izbira = input("Premik strani: '<' ali '>'  ")
        if izbira in ("1", "2", "3", "4", "5", "6", "7", "8", "9"):
            return isciZanr(ZANRI[int(izbira) - 1 + (stran - 1) * 9])
        elif izbira == "<":
            stran = max(1, stran - 1)
        elif izbira == ">":
            stran = min(3, stran + 1)
        else:
            print("Napačen vhod \n")


def isciZanr(izbranZanr):
    izhod = conn.execute(
        """
            SELECT naslovi.id, naslov, ocena FROM naslovi
            JOIN zanr ON zanr.id = naslovi.id
            JOIN ocene ON ocene.id = naslovi.id
            WHERE zanr.zanr = ? AND stVolitev > 10000 AND naslovi.tip = "tvSeries"
            GROUP BY naslov
            ORDER BY ocene.ocena DESC
            LIMIT 10;
        """, [izbranZanr]).fetchall()
    izpisiRezultat(izhod)



def top10():
    izhod = conn.execute(
        """
            SELECT naslovi.id, naslov, ocena FROM naslovi
            JOIN zanr ON zanr.id = naslovi.id
            JOIN ocene ON ocene.id = naslovi.id
            WHERE stVolitev > 100000 AND naslovi.tip = "tvSeries"
            GROUP BY naslov
            ORDER BY ocene.ocena DESC
            LIMIT 10;
        """).fetchall()
    izpisiRezultat(izhod)




def najboljseEpizode(id):
    izhod = conn.execute(
        """
            SELECT n2.id, n2.naslov, ocene.ocena, sezona, epizoda FROM naslovi n1
            JOIN epizode ON epizode.serija = n1.id
            JOIN naslovi n2 ON epizode.id = n2.id
            JOIN ocene ON ocene.id = n2.id
            WHERE n1.id = ?
            ORDER BY ocene.ocena DESC
            LIMIT 10;
        """,[id]).fetchall()
    izpisiRezultat(izhod)


def pregledEpzod(id):
    izhod = conn.execute(
        """
            SELECT n2.id, n2.naslov, ocene.ocena, epizoda, sezona FROM naslovi n1
            JOIN epizode ON epizode.serija = n1.id
            JOIN naslovi n2 ON epizode.id = n2.id
            JOIN ocene ON ocene.id = n2.id
            WHERE n1.id = ?
            ORDER BY sezona, epizoda;
        """,[id]).fetchall()
    
    stran = 1
    while True:
        print(f"stran: {stran} od {len(izhod) // 9 + 1}")
        for i in range((stran - 1) * 9, min(stran * 9, len(izhod))):
            print(str((i + 1) - (stran - 1) * 9) + ")", end = "")
            for e in izhod[i][1:]:
                print(str(e), end = "    ")
            print()
        izbira = input("Premik strani: '<' ali '>'  ")
        if izbira in ("1", "2", "3", "4", "5", "6", "7", "8", "9"):
            return izberi(izhod[int(izbira) - 1 + (stran - 1) * 9][0])
        elif izbira == "<":
            stran = max(1, stran - 1)
        elif izbira == ">":
            stran = min(3, stran + 1)
        else:
            print("Napačen vhod \n")


try:
    conn = dbapi.connect(BAZA)
    cur = conn.cursor()



    with conn:


        
        glavniMeni()


finally:
    conn.close() 




