import discord
import os
from dotenv import load_dotenv
from helperFunctions import memberIsRecentJoiner, messageContainsBannedWord, loadBannedWords

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


    if memberIsRecentJoiner():
        recentJoinFlag = True

    if bannedWordFlag and recentJoinFlag:
        await message.channel.send(message.author.name + " said a bad word! Prepare to be banned " + message.author.name + "!")
        await message.delete()
        await message.guild.ban(message.author)

client.run(os.getenv('TOKEN'))