# Neo4j Racing Teams API

Tato aplikace je webová služba vytvořená v Pythonu s využitím Flask frameworku. Slouží k interakci s databází Neo4j, která ukládá informace o závodních jezdcích, týmech a výsledcích závodů. Aplikace umožňuje provádět dotazy a manipulace s těmito daty prostřednictvím REST API.
Požadavky

    Python 3.8 nebo novější
    Neo4j 4.x nebo novější
    Flask
    Neo4j Python Driver

## Data 

Data jsou z Kaggle z datasetu [https://www.kaggle.com/datasets/debashish311601/formula-1-official-data-19502022](https://www.kaggle.com/datasets/debashish311601/formula-1-official-data-19502022).

## Instalace

Klonujte tento repozitář:

    git clone https://github.com/radimsuckr/neo4j-racing-teams-api.git
    cd neo4j-racing-teams-api

Vytvořte a aktivujte virtuální prostředí:

    python -m venv venv
    source venv/bin/activate  # Na Windows použijte `venv\Scripts\activate`

Nainstalujte závislosti:

    pip install -r requirements.txt

Nakonfigurujte připojení k databázi Neo4j v souboru app.py:

    URI = "neo4j://localhost:7687"
    AUTH = ("neo4j", "SuperPassw0rd!")

## Použití

Spusťte aplikaci:

    flask --app app run --reload

Případně jiným WSGI serverem.

Aplikace poběží na `http://localhost:5000`.

## REST API 

1. Získání seznamu jezdců a týmů, pro které závodili

- Endpoint: `/`
- Metoda: `GET`
- Parametry URL: driver (volitelně), team (volitelně)
- Popis: Vrací seznam jezdců a týmů, pro které závodili. Možno filtrovat podle jména jezdce, týmu nebo obojího.

2. Získání týmů, které mají nejvíce společných jezdců s daným týmem

- Endpoint: `/similar-teams/<team>`
- Metoda: `GET`
- Popis: Vrací pět týmů, které mají nejvíce společných jezdců s daným týmem.

3. Získání jezdců se stejným výsledkem v určitém závodě (Grand Prix)

- Endpoint: `/same-grand-prix-position/<gp>/<position>`
- Metoda: `GET`
- Popis: Vrací seznam jezdců, kteří dosáhli stejné pozice v zadaném závodě.

4. Získání jezdců, kteří změnili tým více než zadaný početkrát

- Endpoint: `/drivers-who-changed-teams`
- Metoda: `GET`
- Parametry URL: threshold (volitelně, výchozí hodnota je 1)
- Popis: Vrací seznam jezdců, kteří změnili tým více než threshold krát.

5. Vytvoření nového jezdce

- Endpoint: `/driver`
- Metoda: `POST`
- Tělo požadavku (JSON): `{ "name": "New Driver" }`
- Popis: Vytvoří nového jezdce v databázi Neo4j.

6. Smazání jezdce podle jména

- Endpoint: `/driver`
- Metoda: `DELETE`
- Tělo požadavku (JSON): `{ "name": "New Driver" }`
- Popis: Smaže jezdce z databáze podle jeho jména.

7. Získaní jezdce podle jména

- Endpoint: `/driver/<name>`
- Metoda: `GET`
- Parametry URL: name (požadováno)
- Popis: Smaže jezdce z databáze podle jeho jména.

8. Nejkratší cesta mezi dvěma jezdci

- Endpoint: `/common-path-between-drivers/<driver1>/<driver2>`
- Metoda: `GET`
- Parametry URL: driver1 (požadováno), driver2 (požadováno)
- Popis: Vrátí nejkratší cestu skrz týmy a jezdce mezi dvěma zadanými jezdci
