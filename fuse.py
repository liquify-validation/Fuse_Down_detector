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
import collections
import errno
from socket import error as socket_error
import time
from autoscraper import AutoScraper
from utils import create_contract, fetch_events
import private

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
    web3Eth = Web3(Web3.HTTPProvider(private.INFURA))
    web3Fuse = Web3(Web3.HTTPProvider(contractABI.RPC_ADDRESS))
    ADDR = Web3.toChecksumAddress(node)

    fuseBalance = (float)(web3Fuse.eth.getBalance(ADDR))/DECIMAL
    ethBalance =  (float)(web3Eth.eth.getBalance(ADDR))/DECIMAL

    balance = {}
    balance['eth'] = ethBalance
    balance['fuse'] = fuseBalance

    return balance

def grabWallets():
    url = 'https://api.covalenthq.com/v1/1/tokens/0x970b9bb2c0444f5e81e9d0efb84c8ccdcdcaf84d/token_holders/?key=ckey_' + private.COVALENT_KEY
    eth = json.loads(requests.get(url).text)['data']['pagination']['total_count']
    url = 'https://api.covalenthq.com/v1/56/tokens/0x5857c96dae9cf8511b08cb07f85753c472d36ea3/token_holders/?key=ckey_' + private.COVALENT_KEY
    bsc = json.loads(requests.get(url).text)['data']['pagination']['total_count']
    wanted_list = ["Validators"]
    scraper = AutoScraper()
    url = 'https://explorer.fuse.io/'
    fuse = scraper.build(url, wanted_list)[1].replace(',', '')

    wallets = {'eth': eth, 'bsc': bsc, 'fuse': fuse}

    return wallets

def getValStats():
    DECIMAL = 10 ** 18
    vals = getValidators()

    returnDict = {}

    web3Fuse = Web3(Web3.HTTPProvider(contractABI.RPC_ADDRESS))
    fuseConsensusContract = web3Fuse.eth.contract(abi=contractABI.CONSENSUS_ABI, address=contractABI.CONSENSUS_ADDRESS)
    totalStaked = fuseConsensusContract.functions.totalStakeAmount().call() / DECIMAL

    for val in vals:
        returnDict[Web3.toChecksumAddress(val)] = {}
        returnDict[Web3.toChecksumAddress(val)]['deleagtes'] = fuseConsensusContract.functions.delegatorsLength(val).call()
        returnDict[Web3.toChecksumAddress(val)]['totalStaked'] = fuseConsensusContract.functions.stakeAmount(val).call() / DECIMAL
        returnDict[Web3.toChecksumAddress(val)]['valFee'] = (fuseConsensusContract.functions.validatorFee(val).call() / DECIMAL) * 100
        returnDict[Web3.toChecksumAddress(val)]['ratioOfStake'] = (returnDict[Web3.toChecksumAddress(val)]['totalStaked'] / totalStaked) * 100

    return returnDict

def checkAddressIsValid(address):
    checkSumAddr = Web3.toChecksumAddress(address)
    return Web3.isAddress(checkSumAddr)

def getTotalDelegates():
    vals = getValidators()
    web3Fuse = Web3(Web3.HTTPProvider(contractABI.RPC_ADDRESS))
    fuseConsensusContract = web3Fuse.eth.contract(abi=contractABI.CONSENSUS_ABI, address=contractABI.CONSENSUS_ADDRESS)
    numDelegates = 0

    for val in vals:
        numDelegates += fuseConsensusContract.functions.delegatorsLength(val).call()

    return numDelegates

def getTotalSupply(block):
    initSupply = 300000000
    blocksPerYear = 6307200
    
    burnt = 8173860.51897
    rewardsADDR = "0x63D4efeD2e3dA070247bea3073BCaB896dFF6C9B"
    
    web3Fuse = Web3(Web3.HTTPProvider(contractABI.RPC_ADDRESS))
    
    rewardContract = create_contract(web3Fuse, REWARDS_CONTRACT, Web3.toChecksumAddress(str(rewardsADDR)))

    rewards = list(fetch_events(lpContract.events.RewardedOnCycle,from_block=1))
    total = 0

    for re in rewards:
        total += re.args['amount']

    total = total/10**18

    totalSupply = initSupply + total - burnt

    return totalSupply

