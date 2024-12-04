from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Database connection
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root",
    database="CandidateDonations2023Test"
)
cursor = connection.cursor(dictionary=True)


@app.route('/candidates', methods=['GET'])
def get_candidates():
    cursor.execute("SELECT * FROM 2023Candidates")
    rows = cursor.fetchall()
    return jsonify(rows)

@app.route('/candidates', methods=['GET'])
def get_candidate_by_name():
    first_name = request.args.get('first_name')
    last_name = request.args.get('last_name')
    query = """
        SELECT * FROM 2023Candidates
        WHERE CandidateName_First = %s AND CandidateName_Last = %s
    """
    cursor.execute(query, (first_name, last_name))
    rows = cursor.fetchall()
    return jsonify(rows)

@app.route('/candidates', methods=['GET'])
def get_candidates_by_electorate():
    electorate = request.args.get('electorate')
    query = "SELECT * FROM 2023Candidates WHERE Electorate = %s"
    cursor.execute(query, (electorate,))
    rows = cursor.fetchall()
    return jsonify(rows)

@app.route('/candidates', methods=['GET'])
def get_candidates_by_party():
    party = request.args.get('party')
    query = "SELECT * FROM 2023Candidates WHERE Party = %s"
    cursor.execute(query, (party,))
    rows = cursor.fetchall()
    return jsonify(rows)

if __name__ == "__main__":
    app.run(debug=True)
