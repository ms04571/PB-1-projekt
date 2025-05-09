from bottle import Bottle, run, template, request
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


def ukazIsci(naslov='', izbraniZanri=ZANRI, letoMin=0, letoMax=9999, ocenaMin=0, ocenaMax=10, sortirajPo="zacetekLeto", sortiranje = "DESC"):
    """
        Vrne vrstice in imena stolpcev kadar iščemo na glavni strani.
        Parametre poberemo iz panela zraven tabele.
    """
    conn = sqlite3.connect(BAZA)
    cursor = conn.cursor()
    
    zanrPlaceholder = ','.join(['?'] * len(izbraniZanri))
    ukaz = f"""
        SELECT naslovi.id, naslov, zacetekLeto, ocena FROM naslovi
        JOIN ocene ON ocene.id = naslovi.id
        JOIN zanr ON zanr.id = naslovi.id
        WHERE tip = "tvSeries"
        AND naslov LIKE ?
        AND zanr IN ({zanrPlaceholder})
        AND zacetekLeto BETWEEN ? AND ?
        AND ocena BETWEEN ? AND ?
        GROUP BY naslov
        ORDER BY {sortirajPo if sortirajPo in ["naslov", "zacetekLeto", "ocena", "stVolitev"] else "naslov"} 
                 {sortiranje if sortiranje in ['ASC', 'DESC'] else 'ASC'}
    """
               
    cursor.execute(ukaz, (f'%{naslov}%', *izbraniZanri, letoMin, letoMax, ocenaMin, ocenaMax))
    
    vrstice = cursor.fetchall()
    stolpci = [opis[0] for opis in cursor.description]  # imena stolpcev
    
    conn.close()
    return vrstice, stolpci


@vmesnik.get('/')
def glavnaStran_get():
    """
        Prikaže stran z privzetimi filtri
    """
    vrstice, stolpci = ukazIsci()  

    return template('main', 
                   parametri={},  # Empty for GET as we just show defaults
                   stolpci=stolpci, 
                   vrstice=vrstice,
                   zanri=ZANRI,  # List of all genres
                   izbraniZanri=ZANRI)  # Default genres when no filters are selected


@vmesnik.post('/')
def glavnaStranPost():
    """
        Prikaže stran z izbranimi filtri iz "forms"
    """
    naslov = request.forms.get('naslov', '')
    letoMin = int(request.forms.get('letoMin', 0))
    letoMax = int(request.forms.get('letoMax', 9999))
    ocenaMin = float(request.forms.get('ocenaMin', 0))
    ocenaMax = float(request.forms.get('ocenaMax', 10))
    sortirajPo = request.forms.get('sortirajPo')
    sortiranje = request.forms.get('sortiranje')
    izbraniZanri = request.forms.getall('zanr')
    if len(izbraniZanri) == 0:
        izbraniZanri = ZANRI
    elif len(izbraniZanri) > 3:
        izbraniZanri = izbraniZanri[:3]  # največ 3 žanri na enkrat

    vrstice, stolpci = ukazIsci(naslov, izbraniZanri, letoMin, letoMax, ocenaMin, ocenaMax, sortirajPo, sortiranje)
    
    return template('main', 
                   parametri=request.forms, 
                   stolpci=stolpci, 
                   vrstice=vrstice,
                   zanri = ZANRI,
                   izbraniZanri = izbraniZanri)

if __name__ == "__main__":
    run(vmesnik, host='localhost', port=8080, debug=True, reloader=True)
