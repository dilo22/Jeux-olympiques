from flask import Flask
import psycopg2

app = Flask(__name__)

# Fonction pour exécuter une requête SQL
def execute_query(query):
    try:
        # Connexion à la base de données PostgreSQL
        conn = psycopg2.connect(
            dbname="jeux_olympiques",
            user="postgres",
            password="",
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()
        
        cursor.execute(query)
        
        # Validation et fermeture 
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Erreur lors de l'exécution de la requête: {e}")

# Fonction pour créer les tables
def create_tables():

    execute_query('''
    CREATE TABLE IF NOT EXISTS discipline (
        id_discipline SERIAL PRIMARY KEY,
        nom_discipline TEXT NOT NULL
    )
    ''')

   
    execute_query('''
    CREATE TABLE IF NOT EXISTS evenement (
        id_evenement SERIAL PRIMARY KEY,
        nom_evenement TEXT NOT NULL,
        categorie TEXT NOT NULL CHECK(categorie IN ('W', 'X', 'M', 'O')),
        id_discipline INTEGER,
        FOREIGN KEY (id_discipline) REFERENCES discipline(id_discipline)
    )
    ''')

    
    execute_query('''
    CREATE TABLE IF NOT EXISTS delegation (
        id_delegation SERIAL PRIMARY KEY,
        nom_delegation TEXT NOT NULL
    )
    ''')

    
    execute_query('''
    CREATE TABLE IF NOT EXISTS athlete (
        id_athlete SERIAL PRIMARY KEY,
        nom_athlete TEXT NOT NULL,
        prenom_athlete TEXT NOT NULL,
        sexe_athlete TEXT NOT NULL CHECK(sexe_athlete IN ('H', 'F')),
        id_delegation INTEGER,
        FOREIGN KEY (id_delegation) REFERENCES delegation(id_delegation)
    )
    ''')

   
    execute_query('''
    CREATE TABLE IF NOT EXISTS participation (
        id_participation SERIAL PRIMARY KEY,
        id_athlete INTEGER,
        id_evenement INTEGER,
        resultat TEXT,
        medaille TEXT CHECK(medaille IN ('OR', 'ARGENT', 'BRONZE', NULL)),
        FOREIGN KEY (id_athlete) REFERENCES athlete(id_athlete),
        FOREIGN KEY (id_evenement) REFERENCES evenement(id_evenement)
    )
    ''')

   
    execute_query('''
    CREATE TABLE IF NOT EXISTS medaille (
        id_medaille SERIAL PRIMARY KEY,
        type_medaille TEXT NOT NULL CHECK(type_medaille IN ('OR', 'ARGENT', 'BRONZE')),
        id_evenement INTEGER,
        id_athlete INTEGER,
        id_delegation INTEGER,
        FOREIGN KEY (id_evenement) REFERENCES evenement(id_evenement),
        FOREIGN KEY (id_athlete) REFERENCES athlete(id_athlete),
        FOREIGN KEY (id_delegation) REFERENCES delegation(id_delegation)
    )
    ''')

    execute_query('''
    CREATE TABLE IF NOT EXISTS calendrier (
        id_calendrier SERIAL PRIMARY KEY,
        id_evenement INTEGER,
        date_evenement DATE NOT NULL,
        heure_debut TIME NOT NULL,
        heure_fin TIME NOT NULL,
        FOREIGN KEY (id_evenement) REFERENCES evenement(id_evenement)
    )
    ''')

    execute_query('''
    CREATE TABLE IF NOT EXISTS athlete_medaille (
        id SERIAL PRIMARY KEY,
        id_athlete INTEGER,
        id_medaille INTEGER,
        nombre_medailles INTEGER NOT NULL,
        FOREIGN KEY (id_athlete) REFERENCES athlete(id_athlete),
        FOREIGN KEY (id_medaille) REFERENCES medaille(id_medaille)
    )
    ''')

# Route pour créer les tables
@app.route('/create_tables')
def create_db_tables():
    create_tables()
    return "Tables créées avec succès!"

if __name__ == '__main__':
    app.run()





