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
                <option value="naslov">Naslov</option>
                <option value="zacetekLeto">Leto</option>
                <option value="ocena">Ocena</option>
                <option value="stVolitev">Število volitev</option>
            </select>
            Način razvrščanja: <select name="sortiranje">
                <option value="ASC">Naraščajoče</option>
                <option value="DESC">Padajoče</option>
            </select>
            Naslov: <input type="text" name="naslov" value="{{params.get('naslov', '')}}"><br><br>
            Žanr: <input type="text" name="zanr" value="{{params.get('zanr', '')}}"><br><br>
            Leto (Min - Max): 
            <input type="number" name="letoMin" value="{{params.get('letoMin', '')}}" style="width: 80px;">
            -
            <input type="number" name="letoMax" value="{{params.get('letoMax', '')}}" style="width: 80px;"><br><br>
            Ocena (Min - Max): 
            <input type="range" name="ocenaMin" min="0" max="10" step="0.1" value="{{params.get('ocenaMin', 0)}}"> 
            do 
            <input type="range" name="ocenaMax" min="0" max="10" step="0.1" value="{{params.get('ocenaMax', 10)}}"><br><br>

            <input type="submit" value="Apply Filters">
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
