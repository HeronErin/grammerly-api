import requests, time, os, json


baseHeaders = {
    'authority': 'developer.grammarly.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    'referer': 'https://developer.grammarly.com/docs/api/',
    'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
}

subHeaders = {
    'authority': 'tokens.grammarly.com',
    'accept': 'application/json',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/json',
    'origin': 'https://developer.grammarly.com',
    'referer': 'https://developer.grammarly.com/',
    'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
    'x-client-type': 'js_plugin',
    'x-client-version': '2.5.5',
}


class GrammarlyToken():
	def __init__(self):
		self.is_authed = False

		if os.path.exists(".grammarly.cache"):
			f = open(".grammarly.cache", "r")

			self.tokenJson = json.loads(f.read())

			assert("access_token" in self.tokenJson)

			self._parse_token_json()

			f.close()


		else:
			self.getTokens()
	def _getClientId(self):
		print("Getting client ID")
		response = requests.get('https://developer.grammarly.com/docs/demo',  headers=baseHeaders)
		baseElement = response.text.split("grammarly-editor-plugin")[1]
		assert(baseElement.startswith(" clientId=\""))

		return baseElement.split('\"')[1]

	def getTokens(self):
		print("Getting access tokens")
		self.clientId = self._getClientId()
		response = requests.post('https://tokens.grammarly.com/oauth2/token',  headers=subHeaders, json={
		    'grant_type': 'urn:ietf:params:oauth:grant-type:origin',
		    'client_id': self.clientId,
		})
		assert(response.status_code==200)
		self.tokenJson = response.json()

		assert("access_token" in self.tokenJson)

		self._parse_token_json(do_add_time=True)

		f = open(".grammarly.cache", "w")
		f.write(json.dumps(self.tokenJson))
		f.close()


	def _parse_token_json(self, do_add_time=False):
		self.access = self.tokenJson["access_token"]
		self.refresh = self.tokenJson["refresh_token"]

		if do_add_time:
			self.tokenJson["expires_in"] += time.time()

		self.expires = self.tokenJson["expires_in"]



		self.is_authed = True
	def handleExpirePrevention(self):
		if (self.expires <= time.time()):
			self.getTokens()
