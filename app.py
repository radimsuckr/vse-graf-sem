import csv

from neo4j import GraphDatabase

# URI examples: "neo4j://localhost", "neo4j+s://xxx.databases.neo4j.io"
URI = "neo4j://localhost"
AUTH = ("neo4j", "SuperPassw0rd!")

with GraphDatabase.driver(URI, auth=AUTH) as driver:
    driver.verify_connectivity()

# with open("./data/team_details.csv") as f:
#     reader = csv.reader(f)
#     lines = [line for line in reader]

# teams = []
# for line in lines:
#     name = line[4]
#     if name not in teams:
#         teams.append(name)

# with GraphDatabase.driver(URI, auth=AUTH) as db:
#     for ix, team in enumerate(teams):
#         records, summary, keys = db.execute_query(
#             "create (t:Team { id: $id, name: $name }) return t;",
#             id=ix,
#             name=team,
#             database_="neo4j",
#         )

with open("./data/driver_details.csv") as f:
    reader = csv.reader(f)
    lines = [line for line in reader]

# drivers = []
# for line in lines:
#     name = line[2]
#     if name not in drivers:
#         drivers.append(name)

with GraphDatabase.driver(URI, auth=AUTH) as db:
    for ix, line in enumerate(lines[1:]):
        records, summary, keys = db.execute_query(
            """
            MERGE (d:Driver { name: $driver })
            MERGE (t:Team { name: $team })
            MERGE (d)-[:RACED_FOR]->(t)
            """,
            driver=line[2],
            team=line[0],
            database_="neo4j",
        )
