import os.path
import configparser
import requests
from web3 import Web3
import contractABI
import sys
import fileinput
import time


debugPrints = False

config = configparser.ConfigParser()
config.optionxform=str
config.read("settings.ini")

teleBotSettings = dict(config.items('BOT'))

RPC_ADDRESS = 'https://rpc.fuse.io'
web3Fuse = Web3(Web3.HTTPProvider(RPC_ADDRESS))
fuseConsensusContract = web3Fuse.eth.contract(abi=contractABI.CONSENSUS_ABI, address=contractABI.CONSENSUS_ADDRESS)

activeValidator = fuseConsensusContract.functions.getValidators().call()

valList = {}
for val in activeValidator:
    valList[val] = 0

if not os.path.exists('lastPublished.txt'):
    f = open("lastPublished.txt", "w")
    for val in valList:
        f.write(val + "=0\n")
    f.close()
    messageToSendToBot = "Hello!, I'm the down detector bot I will let you know if any nodes skip blocks :)"
    botMessage = 'https://api.telegram.org/bot' + teleBotSettings["BOT_KEY"] + '/sendMessage?chat_id=' + \
                 teleBotSettings["CHAT_ID"] + '&text=' + messageToSendToBot
    response = requests.get(botMessage)
    jsonResponse = response.json()

timeSentLastErrors = {}
with open("lastPublished.txt") as f:
    for line in f:
        (key, val) = line.split('=')
        timeSentLastErrors[key] = int(val)

blockNumber = web3Fuse.eth.blockNumber

for block in range(blockNumber, blockNumber - (len(activeValidator)*int(teleBotSettings['DEADFOR'])), -1):
    blockDetails = web3Fuse.eth.getBlock(block)
    valList[blockDetails['miner']] += 1

for val in valList:
    if val not in timeSentLastErrors:
        timeSentLastErrors[val] = 0
        f = open("lastPublished.txt", "a+")
        f.write(val + "=0\n")
        messageToSendToBot = "We have a new Validator! welcome:" + val + "%0A"
        botMessage = 'https://api.telegram.org/bot' + teleBotSettings["BOT_KEY"] + '/sendMessage?chat_id=' + \
                     teleBotSettings["CHAT_ID"] + '&text=' + messageToSendToBot
        response = requests.get(botMessage)
        jsonResponse = response.json()
        f.close()

    if (int(time.time()) - timeSentLastErrors[val] > (int(teleBotSettings['TIMEOUT']) * 60 * 60)):
        if valList[val] == 0:
            foundLastBlock = False
            for i in range(blockNumber - (len(activeValidator)*int(teleBotSettings['DEADFOR'])), blockNumber - 5000, -1):
                blockDetails = web3Fuse.eth.getBlock(i)
                if(blockDetails['miner'] == val):
                    foundLastBlock = True
                    break
            print("last trans at block " + str(i))
            #signal some error

            if(foundLastBlock):
                messageToSendToBot = "Validator: " + val + " has not mined a block since block " + str(i) + " (" + str(web3Fuse.eth.blockNumber - i) + " blocks ago)!" + "%0A"
            else:
                messageToSendToBot = "Validator: " + val + " has not mined for over 5000 blocks! %0A"

            botMessage = 'https://api.telegram.org/bot' + teleBotSettings["BOT_KEY"] + '/sendMessage?chat_id=' + \
                         teleBotSettings["CHAT_ID"] + '&text=' + messageToSendToBot

            response = requests.get(botMessage)
            jsonResponse = response.json()

            for line in fileinput.input("lastPublished.txt", inplace=True):
                if line.strip().startswith(val):
                    line = val + '=' + str(int(time.time())) + '\n'
                sys.stdout.write(line)
