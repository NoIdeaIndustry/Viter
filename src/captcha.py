import re

import src.utils as utils


class Captcha:
    def __init__(self):
        self.verify = None
        self.channel = None

    async def setup(self, channel):
        self.channel = channel
        self.verify = await utils.getCommand(self.channel, 'verify')

    async def _send(self, code):
        await self.verify(self.channel, answer=code)

    @staticmethod
    def _getCode(description):
        match = re.search(r'\*\*(.*?)\*\*', description)
        return match.group(1)

    async def solve(self, message):
        code = self._getCode(message.embeds[0].description)

        if code is None:
            return False

        await self._send(code)
        return True
