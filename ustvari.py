import sqlite3 as dbapi
import csv
import os

# Ta proces lahko traja 10-30 min 



path = os.path.dirname(os.path.realpath(__file__))
BAZA = path + "\\" + 'serije.db'
minVolitev = 10000


try:
    conn = dbapi.connect(BAZA)
    cur = conn.cursor()

    with conn:

        cur.execute(
            """
                CREATE TABLE IF NOT EXISTS naslovi (
                    id TEXT PRIMARY KEY,
                    tip TEXT,
                    naslov TEXT,
                    zacetekLeto INTEGER,
                    konecLeto INTEGER,
                    cas INTEGER
                );
            """
        )

        cur.execute(
            """
                CREATE TABLE IF NOT EXISTS epizode (
                    id TEXT,
                    serija TEXT,
                    sezona INTEGER,
                    epizoda INTEGER,
                    FOREIGN KEY (id) REFERENCES naslovi (id)
                    FOREIGN KEY (serija) REFERENCES naslovi (id)
                );
            """
        )

        cur.execute(
            """
                CREATE TABLE IF NOT EXISTS zanr (
                    id TEXT,
                    zanr INTEGER,
                    FOREIGN KEY (id) REFERENCES naslovi (id)
                );
            """
        )

        cur.execute(
            """
                CREATE TABLE IF NOT EXISTS ocene (
                    id TEXT,
                    ocena FLOAT,
                    stVolitev INTEGER,
                    FOREIGN KEY (id) REFERENCES naslovi (id)
                );
            """
        )

finally:
    conn.close()


def brisi(tabela):
    try:
        conn = dbapi.connect(BAZA)
        cur = conn.cursor()

        with conn:  
            cur.execute(
                "DELETE FROM " + tabela
                )
    finally:
        conn.close() 


def uvozNaslovi():
    try:
        conn = dbapi.connect(BAZA)
        cur = conn.cursor()

        with conn:
            with open(path + "\\" + "title.basics.tsv", encoding = "utf-8") as dat:
                tsv = csv.reader(dat, delimiter = "\t")
                next(tsv)
                j = 0
                for vrstica in tsv:          
                    if vrstica[1] in ("tvSeries", "tvEpisode"):
                        if j % 10000 == 0:
                            print("1/4  " + str(j) + "        ", end = "\r")
                        j += 1
                        if vrstica[5].isdigit():
                            vrstica[5] = int(vrstica[5])
                        else:
                            vrstica[5] = None
                        if vrstica[6].isdigit():
                            vrstica[6] = int(vrstica[6])
                        else:
                            vrstica[6] = None
                        if vrstica[7].isdigit():
                            vrstica[7] = int(vrstica[7]) 
                        else:
                            vrstica[7] = None

                        cur.execute(
                            """
                                INSERT INTO naslovi (id, tip, naslov, zacetekLeto, konecLeto, cas)
                                VALUES (?, ?, ?, ?, ?, ?);
                           """,[vrstica[0], vrstica[1], vrstica[2], vrstica[5], vrstica[6], vrstica[7]]
                                    )
    finally:
        conn.close()

def uvozNaslovi2(): # test
    try:
        conn = dbapi.connect(BAZA)
        cur = conn.cursor()

        with conn:
            with open(path + "\\" + "title.basics.tsv", encoding = "utf-8") as dat:
                tsv = csv.reader(dat, delimiter = "\t")
                next(tsv)
                j = 0
                tab = []
                for vrstica in tsv:          
                    if vrstica[1] in ("tvSeries", "tvEpisode"):
                        if j % 10000 == 0:
                            print("1/4  " + str(j) + "        ", end = "\r")
                        j += 1
                        if vrstica[5].isdigit():
                            vrstica[5] = int(vrstica[5])
                        else:
                            vrstica[5] = None
                        if vrstica[6].isdigit():
                            vrstica[6] = int(vrstica[6])
                        else:
                            vrstica[6] = None
                        if vrstica[7].isdigit():
                            vrstica[7] = int(vrstica[7]) 
                        else:
                            vrstica[7] = None
                        tab.append((vrstica[0], vrstica[1], vrstica[2], vrstica[5], vrstica[6], vrstica[7]))

                cur.executemany(
                    """
                        INSERT INTO naslovi (id, tip, naslov, zacetekLeto, konecLeto, cas)
                        VALUES (?, ?, ?, ?, ?, ?);
                    """, tab)
    finally:
        conn.close()


