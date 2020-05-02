import json
import psycopg2

insert_definition_sql = """INSERT INTO definitions(word, definition)
             VALUES(%s, %s);"""

clear_definitions_sql = "TRUNCATE definitions"

try:
    # read data form json file
    jsonfile = open('data.json')
    data = json.load(jsonfile)
    jsonfile.close()

    # connect to DB
    conn = psycopg2.connect("dbname='english_dictionary' user='postgres' host='localhost' password='postgres'")
    cur = conn.cursor()

    # clear DB first
    cur.execute(clear_definitions_sql)
    
    # insert every definition as a row
    for entry in data:
        for definition in data[entry]:
            cur.execute(insert_definition_sql, (entry, definition))
    
    # commit changes and close comm with DB
    conn.commit()
    cur.close()
    
except (Exception, psycopg2.DatabaseError) as error:
    print("Exit error: %s", error)

finally:
    if conn is not None:
        conn.close()


print("Success!")