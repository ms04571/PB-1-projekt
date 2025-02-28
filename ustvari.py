import sqlite3 as dbapi
import csv


BAZA = 'serije.db'

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
                    id TEXT PRIMARY KEY,
                    serija TEXT,
                    sezona INTEGER,
                    epizoda INTEGER,
                    FOREIGN KEY (serija) REFERENCES naslovi (id)
                );
            """
        )

        cur.execute(
            """
                CREATE TABLE IF NOT EXISTS zanr (
                    id TEXT,
                    zanr TEXT,
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

#    cur.execute(
#        """
#            CREATE TABLE IF NOT EXISTS 
#        """
#    )




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
            with open("title.basics.tsv", encoding = "utf-8") as dat:
                tsv = csv.reader(dat, delimiter = "\t")
                next(tsv)
                j = 0
                for vrstica in tsv:          
                    if vrstica[1] in ("tvSeries", "tvEpisode"):
                        if j % 1000 == 0:
                            print(str(j) + "        ", end = "\r")
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
            with open("title.episode.tsv", encoding = "utf-8") as dat:
                tsv = csv.reader(dat, delimiter = "\t")
                next(tsv)
                j = 0
                for vrstica in tsv:          
                    if j % 1000 == 0:
                        print(str(j) + "        ", end = "\r")
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
            with open("title.basics.tsv", encoding = "utf-8") as dat:
                tsv = csv.reader(dat, delimiter = "\t")
                next(tsv)
                j = 0
                for vrstica in tsv:
                    if vrstica[1] in ("tvSeries", "tvEpisode"):  
                        if j % 1000 == 0:
                            print(str(j) + "        ", end = "\r")
                        j += 1

                        zanri = vrstica[-1]
                        for zanr in zanri.split(","):
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
            with open("title.ratings.tsv", encoding = "utf-8") as dat:
                tsv = csv.reader(dat, delimiter = "\t")
                next(tsv)
                j = 0
                for vrstica in tsv:          
                    if j % 1000 == 0:
                        print(str(j) + "        ", end = "\r")
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



#brisi("epizode")
#brisi("zanr")
#brisi("ocene")


#uvozEpizode()
#uvozNaslovi()
#uvozZanr()
#uvozOcene()