def uvozEpizode():
    try:
        conn = dbapi.connect(BAZA)
        cur = conn.cursor()

        with conn:
            with open(path + "\\" + "title.episode.tsv", encoding = "utf-8") as dat:
                tsv = csv.reader(dat, delimiter = "\t")
                next(tsv)
                j = 0
                for vrstica in tsv:          
                    if j % 10000 == 0:
                        print("2/4  " + str(j) + "        ", end = "\r")
                    j += 1
                    if vrstica[2].isdigit():
                        vrstica[2] = int(vrstica[2])
                    else:
                        vrstica[2] = None
                    if vrstica[3].isdigit():
                        vrstica[3] = int(vrstica[3])
                    else:
                        vrstica[3] = None

                    cur.execute(
                        """
                            INSERT INTO epizode (id, serija, sezona, epizoda)
                            VALUES (?, ?, ?, ?);
                        """,[vrstica[0], vrstica[1], vrstica[2], vrstica[3]]
                    )       
    finally:
        conn.close()



def uvozZanr():
    try:
        conn = dbapi.connect(BAZA)
        cur = conn.cursor()

        with conn:
            with open(path + "\\" + "title.basics.tsv", encoding = "utf-8") as dat:
                tsv = csv.reader(dat, delimiter = "\t")
                next(tsv)
                j = 0
                for vrstica in tsv:
                    if vrstica[1] in ("tvSeries", "tvEpisode"):  
                        if j % 10000 == 0:
                            print("3/4  " + str(j) + "        ", end = "\r")
                        j += 1

                        zanri = vrstica[-1]
                        for zanr in zanri.split(","):
                            if zanr == "\\N":
                                zanr = None
                            cur.execute(
                                """
                                    INSERT INTO zanr (id, zanr)
                                    VALUES (?, ?);
                                """,[vrstica[0], zanr]
                                )
                    
    finally:
        conn.close()




def uvozOcene():
    try:
        conn = dbapi.connect(BAZA)
        cur = conn.cursor()

        with conn:
            with open(path + "\\" + "title.ratings.tsv", encoding = "utf-8") as dat:
                tsv = csv.reader(dat, delimiter = "\t")
                next(tsv)
                j = 0
                for vrstica in tsv:          
                    if j % 10000 == 0:
                        print("4/4  " + str(j) + "        ", end = "\r")
                    j += 1
                    
                    if vrstica[1][0].isdigit():
                        vrstica[1] = float(vrstica[1])
                    else:
                        vrstica[1] = None
                    if vrstica[2].isdigit():
                        vrstica[2] = int(vrstica[2])
                    else:
                        vrstica[2] = None

                    cur.execute(
                        """
                            INSERT INTO ocene (id, ocena, stVolitev)
                            VALUES (?, ?, ?);
                        """,[vrstica[0], vrstica[1], vrstica[2]])
                    
    finally:
        conn.close()



def brisiOdvecneStvari(minVolitev):
    try:
        conn = dbapi.connect(BAZA, isolation_level=None)
        cur = conn.cursor()

        with conn: 
            print("obnavljanje povezovalne tabele...")
            cur.execute(    
                """
                    DELETE FROM epizode
                    WHERE sezona IS NULL OR epizoda IS NULL;
                """
            )
            cur.execute(    
                """
                    DELETE FROM epizode
                    WHERE serija IN 
                    (SELECT naslovi.id FROM naslovi
                    LEFT JOIN ocene ON ocene.id = naslovi.id
                    WHERE stVolitev < ? OR ocene.ocena IS NULL);
                """, [minVolitev]
            )
            print("brisane serij...")
            cur.execute(    # brisanje serij
                """
                    DELETE FROM naslovi
                    WHERE tip = "tvSeries" AND id NOT IN
                    (SELECT epizode.serija FROM epizode);
                """
            )
            print("brisanje epizod...")
            cur.execute(    # brisanje epizod
                """
                    DELETE FROM naslovi
                    WHERE tip = "tvEpisode" AND id NOT IN
                    (SELECT epizode.id FROM epizode);
                """
            )
            print("brisanje ocen...")
            cur.execute(    # brisanje ocen
                """
                    DELETE FROM ocene
                    WHERE ocene.id NOT IN
                    (SELECT naslovi.id FROM naslovi);
                """
            )
            print("brisanje žanr...")
            cur.execute(    # brisanje žanr
                """
                    DELETE FROM zanr
                    WHERE zanr.id NOT IN
                    (SELECT naslovi.id FROM naslovi);
                """
            )
            print("Čiščenje...")
            cur.execute("VACUUM")
            print("KONEC")

    finally:
        conn.close()    





# če usvarjaš na novo odkomentiraj vse
# lahko tudi ročno izbrišeš celo bazo


#brisi("epizode")
#brisi("zanr")
#brisi("ocene")
#brisi("naslovi")


#uvozNaslovi()
#uvozEpizode()
#uvozZanr()
#uvozOcene()
#brisiOdvecneStvari(minVolitev)

