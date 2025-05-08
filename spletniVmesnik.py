from bottle import Bottle, run, template, request
import os
import sqlite3


vmesnik = Bottle()
path = os.path.dirname(os.path.realpath(__file__))
BAZA = path + "\\" + 'serije.db'



def ukazIsci(naslov='', zanr='', letoMin=0, letoMax=9999, ocenaMin=0, ocenaMax=10, sortirajPo="zacetekLeto", sortiranje = "DESC"):
    """
        Vrne vrstice in imena stolpcev kadar iščemo na glavni strani.
        Parametre poberemo iz panela zraven tabele.
    """
    conn = sqlite3.connect(BAZA)
    cursor = conn.cursor()
    
    # manjka ascending descending
    ukaz = """
        SELECT naslovi.id, naslov, zacetekLeto, ocena FROM naslovi
        JOIN ocene ON ocene.id = naslovi.id
        JOIN zanr ON zanr.id = naslovi.id
        WHERE tip = "tvSeries"
        AND naslov LIKE ?
        AND zanr LIKE ?
        AND zacetekLeto BETWEEN ? AND ?
        AND ocena BETWEEN ? AND ?
        GROUP BY naslov
    """
    

    cursor.execute(ukaz, (f'%{naslov}%', zanr, letoMin, letoMax, ocenaMin, ocenaMax))
    
    vrstice = cursor.fetchall()
    stolpci = [opis[0] for opis in cursor.description]  # imena stolpcev
    
    conn.close()
    return vrstice, stolpci


@vmesnik.route('/', method=["GET", "POST"])
def index():
    # Get parameters from the form (if POST request)
    naslov = request.forms.get('naslov', '')
    zanr = request.forms.get('zanr', '')
    letoMin = int(request.forms.get('letoMin', 0))
    letoMax = int(request.forms.get('letoMax', 9999))
    ocenaMin = float(request.forms.get('ocenaMin', 0))
    ocenaMax = float(request.forms.get('ocenaMax', 10))
    sortirajPo = request.forms.get('sortirajPo')
    sortiranje = request.forms.get('sortiranje')

    vrstice, stolpci = ukazIsci(naslov, zanr, letoMin, letoMax, ocenaMin, ocenaMax, sortirajPo, sortiranje)
    
    return template('main', 
                   params=request.forms, 
                   stolpci=stolpci, 
                   vrstice=vrstice)

if __name__ == "__main__":
    run(vmesnik, host='localhost', port=8080, debug=True, reloader=True)
