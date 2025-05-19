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
        self.serijaId = dbInfo[0]
        self.serijaNaslov = dbInfo[1]
        self.id = dbInfo[2]
        self.naslov = dbInfo[3]
        self.leto = dbInfo[4]
        self.ocena = dbInfo[5]
        self.stVolitev = dbInfo[6]
        self.sezona = dbInfo[7]
        self.epizoda = dbInfo[8]
        self.zanri = dbInfo[9]
        self.povezava = f"https://www.imdb.com/title/{self.id}/"

    def novaEpizoda(cur, id):
        # glavni podatki
        cur.execute("""
            SELECT n2.id, n2.naslov, n1.id, n1.naslov, n1.zacetekLeto, ocena, stVolitev, epizode.sezona, epizode.epizoda FROM naslovi n1
            JOIN epizode ON epizode.id = n1.id
            JOIN naslovi n2 ON n2.id = epizode.serija
            JOIN ocene ON n1.id = ocene.id 
            WHERE n1.id = ?
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