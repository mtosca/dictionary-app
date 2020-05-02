import difflib
from difflib import get_close_matches
import psycopg2

br = '\n'

def fetch_word_definition(cursor, word):
    # handle different situations as Paris, paris or PARIS
    word_list = (
        word.lower(),
        word.title(),
        word.upper()
    )
    fetch_sql = """select definition from definitions where word in %s"""
    cursor.execute(fetch_sql, (word_list,))
    defs = cursor.fetchall()
    return [d[0] for d in defs]

def fetch_all_words(cursor):
    all_words_sql = "SELECT DISTINCT word FROM definitions;"
    cursor.execute(all_words_sql)
    words = cursor.fetchall()
    return [w[0] for w in words]

def handle_type_error(cursor, word):
    # handle close matches as 'rainn' to 'rain' 
    matches = get_close_matches(word, fetch_all_words(cur), 3, 0.8)
    
    if matches:
        confirm = input(f"Did you mean '{matches[0]}' instead? Enter 'Yes' or 'No' ")
        if confirm.lower() == 'yes':
            return define(cursor, matches[0])
        elif confirm.lower() == 'no':
            return "The word does not exist. Please double check it."
        else:
            return "Invalid entry."
    else:
        return "The word does not exist. Please double check it."

def define(cur, word):
    definitions = fetch_word_definition(cur, word)
    if definitions:
        return br.join(definitions)
        
    return handle_type_error(cur, word)


input_word = input("Enter word: ")

try:
    # connect to DB
    conn = psycopg2.connect("dbname='english_dictionary' user='postgres' host='localhost' password='postgres'")
    cur = conn.cursor()

    result = define(cur, input_word)
    print(result)

except (Exception, psycopg2.DatabaseError) as error:
    print(f"Failed for word '{input_word}'. Exit with error: '{error}'")

finally:
    conn.close()

