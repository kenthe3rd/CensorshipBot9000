import discord
import os
from dotenv import load_dotenv
from helperFunctions import memberIsRecentJoiner, messageContainsBannedWord, loadBannedWords, getModChannel

### GLOBALS ###
bannedWords = loadBannedWords()

load_dotenv('.env')
client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    bannedWordFlag = False
    recentJoinFlag = False
    if message.author == client.user:
        return

    if messageContainsBannedWord(bannedWords, message.content):
        bannedWordFlag = True

    if memberIsRecentJoiner(message.author):
        recentJoinFlag = True

    if bannedWordFlag and recentJoinFlag:
        notification = message.author.name + " was banned for the following message submitted in " + message.channel.mention + ":" + message.content
        modchannel = getModChannel(message.guild)
        await message.delete()
        await message.guild.ban(message.author)
        await modchannel.send(notification)
        return
    elif bannedWordFlag:
        notification = "Flagged message from " + message.author.name + " submitted in " + message.channel.mention + ":" + message.content
        modchannel = getModChannel(message.guild)
        await modchannel.send(notification)
        return


client.run(os.getenv('TOKEN'))