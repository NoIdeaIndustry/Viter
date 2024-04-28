import asyncio
import random
from datetime import datetime

import src.utils as utils


class Agent:
    def __init__(self):
        self.sell = None
        self.play = None
        self.channel = None
        self.cooldown = 2.8
        self.sellingIn = 45
        self.turns = 0
        self.isInit = False

        self.farm = 'gather 1173702881455648853'

    async def setup(self, channel):
        self.channel = channel
        self.play = await utils.getCommand(self.channel, 'play')

    def setFarmButton(self, button):
        self.farm = button
        print("set FARM button")

    def setSellButton(self, button):
        self.sell = button
        print("set SELL button")

    async def sellAction(self):
        try:
            await self.sell.click()
            print(f"'{datetime.now().strftime("%I:%M:%S %p")}' - Selling!")
            self.sellingIn = random.randint(48, 135)
            print(f"Next selling in {self.sellingIn} turns!")
        except Exception as ex:
            print(ex)
            await self.sellAction()

    async def farmAction(self):
        try:
            self.sellingIn -= 1
            await self.farm.click()

            if self.turns % 22 == 0:
                await self.farm.click()

            print(f"'{datetime.now().strftime("%I:%M:%S %p")}' - Farming! [{self.turns}]")
        except Exception as ex:
            print(ex)
            await self.farmAction()

    async def start(self):
        await self.play(self.channel)

    async def action(self):
        timeout = random.uniform(self.cooldown, self.cooldown + 0.1)
        print(f"Timeout of {timeout} seconds.")
        await asyncio.sleep(timeout)

        if self.sellingIn <= 0: 
            await self.sellAction()
            await self.farmAction()
        else: 
            await self.farmAction()

        self.turns += 1
