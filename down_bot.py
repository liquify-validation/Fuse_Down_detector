import os
import os.path
import json
import telegram
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler
import schedule
from botTools import *
from fuse import *
from multiprocessing import Queue
import queue
from web3 import Web3
from threading import Thread
import time
from flask import Flask, jsonify, abort, send_file, url_for, render_template
from threading import Thread
from flask_cors import CORS, cross_origin
from PIL import Image
import numpy as np
import copy

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
nodeListOld = "nodes_old.json"

def printLogs(message):
    if debug:
        print(message)

command_list = ['update_admins','info','set_eth_warning','set_fuse_warning','add_node','remove_node','set_dead_time','add_name','add_website','add_contact','override_info','set_delegation','set_photo','remove_delegation','set_photo_override','add_locked_account','remove_locked_account','get_locked_account']
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

Leon = ""
Andy = ""
Mark = ""



class DownBot:
    def __init__(self):

        self.available_commands = command_list

        # check if we have passed json file containing chat data
        self.parseSettings()
        self.parseNodes()
        self.parseOldNodes()
        #self.settings["lockedAccounts"] = []
    
        self.lastCheck = time.time()

        self.bot = telegram.Bot(token=defaultKey)
        self.grabAdmins(self.bot)
        self.grabValidators()
        self.blockQueue = Queue()

        self.currentEndOfCycle = getEndOfCycleBlock()

        self.checkBalance()

        createBlockThread(self.blockQueue)

        self.collectedSigData = []

        self.settings['ActiveBallots'] = {}
        self.fillActiveBallots(getOpenBallots())

        self.users = {}

        self.stats = {}

        self.stats['totalSupply'] = {}
        self.stats['totalSupply']['block'] = 0
        self.stats['totalSupply']['supply'] = 0
        
        self.stats['circSupply'] = {}

        self.fillSupplies()

    def fillSupplies(self):
        block = getStartOfCycleBlock()
        self.stats['totalSupply']['block'] = block
        self.stats['totalSupply']['supply'] = getTotalSupply(block)

        circ = getCircSupply(self.stats['totalSupply']['supply'], block, self.settings["lockedAccounts"])
        self.stats['circSupply'] = copy.deepcopy(circ)

    def fillActiveBallots(self, ballots):
        if ballots == None:
            self.settings['ActiveBallots'] = {}
            return

        for ballot in ballots:
            if ballot not in self.settings['ActiveBallots']:
                print("new ballot " + str(ballot))
                self.settings['ActiveBallots'][ballot] = {}
                self.settings['ActiveBallots'][ballot]['startBlock'] = ballots[ballot]['startBlock']
                self.settings['ActiveBallots'][ballot]['endBlock'] = ballots[ballot]['endBlock']
                self.settings['ActiveBallots'][ballot]['disc'] = ballots[ballot]['disc']
                self.settings['ActiveBallots'][ballot]['resultsLastSent'] = 0
                self.bot.send_message(self.settings["ChatID"],"A new ballot has been added ballot open between blocks: " + str(self.settings['ActiveBallots'][ballot]['startBlock']) + "-" + str(self.settings['ActiveBallots'][ballot]['endBlock']) + "\nBallot ID = " + str(ballot) + "\nDiscription: " + str(self.settings['ActiveBallots'][ballot]['disc']))
                
        self.saveSettings(self.settings, chatSettingsFile)

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
            self.settings["lockedAccounts"] = []

    def parseNodes(self):
        if os.path.exists(os.path.join(__location__, nodeList)):
            printLogs("loading Nodes")
            with open(nodeList) as json_file:
                self.nodes = json.load(json_file)
            for node in self.nodes:
                if 'forDelegation' not in self.nodes[node]:
                    self.nodes[node]['forDelegation'] = 0
            self.saveSettings(self.nodes, nodeList)
        else:
            self.nodes = {}

    def parseOldNodes(self):
        if os.path.exists(os.path.join(__location__, nodeListOld)):
            printLogs("loading Old nodes")
            with open(nodeListOld) as json_file:
                self.nodesOld = json.load(json_file)
            self.saveSettings(self.nodes, nodeList)
        else:
            self.nodesOld = {}


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
                if val in self.nodesOld:
                    del self.nodesOld[val]
                self.nodes[Web3.toChecksumAddress(val)] = {}
                self.nodes[Web3.toChecksumAddress(val)]['lastBlock'] = 0
                self.nodes[Web3.toChecksumAddress(val)]['lastWarned'] = 0
                self.nodes[Web3.toChecksumAddress(val)]['missedCount'] = 0
                self.nodes[Web3.toChecksumAddress(val)]['totalMissed'] = 0
                self.nodes[Web3.toChecksumAddress(val)]['totalValidated'] = 0
                self.nodes[Web3.toChecksumAddress(val)]['upTime'] = 1
                self.nodes[Web3.toChecksumAddress(val)]['firstSeen'] = time.time()
                self.nodes[Web3.toChecksumAddress(val)]['forDelegation'] = 0
                message = "We have a new validator welcome: " + str(val)
                self.bot.send_message(self.settings["ChatID"], message)

        valToRemove = []

        for node in self.nodes:
            if node not in valList:
                valToRemove.append(node)

        for key in valToRemove:
            if key not in self.nodesOld:
                self.nodesOld[key] = copy.deepcopy(self.nodes[key])
                self.nodesOld[key]['numberOfCyclesLastSeen'] = 0
            del self.nodes[key]
            print("removed " + key)

    def incOldNodes(self):
        valToRemove = []

        for key in self.nodesOld:
            self.nodesOld[key]['numberOfCyclesLastSeen'] += 1
            if self.nodesOld[key]['numberOfCyclesLastSeen'] == 10:
                valToRemove.append(key)

        for key in valToRemove:
            del self.nodesOld[key]
            print("removed old node: " + key)

        self.saveSettings(self.nodesOld, nodeListOld)

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
                    if node in self.nodes:
                        if 'ID' in self.nodes[node]:
                            self.bot.send_message(chat_id, "node " + str(node) + " already belongs to @" + self.nodes[node]['username'])
                        else:
                            self.nodes[node]['ID'] = from_user
                            self.nodes[node]['username'] = from_user_name
                            #self.nodes[node]['forDelegation'] = 1
                            added += node + '\n'
                if(added != ''):
                    self.bot.send_message(chat_id, "@" + str(from_user_name) + " added:\n" + added )
                self.saveSettings(self.nodes, nodeList)
            elif command == '/remove_node':
                if (message == ''):
                    self.bot.send_message(chat_id, "Cannot add node No node given")
                    return

                listOfNodes = message.split(",")
                removed = ''
                for node in listOfNodes:
                    node = Web3.toChecksumAddress(node.strip())
                    if node in self.nodes:
                        if 'ID' in self.nodes[node]:
                            if from_user == self.nodes[node]['ID']:
                                del self.nodes[node]['ID']
                                del self.nodes[node]['username']
                                if 'website' in self.nodes[node]:
                                    del self.nodes[node]['website']
                                if 'email' in self.nodes[node]:
                                    del self.nodes[node]['email']
                                removed += node + '\n'
                if (removed != ''):
                    self.bot.send_message(chat_id, "@" + str(from_user_name) + " removed:\n" + removed)
                self.saveSettings(self.nodes, nodeList)
            elif command == '/set_delegation':
                if (message == ''):
                    self.bot.send_message(chat_id, "No node address given")
                    return

                nodeAddr = Web3.toChecksumAddress(message.strip())

                for node in self.nodes:
                    if 'ID' in self.nodes[node]:
                        if from_user == self.nodes[node]['ID']:
                            if self.nodes[node]['forDelegation'] == 1:
                                self.bot.send_message(chat_id, "you already have a node for delegation please remove it first " + node)
                                return

                if nodeAddr in self.nodes:
                    if 'ID' in self.nodes[nodeAddr]:
                        if from_user == self.nodes[nodeAddr]['ID']:
                            self.nodes[nodeAddr]['forDelegation'] = 1
                            self.bot.send_message(chat_id, "Node " + nodeAddr + " is now open for delegation")
                        else:
                            self.bot.send_message(chat_id, "you are not the owner of this node!")
                    else:
                        self.bot.send_message(chat_id, "This node has not been registered")
                else:
                    self.bot.send_message(chat_id, "This is not an active validator")
            elif command == '/remove_delegation':
                if (message == ''):
                    self.bot.send_message(chat_id, "No node address given")
                    return

                nodeAddr = Web3.toChecksumAddress(message.strip())

                if nodeAddr in self.nodes:
                    if 'ID' in self.nodes[nodeAddr]:
                        if from_user == self.nodes[nodeAddr]['ID']:
                            self.nodes[nodeAddr]['forDelegation'] = 0
                            self.bot.send_message(chat_id, "Node " + nodeAddr + " is now closed for delegation")
                        else:
                            self.bot.send_message(chat_id, "you are not the owner of this node!")
                    else:
                        self.bot.send_message(chat_id, "This node has not been registered")
                else:
                    self.bot.send_message(chat_id, "This is not an active validator")
            elif command == '/add_name':
                if (message == ''):
                    self.bot.send_message(chat_id, "Cannot add name no name given")
                    return

                added_to = ''
                for node in self.nodes:
                    if 'ID' in self.nodes[node]:
                        if self.nodes[node]['ID'] == from_user:
                            self.nodes[node]['name'] = message
                            added_to += node+'\n'

                if added_to != '':
                    self.bot.send_message(chat_id, "node name " + message + " added to\n" + added_to)
                else:
                    self.bot.send_message(chat_id, "you have no registered nodes")

                self.saveSettings(self.nodes, nodeList)
            elif command == '/add_website':
                if (message == ''):
                    self.bot.send_message(chat_id, "Cannot add name no name given")
                    return

                added_to = ''
                for node in self.nodes:
                    if 'ID' in self.nodes[node]:
                        if self.nodes[node]['ID'] == from_user:
                            self.nodes[node]['website'] = message
                            added_to += node + '\n'

                if added_to != '':
                    self.bot.send_message(chat_id, "website " + message + " added to\n" + added_to)
                else:
                    self.bot.send_message(chat_id, "you have no registered nodes")

                self.saveSettings(self.nodes, nodeList)
            elif command == '/add_contact':
                if (message == ''):
                    self.bot.send_message(chat_id, "Cannot add name no name given")
                    return

                added_to = ''
                for node in self.nodes:
                    if 'ID' in self.nodes[node]:
                        if self.nodes[node]['ID'] == from_user:
                            self.nodes[node]['email'] = message
                            added_to += node + '\n'

                if added_to != '':
                    self.bot.send_message(chat_id, "Contact email " + message + " added to\n" + added_to)
                else:
                    self.bot.send_message(chat_id, "you have no registered nodes")

                self.saveSettings(self.nodes, nodeList)
            elif command == '/override_info':
                stringUser = str(from_user)
                if (stringUser == Andy or stringUser == Mark or stringUser == Leon):
                    if (message == ''):
                        self.bot.send_message(chat_id, "format <node,name,website,email>")
                        return

                    data = message.split(",")
                    if len(data) != 4:
                        self.bot.send_message(chat_id, "format <node,name,website,email>")
                        return

                    node = Web3.toChecksumAddress(data[0].strip())
                    if node in self.nodes:
                        self.nodes[node]['name'] = data[1]
                        self.nodes[node]['website'] = data[2]
                        self.nodes[node]['email'] = data[3]

                        self.nodes[node]['forDelegation'] = 1

                        self.bot.send_message(chat_id, "Node: " + node + " configured as name = " + data[1] + " website = " + data[2] + " email = " + data[3])
                    else:
                        self.bot.send_message(chat_id, "Node: " + node + " not found!")
                        return
                else:
                    return
            elif command == '/set_photo':
                foundYourNodes = False
                nodeName = ''

                for node in self.nodes:
                    if 'ID' in self.nodes[node]:
                        if self.nodes[node]['ID'] == from_user:
                            if 'name' in self.nodes[node]:
                                foundYourNodes = True
                                nodeName = self.nodes[node]['name']

                if not foundYourNodes:
                    self.bot.send_message(chat_id, "You have no nodes registered")
                    return

                if from_user not in self.users:
                    self.users[from_user] = {}

                self.users[from_user]['time'] = time.time()
                self.users[from_user]['name'] = nodeName
                self.bot.send_message(chat_id, "The next photo you send me within the next 2 mins will be used as your logo :)")
            elif command == '/set_photo_override':
                stringUser = str(from_user)
                if (stringUser == Andy or stringUser == Mark or stringUser == Leon):
                    if (message == ''):
                        self.bot.send_message(chat_id, "No node name specified")
                        return

                    foundNode = False

                    for node in self.nodes:
                        if 'name' in self.nodes[node]:
                            if message == self.nodes[node]['name']:
                                foundNode = True

                    if not foundNode:
                        self.bot.send_message(chat_id, "No node with name: " + str(message) + " found")
                        return

                    if from_user not in self.users:
                        self.users[from_user] = {}

                    self.users[from_user]['time'] = time.time()
                    self.users[from_user]['name'] = message
                    self.bot.send_message(chat_id, "The next photo you send me within the next 2 mins will be used as your logo for " + str(message))
            elif command == '/add_locked_account':
                stringUser = str(from_user)
                if (stringUser == Andy or stringUser == Mark or stringUser == Leon):
                    if (message == ''):
                        self.bot.send_message(chat_id, "Cannot add locked account(s) No accounts given")
                        return

                    listOfAddrs = message.split(",")
                    added = ''
                    for addr in listOfAddrs:
                        if (checkAddressIsValid(addr) == False):
                            self.bot.send_message(chat_id, "Sorry " + addr + " is not a valid address")
                            time.sleep(0.1)
                        else:
                            addr = Web3.toChecksumAddress(addr.strip())
                            if addr not in self.settings["lockedAccounts"]:
                                self.settings["lockedAccounts"].append(addr)
                                added += addr + '\n'
                    if(added != ''):
                        self.bot.send_message(chat_id, "@" + str(from_user_name) + " added new locked address:\n" + added )
                    self.saveSettings(self.settings, chatSettingsFile)
                    self.fillSupplies()
            elif command == '/get_locked_account':
                stringUser = str(from_user)
                if (stringUser == Andy or stringUser == Mark or stringUser == Leon):
                    lockedString = ''
                    for account in self.settings["lockedAccounts"]:
                        lockedString += "• " + account + "\n"
                        lockedString += "\n"
                    if (lockedString == ''):
                        lockedString = "no locked account"
                    self.bot.send_message(chat_id, lockedString)
            elif command == '/remove_locked_account':
                stringUser = str(from_user)
                if (stringUser == Andy or stringUser == Mark or stringUser == Leon):
                    if (message == ''):
                        self.bot.send_message(chat_id, "Cannot add locked account(s) No accounts given")
                        return

                    listOfAddrs = message.split(",")
                    removed = ''
                    for addr in listOfAddrs:
                        if addr in self.settings["lockedAccounts"]:
                            self.settings["lockedAccounts"].remove(addr)
                            removed += addr + '\n'
                    if(removed != ''):
                        self.bot.send_message(chat_id, "@" + str(from_user_name) + " removed locked address:\n" + removed )
                    self.saveSettings(self.settings, chatSettingsFile)
                    self.fillSupplies()

    def flagErrors(self, node):
        if self.nodes[node]['missedCount'] >= self.settings["MissedCount"]:
            if (int(time.time()) - self.nodes[node]['lastWarned'] > (int(self.settings["timeOut"]) * 60 * 60)):
                user = ''
                if 'username' in self.nodes[node]:
                    user = '@' + self.nodes[node]['username']

                block = lastBlock()
                message = user + " node: " + node + " has not mined a block since " + str(self.nodes[node]['lastBlock']) + " (" + str(int(block) - int(self.nodes[node]['lastBlock'])) + " blocks ago)"

                self.bot.send_message(self.settings["ChatID"],message)
                self.nodes[node]['lastWarned'] = time.time()
                self.saveSettings(self.nodes, nodeList)

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

    def displayBallot(self, blockNumber):
        removeList = []
        print("display ballot")
        for ballot in self.settings['ActiveBallots']:
            print("ballot " + str(ballot))
            if blockNumber > self.settings['ActiveBallots'][ballot]['endBlock']:
                #ballot has closed
                resStr = getBallotResults(ballot)
                self.bot.send_message(self.settings["ChatID"], "Ballot " + str(ballot) + " has now closed final results = " + resStr)
                removeList.append(ballot)
            elif blockNumber > self.settings['ActiveBallots'][ballot]['startBlock'] and int(time.time()) > (self.settings['ActiveBallots'][ballot]['resultsLastSent'] + (60*60*24)):
                if self.settings['ActiveBallots'][ballot]['resultsLastSent'] != 0:
                    resStr = getBallotResults(ballot)
                    self.bot.send_message(self.settings["ChatID"],"Ballot " + str(ballot) + " results so far = " + resStr)
                else:
                    self.bot.send_message(self.settings["ChatID"],"A new ballot is now open for voting until block: " + str(self.settings['ActiveBallots'][ballot]['endBlock']) + "\nBallot ID = " + str(ballot) + "\nDiscription: " + str(self.settings['ActiveBallots'][ballot]['disc']))

                self.settings['ActiveBallots'][ballot]['resultsLastSent'] = int(time.time())

        for bal in removeList:
            del self.settings['ActiveBallots'][bal]



    def checkBlockQueue(self):
        lastSet = {}
        if self.blockQueue.qsize() >= self.numberOfNodes:
            self.lastCheck = time.time()
            printLogs("last check " + str(self.lastCheck))
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

                self.displayBallot(blockDetails['block'])

                if int(blockDetails['block']) > (int(self.currentEndOfCycle) + 300):
                    self.fillSupplies()
                    self.collectedSigData = grabDataFromGraphQL()
                    if( int(self.collectedSigData[0]['blockNumber']) > (int(self.currentEndOfCycle)) and int(self.collectedSigData[1]['blockNumber']) > (int(self.currentEndOfCycle))):
                        #if we are 100 blocks passed the last end of cycle then grab the new end of cycle block
                        self.currentEndOfCycle = getEndOfCycleBlock()
                        #create a thread which will wait 2hours before checking that the blocks have been relayed
                        Thread(target=self.checkEndOfCycle).start()
                    else:
                        self.bot.send_message(self.settings["ChatID"],"ERROR: Failed to relay end of cycle on fuse net within 300 blocks!")

                    self.incOldNodes()
                    #check to see if a vote is open
                    self.fillActiveBallots(getOpenBallots())
                    self.currentEndOfCycle = getEndOfCycleBlock()

                for node in self.nodes:
                    if node not in lastSet:
                        printLogs("missed a block " + node)
                        printLogs(str(node) + "missed last block mined = " + str(self.nodes[node]['lastBlock']))
                        self.nodes[node]['missedCount'] += 1
                        self.nodes[node]['totalMissed'] += 1
                        self.flagErrors(node)
                    else:
                        self.nodes[node]['lastBlock'] = lastSet[node]['lastBlock']
                        self.nodes[node]['missedCount'] = 0
                        self.nodes[node]['totalValidated'] += 1

                    self.nodes[node]['upTime'] = (self.nodes[node]['totalValidated']/(self.nodes[node]['totalValidated'] + self.nodes[node]['totalMissed'])*100)
            self.saveSettings(self.nodes, nodeList)
            self.saveSettings(self.settings, chatSettingsFile)

    def image_handler(self, update, bot):
        message = update.effective_message
        user = message.from_user
        from_user = message.from_user.id
        chat_id = message.chat.id
        
        print("photo from: " + str(from_user))

        if from_user in self.users:
            print("in list")
            if (int(time.time() - self.users[from_user]['time']) < 120):
                print("in time")
                file = self.bot.getFile(update.message.photo[-1].file_id)
                file.download('temp.jpg')
                im = Image.open('temp.jpg')
                if ( im.size[0] != im.size[1] ):
                    self.bot.send_message(chat_id, "Image is not square making it square!")
                sqrWidth = np.ceil(np.sqrt(im.size[0] * im.size[1])).astype(int)
                im_resize = im.resize((sqrWidth, sqrWidth))
                small = im_resize.resize((64,64), Image.ANTIALIAS)

                name = self.users[from_user]['name']

                for node in self.nodes:
                    if 'name' in self.nodes[node]:
                        if name == self.nodes[node]['name']:
                            if 'photo' not in self.nodes[node]:
                                self.nodes[node]['photo'] = ''
                            self.nodes[node]['photo'] = 'logos/' + name + '.jpg'

                small.save('logos/' + name +'.jpg')

                self.bot.send_message(chat_id, "Photo has been set!")
                self.bot.send_photo(chat_id, photo=open('logos/' + name +'.jpg', 'rb'))
                os.remove("temp.jpg")
                self.saveSettings(self.nodes, nodeList)

    def checkBalance(self):
        test = 1
        # for node in self.nodes:
        #     balance = getBalance(node)
        #     message = ''
        #     if balance['eth'] <= self.settings["EthWarning"]:
        #         message += 'Eth balance low (' + str(balance['eth']) + ')\n'
        #     if balance['fuse'] <= self.settings['FuseWarning']:
        #         message += 'Fuse balance low (' + str(balance['fuse']) + ')\n'
        #
        #     if message != '':
        #         user = ''
        #         if 'username' in self.nodes[node]:
        #             user = '@' + self.nodes[node]['username']
        #
        #         message = user + ' ' + str(node) + '\n' + message
        #         self.bot.send_message(self.settings["ChatID"], message)

    def getNodes(self):
        return self.nodes

    def getOldNodes(self):
        return self.nodesOld

    def getLastCheck(self):
        return self.lastCheck

    def getTotal(self):
        return self.stats['totalSupply']

    def getCirc(self):
        return self.stats['circSupply']

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

        dp.add_handler(MessageHandler(
            Filters.photo, lambda bot, update: self.image_handler(bot, update)
        ))

        schedule.every(1).minutes.do(self.checkBlockQueue)
        schedule.every().day.at("12:00").do(self.checkBalance)

        updater.start_polling()

        while (1):
            schedule.run_pending()
            time.sleep(5)

        updater.idle()

