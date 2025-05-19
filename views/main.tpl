<!DOCTYPE html>
<html>
<head>
    <title>TV Serije</title>
    <link rel="stylesheet" href="/style/main.css">
</head>
<body>
    <h1>Išči serije</h1>

    <div class="glavniOvoj">
        <div class="filtri">
            <form action="/" method="post">
                <fieldset>
                    <legend>Filtri</legend>

                    Naslov: <input type="text" name="naslov" value="{{parametri.get('naslov', '')}}"><br><br>
                    Razvrsti po: <select name="sortirajPo">
                        <option value="zacetekLeto" {{'selected' if parametri.get('sortirajPo') == 'zacetekLeto' else ''}}>Leto</option>
                        <option value="naslov" {{'selected' if parametri.get('sortirajPo') == 'naslov' else ''}}>Naslov</option>
                        <option value="ocena" {{'selected' if parametri.get('sortirajPo') == 'ocena' else ''}}>Ocena</option>
                        <option value="stVolitev" {{'selected' if parametri.get('sortirajPo') == 'stVolitev' else ''}}>Število volitev</option>
                    </select><br><br>
                    Način razvrščanja: <select name="sortiranje">
                        <option value="DESC" {{'selected' if parametri.get('sortiranje') == 'DESC' else ''}}>Padajoče</option>
                        <option value="ASC" {{'selected' if parametri.get('sortiranje') == 'ASC' else ''}}>Naraščajoče</option>
                    </select><br><br>
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
                    <input type="number" name="letoMin"  min="1951" max="2025" value="{{parametri.get('letoMin', 1951)}}" style="width: 60px;">
                    -
                    <input type="number" name="letoMax"  min="1951" max="2025" value="{{parametri.get('letoMax', 2025)}}" style="width: 60px;"><br><br>
                    Ocena (Min - Max): 
                    <input type="number" name="ocenaMin" min="0" max="10" step="0.1" value="{{parametri.get('ocenaMin', 0)}}" style="width: 40px;"> 
                    do 
                    <input type="number" name="ocenaMax" min="0" max="10" step="0.1" value="{{parametri.get('ocenaMax', 10)}}" style="width: 40px;"><br><br>

                    <input type="submit" value="Filtriraj">
                </fieldset>
            </form>
        </div>

        <div class="rezultat">
            <h2>TV Serije</h2>
            % if vrstice:
                <table class="serije-table">
                    <tr>
                        <th>Naslov</th>
                        <th>Leto izida</th>
                        <th>Ocena</th>
                        <th>Število volitev</th>
                    </tr>
                    % for vrstica in vrstice:
                        <tr>
                            % for i in range(1, len(vrstica)):
                                <td>
                                    % if i == 1:
                                        <a href="/{{vrstica[0]}}">{{vrstica[1]}}</a>
                                    % else:
                                        {{vrstica[i]}}
                                    % end
                                </td>
                            % end
                        </tr>
                    % end
                </table>


                <form action="/" method="post" class="strani">
                    % for key, val in parametri.items():
                        % if key != 'stran':
                            <input type="hidden" name="{{key}}" value="{{val}}">
                        % end
                    % end
                    <button type="submit" name="stran" value="{{stran - 1}}" {{'disabled' if stran <= 1 else ''}}>⟵ Prejšnja</button>
                    <span>Stran {{stran}}</span>
                    <button type="submit" name="stran" value="{{stran + 1}}" {{'disabled' if len(vrstice) < naStran else ''}}>Naslednja ⟶</button>
                </form>
            % else:
                <p>No results found.</p>
            % end
        </div>
    </div>
</html>
