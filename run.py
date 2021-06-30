import colorama
from Flappy.flappy import Flappy
from Flappy import __version__
from colorama import Fore, Style


print(Fore.GREEN + Style.BRIGHT + f"On version: {__version__}")
bot = Flappy()
bot.run()