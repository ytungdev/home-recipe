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
        if name == '':
            return 'name error'
        q = f'CREATE (i:Ingredient{{name:\"{name}\",name_chi:\"{name_chi}\"}}) RETURN i as result'
        res = db.query(q)
        # print(q, res)
        if res:
            return [self.serialize_reulst(record.data()) for record in res]
        return False

    def search(self, text):
        if text == '':
            return []
        q = f'CALL db.index.fulltext.queryNodes("ingredientName", "*{text}*") YIELD node, score RETURN node.name as name, node.name_chi as name_chi'
        res = db.query(q)
        print(q, res)
        return [record.data() for record in res]

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
    
    def getFull(self):
        q = 'MATCH p=(n:Dish)-[]->(i:Ingredient) RETURN p as result'
        res = db.query(q)
        serialize_reulst = []
        obj = {}
        for i in range(len(res)):
            data = res[i].data()['result']
            if i == 0:
                obj = data[0]
                obj['ingredients'] = []
            if obj['name'] != data[0]['name']:
                serialize_reulst.append(obj)
                obj = data[0]
                obj['ingredients'] = []                
            obj['ingredients'].append(data[2])
            if i == len(res)-1:
                serialize_reulst.append(obj)
        
        for i in serialize_reulst:
            print(i)
        return serialize_reulst

    def getIngredient(self, name):
        q = f'MATCH (d:Dish{{name:\"{name}\"}})-[:USE]->(i:Ingredient) RETURN i as result'
        # print(q)
        res = db.query(q)
        return [self.serialize_reulst(record.data()) for record in res]

    def add(self, name, name_chi, ingredients):
        if name == '':
            return 'name error'
        for i in ingredients:
            q = f"""
            MERGE (i:Ingredient{{name:"{i}"}})
            MERGE (d:Dish{{name:"{name}",name_chi:"{name_chi}"}})
            MERGE (d)-[:USE]->(i)
            RETURN d
            """
            print(q)
            res = db.query(q)
        return True
