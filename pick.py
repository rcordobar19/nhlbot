import requests
import re
from requests.exceptions import HTTPError

class Pick:
	def getPicks(self, endpoint):
		try:
			headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36'}
			response = requests.get(endpoint, headers = headers)
			response.raise_for_status()
		except HTTPError as err:
			raise SystemExit(err)

		return response.content

	def parsePick(self, data):
		if not data.find('div', class_='PickReasoning__content'):
			return None
		else:
			pick_category = data.find('div', class_='PickPrediction__pick-header').get_text().strip() # Money Line Pick
			pick_event = re.findall(r'data-analytics-event-label=\"(.*)\" data-component', str(data))[0] # TOR Maple Leafs @ MON Canadiens
			pick = data.find('div', class_='PickPrediction__pick-text').get_text().strip() # TOR Maple Leafs Win
			pick_reasoning = data.find('div', class_='PickReasoning__content').get_text().strip() # Marner is second in the NHL with...

			if data.find('button', class_='PickPrediction__toggle-betslip'):
				pick_result = data.find('button', class_='PickPrediction__toggle-betslip').get_text().strip().split("\n") # -6.5
			else:
				pick_result = data.find('a', class_='PickPrediction__toggle-betslip').get_text().strip().split("\n") # -6.5

			bet = {
				"reasoning": pick_reasoning,
				"full_pick": pick_category + ' \n' + '<b>' + pick_event + '</b> \n' + '<pre>' + pick + '</pre>' +  ' ' + pick_result[0]
			}

			return bet
