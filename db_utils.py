

def create_table(cr_connection):
    cur = cr_connection.cursor()
    cur.execute("""
        CREATE TABLE telegram(
         currency_name text,
         currency_val text,
         timestamp timestamp );
    """)
    cr_connection.commit()


def insert_values(ins_connection, val1, val2, val3):
    cur = ins_connection.cursor()
    cur.execute("""
        INSERT INTO telegram VALUES (%s, %s, %s)
        ;
    """, (val1, val2, val3))
    ins_connection.commit()


def get_last_timestamp(t_connection):
    cur = t_connection.cursor()
    cur.execute(""" SELECT timestamp FROM telegram 
                    order by timestamp desc
                    limit 1 ; """)
    db_time = cur.fetchall()
    return db_time


def get_last_data(d_connection):
    cur = d_connection.cursor()
    cur.execute("""
        SELECT *  FROM telegram
        order by timestamp, curr_name desc
        limit 33;""")
    db_data = cur.fetchall()
    return db_data


