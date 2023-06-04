from neo4j import GraphDatabase


class DBconnection:

    def __init__(self, uri, user, password):
        conn = self.driver = GraphDatabase.driver(uri, auth=(user, password))
        if not conn:
            print("no connection")
            return False

    def close(self):
        self.driver.close()

    def query(self, query, parameters=None, db=None):
        session = None
        response = None
        try: 
            session = self.driver.session() 
            response = list(session.run(query, parameters))
        except Exception as e:
            print("Query failed:", e)
        finally: 
            if session is not None:
                session.close()
        return response



if __name__ == "__main__":
    import os
    from dotenv import load_dotenv

    load_dotenv()
    URL = os.getenv('DATABASE_URL')
    USERNAME = os.getenv('DATABASE_USERNAME')
    PASSWORD = os.getenv('DATABASE_PASSWORD')
    conn = DBconnection(URL, USERNAME, PASSWORD)
    res = conn.query('MATCH (n) RETURN n')
    for r in res:
        print(r)
    conn.close()