<!DOCTYPE html>
<html>
<head>
    <title>{{serija.naslov}}</title>
    <link rel="stylesheet" href="/style/main.css">
</head>
<body>
    <a href="/" class="gumb-domov">🏠 Domov</a>
    <h1>{{serija.naslov}}</h1>

    <div class="glavniOvoj">
        <div class="serija-info">
            <table class="serije-table">
                <tr><td>Leto izida:</td><td>{{serija.zacetekLeto}}</td></tr>
                <tr><td>Končno leto:</td><td>{{serija.konecLeto}}</td></tr>
                <tr><td>Ocena:</td><td>{{serija.ocena}}</td></tr>
                <tr><td>Število volitev:</td><td>{{serija.stVolitev}}</td></tr>
                <tr><td>Žanri:</td><td>
                    % for zanr in serija.zanri:
                        {{zanr + "  "}}
                    % end
                    
                </td></tr>
                <tr><td>Več na:</td><td><a href={{serija.povezava}}>{{serija.povezava}}</a></td>  
            </table>
        </div>

        <div class="epizode">
            <h2>Epizode</h2>
            % if epizode:
                <table class="tabela-epizod">
                    <tr><th>Naslov</th><th>Ocena</th><th>Epizoda</th><th>Sezona</th></tr>
                    % for ep in epizode:
                        <tr>
                            <td><a href="/{{serija.id}}/{{ep[0]}}">{{ep[1]}}</a></td>
                            <td>{{ep[2]}}</td>
                            <td>{{ep[3]}}</td>
                            <td>{{ep[4]}}</td>
                        </tr>
                    % end
                </table>
            % else:
                <p>Ni podatkov o epizodah.</p>
            % end
        </div>
    </div>


    <div class="strani-sezone">
        <form action="/{{serija.id}}" method="get">
            <input type="hidden" name="sezona" value="{{sezona - 1}}">
            <button type="submit" {{'disabled' if sezona <= 1 else ''}}>⟵ Prejšnja sezona</button>
        </form>

        <span>Sezona {{sezona}} / {{stSezon}}</span>

        <form action="/{{serija.id}}" method="get">
            <input type="hidden" name="sezona" value="{{sezona + 1}}">
            <button type="submit" {{'disabled' if sezona >= stSezon else ''}}>Naslednja sezona ⟶</button>
        </form>
    </div>  

</body>
</html>
