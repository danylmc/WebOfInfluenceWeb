from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app) 

#cursor = connection.cursor(dictionary=True)
def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="root",
    )
    return connection

@app.route('/candidates', methods=['GET'])
def get_candidates():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Entities.People")
    rows = cursor.fetchall()
    if not rows:  
        return jsonify({"error": "not found"}), 404
    return jsonify(rows)

@app.route('/party', methods=['GET'])
def get_parties():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Entities.Parties")
    rows = cursor.fetchall()
    if not rows:  
        return jsonify({"error": "not found"}), 404
    return jsonify(rows)

@app.route('/electorate', methods=['GET'])
def get_electorates():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Entities.Electorate")
    rows = cursor.fetchall()
    if not rows:  
        return jsonify({"error": "not found"}), 404
    return jsonify(rows)


@app.route('/party/search-id', methods=['GET'])
def get_parties_by_id():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    party_id = request.args.get('party_id')
    query = """
        SELECT * FROM Entities.Parties
        WHERE id = %s
    """
    cursor.execute(query, (party_id,))
    rows = cursor.fetchall()
    if not rows:  
        return jsonify({"error": "not found"}), 404
    return jsonify(rows)

@app.route('/electorate/search-id', methods=['GET'])
def get_electorates_by_id():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    electorate_id = request.args.get('electorate_id')
    query = """
        SELECT * FROM Entities.Electorates
        WHERE id = %s
    """
    cursor.execute(query, (electorate_id,))
    rows = cursor.fetchone()
    if not rows:  
        return jsonify({"error": "not found"}), 404
    return jsonify(rows)


@app.route('/candidates/search-id', methods=['GET'])
def get_candidate_by_id():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    people_id = request.args.get('people_id')
    query = """
        SELECT * FROM Entities.People
        WHERE id = %s 
    """
    cursor.execute(query, (people_id, ))
    rows = cursor.fetchall()
    if not rows:  
        return jsonify({"error": "not found"}), 404
    return jsonify(rows)


@app.route('/party/search', methods=['GET'])
def get_parties_by_name():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    party_name = request.args.get('party_name')
    query = """
        SELECT * FROM Entities.Parties
        WHERE party_name = %s
    """
    cursor.execute(query, (party_name,))
    rows = cursor.fetchall()
    if not rows:  
        return jsonify({"error": "not found"}), 404
    return jsonify(rows)

@app.route('/electorate/search', methods=['GET'])
def get_electorates_by_name():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    party_name = request.args.get('electorate_name')
    query = """
        SELECT * FROM Entities.Electorates
        WHERE electorate_name = %s
    """
    cursor.execute(query, (party_name,))
    rows = cursor.fetchone()
    if not rows:  
        return jsonify({"error": "not found"}), 404
    return jsonify(rows)


@app.route('/candidates/search', methods=['GET'])
def get_candidate_by_name():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    first_name = request.args.get('first_name')
    last_name = request.args.get('last_name')
    query = """
        SELECT * FROM Entities.People
        WHERE first_name = %s AND last_name = %s
    """
    cursor.execute(query, (first_name, last_name))
    rows = cursor.fetchall()
    if not rows:  
        return jsonify({"error": "not found"}), 404
    return jsonify(rows)

@app.route('/candidates/election-overview/2023', methods=['GET'])
def get_candidates_by_election():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM Overviews_Candidate_Donations_By_Year.2023_Candidate_Donation_Overview"
    cursor.execute(query)
    rows = cursor.fetchall()
    if not rows:  
        return jsonify({"error": "not found"}), 404
    return jsonify(rows)

@app.route('/candidates/election-overview/2023/search/electorate', methods=['GET'])
def get_candidates_by_electorate_2023():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    electorate = request.args.get('electorate_name')
    cursor.execute("SELECT id FROM Entities.Electorates WHERE electorate_name = %s", (electorate,))
    result = cursor.fetchone()
    if not result:
        return jsonify({"error": "Electorate not found"}), 404
    electorate_id = result['id']
    query = "SELECT * FROM Overviews_Candidate_Donations_By_Year.2023_Candidate_Donation_Overview WHERE electorate_id = %s"
    cursor.execute(query, (electorate_id,))
    rows = cursor.fetchall()
    if not rows:  
        return jsonify({"error": "not found"}), 404
    return jsonify(rows)

@app.route('/candidates/election-overview/2023/search/party', methods=['GET'])
def get_candidates_by_party_2023():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    party = request.args.get('party_name')
    cursor.execute("SELECT id FROM Entities.Parties WHERE party_name = %s", (party,))
    result = cursor.fetchone()
    if not result:
        return jsonify({"error": "party not found"}), 404
    party_id = result['id']
    query = "SELECT * FROM Overviews_Candidate_Donations_By_Year.2023_Candidate_Donation_Overview WHERE party_id = %s"
    cursor.execute(query, (party_id,))
    rows = cursor.fetchall()
    if not rows:  
        return jsonify({"error": "not found"}), 404
    return jsonify(rows)

@app.route('/candidates/election-overview/2023/search/name', methods=['GET'])
def get_candidates_by_name_2023():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    first_name = request.args.get('first_name')
    last_name = request.args.get('last_name')
    cursor.execute("SELECT id FROM Entities.People WHERE first_name = %s AND last_name = %s", (first_name, last_name, ))
    result = cursor.fetchone()
    if not result:
        return jsonify({"error": "Name not found "}), 404
    people_id = result['id']
    query = "SELECT * FROM Overviews_Candidate_Donations_By_Year.2023_Candidate_Donation_Overview WHERE people_id = %s"
    cursor.execute(query, (people_id,))
    rows = cursor.fetchall()
    if not rows:  
        return jsonify({"error": "not found"}), 404
    return jsonify(rows)


if __name__ == "__main__":
    app.run(debug=True)
