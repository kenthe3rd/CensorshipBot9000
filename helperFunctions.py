import csv
import string
import datetime

def loadBannedWords():
    output = []
    csvFile = open('bannedWords.csv', newline = '')
    csvStream = csv.reader(csvFile, delimiter = ',')
    for row in csvStream:
        for word in row:
            output.append(word)
    return output

def messageContainsBannedWord(bannedWords, message):
    formattedText = message.lower()
    for character in string.punctuation:
        formattedText = formattedText.replace(character, " ")
    formattedText = formattedText.replace("\n", " ")
    for word in bannedWords:
        if " " + word + " " in formattedText:
            return True
        if word == formattedText:
            return True 
        if formattedText[0:len(word)+1] == word + " ":
            return True
        if formattedText[-(len(word)+1):] == " " + word:
            return True
    return False

def memberIsRecentJoiner(member):
    grandfatheredAgeInSeconds = 60 * 60
    joinTimestamp = member.joined_at.replace(tzinfo=datetime.timezone.utc)
    age = datetime.datetime.now(tz=datetime.timezone.utc) -  joinTimestamp
    print(str(age.total_seconds()))
    if age.total_seconds() < grandfatheredAgeInSeconds:
        return True
    return False

def getModChannel(guild):
    channels = guild.channels
    for channel in channels:
        if channel.name == "mod-squad":
            return channel