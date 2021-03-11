import os
import settings
import pytz

from bs4 import BeautifulSoup
from telegram import TelegramBot
from pick import Pick
from datetime import datetime


picks = Pick().getPicks(os.getenv("PICKS_URL"))
soup = BeautifulSoup(picks, 'lxml')
divs = soup.find_all('div', class_='CardV2')

panama_time = pytz.timezone('America/Panama')
datime_pa = datetime.now(panama_time)

for bet in divs:
	if not bet.find('div', class_='PickPrediction__pick-header'):
		continue

	pick = Pick().parsePick(bet)
	stored_pick = Pick().getFromDB(pick)

	if not stored_pick:
		Pick().store(pick)
		TelegramBot().sendMessage(pick['full_pick'])

		print("[", datime_pa.strftime("%d/%m/%Y %H:%M:%S"), "] Message Sent")
	else:
		print("[", datime_pa.strftime("%d/%m/%Y %H:%M:%S"), "] Old pick")
