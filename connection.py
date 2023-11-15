from websockets.sync.client import connect
import json, random


OpenningLine = {
    "id": 0,
    "action": "start",
    "client": "js_plugin",
    "clientSubtype": "general",
    "clientVersion": "2.5.5",
    "docid": "2704081324",
    "clientSupports": [
        "full_sentence_rewrite_card",
        "readability_check",
        "sentence_variety_check",
        "text_info",
        "tone_cards",
        "user_mutes",
        "vox_check"
    ],
    "dialect": "american",
    "documentContext": {
        "dialect": "american"
    },
    "partnerConfiguration": {
        "muteCategories": [
            "oxfordcomma",
            "unnecessaryellipses",
            "stylisticfragments",
            "informalpronounsacademic",
            "conjunctionatstartofsentence",
            "prepositionattheendofsentence",
            "passivevoice"
        ],
        "dictionaries": [
            "on"
        ]
    }
}



class Connection:
	def __init__(self, token):
		self.token = token
		token.handleExpirePrevention()

		self.raw = connect("wss://capi.grammarly.com/pws?accessToken="+token.access, 
			additional_headers={"host": "capi.grammarly.com", "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"},
			origin="https://developer.grammarly.com")

		self.raw.send(json.dumps(OpenningLine))

		self.openingPong = json.loads(self.raw.recv())

		assert(self.openingPong.get("action")=="start")

		self.id = 1
		self.revCount = 0

		self.raw.send(json.dumps({"id":self.id,"action":"option","name":"gnar_containerId","value":self._random_string()}))
		self.id+=1
		self.raw.recv()

		self.doc_len=0
		self.firstCall=True
	def _random_string(self):
		return "".join([random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789") for _ in range(15)])

	def sendText(self, text):
		ops = []
		
		ops.append({"insert": text})

		new_len = len(text)

		if not self.firstCall:
			if self.new_len != 0:
				ops.append({'delete': self.new_len})
		self.raw.send(json.dumps(
				{
				  "id": self.id,
				  "action": "submit_ot",
				  "rev": self.revCount,
				  "doc_len": self.doc_len,
				  "deltas": [
				    {
				      "ops": ops
				    }
				  ]
				}
			))


		self.id+=1
		self.revCount+=1
		self.doc_len = new_len

		return self.revCount-1
	def getUntilFinish(self, rev=None):
		ret = []
		while True:
			packet = json.loads(self.raw.recv())
			if rev is not None:
				if not packet.get("rev") == rev:
					continue

			ret.append(packet)
			
			if (packet.get("action") == "finished"):
				break
		return ret
