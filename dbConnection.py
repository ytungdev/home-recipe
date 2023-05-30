from neo4j import GraphDatabase


class DBconnection:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

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
    conn = DBconnection("bolt://localhost:7687", "neo4j", "password")
    res = conn.query('MATCH (n) RETURN n')
    print(res[0])
    conn.close()