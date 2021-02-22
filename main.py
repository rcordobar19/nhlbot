import re
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
		pick_category = bet.find('div', class_='PickPrediction__pick-header').get_text().strip() # Money Line Pick
		pick_event = re.findall(r'data-analytics-event-label=\"(.*)\" data-component', str(bet))[0] # TOR Maple Leafs @ MON Canadiens
		pick = bet.find('div', class_='PickPrediction__pick-text').get_text().strip() # TOR Maple Leafs Win
		pick_result = bet.find('button', class_='PickPrediction__toggle-betslip').get_text().strip().split("\n") # -6.5
		full_pick = pick_category + ' \n' + '<b>' + pick_event + '</b> \n' + '<pre>' + pick + '</pre>' +  ' ' + pick_result[0]

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

schedule.every(30).minutes.do(sendPicks)

while True:
	schedule.run_pending()
	time.sleep(1)