downBot = DownBot()


@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404


@app.errorhandler(500)
def error(e):
    return jsonify(error=str(e)), 500

@app.route('/bot/api/v1/health', methods=['GET'])
@cross_origin()
def bot_health():
    timeNow = time.time()
    lastCheck = downBot.getLastCheck()
    healthStr = 'Bot up'

    if lastCheck != 0:
        if (int(timeNow - lastCheck) > 60 * 20):
            abort(500, description="data is stale")
        else:
            healthStr += " Data valid as of " + str(int(timeNow - lastCheck)) + "seconds ago"

    return jsonify({'health ': healthStr})

@app.route('/bot/api/v1/stats/supply', methods=['GET'])
@cross_origin()
def get_total_supply():
    supply = downBot.getTotal()

    return jsonify(block=supply['block'],
                   total_supply=supply['supply'])

@app.route('/bot/api/v1/stats/circulating', methods=['GET'])
@cross_origin()
def get_circulating_supply():
    circ = downBot.getCirc()

    return jsonify(circ)

@app.route('/bot/api/v1/getNodeLogo=<node_id>', methods=['GET'])
@cross_origin()
def get_Logo(node_id):
    nodes = downBot.getNodes()
    if node_id not in nodes:
        abort(404, description="node not found")

    node = nodes[node_id]
    if len(node) == 0:
        abort(404, description="node not found")
    if 'photo' not in node:
        abort(404, description="photo for node not found")

    if not os.path.isfile(node['photo']):
        abort(404, description="photo not found on server")

    return send_file(node['photo'], mimetype='image/gif')


