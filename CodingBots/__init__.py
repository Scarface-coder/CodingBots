from CodingBots.core.bot import sxyseller
from CodingBots.core.dir import dirr
from CodingBots.core.git import git
from CodingBots.core.userbot import Userbot
from CodingBots.misc import dbb, heroku

from .logging import LOGGER

dirr()
git()
dbb()
heroku()

app = sxyseller()
userbot = Userbot()


from .platforms import *

Apple = AppleAPI()
Carbon = CarbonAPI()
SoundCloud = SoundAPI()
Spotify = SpotifyAPI()
Resso = RessoAPI()
Telegram = TeleAPI()
YouTube = YouTubeAPI()
