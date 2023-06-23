# home-recipe

Store and represent recipes in Neo4j database.


---


### Technology
- **Framework** : Flask
- **Database** : Neo4j

---

### Functions

- Add **ingredient** (Neo4j `node`) with
    -  _name_ and _name_chi_ (Neo4j `properties`)
- Add **recipe** (Neo4j `node`) with
    -   required **ingredient** (Neo4j `relationship`)
    -   _name_ and _name_chi_ (Neo4j `properties`)
    -   _category_ and _style_ (Neo4j `properties`)
- Ingredient suggestion when start typing in "Add recipe > ingredient" (Neo4j `FULLTEXT` search)
- API endpoint:
    >  `GET /dishes` : retrieve all dishes in json format, sorted by _category_, _style_
    
    >  `POST /add/dish` : add new dish
    
    >  `GET /ingredients` : retrieve all ingredients in json format
    
    >  `POST /add/ingredient` : add new ingredient
    
    >  `POST /search` :  full-text search ingredient with given string
    
---
    
#### Usage

```
python main.py
```
