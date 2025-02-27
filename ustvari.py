import sqlite3 as dbapi

BAZA = 'serije.db'

try:
    conn = dbapi.connect(BAZA)
    cur = conn.cursor()


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

    




finally:
    conn.close()



