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
        newBlock = web3Fuse.eth.blockNumber
        if (oldBlockNumber != newBlock):
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

def createBlockThread(blockQueue):
    web3Fuse = Web3(Web3.HTTPProvider(contractABI.RPC_ADDRESS))
    worker = Thread(target=log_loop, args=(web3Fuse, 1, blockQueue), daemon=True)
    worker.start()

def getEndOfCycleBlock():
    web3Fuse = Web3(Web3.HTTPProvider(contractABI.RPC_ADDRESS))
    fuseConsensusContract = web3Fuse.eth.contract(abi=contractABI.CONSENSUS_ABI, address=contractABI.CONSENSUS_ADDRESS)
    endOfCycleBlockNum = fuseConsensusContract.functions.getCurrentCycleEndBlock ().call()
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