<!DOCTYPE html>
<html>
<head>
    <title>{{serija.naslov}}</title>
    <style>
        .main-panel {
            border: 1px solid #ccc;
            padding: 20px;
            margin-bottom: 30px;
            background-color: #f9f9f9;
            width: 80%;
        }
        .episode-table {
            width: 80%;
            border-collapse: collapse;
        }
        .episode-table th, .episode-table td {
            border: 1px solid #aaa;
            padding: 8px;
            text-align: left;
        }
    </style>
</head>
<body>

    <h1>{{serija.naslov}}</h1>

    <div class="glavni-panel">
        <h2>Podrobnosti</h2>
        <table>
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

    <h2>Epizode</h2>
    % if epizode:
        <table class="tabela-epizod">
            <tr><th>Naslov</th><th>Ocena</th><th>Epizoda</th><th>Sezona</th></tr>
            % for ep in epizode:
                <tr>
                    <td>{{ep[1]}}</td>
                    <td>{{ep[2]}}</td>
                    <td>{{ep[3]}}</td>
                    <td>{{ep[4]}}</td>
                </tr>
            % end
        </table>
    % else:
        <p>Ni podatkov o epizodah.</p>
    % end

    <div style="display: flex; justify-content: space-between; align-items: center; margin: 10px 0;">
        <form action="/{{serija.id}}" method="get" style="margin: 0;">
            <input type="hidden" name="sezona" value="{{sezona - 1}}">
            <button type="submit" {{'disabled' if sezona <= 1 else ''}}>⟵ Prejšnja sezona</button>
        </form>

        <span>Sezona {{sezona}} / {{stSezon}}</span>

        <form action="/{{serija.id}}" method="get" style="margin: 0;">
            <input type="hidden" name="sezona" value="{{sezona + 1}}">
            <button type="submit" {{'disabled' if sezona >= stSezon else ''}}>Naslednja sezona ⟶</button>
        </form>
    </div>

</body>
</html>
