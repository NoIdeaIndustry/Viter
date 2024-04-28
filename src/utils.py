import os

import constants


def clearConsole():
    os.system('cls' if os.name == 'nt' else 'clear')


def getChannel(client, uid):
    return client.get_channel(uid)


async def getCommand(channel, name):
    for command in await channel.application_commands():
        if command.name == name:
            return command


async def getLastUserMessages(channel, uid, limit=10):
    messages = []

    async for message in channel.history(limit=limit):
        if not message.author.id == constants.BOT_ID:
            continue

        if not message.interaction.user.id == uid:
            continue

        messages.append(message)

    return messages


async def findSellAndFarmButtons(channel, uid):
    messages = await getLastUserMessages(channel, uid)

    if len(messages) == 0:
        return None, None

    for message in messages:
        if message.embeds is None:
            continue

        if len(message.components) == 0:
            continue

        buttons = message.components[0].children

        if any("shop" in button.custom_id for button in buttons):
            await message.components[0].children[0].click()
            return await findSellAndFarmButtons(channel, uid)

        farm = [button for button in buttons if "gather" in button.custom_id]
        sell = [button for button in buttons if "sell" in button.custom_id]

        return farm[0], sell[0]

    return None, None
