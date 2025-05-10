class Serija:


    def __init__(self, dbInfo):
        self.id = dbInfo[0]
        self.naslov = dbInfo[1]
        self.zacetekLeto = dbInfo[2]
        self.konecLeto = dbInfo[3]
        self.ocena = dbInfo[4]
        self.stVolitev = dbInfo[5]
        self.zanri = dbInfo[6]
        self.povezava = f"https://www.imdb.com/title/{self.id}/"



    def novaSerija(cur, id):
        # glavni podatki
        cur.execute("""
            SELECT naslovi.id, naslov, zacetekLeto, konecLeto, ocena, stVolitev FROM naslovi 
            JOIN ocene ON naslovi.id = ocene.id 
            WHERE naslovi.id = ?
        """, (id,))
        serija = list(cur.fetchone())

        if not serija:
           raise Exception("Serija ne obstaja")
        
        # žanri posebej ker so svoja tabela
        cur.execute("""
            SELECT zanr FROM zanr  
            WHERE id = ?
        """, (id,))
        
        tabZanrov = []
        for zanr in cur.fetchall():
            tabZanrov.append(zanr[0])

        serija.append(tabZanrov)

        return Serija(serija)
    



class Epizoda:

    def __init__(self, dbInfo):
        self.id = dbInfo[0]
        self.naslov = dbInfo[1]
        self.leto = dbInfo[2]
        self.ocena = dbInfo[3]
        self.stVolitev = dbInfo[4]
        self.zanri = dbInfo[5]
        self.povezava = f"https://www.imdb.com/title/{self.id}/"

    def novaEpizoda(cur, id):
        # glavni podatki
        cur.execute("""
            SELECT naslovi.id, naslov, zacetekLeto, ocena, stVolitev FROM naslovi 
            JOIN ocene ON naslovi.id = ocene.id 
            WHERE naslovi.id = ?
        """, (id,))
        epizoda = list(cur.fetchone())

        if not epizoda:
           raise Exception("Epizoda ne obstaja")
        
        # žanri posebej ker so svoja tabela
        cur.execute("""
            SELECT zanr FROM zanr  
            WHERE id = ?
        """, (id,))
        
        tabZanrov = []
        for zanr in cur.fetchall():
            tabZanrov.append(zanr[0])

        epizoda.append(tabZanrov)

        return Epizoda(epizoda)