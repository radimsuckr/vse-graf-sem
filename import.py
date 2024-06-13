#!/usr/bin/env python
from neo4j import GraphDatabase

URI = "neo4j://localhost"
AUTH = ("neo4j", "SuperPassw0rd!")

with GraphDatabase.driver(URI, auth=AUTH) as db:
    db.verify_connectivity()
    records, sumary, keys = db.execute_query("""
LOAD CSV WITH HEADERS FROM 'file:///driver_details.csv' AS row
WITH row
WHERE row.Driver IS NOT NULL AND row.GrandPrix IS NOT NULL
WITH row,
     coalesce(row.Car, "Unknown") AS teamName,
     coalesce(toString(row.RacePosition), "Unknown") AS racePosition,
     coalesce(row.PTS, 0) AS points
MERGE (d:Driver {name: row.Driver})
MERGE (t:Team {name: teamName})
MERGE (g:GPResult {name: row.GrandPrix, year: row.Year})
ON CREATE SET g.position = racePosition, g.points = points
WITH d, t, g
MERGE (d)-[:RACED_FOR]->(t)
MERGE (d)-[:RACED_IN]->(g)
MERGE (t)-[:RACED_IN]->(g);
""")
    #         """
    # LOAD CSV WITH HEADERS FROM 'file:///driver_details.csv' AS row
    #     WITH row
    #     MERGE (d:Driver { name: row.Driver })
    #     MERGE (t:Team { name: coalesce(row.Car, "Unknown") })
    #     MERGE (g:GPResult { name: row.GrandPrix, position: coalesce(toString(row.RacePosition), "Unknown"), points: coalesce(row.PTS, 0), year: row.Year })
    #     MERGE (d)-[:RACED_FOR]->(t)
    #     MERGE (d)-[:RACED_IN]->(g)
    #     MERGE (t)-[:RACED_IN]->(g)
    #             """
