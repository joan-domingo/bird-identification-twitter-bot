#!/usr/bin/python

def init_db(conn):
	cur = conn.cursor()

	# cur.execute("DROP TABLE PERSISTED_VALUES;")

	try:
		cur.execute('''CREATE TABLE PERSISTED_VALUES
		      (ID TEXT PRIMARY KEY     NOT NULL,
		      VALUE            BIGINT  NOT NULL);''')

		print("Table created successfully")

		cur.execute("INSERT INTO PERSISTED_VALUES (ID,VALUE) \
	      VALUES ('mention_id', 1)");

		print("Mention ID row created successfully")

	except Exception as e:
		print(e)

	conn.commit()

def read_mention_id_value(conn):
	cur = conn.cursor()

	cur.execute("SELECT VALUE from PERSISTED_VALUES where ID = 'mention_id'")
	rows = cur.fetchall()
	mention_id = rows[0][0]
	print("Mention ID row read successfully: " + str(mention_id))

	return mention_id

def write_mention_id_value(conn, value):
	cur = conn.cursor()

	cur.execute(f"UPDATE PERSISTED_VALUES set VALUE = {value} where ID = 'mention_id'")
	conn.commit()
	print("Mention ID row write successfully: " + str(value))
