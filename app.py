from flask import Flask, abort, jsonify, request
from neo4j import GraphDatabase


class Query:
    def __init__(self, driver):
        self._driver = driver

    def create_driver(self, name):
        query = "CREATE (d:Driver {name: $driverName})"
        self._driver.execute_query(query, parameters_={"driverName": name})
        return True

    def read_driver(self, name):
        query = "MATCH (d:Driver {name: $driverName}) RETURN d.name AS name"
        records, summary, keys = self._driver.execute_query(
            query, parameters_={"driverName": name}
        )
        results = [{"driver": r["name"]} for r in records]
        return results

    def delete_driver(self, name):
        try:
            query = "MATCH (d:Driver {name: $driverName}) DETACH DELETE d"
            self._driver.execute_query(query, parameters_={"driverName": name})
            return True
        except Exception as e:
            print(f"Failed to delete driver: {str(e)}")
            return False

    def get_drivers_racing_for_teams(self):
        driver = request.args.get("driver")
        team = request.args.get("team")
        match (isinstance(driver, str), isinstance(team, str)):
            case False, False:
                query = "MATCH (d:Driver)-[r:RACED_FOR]-(t:Team) RETURN d.name as driver, t.name as team;"
            case True, False:
                query = "MATCH (d:Driver {name: $driver})-[r:RACED_FOR]-(t:Team) RETURN d.name as driver, t.name as team;"
            case False, True:
                query = "MATCH (d:Driver)-[r:RACED_FOR]-(t:Team {name: $team}) RETURN d.name as driver, t.name as team;"
            case True, True:
                query = "MATCH (d:Driver {name: $driver})-[r:RACED_FOR]-(t:Team {name: $team}) RETURN d.name as driver, t.name as team;"
        records, summary, keys = self._driver.execute_query(
            query, parameters_={"driver": driver, "team": team}
        )
        results = [
            {
                "driver": r["driver"],
                "team": r["team"],
            }
            for r in records
        ]
        return results

    def get_other_teams_with_most_common_drivers(self, team: str):
        records, summary, keys = self._driver.execute_query(
            """
MATCH (team:Team {name: $teamName})<-[:RACED_FOR]-(driver:Driver)-[:RACED_FOR]->(otherTeam:Team)
WHERE team <> otherTeam
WITH otherTeam, count(driver) AS commonDriversCount
RETURN otherTeam.name AS Team, commonDriversCount
ORDER BY commonDriversCount DESC
LIMIT 5
        """,
            parameters_={"teamName": team},
        )
        teams = [
            {"team": r["Team"], "commonDrivers": r["commonDriversCount"]}
            for r in records
        ]
        return teams

    def get_drivers_with_same_result_in_grandprix(self, grandprix: str, position: str):
        records, summary, keys = self._driver.execute_query(
            """
MATCH (d1:Driver)-[:RACED_IN]->(g:GPResult {name: $grandprix})<-[:RACED_IN]-(d2:Driver)
WHERE g.position = $position
WITH DISTINCT d1, g
RETURN d1.name AS firstDriver, g.name AS gpName, g.year AS gpYear, g.position AS position
ORDER BY gpYear DESC
        """,
            parameters_={"grandprix": grandprix, "position": position},
        )
        results = [
            {
                "driver": r["firstDriver"],
                "grandPrix": r["gpName"],
                "year": r["gpYear"],
                "position": r["position"],
            }
            for r in records
        ]
        return results

    def get_drivers_who_changed_teams(self, threshold=1):
        records, summary, keys = self._driver.execute_query(
            f"""
MATCH (d:Driver)-[:RACED_FOR]->(t:Team)
WITH d, count(distinct t) AS numTeams
WHERE numTeams > {threshold}
RETURN d.name AS driverName, numTeams
ORDER BY numTeams DESC
            """
        )
        results = [
            {
                "driver": r["driverName"],
                "numTeams": r["numTeams"],
            }
            for r in records
        ]
        return results

    def common_path_between_drivers(self, driver1, driver2):
        records, summary, keys = self._driver.execute_query(
            """
MATCH (d1:Driver {name: $driver1}), (d2:Driver {name: $driver2})
MATCH path = shortestPath((d1)-[:RACED_FOR*]-(d2))
RETURN nodes(path) as nodes, relationships(path) as edges
            """,
            parameters_={"driver1": driver1, "driver2": driver2},
        )
        results = [r._properties["name"] for r in records[0]["nodes"]]
        return results


URI = "neo4j://localhost"
AUTH = ("neo4j", "SuperPassw0rd!")


with GraphDatabase.driver(URI, auth=AUTH) as driver:
    driver.verify_connectivity()
    q = Query(driver=driver)


app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return q.get_drivers_racing_for_teams()


@app.route("/similar-teams/<team>", methods=["GET"])
def similar_teams(team):
    return q.get_other_teams_with_most_common_drivers(team)


@app.route("/same-grand-prix-position/<gp>/<position>", methods=["GET"])
def same_grand_prix_position(gp, position):
    return q.get_drivers_with_same_result_in_grandprix(grandprix=gp, position=position)


@app.route("/drivers-who-changed-teams", methods=["GET"])
def drivers_who_changed_teams():
    threshold = request.args.get("threshold")
    return q.get_drivers_who_changed_teams(threshold)


@app.route("/driver", methods=["POST"])
def create_driver():
    data = request.json
    if not data or "name" not in data:
        abort(400, "Request must contain JSON data with 'name' field.")

    driver_name = data["name"]
    try:
        q.create_driver(driver_name)
        return jsonify(
            {"message": f"Driver '{driver_name}' successfully created."}
        ), 201
    except Exception as e:
        abort(500, f"Failed to create driver: {str(e)}")


@app.route("/driver/<name>", methods=["GET"])
def read_driver(name):
    return q.read_driver(name)


@app.route("/driver", methods=["DELETE"])
def delete_driver():
    data = request.json
    if not data or "name" not in data:
        abort(400, "Request must contain JSON data with 'name' field.")

    driver_name = data["name"]

    if q.delete_driver(driver_name):
        return jsonify(
            {"message": f"Driver '{driver_name}' successfully deleted."}
        ), 200
    else:
        abort(500, f"Failed to delete driver '{driver_name}'.")


@app.route("/common-path-between-drivers/<driver1>/<driver2>", methods=["GET"])
def common_path_between_drivers(driver1, driver2):
    return q.common_path_between_drivers(driver1, driver2)