def getCircSupply(totalSupply, block, lockedAccountsList):
    circSupplyFuse = totalSupply

    RPC_ADDRESS = contractABI.RPC_ADDRESS
    DECIMAL = 10 ** 18
    web3Eth = Web3(Web3.HTTPProvider(private.INFURA))
    web3Fuse = Web3(Web3.HTTPProvider(RPC_ADDRESS))
    CONTRACT_ADDRESS = "0x970B9bB2C0444F5E81e9d0eFb84C8ccdcdcAf84d"
    WFUSE_CONTRACT = "0x0BE9e53fd7EDaC9F859882AfdDa116645287C629"
    wfuseWallet = Web3.toChecksumAddress("0xD418c5d0c4a3D87a6c555B7aA41f13EF87485Ec6")
    tokenContract = web3Eth.eth.contract(abi=contractABI.TOKEN_CONTRACT_ABI, address=CONTRACT_ADDRESS)
    wrappedFuseContract = web3Fuse.eth.contract(abi=contractABI.TOKEN_CONTRACT_ABI, address=WFUSE_CONTRACT)
    fuseConsensusContract = web3Fuse.eth.contract(abi=contractABI.CONSENSUS_ABI, address=contractABI.CONSENSUS_ADDRESS)

    totalSupplyMainnet = float(tokenContract.functions.totalSupply().call() / DECIMAL)


    for address in lockedAccountsList:
        addr = Web3.toChecksumAddress(address)
        fusenetBalance = float(web3Fuse.eth.getBalance(addr) / DECIMAL)
        print("fuse locked " + address + " " + str(fusenetBalance))
        circSupplyFuse = circSupplyFuse - fusenetBalance
        wFuseAmount = float(wrappedFuseContract.functions.balanceOf(address).call() / DECIMAL)
        circSupplyFuse = circSupplyFuse - wFuseAmount
    
    wFuseAmount = float(wrappedFuseContract.functions.balanceOf(wfuseWallet).call() / DECIMAL)

    print("wfuse " + str(wFuseAmount))

    circSupplyFuse = circSupplyFuse - 8173860.51897
    
    circSupplyMain = totalSupplyMainnet

    for address in lockedAccountsList:
        addr = Web3.toChecksumAddress(address)
        mainnetBalance = float(tokenContract.functions.balanceOf(addr).call() / DECIMAL)
        print("main locked " + address + " " + str(mainnetBalance))
        circSupplyMain = circSupplyMain - mainnetBalance

    stakedAmount = float(fuseConsensusContract.functions.totalStakeAmount().call() / DECIMAL)

    returnDict = collections.OrderedDict()
    returnDict['fuseBlock'] = block
    returnDict['ethereumBlock'] = web3Eth.eth.blockNumber
    returnDict['total'] = circSupplyFuse + circSupplyMain + stakedAmount
    returnDict['totalWithoutStake'] = circSupplyFuse + circSupplyMain
    returnDict['onFuseNetwork'] = circSupplyFuse
    returnDict['onEtherumNetwork'] = circSupplyMain
    returnDict['staked'] = stakedAmount
    returnDict['ratioStaked'] = (stakedAmount/returnDict['total']) * 100

    return returnDict

def getTotalSupplyVolt():
    DECIMAL = 10 ** 18
    RPC_ADDRESS = contractABI.RPC_ADDRESS
    web3Fuse = Web3(Web3.HTTPProvider(RPC_ADDRESS))
    voltContract = web3Fuse.eth.contract(abi=contractABI.VOLT_CONTRACT, address=contractABI.VOLTS_ADDRESS)

    totalVoltage = float(voltContract.functions.totalSupply().call() / DECIMAL)

    return totalVoltage

def getCircSupplyVolt(block,lockedAccountsList):
    DECIMAL = 10 ** 18
    total = getTotalSupplyVolt()
    circ = total
    RPC_ADDRESS = contractABI.RPC_ADDRESS
    web3Fuse = Web3(Web3.HTTPProvider(RPC_ADDRESS))
    voltContract = web3Fuse.eth.contract(abi=contractABI.VOLT_CONTRACT, address=contractABI.VOLTS_ADDRESS)

    for address in lockedAccountsList:
        addr = Web3.toChecksumAddress(address)
        circ -= float(voltContract.functions.balanceOf(address).call() / DECIMAL)

    returnDict = collections.OrderedDict()
    returnDict['fuseBlock'] = block
    returnDict['totalSupply'] = total
    returnDict['circSupply'] = circ
    returnDict['ratio'] = float(circ/total)
    
    return returnDict


