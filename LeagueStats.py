##LeagueStats by Mike Kim
# W.I.P

import os
import discord
from discord.ext import commands
from bs4 import BeautifulSoup as soup
import requests
from urllib.request  import urlopen as uReq
from dotenv import load_dotenv


global my_url 
my_url = 'https://na.op.gg/summoner/userName='

global page
global page_soup
page = requests.get(my_url)
page_soup = soup(page.content, 'html.parser')

def sendStats():
    page = requests.get(my_url)
    page_soup = soup(page.content, 'html.parser')
    summonerContainer = page_soup.find_all('div', class_='SideContent')
    summonerInfo = []
    for summ in summonerContainer:
        rankType = summ.find('div',class_='RankType').text.replace('\t', '')
        tierRank = summ.find('div',class_='TierRank').text.replace('\t', '')
        divName = summ.find('div',class_='LeagueName').text.replace('\t', '')
        divName = divName.replace('\n','')
        leaguePoints = summ.find('span',class_='LeaguePoints').text.replace('\t', '')
        leaguePoints = leaguePoints.replace('\n','')
        wins = summ.find('span',class_='wins').text.replace('\t', '')
        losses = summ.find('span',class_='losses').text.replace('\t', '')
        winRatio = summ.find('span',class_="winratio").text.replace('\t', '')
        summonerInfo = [rankType,tierRank,divName,leaguePoints,wins,losses,winRatio]
        print(summonerInfo)
        print(rankType)
    return(summonerInfo)

#scrapes data from match history


def matchHist():
    page = requests.get(my_url)
    page_soup = soup(page.content, 'html.parser')
    matchContainer = page_soup.find_all('div', class_='GameItemWrap')
    historyArray = []
    for match in matchContainer:    
        gameType = match.find('div', class_='GameType').text.replace('\t', '')
        gameType = gameType.replace('\n','')
        gameRes = match.find('div', class_='GameResult').text.replace('\t', '')
        gameRes = gameRes.replace('\n','')
        gameLen = match.find('div', class_='GameLength').text.replace('\t', '')
        kills = match.find('span', class_='Kill').text.replace('\t', '')
        deaths = match.find('span', class_='Death').text.replace('\t', '')
        assists = match.find('span', class_='Assist').text.replace('\t', '')
        KDA_ratio = match.find('span', class_='KDARatio').text.replace('\t', '')
        date = match.find('div',class_='TimeStamp').text
        champImage = match.find('img',class_="Image")
        matchHistory = [gameType,gameRes,gameLen,kills,deaths,assists,KDA_ratio]
        historyArray.append(matchHistory)
    return(historyArray)

####         ####
# Discord Bot 
####         ####

#Loads environment variables from the local .env file to keep tokens safe
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()

prefix = '!'

# Function lets users change the prefix so it doesn't conflict with other bots.
def changePrefix (newPrefix): 
    global prefix
    prefix = newPrefix

def setUser (leagueName):
    global my_url 
    my_url = my_url + leagueName

bot = commands.Bot(command_prefix = "!")

@client.event
async def on_ready():
    print("I'm ready {0.user}.".format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
         return
    
    if message.content.startswith(prefix+'hello'):
        await message.channel.send('Hello!')

    if message.content.startswith(prefix+'prefix'):
        if message.content[8].isalnum(): 
            await message.channel.send("Prefix must be one symbol e.g. !, $, <, >, %...")
            pass
        else:
            changePrefix(message.content[8])
            await message.channel.send('The prefix has been changed to ' + message.content[8])
            print(prefix)

    if message.content.startswith(prefix+'stats'):
        lolName = message.content.split(" ")
        await message.channel.send(lolName[1])
        setUser(lolName[1])
        playerStats = sendStats()
        await message.channel.send(playerStats)

    if message.content.startswith(prefix+'test'):
        await message.channel.send(my_url)
     
    if message.content.startswith(prefix+'send'):
        playerStats2 = sendStats()
        await message.channel.send(playerStats2)

    if message.content.startswith(prefix+'history'):
        lolName = message.content.split(" ")
        await message.channel.send(lolName[1])
        setUser(lolName[1])
        matchHistory = matchHist()
        await message.channel.send(matchHistory)
        



client.run(TOKEN)
