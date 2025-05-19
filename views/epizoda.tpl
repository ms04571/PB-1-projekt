<!DOCTYPE html>
<html>
<head>
    <title>{{epizoda.naslov}}</title>
    <link rel="stylesheet" href="/style/main.css">
</head>
<body>
    <h1>{{epizoda.naslov}}</h1>

    <div class="epizoda-container">
        <div class="epizoda-info">
            <table class="epizoda-table">
                <tr><td>Serija:</td><td><a href="/{{epizoda.serijaId}}">{{epizoda.serijaNaslov}}</a></td></tr>
                <tr><td>Sezona:</td><td>{{epizoda.sezona}}</td></tr>
                <tr><td>Epizoda:</td><td>{{epizoda.epizoda}}</td></tr>
                <tr><td>Leto:</td><td>{{epizoda.leto}}</td></tr>
                <tr><td>Ocena:</td><td>{{epizoda.ocena}}</td></tr>
                <tr><td>Število volitev:</td><td>{{epizoda.stVolitev}}</td></tr>
                <tr>
                    <td>Žanri:</td>
                    <td>
                        % for zanr in epizoda.zanri:
                            {{zanr + " "}}
                        % end    
                    </td>
                </tr>
                <tr>
                    <td>Več na:</td>
                    <td><a href="{{epizoda.povezava}}">{{epizoda.povezava}}</a></td>
                </tr>
            </table>

            <p><a href="/{{epizoda.serijaId}}">⟵ Nazaj na serijo</a></p>
        </div>
    </div>
</body>
</html>