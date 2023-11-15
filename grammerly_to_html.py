import sys, json, random

from grammarly import Grammer

prologue = """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- Latest compiled and minified CSS -->



	<style>
		.gcritical{
			display: inline-block;
		 	background: red;
		}
		.gadvanced{
			display: inline-block;
		 	background: #00FFFF;
		}
		textarea {
			width: 100%;
		}


/* Tooltip container */
.tooltip {
  position: relative;
  display: inline-block;
  border-bottom: 1px dotted black; /* If you want dots under the hoverable text */
}

/* Tooltip text */
.tooltip .tooltiptext {
  visibility: hidden;
  width: 20em;
  background-color: #555;
  color: #fff;
  text-align: center;
  padding: 5px 0;
  border-radius: 6px;

  /* Position the tooltip text */
  position: absolute;
  z-index: 1;
  bottom: 125%;
  left: 50%;
  margin-left: -10em;

  /* Fade in tooltip */
  opacity: 0;
  transition: opacity 0.3s;
}

/* Tooltip arrow */
.tooltip .tooltiptext::after {
  content: "";
  position: absolute;
  top: 100%;
  left: 50%;
  margin-left: -5px;
  border-width: 5px;
  border-style: solid;
  border-color: #555 transparent transparent transparent;
}

/* Show the tooltip text when you mouse over the tooltip container */
.tooltip:hover .tooltiptext {
  visibility: visible;
  opacity: 1;
}

	</style>
	<script>
	function edit(id){
		if (document.getElementById(id).style.visibility == "hidden")
			document.getElementById(id).style.visibility="";
		else
			document.getElementById(id).style.visibility="hidden";
	}
	</script>

   </head>

  <body>
"""

epilogue = """
</body>
</html>"""


class HighLightHandler:
	def __init__(self, text):
		self.text = text
		self.changes = []
	def index_to_mod_index(self, Iindex):
		offset = 0
		change_index = 0
		for change_oindex, change_len in self.changes:
			if change_oindex > Iindex:
				break
			offset+=change_len
			change_index+=1
		return Iindex+offset, change_index
	def mod_index_to_index(self, Mindex):
		offset = 0
		change_index = 0
		for change_oindex, change_len in self.changes:
			if offset+change_oindex > Mindex:
				break
			offset-=change_len
			change_index+=1
		return offset + Mindex, change_index


	def insert(self, index, value):
		mod, ins = self.index_to_mod_index(index)
		self.text = self.text[:mod] + value + self.text[mod:]
		self.changes.insert(ins, [index, len(value)])


def resps_to_html(r, text):
	h = HighLightHandler(text)
	for element in r: # Packets recived from grammerly
		if "highlightBegin" in element:
			tooltip = element['title']
			if "replacements" in element:
				tooltip+="<br>"

				if len(element["replacements"]) == 0 or len(element["replacements"][0]) == 0:
					tooltip+="Try removing it."
				else:
					tooltip+="Try replacing it with: <i>" + ", ".join(element["replacements"]) + "</i>"

			tooltip = tooltip.replace('"', "&quot;").replace("\\", "&#92;")
			h.insert(element["begin"], f"<div class=\"tooltip g{element['impact']}\">")
			h.insert(element["end"], f"<span class=\"tooltiptext\">{tooltip}</span></div>")
			print(element)
	idd = "I"+str(random.randrange(0, 99999999999999999))


	return \
			h.text.encode('ascii', 'xmlcharrefreplace').decode("UTF-8")+ \
			f"<br><textarea id='{idd}' rows='5' style='visibility: hidden;'>" + text.encode('ascii', 'xmlcharrefreplace').decode("UTF-8") + "</textarea>"

def text_to_html(g, text):

	spells = g.text(text)

	return resps_to_html(spells, text)