@app.route('/bot/api/v1/node=<node_id>', methods=['GET'])
@cross_origin()
def get_task(node_id):
    nodes = downBot.getNodes()
    if node_id not in nodes:
        abort(404, description="node not found")

    node = nodes[node_id]
    if len(node) == 0:
        abort(404, description="node not found")
    return jsonify({'Node': node})


@app.route('/bot/api/v1/nodes', methods=['GET'])
@cross_origin()
def all_nodes():
    nodes = downBot.getNodes()
    return jsonify(nodes)

@app.route('/bot/api/v1/oldNodes', methods=['GET'])
@cross_origin()
def old_nodes():
    oldNodes = downBot.getOldNodes()
    return jsonify(oldNodes)

@app.route('/bot/api/v1/delegatedNodes', methods=['GET'])
@cross_origin()
def all_nodes_delegated():
    nodes = downBot.getNodes()
    delegated = {}

    for key in nodes:
        if 'forDelegation' in nodes[key]:
            if nodes[key]['forDelegation'] == 1:
                delegated[key] = nodes[key]

    return jsonify(delegated)


@app.route('/bot/api/v1/delegatedNodes_sorted', methods=['GET'])
@cross_origin()
def all_nodes_delegated_sorted():
    nodes = downBot.getNodes()
    delegated = {}

    for key in nodes:
        if 'name' in nodes[key]:
            if nodes[key]['name'] not in delegated:
                delegated[nodes[key]['name']] = {}

            delegated[nodes[key]['name']][key] = nodes[key]

    return jsonify(delegated)


@app.route('/bot/api/v1/offline', methods=['GET'])
@cross_origin()
def offline():
    nodes = downBot.getNodes()
    offlineNodes = ''

    for node in nodes:
        if nodes[node]['missedCount'] != 0:
            offlineNodes += str(node) + ', '

    if (offlineNodes != ''):
        offlineNodes = offlineNodes[:-2]
    else:
        offlineNodes = 'No nodes offline'

    return jsonify({'Offline Nodes ': offlineNodes})

def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)

@app.route("/api")
def all_links():
    links = []
    for rule in app.url_map.iter_rules():
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            links.append((url, rule.endpoint))
    return render_template("all_links.html", links=links)

def flaskThread():
     app.run(host= '0.0.0.0',port=80)


if __name__ == '__main__':
    worker = Thread(target=flaskThread)
    worker.start()

    downBot.start()
