import os
import io
import requests
from mastodon import Mastodon
from dotenv import load_dotenv

class Bot():

	def __init__(self):
		load_dotenv()
		self.mastodon = Mastodon(
			access_token = os.getenv("ACCESS_TOKEN"),
			api_base_url = os.getenv("INSTANCE_URL")
		)
		url = "https://api.prod.headspace.com/sharing/v1/mindfulmoment/today"
		self.data = requests.get(url).json()

	def uploadImage(self, url):
		r = requests.get(url, allow_redirects=True)
		img = self.mastodon.media_post(io.BytesIO(r.content), "image/png")
		return img

	def toot(self):
		if os.getenv("POST_IMG") == "True":
			self.mastodon.status_post(
				self.data["text"], 
				media_ids=self.uploadImage(self.data["previewImage"])["id"], 
				language="eng", 
				visibility=os.getenv("VISIBILITY")
			)
		else:
			self.mastodon.status_post(
				self.data["text"], 
				language="eng",
				visibility=os.getenv("VISIBILITY")
			)

bot = Bot()
bot.toot()
