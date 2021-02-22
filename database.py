import mariadb

class Database:
	def connection(self):
		try:
			conn = mariadb.connect(
				user="root",
				password="qwer1234",
				host="localhost",
				port=3306,
				database="bet_picks"
			)

		except mariadb.Error as e:
			print(f"Error connecting to MariaDB Platform: {e}")
			sys.exit(1)

		return conn
