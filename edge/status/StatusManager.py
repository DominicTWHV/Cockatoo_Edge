import datetime
from edge.registry.status import BotStatus

# The decision file for the bot's status

class StatusDecider:

    @staticmethod
    async def decide_content():

        now = datetime.datetime.now()
        hour = now.hour

        if 6 <= hour < 12:
            return BotStatus.morning
        elif 12 <= hour < 14:
            return BotStatus.noon
        elif 14 <= hour < 18:
            return BotStatus.afternoon
        elif 18 <= hour < 22:
            return BotStatus.evening
        else:
            return BotStatus.night