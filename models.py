from dbConnection import DBconnection

db = DBconnection("bolt://localhost:7687", "neo4j", "password")


class Ingredient:
    @staticmethod
    def format(name, chi=False):
        if not chi:
            return name.capitalize()
        else:
            return name if name == "" else f"({name})"

    def serialize_reulst(self, data):
        # print(data)
        return {
            'name': data['result']['name'],
            'name_chi': data['result']['name_chi'],
        }
    
    def getAll(self):
        q = 'MATCH (n:Ingredient) RETURN n as result'
        res = db.query(q)
        return [self.serialize_reulst(record.data()) for record in res]

    def add(self, name, name_chi):
        q = f'CREATE (d:Ingredient{{name:\"{name}\",name_chi:\"{name_chi}\"}}) RETURN d as result'
        res = db.query(q)
        print(q, res)
        return [self.serialize_reulst(record.data()) for record in res]


class Dish:
    @staticmethod
    def format(name, chi=False):
        if not chi:
            return name.capitalize()
        else:
            return name if name == "" else f"({name})"

    def serialize_reulst(self, data):
        # print(data)
        return {
            'name': data['result']['name'],
            'name_chi': data['result']['name_chi'],
        }

    def getAll(self):
        q = 'MATCH (n:Dish) RETURN n as result'
        res = db.query(q)
        return [self.serialize_reulst(record.data()) for record in res]

    def getIngredient(self, name):
        q = f'MATCH (d:Dish{{name:\"{name}\"}})-[:USE]->(i:Ingredient) RETURN i as result'
        # print(q)
        res = db.query(q)
        return [self.serialize_reulst(record.data()) for record in res]

    def add(self, name, name_chi):
        q = f'CREATE (d:Dish{{name:\"{name}\",name_chi:\"{name_chi}\"}}) RETURN d as result'
        # print(q)
        res = db.query(q)
        return [self.serialize_reulst(record.data()) for record in res]
