import os
import json
import telegram
from telegram.ext import Updater, CommandHandler, Filters
import schedule
from botTools import *
from fuse import *
from multiprocessing import Queue
import queue
from web3 import Web3
from threading import Thread

debug = True
defaultKey = ''
defaultID = ''
defaultMissed = 3
defaultTimeOut = 6
defaultFuse = 0.5
defaultEth = 0.4

HOURS_TO_WAIT = 3

chatSettingsFile = "settings.json"
nodeList = "nodes.json"

command_list = ['update_admins','info','set_eth_warning','set_fuse_warning','add_node','remove_node','set_dead_time']
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

def printLogs(message):
    if debug:
        print(message)

class DownBot:
    def __init__(self):

        self.available_commands = command_list

        # check if we have passed json file containing chat data
        self.parseSettings()
        self.parseNodes()

        self.bot = telegram.Bot(token=defaultKey)
        self.grabAdmins(self.bot)
        self.grabValidators()
        self.blockQueue = Queue()

        self.currentEndOfCycle = getEndOfCycleBlock()

        self.checkBalance()

        createBlockThread(self.blockQueue)

        self.collectedSigData = []



    def parseSettings(self):
        """Function is called at start up to read bot settings data from a file (if present), if not it builds the dicts from scratch

        Returns None
        """
        if os.path.exists(os.path.join(__location__, chatSettingsFile)):
            printLogs("loading Settings")
            with open('settings.json') as json_file:
                self.settings = json.load(json_file)
        else:
            printLogs("No Settings Generate defaults")
            self.settings = {}
            self.settings["BOTKey"] = defaultKey
            self.settings["ChatID"] = defaultID
            self.settings["MissedCount"] = defaultMissed
            self.settings["timeOut"] = defaultTimeOut
            self.settings["FuseWarning"] = defaultFuse
            self.settings["EthWarning"] = defaultEth

    def parseNodes(self):
        if os.path.exists(os.path.join(__location__, nodeList)):
            printLogs("loading Settings")
            with open(nodeList) as json_file:
                self.nodes = json.load(json_file)
        else:
            self.nodes = {}

    def grabAdmins(self, bot):
        """Function to grab and update the current admin list

        Returns None
        """
        printLogs("grabbing admins")
        admins = bot.get_chat_administrators(self.settings["ChatID"])
        self.settings["admins"] = []
        for admin in admins:
            self.settings["admins"].append(admin['user']['_id_attrs'][0])
        self.saveSettings(self.settings, chatSettingsFile)

    def saveSettings(self, dict, saveFileName):
        """Function to write a dictionary to a json file

                   Returns None
                   """
        with open(saveFileName, 'w') as fp:
            json.dump(dict, fp)

    def grabValidators(self):
        valList = getValidators()
        self.numberOfNodes = len(valList)
        for val in valList:
            if val not in self.nodes:
                self.nodes[Web3.toChecksumAddress(val)] = {}
                self.nodes[Web3.toChecksumAddress(val)]['lastBlock'] = 0
                self.nodes[Web3.toChecksumAddress(val)]['lastWarned'] = 0
                self.nodes[Web3.toChecksumAddress(val)]['missedCount'] = 0
                message = "We have a new validator welcome: " + str(val)
                self.bot.send_message(self.settings["ChatID"], message)

    def handle_command(self, update, bot):
        """Main command handler

           Returns None
           """
        user_id = update.effective_message.from_user.id

        chat_id = None
        command = None
        message_id = update.effective_message.message_id
        command = command_from_message(update.effective_message)
        command = command.split("@")[0]

        user = update.effective_user
        from_user_id = "UNKNOWN"
        fom_user_name = "UNKNOWN"
        if user:
            from_user = user.id
            from_user_name = user.username
        else:
            return

        if update.effective_message.chat:
            chat_id = update.effective_message.chat.id

        try:
            message = message_from_message(update.effective_message).lstrip()
        except Exception as e:
            message = ''
            printLogs("Catch")
        if (user_id in self.settings["admins"]):
            if command == '/add_node':
                if (message == ''):
                    self.bot.send_message(chat_id, "Cannot add node No node given")
                    return

                listOfNodes = message.split(",")
                added = ''
                for node in listOfNodes:
                    node = Web3.toChecksumAddress(node.strip())
                    if 'ID' in self.nodes[node]:
                        self.bot.send_message(chat_id, "node " + str(node) + " already belongs to @" + self.nodes[node]['username'])
                    else:
                        self.nodes[node]['ID'] = from_user
                        self.nodes[node]['username'] = from_user_name
                        added += node + '\n'
                if(added != ''):
                    self.bot.send_message(chat_id, "@" + str(from_user_name) + " added:\n" + added )
                self.saveSettings(self.nodes, nodeList)
            if command == '/remove_node':
                if (message == ''):
                    self.bot.send_message(chat_id, "Cannot add node No node given")
                    return

                listOfNodes = message.split(",")
                removed = ''
                for node in listOfNodes:
                    node = Web3.toChecksumAddress(node.strip())
                    if 'ID' in self.nodes[node]:
                        if from_user == self.nodes[node]['ID']:
                            del self.nodes[node]['ID']
                            del self.nodes[node]['username']
                            removed += node + '\n'
                if (removed != ''):
                    self.bot.send_message(chat_id, "@" + str(from_user_name) + " removed:\n" + removed)
                self.saveSettings(self.nodes, nodeList)

    def flagErrors(self, node):
        if self.nodes[node]['missedCount'] >= self.settings["MissedCount"]:
            if (int(time.time()) - self.nodes[node]['lastWarned'] > (int(self.settings["timeOut"]) * 60 * 60)):
                user = ''
                if 'username' in self.nodes[node]:
                    user = '@' + self.nodes[node]['username']

                block = lastBlock()
                message = user + " node: " + node + " has not mined a block since " + str(self.nodes[node]['lastBlock']) + " (" + str(block - int(self.nodes[node]['lastBlock']) + " blocks ago)")

                self.bot.send_message(self.settings["ChatID"],message)
                self.nodes[node]['lastWarned'] = time.time()

    def checkEndOfCycle(self):
        time.sleep(60*60*HOURS_TO_WAIT)
        for i in len(self.collectedSigData):
            address = self.collectedSigData[i]['authorityResponsibleForRelay']
            if(checkIfRelayed(address) == False):
                user = ''
                if 'username' in self.nodes[address]:
                    user = '@' + self.nodes[address]['username']

                block = lastBlock()
                message = user + " node: " + address + " was meant to relay to mainnet but still hasen't previous cycle ended ~3hours ago"
                self.bot.send_message(self.settings["ChatID"], message)

    def checkBlockQueue(self):
        lastSet = {}
        if self.blockQueue.qsize() >= self.numberOfNodes:
            printLogs("running queue length " + str(self.blockQueue.qsize()))
            if len(getValidators()) != self.numberOfNodes:
                printLogs("new Validator set")
                self.grabValidators()
                while not self.blockQueue.empty():
                    try:
                        self.blockQueue.get(False)
                    except queue.Empty:
                        continue
                printLogs("queue empty " + str(self.blockQueue.qsize()))
            else:
                for i in range (0,self.numberOfNodes):
                    blockDetails = self.blockQueue.get()
                    if blockDetails['miner'] not in lastSet:
                        lastSet[blockDetails['miner']] = {}
                        lastSet[blockDetails['miner']]['count'] = 1
                        lastSet[blockDetails['miner']]['lastBlock'] = blockDetails['block']
                    else:
                        lastSet[blockDetails['miner']]['count'] += 1
                        lastSet[blockDetails['miner']]['lastBlock'] = blockDetails['block']
                if int(blockDetails['block']) > (int(self.currentEndOfCycle) + 100):
                    self.collectedSigData = grabDataFromGraphQL()
                    if( int(self.collectedSigData[0]['blockNumber']) > (int(self.currentEndOfCycle)) and int(self.collectedSigData[1]['blockNumber']) > (int(self.currentEndOfCycle))):
                        #if we are 100 blocks passed the last end of cycle then grab the new end of cycle block
                        self.currentEndOfCycle = getEndOfCycleBlock()
                        #create a thread which will wait 2hours before checking that the blocks have been relayed
                        Thread(target=self.checkEndOfCycle).start()

                for node in self.nodes:
                    if node not in lastSet:
                        printLogs("missed a block " + node)
                        printLogs(str(node) + "missed last block mined = " + str(self.nodes[node]['lastBlock']))
                        self.nodes[node]['missedCount'] += 1
                        self.flagErrors(node)
                    else:
                        self.nodes[node]['lastBlock'] = lastSet[node]['lastBlock']
                        self.nodes[node]['missedCount'] = 0


    def checkBalance(self):
        for node in self.nodes:
            balance = getBalance(node)
            message = ''
            if balance['eth'] <= self.settings["EthWarning"]:
                message += 'Eth balance low (' + str(balance['eth']) + ')\n'
            if balance['fuse'] <= self.settings['FuseWarning']:
                message += 'Fuse balance low (' + str(balance['fuse']) + ')\n'

            if message != '':
                user = ''
                if 'username' in self.nodes[node]:
                    user = '@' + self.nodes[node]['username']

                message = user + ' ' + str(node) + '\n' + message
                self.bot.send_message(self.settings["ChatID"], message)

    def start(self):
        updater = Updater(token=self.settings["BOTKey"], use_context=True)
        dp = updater.dispatcher

        # command handler
        dp.add_handler(
            CommandHandler(
                command=self.available_commands,
                callback=self.handle_command,
                filters=Filters.all,
            )
        )

        schedule.every(1).minutes.do(self.checkBlockQueue)
        schedule.every().day.at("12:00").do(self.checkBalance)

        updater.start_polling()

        while (1):
            schedule.run_pending()
            time.sleep(5)

        updater.idle()

if __name__ == '__main__':
    c = DownBot()
    c.start()
