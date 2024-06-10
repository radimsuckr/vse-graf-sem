CREATE (charlie:Person:Actor {name: 'Charlie Sheen'})-[:ACTED_IN {role: 'Bud Fox'}]->(wallStreet:Movie {title: 'Wall Street'})<-[:DIRECTED]-(oliver:Person:Director {name: 'Oliver Stone'})


match (d:Driver {name: "Michael Schumacher"})-[r:RACED_FOR]-(t:Team) return d, r, t;
