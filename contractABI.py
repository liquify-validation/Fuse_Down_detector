CONSENSUS_ADDRESS = '0x3014ca10b91cb3D0AD85fEf7A3Cb95BCAc9c0f79'

RPC_ADDRESS = ''

TOKEN_CONTRACT_ABI = [
    {
        "constant": True,
        "inputs": [],
        "name": "name",
        "outputs": [
            {
                "name": "",
                "type": "string"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {
                "name": "_spender",
                "type": "address"
            },
            {
                "name": "_value",
                "type": "uint256"
            }
        ],
        "name": "approve",
        "outputs": [
            {
                "name": "",
                "type": "bool"
            }
        ],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "totalSupply",
        "outputs": [
            {
                "name": "",
                "type": "uint256"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {
                "name": "_from",
                "type": "address"
            },
            {
                "name": "_to",
                "type": "address"
            },
            {
                "name": "_value",
                "type": "uint256"
            }
        ],
        "name": "transferFrom",
        "outputs": [
            {
                "name": "",
                "type": "bool"
            }
        ],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "decimals",
        "outputs": [
            {
                "name": "",
                "type": "uint8"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [
            {
                "name": "_owner",
                "type": "address"
            }
        ],
        "name": "balanceOf",
        "outputs": [
            {
                "name": "balance",
                "type": "uint256"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "symbol",
        "outputs": [
            {
                "name": "",
                "type": "string"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {
                "name": "_to",
                "type": "address"
            },
            {
                "name": "_value",
                "type": "uint256"
            }
        ],
        "name": "transfer",
        "outputs": [
            {
                "name": "",
                "type": "bool"
            }
        ],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [
            {
                "name": "_owner",
                "type": "address"
            },
            {
                "name": "_spender",
                "type": "address"
            }
        ],
        "name": "allowance",
        "outputs": [
            {
                "name": "",
                "type": "uint256"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "payable": True,
        "stateMutability": "payable",
        "type": "fallback"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "name": "owner",
                "type": "address"
            },
            {
                "indexed": True,
                "name": "spender",
                "type": "address"
            },
            {
                "indexed": False,
                "name": "value",
                "type": "uint256"
            }
        ],
        "name": "Approval",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "name": "from",
                "type": "address"
            },
            {
                "indexed": True,
                "name": "to",
                "type": "address"
            },
            {
                "indexed": False,
                "name": "value",
                "type": "uint256"
            }
        ],
        "name": "Transfer",
        "type": "event"
    }
]


CONSENSUS_ABI = [{"constant": True, "inputs": [], "name": "getLastSnapshotTakenAtBlock",
                      "outputs": [{"name": "", "type": "uint256"}], "payable": False, "stateMutability": "view",
                      "type": "function"}, {"constant": True, "inputs": [{"name": "_p", "type": "uint256"}],
                                            "name": "pendingValidatorsAtPosition",
                                            "outputs": [{"name": "", "type": "address"}], "payable": False,
                                            "stateMutability": "view", "type": "function"},
                     {"constant": True, "inputs": [{"name": "_snapshotId", "type": "uint256"}],
                      "name": "getSnapshotAddresses", "outputs": [{"name": "", "type": "address[]"}], "payable": False,
                      "stateMutability": "view", "type": "function"},
                     {"constant": False, "inputs": [{"name": "_newAddress", "type": "address"}],
                      "name": "setProxyStorage", "outputs": [], "payable": False, "stateMutability": "nonpayable",
                      "type": "function"}, {"constant": True, "inputs": [{"name": "_address", "type": "address"},
                                                                         {"name": "_validator", "type": "address"}],
                                            "name": "delegatedAmount", "outputs": [{"name": "", "type": "uint256"}],
                                            "payable": False, "stateMutability": "view", "type": "function"},
                     {"constant": True, "inputs": [], "name": "SNAPSHOTS_PER_CYCLE",
                      "outputs": [{"name": "", "type": "uint256"}], "payable": False, "stateMutability": "view",
                      "type": "function"}, {"constant": True, "inputs": [], "name": "pendingValidatorsLength",
                                            "outputs": [{"name": "", "type": "uint256"}], "payable": False,
                                            "stateMutability": "view", "type": "function"},
                     {"constant": True, "inputs": [], "name": "newValidatorSetLength",
                      "outputs": [{"name": "", "type": "uint256"}], "payable": False, "stateMutability": "view",
                      "type": "function"},
                     {"constant": True, "inputs": [], "name": "DECIMALS", "outputs": [{"name": "", "type": "uint256"}],
                      "payable": False, "stateMutability": "view", "type": "function"},
                     {"constant": True, "inputs": [], "name": "isInitialized",
                      "outputs": [{"name": "", "type": "bool"}], "payable": False, "stateMutability": "view",
                      "type": "function"}, {"constant": True, "inputs": [], "name": "currentValidatorsLength",
                                            "outputs": [{"name": "", "type": "uint256"}], "payable": False,
                                            "stateMutability": "view", "type": "function"},
                     {"constant": True, "inputs": [], "name": "getMinStake",
                      "outputs": [{"name": "", "type": "uint256"}], "payable": False, "stateMutability": "pure",
                      "type": "function"}, {"constant": True, "inputs": [{"name": "_p", "type": "uint256"}],
                                            "name": "currentValidatorsAtPosition",
                                            "outputs": [{"name": "", "type": "address"}], "payable": False,
                                            "stateMutability": "view", "type": "function"},
                     {"constant": True, "inputs": [], "name": "newValidatorSet",
                      "outputs": [{"name": "", "type": "address[]"}], "payable": False, "stateMutability": "view",
                      "type": "function"}, {"constant": True, "inputs": [], "name": "CYCLE_DURATION_BLOCKS",
                                            "outputs": [{"name": "", "type": "uint256"}], "payable": False,
                                            "stateMutability": "view", "type": "function"},
                     {"constant": True, "inputs": [], "name": "getSnapshotsPerCycle",
                      "outputs": [{"name": "", "type": "uint256"}], "payable": False, "stateMutability": "pure",
                      "type": "function"}, {"constant": True, "inputs": [], "name": "requiredSignatures",
                                            "outputs": [{"name": "", "type": "uint256"}], "payable": False,
                                            "stateMutability": "view", "type": "function"},
                     {"constant": True, "inputs": [], "name": "isFinalized", "outputs": [{"name": "", "type": "bool"}],
                      "payable": False, "stateMutability": "view", "type": "function"},
                     {"constant": True, "inputs": [], "name": "getCurrentCycleStartBlock",
                      "outputs": [{"name": "", "type": "uint256"}], "payable": False, "stateMutability": "view",
                      "type": "function"}, {"constant": True, "inputs": [], "name": "currentValidators",
                                            "outputs": [{"name": "", "type": "address[]"}], "payable": False,
                                            "stateMutability": "view", "type": "function"},
                     {"constant": True, "inputs": [], "name": "getCycleDurationBlocks",
                      "outputs": [{"name": "", "type": "uint256"}], "payable": False, "stateMutability": "pure",
                      "type": "function"}, {"constant": True, "inputs": [], "name": "pendingValidators",
                                            "outputs": [{"name": "", "type": "address[]"}], "payable": False,
                                            "stateMutability": "view", "type": "function"},
                     {"constant": True, "inputs": [], "name": "getCurrentCycleEndBlock",
                      "outputs": [{"name": "", "type": "uint256"}], "payable": False, "stateMutability": "view",
                      "type": "function"},
                     {"constant": True, "inputs": [{"name": "_address", "type": "address"}], "name": "stakeAmount",
                      "outputs": [{"name": "", "type": "uint256"}], "payable": False, "stateMutability": "view",
                      "type": "function"},
                     {"constant": True, "inputs": [], "name": "MIN_STAKE", "outputs": [{"name": "", "type": "uint256"}],
                      "payable": False, "stateMutability": "view", "type": "function"},
                     {"constant": True, "inputs": [], "name": "getNextSnapshotId",
                      "outputs": [{"name": "", "type": "uint256"}], "payable": False, "stateMutability": "view",
                      "type": "function"}, {"constant": True, "inputs": [], "name": "getProxyStorage",
                                            "outputs": [{"name": "", "type": "address"}], "payable": False,
                                            "stateMutability": "view", "type": "function"},
                     {"constant": True, "inputs": [], "name": "shouldEmitInitiateChange",
                      "outputs": [{"name": "", "type": "bool"}], "payable": False, "stateMutability": "view",
                      "type": "function"},
                     {"constant": True, "inputs": [{"name": "_address", "type": "address"}], "name": "isValidator",
                      "outputs": [{"name": "", "type": "bool"}], "payable": False, "stateMutability": "view",
                      "type": "function"}, {"constant": True, "inputs": [{"name": "_address", "type": "address"}],
                                            "name": "isPendingValidator", "outputs": [{"name": "", "type": "bool"}],
                                            "payable": False, "stateMutability": "view", "type": "function"},
                     {"payable": True, "stateMutability": "payable", "type": "fallback"},
                     {"anonymous": False, "inputs": [{"indexed": False, "name": "newSet", "type": "address[]"}],
                      "name": "ChangeFinalized", "type": "event"},
                     {"anonymous": False, "inputs": [], "name": "ShouldEmitInitiateChange", "type": "event"},
                     {"anonymous": False, "inputs": [{"indexed": True, "name": "parentHash", "type": "bytes32"},
                                                     {"indexed": False, "name": "newSet", "type": "address[]"}],
                      "name": "InitiateChange", "type": "event"},
                     {"constant": False, "inputs": [{"name": "_initialValidator", "type": "address"}],
                      "name": "initialize", "outputs": [], "payable": False, "stateMutability": "nonpayable",
                      "type": "function"}, {"constant": True, "inputs": [], "name": "getValidators",
                                            "outputs": [{"name": "", "type": "address[]"}], "payable": False,
                                            "stateMutability": "view", "type": "function"},
                     {"constant": False, "inputs": [], "name": "finalizeChange", "outputs": [], "payable": False,
                      "stateMutability": "nonpayable", "type": "function"},
                     {"constant": False, "inputs": [], "name": "stake", "outputs": [], "payable": True,
                      "stateMutability": "payable", "type": "function"},
                     {"constant": False, "inputs": [{"name": "_validator", "type": "address"}], "name": "delegate",
                      "outputs": [], "payable": True, "stateMutability": "payable", "type": "function"},
                     {"constant": False, "inputs": [{"name": "_amount", "type": "uint256"}], "name": "withdraw",
                      "outputs": [], "payable": False, "stateMutability": "nonpayable", "type": "function"},
                     {"constant": False,
                      "inputs": [{"name": "_validator", "type": "address"}, {"name": "_amount", "type": "uint256"}],
                      "name": "withdraw", "outputs": [], "payable": False, "stateMutability": "nonpayable",
                      "type": "function"},
                     {"constant": False, "inputs": [], "name": "cycle", "outputs": [], "payable": False,
                      "stateMutability": "nonpayable", "type": "function"},
                     {"constant": False, "inputs": [], "name": "emitInitiateChange", "outputs": [], "payable": False,
                      "stateMutability": "nonpayable", "type": "function"}]
