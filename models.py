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
        q = 'MATCH (n:Ingredient) RETURN n as result ORDER BY id(n)'
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

    @staticmethod
    def formatObj(obj, chi=False):
        if 'name' in obj:
            obj['name'] = obj['name'].capitalize()
        if 'name_chi' in obj:
            if obj['name_chi'] != '':
                obj['name_chi'] = f"({obj['name_chi']})"
        return obj

    def serialize_reulst(self, data):
        # print(data)
        return {
            'name': data['result']['name'],
            'name_chi': data['result']['name_chi'],
        }

    def getAll(self):
        q = 'MATCH p=(n:Dish)-[]->(i:Ingredient) RETURN p as result'
        res = db.query(q)
        serialize_reulst = []
        idx = {}
        dish_count = 0
        for r in res:
            data = r.data()['result']
            id = data[0]['name']
            if id not in idx:
                idx[id] = dish_count
                obj = data[0]
                obj['ingredients'] = []
                serialize_reulst.append(obj)
                target = serialize_reulst[dish_count]['ingredients']
                dish_count +=1
            else:
                i = idx[id]
                target = serialize_reulst[i]['ingredients']                

            target.append(data[2])
        return serialize_reulst
    
    def getStructure(self):
        # return self.getAll()
        q = 'MATCH p=(n:Dish)-[]->(i:Ingredient) RETURN p as result'
        res = db.query(q)
        result = {}
        for r in res:
            data = r.data()['result']
            id = data[0]['name']
            cat = data[0]['category']
            style = data[0]['style']
            if cat not in result:
                result[cat] = {}
            if style not in result[cat]:
                result[cat][style] = {}
            if id not in result[cat][style]:
                result[cat][style][id] = data[0]            
                result[cat][style][id]['ingredients'] = []
            
            result[cat][style][id]['ingredients'].append(data[2])
        return result


    def getIngredient(self, name):
        q = f'MATCH (d:Dish{{name:\"{name}\"}})-[:USE]->(i:Ingredient) RETURN i as result'
        # print(q)
        res = db.query(q)
        return [self.serialize_reulst(record.data()) for record in res]

    def add(self, name, name_chi, category,style, ingredients):
        if name == '':
            return 'name error'
        for i in ingredients:
            q = f"""
            MERGE (i:Ingredient{{name:"{i}"}})
            MERGE (d:Dish{{name:"{name}",name_chi:"{name_chi}",category:"{category}",style:"{style}"}})
            MERGE (d)-[:USE]->(i)
            RETURN d
            """
            print(q)
            res = db.query(q)
        return True
