import schedule
import time
from bs4 import BeautifulSoup
from telegram import TelegramBot
from pick import Pick

def sendPicks():
	picks = Pick().getPicks('https://www.pickswise.com/nhl/best-bets/')
	soup = BeautifulSoup(picks, 'lxml')
	divs = soup.find_all('div', class_='CardV2')

	for bet in divs:
		if not bet.find('div', class_='PickPrediction__pick-header'):
			continue

		pick = Pick().parsePick(bet)
		stored_pick = Pick().getFromDB(pick)

		if not stored_pick:
			Pick().store(pick)
			TelegramBot().sendMessage(pick['full_pick'])
			print('Message sent')
		else:
			print('Old pick')

schedule.every(30).minutes.do(sendPicks)
# schedule.every(1).seconds.do(sendPicks)

while True:
	schedule.run_pending()
	time.sleep(1)
