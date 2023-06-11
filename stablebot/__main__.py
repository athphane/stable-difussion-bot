import stablebot
from stablebot import StableBot

if __name__ == '__main__':
    stablebot.client = StableBot

    # scheduler.start()

    StableBot.run()
