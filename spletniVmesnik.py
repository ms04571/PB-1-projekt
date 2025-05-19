from bottle import Bottle, run, template, request, static_file
from razredi import Serija, Epizoda
import os
import sqlite3


vmesnik = Bottle()
path = os.path.dirname(os.path.realpath(__file__))
BAZA = path + "\\" + 'serije.db'
ZANRI = ['Musical', 'Documentary', 'News', 'Talk-Show',
         'Family', 'Game-Show', 'Comedy', 'Music', 'Drama', 'Crime',
         'Mystery', 'Fantasy', 'Reality-TV', 'History', 'Sport', 'Action',
         'Adventure', 'Western', 'Horror', 'Sci-Fi', 'Romance', 'War',
         'Animation', 'Thriller', 'Biography', 'Short']
naStran = 20


@vmesnik.route('/style/<filename:path>')
def static_files(filename):
    return static_file(filename, root='style')

def ukazIsci(naslov='', izbraniZanri=[], letoMin=1951, letoMax=2025, ocenaMin=0, ocenaMax=10,
             sortirajPo="zacetekLeto", sortiranje = "DESC", stran=1):
    """
        Vrne vrstice in imena stolpcev kadar iščemo na glavni strani.
        Parametre poberemo iz panela zraven tabele (iz form-a).
    """
    conn = sqlite3.connect(BAZA)
    cur = conn.cursor()
    
    ukazOsnovni = f"""
        SELECT naslovi.id, naslov, zacetekLeto, ocena, stVolitev FROM naslovi
        JOIN ocene ON ocene.id = naslovi.id
        JOIN zanr AS z ON z.id = naslovi.id
        WHERE tip = "tvSeries"
        AND naslov LIKE ?
        AND zacetekLeto BETWEEN ? AND ?
        AND ocena BETWEEN ? AND ?
        GROUP BY naslovi.id 
    """

    zanrPlaceholder = ','.join(['?'] * len(izbraniZanri)) # naredi niz: "?, ?, ... ,?, ?"
    ukazZanri = f"""
        SELECT naslovi.id, naslov, zacetekLeto, ocena, stVolitev FROM naslovi
        JOIN ocene ON ocene.id = naslovi.id
        JOIN zanr AS z ON z.id = naslovi.id
        WHERE tip = "tvSeries"
        AND naslov LIKE ?
        AND zacetekLeto BETWEEN ? AND ?
        AND ocena BETWEEN ? AND ?
        AND zanr IN ({zanrPlaceholder})
        GROUP BY naslovi.id
        HAVING COUNT(DISTINCT z.zanr) = ?
    """

    ukazKonec = f"""
        ORDER BY {sortirajPo if sortirajPo in ["naslov", "zacetekLeto", "ocena", "stVolitev"] else "naslov"} 
                 {sortiranje if sortiranje in ['ASC', 'DESC'] else 'ASC'}
        LIMIT ? OFFSET ?
    """

    zamik = (stran - 1) * naStran
    parametri = [f'%{naslov}%', letoMin, letoMax, ocenaMin, ocenaMax]

    if len(izbraniZanri) == 0: # če niso izbrabi nobeni žanri iščemo brez žanrov
        ukaz = ukazOsnovni + ukazKonec
        parametri += [naStran, zamik]
    else:
        ukaz = ukazZanri + ukazKonec
        parametri += [*izbraniZanri, len(izbraniZanri), naStran, zamik]

    cur.execute(ukaz, parametri)
    vrstice = cur.fetchall()

    conn.close()
    return vrstice


@vmesnik.get('/')
def glavnaStran_get():
    """
        Prikaže stran z privzetimi filtri
    """
    vrstice = ukazIsci()  

    return template('main', 
                    parametri={}, 
                    vrstice=vrstice,
                    zanri=ZANRI,
                    izbraniZanri=[],
                    stran=1,
                    naStran=naStran)


@vmesnik.post('/')
def glavnaStranPost():
    """
        Prikaže stran z izbranimi filtri iz "forms"
    """
    naslov = request.forms.get('naslov', '')
    letoMin = int(request.forms.get('letoMin', 1951))
    letoMax = int(request.forms.get('letoMax', 2025))
    ocenaMin = float(request.forms.get('ocenaMin', 0))
    ocenaMax = float(request.forms.get('ocenaMax', 10))
    sortirajPo = request.forms.get('sortirajPo')
    sortiranje = request.forms.get('sortiranje')
    izbraniZanri = request.forms.getall('zanr')
    stran = int(request.forms.get('stran', 1))
    # naslov ima lahko največ 3 žanre (če bi dovolil več bi dobili prazno tabelo)
    if len(izbraniZanri) > 3: 
        izbraniZanri = izbraniZanri[:3]  

    vrstice = ukazIsci(naslov, izbraniZanri, letoMin, letoMax, ocenaMin, ocenaMax, sortirajPo, sortiranje, stran)
    
    return template('main', 
                    parametri=request.forms, 
                    vrstice=vrstice,
                    zanri = ZANRI,
                    izbraniZanri = izbraniZanri,
                    stran=stran,
                    naStran=naStran)


@vmesnik.route('/<serijaId>')
def prikaziSerijo(serijaId):
    """
        Stran, ki bolj podrobno prikže serijo in njene epizode
    """
    sezona = request.query.get('sezona', default='1')
    try:
        sezona = int(sezona)
    except ValueError:
        sezona = 1

    conn = sqlite3.connect(BAZA)
    cur = conn.cursor()

    # razred Serija za boljše preglednost
    serija = Serija.novaSerija(cur, serijaId)

    # število vseh sezon
    stSezon = cur.execute("""
        SELECT MAX(sezona) FROM naslovi n1
        JOIN epizode ON epizode.serija = n1.id
        JOIN naslovi n2 ON epizode.id = n2.id
        WHERE n1.id = ?
    """, (serijaId,)).fetchone()[0] or 1

    epizode = epizodeOdSezone(serijaId, sezona)

    conn.close()
    return template('serija', serija=serija,
                              epizode=epizode,
                              sezona=sezona,
                              stSezon=stSezon)


def epizodeOdSezone(serijaId, stSezone):
    """
        vrne seznam epizod serije za podanim id-jem, ki 
        spadajo pod sezono stSezone
    """
    conn = sqlite3.connect(BAZA)
    cur = conn.cursor()

    cur.execute("""
        SELECT n2.id, n2.naslov, ocene.ocena, epizoda, sezona FROM naslovi n1
        JOIN epizode ON epizode.serija = n1.id
        JOIN naslovi n2 ON epizode.id = n2.id
        JOIN ocene ON ocene.id = n2.id
        WHERE n1.id = ?
        AND sezona = ?
        ORDER BY sezona, epizoda;
    """, (serijaId, stSezone))

    rez = cur.fetchall()
    conn.close()
    return rez


@vmesnik.route('/<serijaId>/<epizodaId>')
def prikaziEpizodo(serijaId, epizodaId):
    """
        Stran, ki bolj podrobno prikaže epizodo
    """
    conn = sqlite3.connect(BAZA)
    cur = conn.cursor()

    epizoda = Epizoda.novaEpizoda(cur, epizodaId)

    conn.close()

    return template('epizoda', epizoda=epizoda)




if __name__ == "__main__":
    run(vmesnik, host='localhost', port=8080, debug=True, reloader=True)
