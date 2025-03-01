import sqlite3 as dbapi


BAZA = 'serije.db'


GLAVNI_MENI = ["Išči", "Kategorije", "Dobre serije", "Zapri"]
ISCI_NE_OBSTAJA = ["Ponovno išči", "Glavni meni"]




def galavniMeni():
    izbira = menu(GLAVNI_MENI)
    match izbira:
        case 1:
            isci()
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
            WHERE naslov LIKE ? AND tip = "tvSeries"
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
                galavniMeni()
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
    while True:
        for i in range(min(dolzina, 10)):
            print(str(i + 1) + ")", end = " ")
            for e in rez[i]:
                print(e, end = " ")
            print()

        vhod = input()
        if (len(vhod) > 0) and (vhod.isdigit()) and (int(vhod) in range(1, dolzina + 1)):
            izberi(rez[int(vhod) - 1][0])
            return
        else:
            print("Napačen vhod \n")
    

def izberi(id):
    vrstica = conn.execute("SELECT * FROM naslovi WHERE id = ?;", [id]).fetchone()
    print(vrstica)
    if vrstica[1] == "tvSeries":
        izpisiSerijo(vrstica)
        
    else:
        izpisiEpizodo(vrstica)

    






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
    return izhod.fetchone()[0]# or "\\N"

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
            žanri : 
        """, end = "")
    print(tabZanri)
    for zanr in tabZanri:
        print(zanr + " ", end = "")
    print()



def sezonaInEpizoda(id):
    izhod = conn.execute(
        """
            SELECT sezona, epizoda FROM epizode
            WHERE id = ?;
        """,[id]).fetchall()
    print(izhod)
    sezona = izhod[0][0]
    epizoda = izhod[0][1]
    return (sezona, epizoda)













try:
    conn = dbapi.connect(BAZA)
    cur = conn.cursor()



    with conn:


        
        galavniMeni()


finally:
    conn.close() 




