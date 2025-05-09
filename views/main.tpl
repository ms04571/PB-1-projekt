<!DOCTYPE html>
<html>
<head>
    <title>TV Serije</title>
</head>
<body>
    <h1>Išči serije</h1>

    <form action="/" method="post">
        <fieldset>
            <legend>Filtri</legend>

            Razvrsti po: <select name="sortirajPo">
                <option value="naslov" {{'selected' if parametri.get('sortirajPo') == 'naslov' else ''}}>Naslov</option>
                <option value="zacetekLeto" {{'selected' if parametri.get('sortirajPo') == 'zacetekLeto' else ''}}>Leto</option>
                <option value="ocena" {{'selected' if parametri.get('sortirajPo') == 'ocena' else ''}}>Ocena</option>
                <option value="stVolitev" {{'selected' if parametri.get('sortirajPo') == 'stVolitev' else ''}}>Število volitev</option>
            </select><br><br>
            Način razvrščanja: <select name="sortiranje">
                <option value="ASC" {{'selected' if parametri.get('sortiranje') == 'ASC' else ''}}>Naraščajoče</option>
                <option value="DESC" {{'selected' if parametri.get('sortiranje') == 'DESC' else ''}}>Padajoče</option>
            </select><br><br>
            Naslov: <input type="text" name="naslov" value="{{parametri.get('naslov', '')}}"><br><br>
            <details>
                <summary>Žanri (izberi do 3)</summary>
                <div id="zanriOkno">
                    % for zanr in zanri:
                        <label>
                            <input type="checkbox" name="zanr" value="{{zanr}}" 
                                {{'checked' if zanr in izbraniZanri else ''}}>
                            {{zanr}}
                        </label><br>
                    % end
                </div>
            </details><br>
            Leto (Min - Max): 
            <input type="number" name="letoMin" value="{{parametri.get('letoMin', '')}}" style="width: 80px;">
            -
            <input type="number" name="letoMax" value="{{parametri.get('letoMax', '')}}" style="width: 80px;"><br><br>
            Ocena (Min - Max): 
            <input type="range" name="ocenaMin" min="0" max="10" step="0.1" value="{{parametri.get('ocenaMin', 0)}}"> 
            do 
            <input type="range" name="ocenaMax" min="0" max="10" step="0.1" value="{{parametri.get('ocenaMax', 10)}}"><br><br>

            <input type="submit" value="Filtriraj">
        </fieldset>
    </form>

    <hr>

    <h2>TV Serije</h2>
    % if vrstice:
        <table border="1">
            <tr>
                % for stolpec in stolpci:
                    <th>{{stolpec}}</th>
                % end
            </tr>
            % for vrstica in vrstice:
                <tr>
                    % for el in vrstica:
                        <td>{{el}}</td>
                    % end
                </tr>
            % end
        </table>
    % else:
        <p>No results found.</p>
    % end

</body>
</html>
