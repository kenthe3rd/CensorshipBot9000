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
    grandfatheredAgeInSeconds = 60 * 60 * 24
    age = datetime.datetime.now() - member.joined_at
    print("age=" + age.total_seconds())
    if age.total_seconds() < grandfatheredAgeInSeconds:
        return True
    return False

