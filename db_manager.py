import psycopg2

class DBManager:
    def __init__(self):
        self.conn = None
    
    def connect_db(self):
        try:
            self.conn = psycopg2.connect(
                dbname="jeux_olympiques",
                user="postgres",
                password="1234",  
                host="localhost",
                port="5432",
                options="-c client_encoding=UTF8"  # Forcer l'encodage UTF-8
            )
           
        except Exception as e:
            print(f"Erreur lors de la connexion à la base de données : {e}")
    def match_existe(self, id_match):
        """
        Vérifie si un match existe déjà dans la base de données.
        """
        query = "SELECT COUNT(*) FROM match WHERE id_match = %s"
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, (id_match,))
            result = cursor.fetchone()
            return result[0] > 0
        except Exception as e:
            print(f"Erreur lors de la vérification du match : {e}")
            return False
        finally:
            cursor.close()

    def fetch_athletes(self, delegation=None, sexe=None, nom=None, medal=None):
        athletes = []
        
        query = """
            SELECT a.nom_athlete, a.prenom_athlete, a.sexe_athlete, a.id_delegation, m.type_medaille
            FROM athlete a
            LEFT JOIN medaille m ON a.id_athlete = m.id_athlete
            WHERE TRUE
            """
        
        params = []

        if delegation:
            query += " AND a.id_delegation = %s"
            params.append(delegation)
        if sexe:
            query += " AND a.sexe_athlete = %s"
            params.append(sexe)
        if nom:
            query += " AND LOWER(a.nom_athlete) LIKE %s"
            params.append(f"%{nom.lower()}%")
        if medal:
            query += " AND m.type_medaille = %s"
            params.append(medal)  

        if self.conn:
            try:
                cursor = self.conn.cursor()
                cursor.execute(query, params)
                athletes = cursor.fetchall()
            except Exception as e:
                print(f"Erreur lors de la récupération des athlètes : {e}")
            finally:
                cursor.close()
        return athletes
    def fetch_athletes2(self):
        query = """
            SELECT
                a.nom_athlete,
                a.prenom_athlete,
                a.sexe_athlete,
                d.nom_delegation,
                a.id_athlete,
                a.nb_medaille_or,
                a.nb_medaille_argent,
                a.nb_medaille_bronze,
                a.id_discipline
            FROM athlete a
            JOIN delegation d ON a.id_delegation = d.id_delegation
            WHERE (COALESCE(a.nb_medaille_or, 0)
                + COALESCE(a.nb_medaille_argent, 0)
                + COALESCE(a.nb_medaille_bronze, 0)) > 0
            ORDER BY (COALESCE(a.nb_medaille_or, 0)
                    + COALESCE(a.nb_medaille_argent, 0)
                    + COALESCE(a.nb_medaille_bronze, 0)) DESC,
                    a.nb_medaille_or DESC,
                    a.nb_medaille_argent DESC,
                    a.nb_medaille_bronze DESC,
                    a.nom_athlete ASC
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            print(f"Erreur lors de la récupération des athlètes : {e}")
            return []
        finally:
            cursor.close()


    def fetch_delegations(self):
        delegations = []
        if self.conn:
            try:
                cursor = self.conn.cursor()
                cursor.execute("SELECT id_delegation, nom_delegation FROM delegation")
                delegations = cursor.fetchall()
            except Exception as e:
                print(f"Erreur lors de la récupération des délégations : {e}")
            finally:
                cursor.close()
        return delegations
    
    def fetch_delegations2(self):
        delegations = []
        if self.conn:
            try:
                cursor = self.conn.cursor()
                cursor.execute("SELECT nom_delegation FROM delegation ORDER BY nom_delegation ASC")
                result = cursor.fetchall()
                delegations = [row[0] for row in result]  
            except Exception as e:
                print(f"Erreur lors de la récupération des délégations : {e}")
            finally:
                cursor.close()
        return delegations
    def fetch_all_disciplines(self):
        disciplines = []
        if self.conn:
            try:
                cursor = self.conn.cursor()
                cursor.execute("SELECT nom_discipline FROM discipline ORDER BY nom_discipline ASC")
                result = cursor.fetchall()
                # Extraire les noms des délégations (supprimer les accolades ou autres caractères incorrects)
                disciplines = [row[0] for row in result]  # row[0] car fetchall() retourne des tuples
            except Exception as e:
                print(f"Erreur lors de la récupération des disciplines : {e}")
            finally:
                cursor.close()
        return disciplines

    
    def fetch_countries_by_continent(self):
        countries = []
        if self.conn:
            try:
                cursor = self.conn.cursor()
                # Requête pour récupérer les pays et leurs continents
                cursor.execute("SELECT nom_delegation, continent FROM delegation ORDER BY continent, nom_delegation")
                countries = cursor.fetchall()
            except Exception as e:
                print(f"Erreur lors de la récupération des pays : {e}")
            finally:
                cursor.close()
        return countries
    def close(self):
        if self.conn:
            self.conn.close()

    def fetch_athletes(self, delegation=None, sexe=None, nom=None, prenom=None):
        athletes = []
        
        # Requête SQL avec jointure sur les tables delegation et discipline
        query = """
            SELECT a.id_athlete, a.nom_athlete, a.prenom_athlete, a.sexe_athlete, d.nom_delegation, 
                a.nb_medaille_or, a.nb_medaille_argent, a.nb_medaille_bronze, dis.nom_discipline
            FROM athlete a
            LEFT JOIN delegation d ON a.id_delegation = d.id_delegation
            LEFT JOIN discipline dis ON a.id_discipline = dis.id_discipline
            WHERE TRUE
            """
        
        params = []

        if delegation:
            query += " AND a.id_delegation = %s"
            params.append(delegation)
        if sexe:
            query += " AND a.sexe_athlete = %s"
            params.append(sexe)
        if nom:
            query += " AND LOWER(a.nom_athlete) LIKE %s"
            params.append(f"%{nom.lower()}%")  # Recherche partielle sur le nom
        if prenom:
            query += " AND LOWER(a.prenom_athlete) LIKE %s"
            params.append(f"%{prenom.lower()}%")  # Recherche partielle sur le prénom

        if self.conn:
            try:
                cursor = self.conn.cursor()
                cursor.execute(query, params)
                athletes = cursor.fetchall()
            except Exception as e:
                print(f"Erreur lors de la récupération des athlètes : {e}")
            finally:
                cursor.close()
        return athletes
    
    def insert_athlete(self, nom, prenom, sexe, id_delegation, id_discipline):
        query = """
            INSERT INTO athlete (nom_athlete, prenom_athlete, sexe_athlete, id_delegation, id_discipline)
            VALUES (%s, %s, %s, %s, %s)
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, (nom, prenom, sexe, id_delegation, id_discipline))
            self.conn.commit()
            print(f"Athlète {nom} {prenom} ajouté avec succès.")
        except Exception as e:
            self.conn.rollback()  # Annuler les changements en cas d'erreur
            print(f"Erreur lors de l'ajout de l'athlète : {e}")
        finally:
            cursor.close()
    def update_athlete(self, id_athlete, nom, prenom, sexe, id_delegation, nb_medaille_or, nb_medaille_argent, nb_medaille_bronze, id_discipline):
        query = """
            UPDATE athlete
            SET nom_athlete = %s, prenom_athlete = %s, sexe_athlete = %s, 
                id_delegation = %s, nb_medaille_or = %s, nb_medaille_argent = %s, 
                nb_medaille_bronze = %s, id_discipline = %s
            WHERE id_athlete = %s
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, (nom, prenom, sexe, id_delegation, nb_medaille_or, nb_medaille_argent, nb_medaille_bronze, id_discipline, id_athlete))
            self.conn.commit()
            print(f"Athlète {nom} {prenom} mis à jour avec succès.")
        except Exception as e:
            self.conn.rollback()  # Annuler les changements en cas d'erreur
            print(f"Erreur lors de la mise à jour de l'athlète : {e}")
        finally:
            cursor.close()

    def fetch_athlete_by_id(self, id_athlete):
        query = """
            SELECT nom_athlete, prenom_athlete, sexe_athlete, id_delegation, 
                nb_medaille_or, nb_medaille_argent, nb_medaille_bronze, id_discipline
            FROM athlete
            WHERE id_athlete = %s
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, (id_athlete,))
            athlete = cursor.fetchone()
            return athlete
        except Exception as e:
            print(f"Erreur lors de la récupération de l'athlète : {e}")
            return None
        finally:
            cursor.close()


    def delete_athlete(self, id_athlete):
        query = "DELETE FROM athlete WHERE id_athlete = %s"
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, (id_athlete,))
            self.conn.commit()
            print(f"Athlète avec l'ID {id_athlete} supprimé avec succès.")
        except Exception as e:
            self.conn.rollback()  # Annuler les changements en cas d'erreur
            print(f"Erreur lors de la suppression de l'athlète : {e}")
        finally:
            cursor.close()
    def insert_match(self, id_match, id_evenement, phase, date):
        query = """
            INSERT INTO match (id_match, id_evenement, phase, date)
            VALUES (%s, %s, %s, %s)
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, (id_match, id_evenement, phase, date))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            cursor.close()

    def insert_participant(self, participant_type, id_athlete):
        query = """
            INSERT INTO participant (type, id_athlete)
            VALUES (%s, %s) RETURNING id_participant
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, (participant_type, id_athlete))
            id_participant = cursor.fetchone()[0]
            self.conn.commit()
            return id_participant
        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            cursor.close()
    def insert_participation(self, id_match, id_participant, resultat, medaille, type_resultat):
        query = """
            INSERT INTO participation (id_match, id_participant, resultat, medaille, type_resultat)
            VALUES (%s, %s, %s, %s, %s)
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, (id_match, id_participant, resultat, medaille, type_resultat))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            cursor.close()

    def fetch_participations_by_match(self, id_match):
        query = """
            SELECT COALESCE(a.nom_athlete || ' ' || a.prenom_athlete, d.nom_delegation) AS participant_name,
                e.nom_evenement, p.resultat, p.medaille, p.type_resultat
            FROM participation p
            LEFT JOIN participant par ON p.id_participant = par.id_participant
            LEFT JOIN athlete a ON par.id_athlete = a.id_athlete
            LEFT JOIN delegation d ON par.id_delegation = d.id_delegation
            LEFT JOIN match m ON p.id_match = m.id_match
            LEFT JOIN evenement e ON m.id_evenement = e.id_evenement
            WHERE p.id_match = %s
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, (id_match,))
            participations = cursor.fetchall()
            return participations
        except Exception as e:
            print(f"Erreur lors de la récupération des participations : {e}")
            return []
        finally:
            cursor.close()


    def fetch_all_matches(self):
        query = "SELECT * FROM match"
        cursor = self.conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()

    def fetch_all_participants(self):
        query = "SELECT * FROM participant"
        cursor = self.conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()
    def fetch_delegations_sorted_by_medals(self):
        query = """
            SELECT
                d.id_delegation,
                d.nom_delegation,
                d.continent,
                COALESCE(d.nb_medaille_or, 0) AS or_,
                COALESCE(d.nb_medaille_argent, 0) AS argent,
                COALESCE(d.nb_medaille_bronze, 0) AS bronze
            FROM delegation d
            WHERE (COALESCE(d.nb_medaille_or, 0)
                + COALESCE(d.nb_medaille_argent, 0)
                + COALESCE(d.nb_medaille_bronze, 0)) > 0
            ORDER BY (COALESCE(d.nb_medaille_or, 0)
                    + COALESCE(d.nb_medaille_argent, 0)
                    + COALESCE(d.nb_medaille_bronze, 0)) DESC,
                    COALESCE(d.nb_medaille_or, 0) DESC,
                    COALESCE(d.nb_medaille_argent, 0) DESC,
                    COALESCE(d.nb_medaille_bronze, 0) DESC,
                    d.nom_delegation ASC
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            return cursor.fetchall()
        
        except Exception as e:
            print(f"Erreur lors de la récupération des délégations : {e}")
            return []
        finally:
            cursor.close()
    def fetch_all_participations(self):
        query = "SELECT * FROM participation"
        cursor = self.conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()

    # Pour mettre à jour une entrée dans les tables
    def update_match(self, id_match, id_evenement, phase, date):
        query = "UPDATE match SET id_evenement = %s, phase = %s, date = %s WHERE id_match = %s"
        cursor = self.conn.cursor()
        cursor.execute(query, (id_evenement, phase, date, id_match))
        self.conn.commit()

    def update_participant(self, id_participant, participant_type, id_athlete, id_delegation):
        query = "UPDATE participant SET type = %s, id_athlete = %s, id_delegation = %s WHERE id_participant = %s"
        cursor = self.conn.cursor()
        cursor.execute(query, (participant_type, id_athlete, id_delegation, id_participant))
        self.conn.commit()

    def update_participation(self, id_participation, resultat, medaille, type_resultat):
        query = "UPDATE participation SET resultat = %s, medaille = %s, type_resultat = %s WHERE id_participation = %s"
        cursor = self.conn.cursor()
        cursor.execute(query, (resultat, medaille, type_resultat, id_participation))
        self.conn.commit()

    # Pour supprimer une entrée dans les tables
    def delete_match(self, id_match):
        query = "DELETE FROM match WHERE id_match = %s"
        cursor = self.conn.cursor()
        cursor.execute(query, (id_match,))
        self.conn.commit()

    def delete_participant(self, id_participant):
        query = "DELETE FROM participant WHERE id_participant = %s"
        cursor = self.conn.cursor()
        cursor.execute(query, (id_participant,))
        self.conn.commit()

    def delete_participation(self, id_match, id_participant):
        query = "DELETE FROM participation WHERE id_match = %s AND id_participant = %s"
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, (id_match, id_participant))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            cursor.close()

    def update_match(self, id_match, id_evenement, phase, date):
        query = """
            UPDATE match
            SET id_evenement = %s, phase = %s, date = %s
            WHERE id_match = %s
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, (id_evenement, phase, date, id_match))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            cursor.close()

    """def fetch_delegations_sorted_by_medals(self):
        delegations = []
        query = 
            SELECT id_delegation, nom_delegation, continent, nb_medaille_or, nb_medaille_argent, nb_medaille_bronze
            FROM delegation
            ORDER BY (nb_medaille_or + nb_medaille_argent + nb_medaille_bronze) DESC
        
        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            delegations = cursor.fetchall()
        except Exception as e:
            print(f"Erreur lors de la récupération des délégations : {e}")
        finally:
            cursor.close()
        
        return delegations"""

    def fetch_epreuves_filtrees(self, date, equipe=None, sport=None, genre=None, phase=None):
        epreuves = []
        if self.conn:
            cursor = None
            try:
                cursor = self.conn.cursor()

                query = """
                    SELECT DISTINCT
                        ev.nom_evenement,
                        m.phase
                    FROM match m
                    JOIN evenement ev ON m.id_evenement = ev.id_evenement
                    JOIN discipline dis ON ev.id_discipline = dis.id_discipline

                    LEFT JOIN participation p ON p.id_match = m.id_match
                    LEFT JOIN participant par ON par.id_participant = p.id_participant
                    LEFT JOIN delegation d ON d.id_delegation = par.id_delegation

                    WHERE m.date::date = %s
                """
                params = [date]

                # Filtrer par équipe (nom de délégation)
                if equipe and equipe != "Toutes les équipes":
                    query += " AND d.nom_delegation = %s"
                    params.append(equipe)

                # Filtrer par sport (discipline)
                if sport and sport != "Tous les sports":
                    query += " AND dis.nom_discipline = %s"
                    params.append(sport)

                # Filtrer par genre
                if genre and genre != "Toutes genres":
                    query += " AND ev.sexe_participants = %s"
                    params.append(genre)

                # Filtrer par phase
                if phase and phase != "Toutes les phases":
                    query += " AND m.phase = %s"
                    params.append(phase)

                cursor.execute(query, params)
                epreuves = cursor.fetchall()

            except Exception as e:
                print(f"Erreur lors de la récupération des épreuves filtrées : {e}")
                self.conn.rollback()
            finally:
                if cursor:
                    cursor.close()

        return epreuves


    def get_id_match_from_evenement(self, nom_evenement):
        id_match = None
        if self.conn:
            try:
                cursor = self.conn.cursor()

                # Requête pour récupérer l'id_match à partir du nom de l'événement
                query = """
                    SELECT m.id_match
                    FROM match m
                    JOIN evenement ev ON m.id_evenement = ev.id_evenement
                    WHERE ev.nom_evenement = %s
                    LIMIT 1  -- Si plusieurs matchs existent pour cet événement, on en récupère un seul
                """
                cursor.execute(query, (nom_evenement,))
                result = cursor.fetchone()

                if result:
                    id_match = result[0]  # Récupérer l'id_match

            except Exception as e:
                print(f"Erreur lors de la récupération de l'ID du match : {e}")
                self.conn.rollback()
            finally:
                cursor.close()

        return id_match





