import discord
import os
from dotenv import load_dotenv
from helperFunctions import memberIsRecentJoiner, messageContainsBannedWord, loadBannedWords, getModChannel
import datetime

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
    if message.author == client.user or message.channel.name == getModChannel(message.guild):
        return
    age = datetime.datetime.now() - message.author.joined_at.replace(tzinfo=datetime.timezone.utc)
    await message.channel.send(message.author.name + " age=" + str(age.total_seconds()))
    if messageContainsBannedWord(bannedWords, message.content):
        bannedWordFlag = True

    if memberIsRecentJoiner(message.author):
        recentJoinFlag = True

    if bannedWordFlag and recentJoinFlag:
        notification = message.author.mention + " was banned for the following message submitted in " + message.channel.mention + ":" + message.content
        modchannel = getModChannel(message.guild)
        await message.delete()
        await message.guild.ban(message.author)
        await modchannel.send(notification)
        return
    elif bannedWordFlag:
        notification = "Flagged message from " + message.author.mention + " submitted in " + message.channel.mention + ":" + message.content + "\n" + message.jump_url
        modchannel = getModChannel(message.guild)
        await modchannel.send(notification)
        return


client.run(os.getenv('TOKEN'))