def getCircSupplyV2(totalSupply, block, lockedAccountsList):
    returnDict = getCircSupply(totalSupply,block,lockedAccountsList)

    web3BSC = Web3(Web3.HTTPProvider('https://bsc-dataseed.binance.org/'))

    DECIMAL = 10 ** 18
    CONTRACT_ADDRESS_BSC = Web3.toChecksumAddress("0x5857c96dae9cf8511b08cb07f85753c472d36ea3")
    tokenContractBSC = web3BSC.eth.contract(abi=contractABI.TOKEN_CONTRACT_ABI, address=CONTRACT_ADDRESS_BSC)
    totalSupplyBSC = float(tokenContractBSC.functions.totalSupply().call() / DECIMAL)

    returnDict['bscBlock'] = web3BSC.eth.blockNumber
    returnDict['total'] = returnDict['total'] + totalSupplyBSC
    returnDict['onBSCNetwork'] = totalSupplyBSC
    
    return returnDict

def log_loop(web3Fuse, poll_interval,blockQueue):
    oldBlockNumber = 0
    while True:
        try:
            newBlock = web3Fuse.eth.blockNumber
            if newBlock > oldBlockNumber:
                if (oldBlockNumber != newBlock):
                    if (oldBlockNumber + 1 != newBlock) and oldBlockNumber != 0:
                        print("missedBlocks")
                        while (oldBlockNumber + 1 != newBlock):
                            print("ob: " + str(oldBlockNumber) + " nb: " + str(newBlock))
                            oldBlockNumber += 1
                            try:
                                block = web3Fuse.eth.getBlock(oldBlockNumber)
                                blockDetails = {}
                                blockDetails['block'] = oldBlockNumber
                                blockDetails['miner'] = block['miner']
                                blockDetails['timeStamp'] = block['timestamp']
                                blockDetails['numTransactions'] = len(block.transactions)
                                blockDetails['gasUsed'] = block.gasUsed
                                blockQueue.put(blockDetails)
                            except BaseException as e:
                                print(str(e))
                                continue
                time.sleep(0.6)
                try:
                    block = web3Fuse.eth.getBlock(newBlock)
                    blockDetails = {}
                    blockDetails['block'] = newBlock
                    blockDetails['miner'] = block['miner']
                    blockDetails['timeStamp'] = block['timestamp']
                    blockDetails['numTransactions'] = len(block.transactions)
                    blockDetails['gasUsed'] = block.gasUsed
                    blockQueue.put(blockDetails)
                    oldBlockNumber = newBlock
                except BaseException as e:
                    print(str(e))
                    continue
            time.sleep(poll_interval)
        except (socket_error, KeyError) as serr:
            print("Caught connection exception")
            time.sleep(0.5)

def createBlockThread(blockQueue):
    web3Fuse = Web3(Web3.HTTPProvider(contractABI.RPC_ADDRESS))
    worker = Thread(target=log_loop, args=(web3Fuse, 1.0, blockQueue), daemon=True)
    worker.start()

def getEndOfCycleBlock():
    web3Fuse = Web3(Web3.HTTPProvider(contractABI.RPC_ADDRESS))
    fuseConsensusContract = web3Fuse.eth.contract(abi=contractABI.CONSENSUS_ABI, address=contractABI.CONSENSUS_ADDRESS)
    endOfCycleBlockNum = fuseConsensusContract.functions.getCurrentCycleEndBlock().call()
    return endOfCycleBlockNum

def getStartOfCycleBlock():
    web3Fuse = Web3(Web3.HTTPProvider(contractABI.RPC_ADDRESS))
    fuseConsensusContract = web3Fuse.eth.contract(abi=contractABI.CONSENSUS_ABI, address=contractABI.CONSENSUS_ADDRESS)
    endOfCycleBlockNum = fuseConsensusContract.functions.getCurrentCycleStartBlock().call()
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
    api = Account(address=Web3.toChecksumAddress(address), api_key=private.ETHER_SCAN)
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


