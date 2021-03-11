import requests

class TelegramBot:
	def __init__(self):
		# self.chatId = '1550332109'
		self.chatId = '-544323793'
		self.token = '1654675887:AAGLhaCKbj40HiFarnpuU5RM-FTKqqb5JEQ'

	def sendMessage(self, message):
		if not message:
			return 'no message'
		else:
			send_text = 'https://api.telegram.org/bot' + self.token + '/sendMessage?chat_id=' + self.chatId + '&parse_mode=html&text=' + message
			response = requests.get(send_text)

			return response.json()
