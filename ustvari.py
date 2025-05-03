import sqlite3 as dbapi
import csv
import os

# Ta proces lahko traja 10-30 min 



path = os.path.dirname(os.path.realpath(__file__))
BAZA = path + "\\" + 'serije.db'
ZANRI = {'Musical' : 1, 
         'Documentary' : 2, 
         'News' : 3, 
         'Talk-Show' : 4,
         'Family' : 5, 
         'Game-Show' : 6, 
         'Comedy' : 7, 
         'Music' : 8, 
         'Drama' : 9, 
         'Crime' : 10,
         'Mystery' : 11, 
         'Fantasy' : 12, 
         'Reality-TV' : 13, 
         'History' : 14, 
         'Sport' : 15, 
         'Action' : 16,
         'Adventure' : 17, 
         'Western' : 18, 
         'Horror' : 19, 
         'Sci-Fi' : 20, 
         'Romance' : 21, 
         'War' : 22,
         'Animation' : 23, 
         'Thriller' : 24, 
         'Biography' : 25,
         'Short' : 26, 
         'Adult' : 27}


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

        cur.execute(
            """
                CREATE TABLE IF NOT EXISTS tabZanr (
                    id INTEGER PRIMARY KEY,
                    zanr TEXT,
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
                        if j % 1000 == 0:
                            print("1/4" + str(j) + "        ", end = "\r")
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
                    if j % 1000 == 0:
                        print("2/4" + str(j) + "        ", end = "\r")
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
                        if j % 1000 == 0:
                            print("3/4" + str(j) + "        ", end = "\r")
                        j += 1

                        zanri = vrstica[-1]
                        for zanr in zanri.split(","):
                            if zanr == "\\N":
                                zanr = None
                            else:
                                zanr = ZANRI[zanr]
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
                    if j % 1000 == 0:
                        print("4/4" + str(j) + "        ", end = "\r")
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
                        """,[vrstica[0], vrstica[1], vrstica[2]]
                                )
                    
    finally:
        conn.close()

def tabZanr():
    try:
        conn = dbapi.connect(BAZA)
        cur = conn.cursor()

        with conn:
            for k, v in ZANRI.items():
                cur.execute(
                    """
                        INSERT INTO tabZanr (id, zanr)
                        VALUES (?, ?)
                    """, [v, k])    
    finally:
        conn.close()



def brisiOdvecneStvari():
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
                    JOIN ocene ON ocene.id = naslovi.id
                    WHERE stVolitev < 100000);
                """
            )
            print("obnovljena povezovalna tabela")
            print("brisane serij...")
            cur.execute(    # brisanje serij
                """
                    DELETE FROM naslovi
                    WHERE tip = "tvSeries" AND id NOT IN
                    (SELECT epizode.serija FROM epizode);
                """
            )
            print("serije izbrisane")
            print("brisanje epizod...")
            cur.execute(    # brisanje epizod
                """
                    DELETE FROM naslovi
                    WHERE tip = "tvEpisode" AND id NOT IN
                    (SELECT epizode.id FROM epizode);
                """
            )
            print("epizode izbrisane")
            print("brisanje ocen...")
            cur.execute(    # brisanje ocen
                """
                    DELETE FROM ocene
                    WHERE ocene.id NOT IN
                    (SELECT naslovi.id FROM naslovi);
                """
            )
            print("ocene izbrisane")
            print("brisanje žanr...")
            cur.execute(    # brisanje žanr
                """
                    DELETE FROM zanr
                    WHERE zanr.id NOT IN
                    (SELECT naslovi.id FROM naslovi);
                """
            )
            print("žanri izbrisani")
            print("Čiščenje...")
            cur.execute("VACUUM")
            print("KONEC")

    finally:
        conn.close()    








#brisi("epizode")
#brisi("zanr")
#brisi("ocene")
#brisi("naslovi")


uvozNaslovi()
uvozEpizode()
uvozZanr()
uvozOcene()
brisiOdvecneStvari()

