import random
import re
import time

import discord
import keyboard

import agent
import captcha
import constants
import src.utils as utils


class Client(discord.Client):
    def __init__(self):
        super().__init__()
        self.channel = None
        self.captcha = None
        self.agent = None
        self.task = None

    async def on_ready(self):
        self.task = None
        self.agent = agent.Agent()
        self.captcha = captcha.Captcha()
        self.channel = utils.getChannel(self, constants.CHANNEL_ID)

        await self.captcha.setup(self.channel)
        await self.agent.setup(self.channel)

        await self.agent.play()
        time.sleep(random.uniform(10, 20))
        await self.agent.play()

        farm, sell = await utils.findSellAndFarmButtons(self.channel, self.user.id)

        self.agent.setFarmButton(farm)
        self.agent.setSellButton(sell)

        client.startTask()

    async def on_message_edit(self, before, after):
        if after.author.id != constants.BOT_ID: return
        if not after.interaction.user.id == self.user.id: return
        if len(after.embeds) == 0: return

        embed = after.embeds[0]
        title = embed.title

        if title is None:
            description = embed.description

            if 'cooldown' in description:
                matches = re.findall(r'\*\*(.*?)\*\*', description)
                self.agent.cooldown = float(matches[-1]) + 0.1
                return

        elif 'Antibot Verification' in title:
            self.stopTask()
            if not await self.captcha.solve(after):
                return

    async def on_message(self, message):
        if message.author.id != constants.BOT_ID:
            return

        if not message.interaction.user.id == self.user.id:
            return

        if message.content == '':
            return

        if "You may now continue." in message.content:
            self.startTask()

    def startTask(self):
        print("Program started!")
        self.task = client.loop.create_task(client.action())

    def stopTask(self):
        print("Program stopped!")
        self.task.cancel()
        self.task = None

    def hasTask(self):
        return self.task is not None

    async def action(self):
        while True:
            await self.agent.action()


# Bind emergency shutdown keybind
def shutdown(event):
    global IsRunning
    if event.name == 'space':
        if client.hasTask():
            client.stopTask()
        else:
            client.startTask()


keyboard.on_press(shutdown)

client = Client()
client.run(constants.TOKEN)
