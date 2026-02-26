from flask import Flask, jsonify, request, g
import psycopg2
import os

app = Flask(__name__)

# Connexion à la base de données 
def get_db():
    if 'db' not in g:
        g.db = psycopg2.connect(
            dbname="jeux_olympiques",
            user="postgres",
            password="1234",
            host="localhost",  
            port="5432"        
        )
    return g.db

@app.teardown_appcontext
def close_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

# Route pour récupérer tous les athlètes (GET)
@app.route('/athletes', methods=['GET'])
def get_athletes():
    cur = get_db().cursor()
    cur.execute("SELECT id_athlete, nom_athlete, prenom_athlete, sexe_athlete, id_delegation, nb_medaille_or, nb_medaille_argent, nb_medaille_bronze, id_discipline FROM athlete")
    rows = cur.fetchall()
    athletes = [{
        'id_athlete': row[0], 
        'nom_athlete': row[1], 
        'prenom_athlete': row[2], 
        'sexe_athlete': row[3], 
        'id_delegation': row[4], 
        'nb_medaille_or': row[5], 
        'nb_medaille_argent': row[6], 
        'nb_medaille_bronze': row[7],
        'id_discipline': row[8]
    } for row in rows]
    cur.close()
    return jsonify(athletes)



# Route pour récupérer un athlète par ID (GET)
@app.route('/athletes/<int:id_athlete>', methods=['GET'])
def get_athlete(id_athlete):
    cur = get_db().cursor()
    cur.execute("SELECT id_athlete, nom_athlete, prenom_athlete, sexe_athlete, id_delegation, nb_medaille_or, nb_medaille_argent, nb_medaille_bronze, id_discipline FROM athlete WHERE id_athlete = %s", (id_athlete,))
    row = cur.fetchone()
    cur.close()
    if row:
        athlete = {
            'id_athlete': row[0], 
            'nom_athlete': row[1], 
            'prenom_athlete': row[2], 
            'sexe_athlete': row[3], 
            'id_delegation': row[4], 
            'nb_medaille_or': row[5], 
            'nb_medaille_argent': row[6], 
            'nb_medaille_bronze': row[7],
            'id_discipline': row[8]
        }
        return jsonify(athlete)
    return jsonify({"error": "Athlete not found"}), 404

# Route pour ajouter un athlète (POST)
@app.route('/athletes', methods=['POST'])
def add_athlete():
    new_athlete = request.json
    cur = get_db().cursor()
    cur.execute("""
        INSERT INTO athlete (nom_athlete, prenom_athlete, sexe_athlete, id_delegation, nb_medaille_or, nb_medaille_argent, nb_medaille_bronze, id_discipline) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id_athlete
        """, 
        (new_athlete['nom_athlete'], new_athlete['prenom_athlete'], new_athlete['sexe_athlete'], new_athlete['id_delegation'], 
         new_athlete['nb_medaille_or'], new_athlete['nb_medaille_argent'], new_athlete['nb_medaille_bronze'], new_athlete['id_discipline'])
    )
    new_id = cur.fetchone()[0]
    get_db().commit()
    cur.close()
    new_athlete['id_athlete'] = new_id
    return jsonify(new_athlete), 201

# Route pour mettre à jour un athlète (PUT)
@app.route('/athletes/<int:id_athlete>', methods=['PUT'])
def update_athlete(id_athlete):
    update_data = request.json
    cur = get_db().cursor()
    cur.execute("""
        UPDATE athlete 
        SET nom_athlete = %s, prenom_athlete = %s, sexe_athlete = %s, id_delegation = %s, nb_medaille_or = %s, nb_medaille_argent = %s, nb_medaille_bronze = %s, id_discipline = %s
        WHERE id_athlete = %s
        """, 
        (update_data['nom_athlete'], update_data['prenom_athlete'], update_data['sexe_athlete'], update_data['id_delegation'], 
         update_data['nb_medaille_or'], update_data['nb_medaille_argent'], update_data['nb_medaille_bronze'], update_data['id_discipline'], id_athlete)
    )
    get_db().commit()
    cur.close()
    return jsonify(update_data)

# Route pour supprimer un athlète (DELETE)
@app.route('/athletes/<int:id_athlete>', methods=['DELETE'])
def delete_athlete(id_athlete):
    cur = get_db().cursor()
    cur.execute("DELETE FROM athlete WHERE id_athlete = %s", (id_athlete,))
    get_db().commit()
    cur.close()
    return '', 204

# Route pour récupérer tous les delegation (GET)
@app.route('/delegation', methods=['GET'])
def get_delegations ():
    cur = get_db().cursor()
    cur.execute("SELECT id_delegation, nom_delegation, continent, nb_medaille_or, nb_medaille_argent, nb_medaille_bronze FROM delegation")
    rows = cur.fetchall()
    delegations = [{
        'id_delegation': row[0], 
        'nom_delegation': row[1], 
        'continent': row[2], 
        'nb_medaille_or': row[3], 
        'nb_medaille_argent': row[4], 
        'nb_medaille_bronze': row[5] 
        
    } for row in rows]
    cur.close()
    return jsonify(delegations)
 
#Route pour récupérer tous les discipline (GET)
@app.route('/discipline',methods=['GET'])
def get_disciplines():
    cur=get_db().cursor()
    cur.execute("Select id_discipline, nom_discipline FROM discipline")
    rows = cur.fetchall()
    discipline=[{
        'id_discipline' : row[0],
        'nom_discipline' : row[1]
    }for row in rows]
    
    cur.close()
    return jsonify(discipline)


#Route pour récupérer la liste des médailles pour un pays :

@app.route('/medaille_pays',methods=["GET"])
def get_delegation_medaille():
    cur=get_db().cursor()
    query = """ 
            SELECT id_delegation, nom_delegation, continent, nb_medaille_or,
             nb_medaille_argent, nb_medaille_bronze
            FROM delegation
            ORDER BY (nb_medaille_or + nb_medaille_argent + nb_medaille_bronze) DESC
        """
    cur.execute(query)
    rows = cur.fetchall()
    
    delegation_medaille = [
        {
            'id_delegation': row[0],
            'nom_delegation': row[1],
            'continent': row[2],
            'nb_medaille_or': row[3],
            'nb_medaille_argent': row[4],
            'nb_medaille_bronze': row[5]
        } for row in rows
    ]
    
    cur.close()
    return jsonify(delegation_medaille)



#Route pour médailles gagnées par un sportif

@app.route('/medaille_athelets',methods=["GET"])

def get_athlete_medaille():
    cur=get_db().cursor()

    id_athlete = request.args.get('id_athlete')

    if not id_athlete:
        return jsonify({"error": "id_athlete parameter is required"}), 404

    query='''SELECT  nom_athlete, prenom_athlete, sexe_athlete,  
    nb_medaille_or, nb_medaille_argent, nb_medaille_bronze, 
    id_discipline FROM athlete WHERE id_athlete = %s'''

    cur.execute(query, (id_athlete,))
    row = cur.fetchone()
    cur.close()
    if row:
        athlete = {
            
            'nom_athlete': row[0], 
            'prenom_athlete': row[1], 
            'sexe_athlete': row[2], 
            'nb_medaille_or': row[3], 
            'nb_medaille_argent': row[4], 
            'nb_medaille_bronze': row[5],
            'id_discipline': row[6]
        }
        return jsonify(athlete)
    return jsonify({"error": "Athlete not found"}), 404


if __name__ == '__main__':
    app.run(debug=True)
