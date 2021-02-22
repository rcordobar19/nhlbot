import requests
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
