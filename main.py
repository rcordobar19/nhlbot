import schedule
import time
from bs4 import BeautifulSoup
from telegram import TelegramBot
from pick import Pick
from database import Database

def sendPicks():
	picks = Pick().getPicks('https://www.pickswise.com/nhl/best-bets/')
	soup = BeautifulSoup(picks, 'lxml')
	bets = soup.find_all('div', class_='PickPrediction__body')

	for bet in bets:
		full_pick = Pick().parsePick(bet)

		connection = Database().connection()

		# Get Cursor
		cur = connection.cursor()
		cur.execute("SELECT * FROM nhl WHERE pick=?", (full_pick,))
		db_pick = cur.fetchall()

		# Insert if pick doesnt exists
		if not db_pick:
			try:
				db_insert = cur.execute("INSERT INTO nhl (pick) VALUES (?)", (full_pick,))
				print('Sending message')
			except mariadb.Error as e:
				print(f"Error: {e}")
			connection.commit()
			connection.close()

			TelegramBot().sendMessage(full_pick)
			print('Pick sent')
		else:
			print('Old pick')

# schedule.every(30).minutes.do(sendPicks)
schedule.every(2).seconds.do(sendPicks)

while True:
	schedule.run_pending()
	time.sleep(1)
