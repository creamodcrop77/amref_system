import psycopg2

try:
    conn = psycopg2.connect("dbname= duka user=postgres password=leo.steve")
    cur = conn.cursor()
except Exception as e:
    print(e)




def loginn():
    q = "SELECT email, password FROM users;"
    cur.execute(q)
    results = cur.fetchall()
    return results 



    