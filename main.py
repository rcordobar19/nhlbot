import schedule
import time
from bs4 import BeautifulSoup
from telegram import TelegramBot
from pick import Pick
from database import Database

def sendPicks():
	picks = Pick().getPicks('https://www.pickswise.com/nhl/best-bets/')
	soup = BeautifulSoup(picks, 'lxml')
	divs = soup.find_all('div', class_='CardV2')

	for bet in divs:
		if not bet.find('div', class_='PickPrediction__pick-header'):
			continue

		pick = Pick().parsePick(bet)

		connection = Database().connection()
		cur = connection.cursor()
		cur.execute("SELECT * FROM nhl WHERE reasoning=?", (pick['reasoning'],))
		db_pick = cur.fetchall()

		# Insert if pick doesnt exists
		if not db_pick:
			try:
				db_insert = cur.execute("INSERT INTO nhl (pick, reasoning) VALUES (?, ?)", (pick['full_pick'], pick['reasoning'],))
			except mariadb.Error as e:
				print(f"Error: {e}")

			connection.commit()
			connection.close()

			TelegramBot().sendMessage(pick['full_pick'])
			print('Message sent')
		else:
			print('Old pick')

schedule.every(30).minutes.do(sendPicks)

while True:
	schedule.run_pending()
	time.sleep(1)
