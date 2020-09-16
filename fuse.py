import json
from web3 import Web3
import contractABI
from threading import Thread
import time
from datetime import datetime
import requests
from etherscan.accounts import Account
from multiprocessing import Queue
import calendar
import votingABI


HOURS_TO_SEARCH_BACK = 3

def getValidators():
    web3Fuse = Web3(Web3.HTTPProvider(contractABI.RPC_ADDRESS))
    fuseConsensusContract = web3Fuse.eth.contract(abi=contractABI.CONSENSUS_ABI, address=contractABI.CONSENSUS_ADDRESS)
    activeValidator = fuseConsensusContract.functions.getValidators().call()
    return activeValidator

def lastBlock():
    web3Fuse = Web3(Web3.HTTPProvider(contractABI.RPC_ADDRESS))
    return web3Fuse.eth.blockNumber

def getBalance(node):
    DECIMAL = 10 ** 18
    web3Eth = Web3(Web3.HTTPProvider(""))
    web3Fuse = Web3(Web3.HTTPProvider(contractABI.RPC_ADDRESS))
    ADDR = Web3.toChecksumAddress(node)

    fuseBalance = (float)(web3Fuse.eth.getBalance(ADDR))/DECIMAL
    ethBalance =  (float)(web3Eth.eth.getBalance(ADDR))/DECIMAL

    balance = {}
    balance['eth'] = ethBalance
    balance['fuse'] = fuseBalance

    return balance

def log_loop(web3Fuse, poll_interval,blockQueue):
    oldBlockNumber = 0
    while True:
        try:
            newBlock = web3Fuse.eth.blockNumber
            if (oldBlockNumber != newBlock):
                if oldBlockNumber + 1 != newBlock:
                    print("missedBlocks")

                time.sleep(0.4)
                block = web3Fuse.eth.getBlock(newBlock)
                blockDetails = {}
                blockDetails['block'] = newBlock
                blockDetails['miner'] = block['miner']
                blockDetails['timeStamp'] = block['timestamp']
                blockQueue.put(blockDetails)
                #print(newBlock)
                #print(web3Fuse.eth.getBlock(newBlock)['miner'])
                oldBlockNumber = newBlock
            time.sleep(poll_interval)
        except ConnectionError:
            print("Caught connection exception")
            time.sleep(0.5)

def createBlockThread(blockQueue):
    web3Fuse = Web3(Web3.HTTPProvider(contractABI.RPC_ADDRESS))
    worker = Thread(target=log_loop, args=(web3Fuse, 1.5, blockQueue), daemon=True)
    worker.start()

def getEndOfCycleBlock():
    web3Fuse = Web3(Web3.HTTPProvider(contractABI.RPC_ADDRESS))
    fuseConsensusContract = web3Fuse.eth.contract(abi=contractABI.CONSENSUS_ABI, address=contractABI.CONSENSUS_ADDRESS)
    endOfCycleBlockNum = fuseConsensusContract.functions.getCurrentCycleEndBlock().call()
    return endOfCycleBlockNum

def grabDataFromGraphQL():
    query = """{collectedSignaturesEvents(first: 2, orderBy: blockNumber, orderDirection: desc) {blockNumber txHash messageHash numberOfCollectedSignatures authorityResponsibleForRelay}}"""

    url = "https://graph.fuse.io/subgraphs/name/fuseio/fuse-consensus"
    r = requests.post(url, json={'query': query})
    collectedSigs = r.json()
    return collectedSigs['data']['collectedSignaturesEvents']

def checkIfRelayed(address):
    #check if a transcation has been sent to the consensus within the last 3 hours
    time_now_utc = datetime.utcnow()
    unixtime = calendar.timegm(time_now_utc.utctimetuple())
    api = Account(address=Web3.toChecksumAddress(address), api_key="")
    transactions = api.get_transaction_page(page=1, offset=10, sort='des',
                                            internal=False)

    relayed = False

    for trans in transactions:
        if Web3.toChecksumAddress(trans['to']) == Web3.toChecksumAddress('0x3014ca10b91cb3D0AD85fEf7A3Cb95BCAc9c0f79'):
            if int(trans['timeStamp']) > (unixtime - 60 * 60 * HOURS_TO_SEARCH_BACK):
                relayed = True
                break;

    return relayed

def getOpenBallots():
    web3Fuse = Web3(Web3.HTTPProvider(contractABI.RPC_ADDRESS))
    fuseVotingContract = web3Fuse.eth.contract(abi=votingABI.VOTING_ABI, address=votingABI.VOTING_ADDR)
    activeBallots = fuseVotingContract.functions.activeBallots().call()
    if len(activeBallots) != 0:
        returnData = {}
        for ballot in activeBallots:
            returnData[ballot] = {}
            ballotInfo = fuseVotingContract.functions.getBallotInfo(ballot,Web3.toChecksumAddress('0x3014ca10b91cb3D0AD85fEf7A3Cb95BCAc9c0f79')).call()
            returnData[ballot]['startBlock'] = ballotInfo[0]
            returnData[ballot]['endBlock'] = ballotInfo[1]
            returnData[ballot]['disc'] = ballotInfo[6]

        return returnData
    else:
        return None

def getBallotResults(ballotID):
    web3Fuse = Web3(Web3.HTTPProvider(contractABI.RPC_ADDRESS))
    fuseVotingContract = web3Fuse.eth.contract(abi=votingABI.VOTING_ABI, address=votingABI.VOTING_ADDR)
    fuseConsensusContract = web3Fuse.eth.contract(abi=contractABI.CONSENSUS_ABI, address=contractABI.CONSENSUS_ADDRESS)

    activeValidator = fuseConsensusContract.functions.getValidators().call()

    forVote = 0
    againstVote = 0
    abstained = 0

    totalValidators = len(activeValidator)

    for address in activeValidator:
        voted = fuseVotingContract.functions.getVoterChoice(int(ballotID), address).call()
        time.sleep(0.1)
        if voted == 0:
            abstained += 1
        elif voted == 1:
            forVote += 1
        elif voted == 2:
            againstVote += 1

    stringToRet = "total Validators = " + str(totalValidators) + " For = " + str(forVote) + " (" + str(
        (forVote / totalValidators) * 100) + '%) , Against = ' + str(againstVote) + " (" + str(
        (againstVote / totalValidators) * 100) + '%) , Abstained = ' + str(abstained) + " (" + str(
        (abstained / totalValidators) * 100) + '%)'

    return stringToRet
