CONSENSUS_ADDRESS = '0x3014ca10b91cb3D0AD85fEf7A3Cb95BCAc9c0f79'

VOLTS_ADDRESS = '0x34Ef2Cc892a88415e9f02b91BfA9c91fC0bE6bD4'

RPC_ADDRESS ='https://rpc.fuse.io' #'https://fuse-rpc.gateway.pokt.network/' #'https://rpc.fuse.io'#'https://oefusefull1.liquify.info'# 'https://fuse-mainnet.gateway.pokt.network/v1/lb/60d1a24d79eef000351e8949'

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


CONSENSUS_ABI = [
  {
    "type": "function",
    "stateMutability": "view",
    "payable": False,
    "outputs": [
      {
        "type": "uint256",
        "name": ""
      }
    ],
    "name": "getLastSnapshotTakenAtBlock",
    "inputs": [
      
    ],
    "constant": True
  },
  {
    "type": "function",
    "stateMutability": "view",
    "payable": False,
    "outputs": [
      {
        "type": "address",
        "name": ""
      }
    ],
    "name": "pendingValidatorsAtPosition",
    "inputs": [
      {
        "type": "uint256",
        "name": "_p"
      }
    ],
    "constant": True
  },
  {
    "type": "function",
    "stateMutability": "view",
    "payable": False,
    "outputs": [
      {
        "type": "address[]",
        "name": ""
      }
    ],
    "name": "getSnapshotAddresses",
    "inputs": [
      {
        "type": "uint256",
        "name": "_snapshotId"
      }
    ],
    "constant": True
  },
  {
    "type": "function",
    "stateMutability": "nonpayable",
    "payable": False,
    "outputs": [
      
    ],
    "name": "setProxyStorage",
    "inputs": [
      {
        "type": "address",
        "name": "_newAddress"
      }
    ],
    "constant": False
  },
  {
    "type": "function",
    "stateMutability": "view",
    "payable": False,
    "outputs": [
      {
        "type": "uint256",
        "name": ""
      }
    ],
    "name": "delegatedAmount",
    "inputs": [
      {
        "type": "address",
        "name": "_address"
      },
      {
        "type": "address",
        "name": "_validator"
      }
    ],
    "constant": True
  },
  {
    "type": "function",
    "stateMutability": "view",
    "payable": False,
    "outputs": [
      {
        "type": "uint256",
        "name": ""
      }
    ],
    "name": "SNAPSHOTS_PER_CYCLE",
    "inputs": [
      
    ],
    "constant": True
  },
  {
    "type": "function",
    "stateMutability": "view",
    "payable": False,
    "outputs": [
      {
        "type": "uint256",
        "name": ""
      }
    ],
    "name": "pendingValidatorsLength",
    "inputs": [
      
    ],
    "constant": True
  },
  {
    "type": "function",
    "stateMutability": "view",
    "payable": False,
    "outputs": [
      {
        "type": "uint256",
        "name": ""
      }
    ],
    "name": "newValidatorSetLength",
    "inputs": [
      
    ],
    "constant": True
  },
  {
    "type": "function",
    "stateMutability": "view",
    "payable": False,
    "outputs": [
      {
        "type": "uint256",
        "name": ""
      }
    ],
    "name": "DECIMALS",
    "inputs": [
      
    ],
    "constant": True
  },
  {
    "type": "function",
    "stateMutability": "nonpayable",
    "payable": False,
    "outputs": [
      
    ],
    "name": "withdraw",
    "inputs": [
      {
        "type": "uint256",
        "name": "_amount"
      }
    ],
    "constant": False
  },
  {
    "type": "function",
    "stateMutability": "view",
    "payable": False,
    "outputs": [
      {
        "type": "bool",
        "name": ""
      }
    ],
    "name": "isInitialized",
    "inputs": [
      
    ],
    "constant": True
  },
  {
    "type": "function",
    "stateMutability": "payable",
    "payable": True,
    "outputs": [
      
    ],
    "name": "stake",
    "inputs": [
      
    ],
    "constant": False
  },
  {
    "type": "function",
    "stateMutability": "view",
    "payable": False,
    "outputs": [
      {
        "type": "uint256",
        "name": ""
      }
    ],
    "name": "currentValidatorsLength",
    "inputs": [
      
    ],
    "constant": True
  },
  {
    "type": "function",
    "stateMutability": "nonpayable",
    "payable": False,
    "outputs": [
      
    ],
    "name": "setValidatorFee",
    "inputs": [
      {
        "type": "uint256",
        "name": "_amount"
      }
    ],
    "constant": False
  },
  {
    "type": "function",
    "stateMutability": "pure",
    "payable": False,
    "outputs": [
      {
        "type": "uint256",
        "name": ""
      }
    ],
    "name": "getMinStake",
    "inputs": [
      
    ],
    "constant": True
  },
  {
    "type": "function",
    "stateMutability": "view",
    "payable": False,
    "outputs": [
      {
        "type": "address",
        "name": ""
      }
    ],
    "name": "currentValidatorsAtPosition",
    "inputs": [
      {
        "type": "uint256",
        "name": "_p"
      }
    ],
    "constant": True
  },
  {
    "type": "function",
    "stateMutability": "payable",
    "payable": True,
    "outputs": [
      
    ],
    "name": "delegate",
    "inputs": [
      {
        "type": "address",
        "name": "_validator"
      }
    ],
    "constant": False
  },
  {
    "type": "function",
    "stateMutability": "view",
    "payable": False,
    "outputs": [
      {
        "type": "address[]",
        "name": ""
      }
    ],
    "name": "newValidatorSet",
    "inputs": [
      
    ],
    "constant": True
  },
  {
    "type": "function",
    "stateMutability": "nonpayable",
    "payable": False,
    "outputs": [
      
    ],
    "name": "cycle",
    "inputs": [
      
    ],
    "constant": False
  },
  {
    "type": "function",
    "stateMutability": "view",
    "payable": False,
    "outputs": [
      {
        "type": "address[]",
        "name": ""
      },
      {
        "type": "uint256[]",
        "name": ""
      }
    ],
    "name": "getDelegatorsForRewardDistribution",
    "inputs": [
      {
        "type": "address",
        "name": "_validator"
      },
      {
        "type": "uint256",
        "name": "_rewardAmount"
      }
    ],
    "constant": True
  },
  {
    "type": "function",
    "stateMutability": "view",
    "payable": False,
    "outputs": [
      {
        "type": "uint256",
        "name": ""
      }
    ],
    "name": "MAX_VALIDATORS",
    "inputs": [
      
    ],
    "constant": True
  },
  {
    "type": "function",
    "stateMutability": "nonpayable",
    "payable": False,
    "outputs": [
      
    ],
    "name": "finalizeChange",
    "inputs": [
      
    ],
    "constant": False
  },
  {
    "type": "function",
    "stateMutability": "pure",
    "payable": False,
    "outputs": [
      {
        "type": "uint256",
        "name": ""
      }
    ],
    "name": "getMaxValidators",
    "inputs": [
      
    ],
    "constant": True
  },
  {
    "type": "function",
    "stateMutability": "view",
    "payable": False,
    "outputs": [
      {
        "type": "uint256",
        "name": ""
      }
    ],
    "name": "CYCLE_DURATION_BLOCKS",
    "inputs": [
      
    ],
    "constant": True
  },
  {
    "type": "function",
    "stateMutability": "pure",
    "payable": False,
    "outputs": [
      {
        "type": "uint256",
        "name": ""
      }
    ],
    "name": "getSnapshotsPerCycle",
    "inputs": [
      
    ],
    "constant": True
  },
  {
    "type": "function",
    "stateMutability": "view",
    "payable": False,
    "outputs": [
      {
        "type": "uint256",
        "name": ""
      }
    ],
    "name": "requiredSignatures",
    "inputs": [
      
    ],
    "constant": True
  },
  {
    "type": "function",
    "stateMutability": "view",
    "payable": False,
    "outputs": [
      {
        "type": "address[]",
        "name": ""
      }
    ],
    "name": "delegators",
    "inputs": [
      {
        "type": "address",
        "name": "_validator"
      }
    ],
    "constant": True
  },
  {
    "type": "function",
    "stateMutability": "view",
    "payable": False,
    "outputs": [
      {
        "type": "bool",
        "name": ""
      }
    ],
    "name": "isFinalized",
    "inputs": [
      
    ],
    "constant": True
  },
  {
    "type": "function",
    "stateMutability": "view",
    "payable": False,
    "outputs": [
      {
        "type": "uint256",
        "name": ""
      }
    ],
    "name": "DEFAULT_VALIDATOR_FEE",
    "inputs": [
      
    ],
    "constant": True
  },
  {
    "type": "function",
    "stateMutability": "view",
    "payable": False,
    "outputs": [
      {
        "type": "uint256",
        "name": ""
      }
    ],
    "name": "getCurrentCycleStartBlock",
    "inputs": [
      
    ],
    "constant": True
  },
  {
    "type": "function",
    "stateMutability": "nonpayable",
    "payable": False,
    "outputs": [
      
    ],
    "name": "emitInitiateChange",
    "inputs": [
      
    ],
    "constant": False
  },
  {
    "type": "function",
    "stateMutability": "view",
    "payable": False,
    "outputs": [
      {
        "type": "uint256",
        "name": ""
      }
    ],
    "name": "totalStakeAmount",
    "inputs": [
      
    ],
    "constant": True
  },
  {
    "type": "function",
    "stateMutability": "view",
    "payable": False,
    "outputs": [
      {
        "type": "uint256",
        "name": ""
      }
    ],
    "name": "validatorFee",
    "inputs": [
      {
        "type": "address",
        "name": "_validator"
      }
    ],
    "constant": True
  },
  {
    "type": "function",
    "stateMutability": "view",
    "payable": False,
    "outputs": [
      {
        "type": "bool",
        "name": ""
      }
    ],
    "name": "isDelegator",
    "inputs": [
      {
        "type": "address",
        "name": "_validator"
      },
      {
        "type": "address",
        "name": "_address"
      }
    ],
    "constant": True
  },
  {
    "type": "function",
    "stateMutability": "view",
    "payable": False,
    "outputs": [
      {
        "type": "address[]",
        "name": ""
      }
    ],
    "name": "currentValidators",
    "inputs": [
      
    ],
    "constant": True
  },
  {
    "type": "function",
    "stateMutability": "pure",
    "payable": False,
    "outputs": [
      {
        "type": "uint256",
        "name": ""
      }
    ],
    "name": "getCycleDurationBlocks",
    "inputs": [
      
    ],
    "constant": True
  },
  {
    "type": "function",
    "stateMutability": "view",
    "payable": False,
    "outputs": [
      {
        "type": "address[]",
        "name": ""
      }
    ],
    "name": "pendingValidators",
    "inputs": [
      
    ],
    "constant": True
  },
  {
    "type": "function",
    "stateMutability": "view",
    "payable": False,
    "outputs": [
      {
        "type": "uint256",
        "name": ""
      }
    ],
    "name": "getCurrentCycleEndBlock",
    "inputs": [
      
    ],
    "constant": True
  },
  {
    "type": "function",
    "stateMutability": "view",
    "payable": False,
    "outputs": [
      {
        "type": "address[]",
        "name": ""
      }
    ],
    "name": "getValidators",
    "inputs": [
      
    ],
    "constant": True
  },
  {
    "type": "function",
    "stateMutability": "view",
    "payable": False,
    "outputs": [
      {
        "type": "uint256",
        "name": ""
      }
    ],
    "name": "stakeAmount",
    "inputs": [
      {
        "type": "address",
        "name": "_address"
      }
    ],
    "constant": True
  },
  {
    "type": "function",
    "stateMutability": "nonpayable",
    "payable": False,
    "outputs": [
      
    ],
    "name": "initialize",
    "inputs": [
      {
        "type": "address",
        "name": "_initialValidator"
      }
    ],
    "constant": False
  },
  {
    "type": "function",
    "stateMutability": "view",
    "payable": False,
    "outputs": [
      {
        "type": "uint256",
        "name": ""
      }
    ],
    "name": "MAX_STAKE",
    "inputs": [
      
    ],
    "constant": True
  },
  {
    "type": "function",
    "stateMutability": "view",
    "payable": False,
    "outputs": [
      {
        "type": "uint256",
        "name": ""
      }
    ],
    "name": "MIN_STAKE",
    "inputs": [
      
    ],
    "constant": True
  },
  {
    "type": "function",
    "stateMutability": "view",
    "payable": False,
    "outputs": [
      {
        "type": "uint256",
        "name": ""
      }
    ],
    "name": "delegatorsLength",
    "inputs": [
      {
        "type": "address",
        "name": "_validator"
      }
    ],
    "constant": True
  },
  {
    "type": "function",
    "stateMutability": "view",
    "payable": False,
    "outputs": [
      {
        "type": "uint256",
        "name": ""
      }
    ],
    "name": "getNextSnapshotId",
    "inputs": [
      
    ],
    "constant": True
  },
  {
    "type": "function",
    "stateMutability": "view",
    "payable": False,
    "outputs": [
      {
        "type": "address",
        "name": ""
      }
    ],
    "name": "delegatorsAtPosition",
    "inputs": [
      {
        "type": "address",
        "name": "_validator"
      },
      {
        "type": "uint256",
        "name": "_p"
      }
    ],
    "constant": True
  },
  {
    "type": "function",
    "stateMutability": "view",
    "payable": False,
    "outputs": [
      {
        "type": "address",
        "name": ""
      }
    ],
    "name": "getProxyStorage",
    "inputs": [
      
    ],
    "constant": True
  },
  {
    "type": "function",
    "stateMutability": "view",
    "payable": False,
    "outputs": [
      {
        "type": "bool",
        "name": ""
      }
    ],
    "name": "shouldEmitInitiateChange",
    "inputs": [
      
    ],
    "constant": True
  },
  {
    "type": "function",
    "stateMutability": "nonpayable",
    "payable": False,
    "outputs": [
      
    ],
    "name": "withdraw",
    "inputs": [
      {
        "type": "address",
        "name": "_validator"
      },
      {
        "type": "uint256",
        "name": "_amount"
      }
    ],
    "constant": False
  },
  {
    "type": "function",
    "stateMutability": "view",
    "payable": False,
    "outputs": [
      {
        "type": "bool",
        "name": ""
      }
    ],
    "name": "isValidator",
    "inputs": [
      {
        "type": "address",
        "name": "_address"
      }
    ],
    "constant": True
  },
  {
    "type": "function",
    "stateMutability": "view",
    "payable": False,
    "outputs": [
      {
        "type": "bool",
        "name": ""
      }
    ],
    "name": "isPendingValidator",
    "inputs": [
      {
        "type": "address",
        "name": "_address"
      }
    ],
    "constant": True
  },
  {
    "type": "function",
    "stateMutability": "pure",
    "payable": False,
    "outputs": [
      {
        "type": "uint256",
        "name": ""
      }
    ],
    "name": "getMaxStake",
    "inputs": [
      
    ],
    "constant": True
  },
  {
    "type": "fallback",
    "stateMutability": "payable",
    "payable": True
  },
  {
    "type": "event",
    "name": "ChangeFinalized",
    "inputs": [
      {
        "type": "address[]",
        "name": "newSet",
        "indexed": False
      }
    ],
    "anonymous": False
  },
  {
    "type": "event",
    "name": "ShouldEmitInitiateChange",
    "inputs": [
      
    ],
    "anonymous": False
  },
  {
    "type": "event",
    "name": "InitiateChange",
    "inputs": [
      {
        "type": "bytes32",
        "name": "parentHash",
        "indexed": True
      },
      {
        "type": "address[]",
        "name": "newSet",
        "indexed": False
      }
    ],
    "anonymous": False
  }
]

VOLT_CONTRACT = [{"type":"event","name":"Approval","inputs":[{"type":"address","name":"owner","internalType":"address","indexed":True},{"type":"address","name":"spender","internalType":"address","indexed":True},{"type":"uint256","name":"value","internalType":"uint256","indexed":False}],"anonymous":False},{"type":"event","name":"DelegateChanged","inputs":[{"type":"address","name":"delegator","internalType":"address","indexed":True},{"type":"address","name":"fromDelegate","internalType":"address","indexed":True},{"type":"address","name":"toDelegate","internalType":"address","indexed":True}],"anonymous":False},{"type":"event","name":"DelegateVotesChanged","inputs":[{"type":"address","name":"delegate","internalType":"address","indexed":True},{"type":"uint256","name":"previousBalance","internalType":"uint256","indexed":False},{"type":"uint256","name":"newBalance","internalType":"uint256","indexed":False}],"anonymous":False},{"type":"event","name":"OwnershipTransferred","inputs":[{"type":"address","name":"previousOwner","internalType":"address","indexed":True},{"type":"address","name":"newOwner","internalType":"address","indexed":True}],"anonymous":False},{"type":"event","name":"Transfer","inputs":[{"type":"address","name":"from","internalType":"address","indexed":True},{"type":"address","name":"to","internalType":"address","indexed":True},{"type":"uint256","name":"value","internalType":"uint256","indexed":False}],"anonymous":False},{"type":"function","stateMutability":"view","outputs":[{"type":"bytes32","name":"","internalType":"bytes32"}],"name":"DELEGATION_TYPEHASH","inputs":[]},{"type":"function","stateMutability":"view","outputs":[{"type":"bytes32","name":"","internalType":"bytes32"}],"name":"DOMAIN_TYPEHASH","inputs":[]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"allowance","inputs":[{"type":"address","name":"owner","internalType":"address"},{"type":"address","name":"spender","internalType":"address"}]},{"type":"function","stateMutability":"nonpayable","outputs":[{"type":"bool","name":"","internalType":"bool"}],"name":"approve","inputs":[{"type":"address","name":"spender","internalType":"address"},{"type":"uint256","name":"amount","internalType":"uint256"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"balanceOf","inputs":[{"type":"address","name":"account","internalType":"address"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint32","name":"fromBlock","internalType":"uint32"},{"type":"uint256","name":"votes","internalType":"uint256"}],"name":"checkpoints","inputs":[{"type":"address","name":"","internalType":"address"},{"type":"uint32","name":"","internalType":"uint32"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint8","name":"","internalType":"uint8"}],"name":"decimals","inputs":[]},{"type":"function","stateMutability":"nonpayable","outputs":[{"type":"bool","name":"","internalType":"bool"}],"name":"decreaseAllowance","inputs":[{"type":"address","name":"spender","internalType":"address"},{"type":"uint256","name":"subtractedValue","internalType":"uint256"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"delegate","inputs":[{"type":"address","name":"delegatee","internalType":"address"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"delegateBySig","inputs":[{"type":"address","name":"delegatee","internalType":"address"},{"type":"uint256","name":"nonce","internalType":"uint256"},{"type":"uint256","name":"expiry","internalType":"uint256"},{"type":"uint8","name":"v","internalType":"uint8"},{"type":"bytes32","name":"r","internalType":"bytes32"},{"type":"bytes32","name":"s","internalType":"bytes32"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"address","name":"","internalType":"address"}],"name":"delegates","inputs":[{"type":"address","name":"delegator","internalType":"address"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"getCurrentVotes","inputs":[{"type":"address","name":"account","internalType":"address"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"getPriorVotes","inputs":[{"type":"address","name":"account","internalType":"address"},{"type":"uint256","name":"blockNumber","internalType":"uint256"}]},{"type":"function","stateMutability":"nonpayable","outputs":[{"type":"bool","name":"","internalType":"bool"}],"name":"increaseAllowance","inputs":[{"type":"address","name":"spender","internalType":"address"},{"type":"uint256","name":"addedValue","internalType":"uint256"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"maxSupply","inputs":[]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"mint","inputs":[{"type":"address","name":"_to","internalType":"address"},{"type":"uint256","name":"_amount","internalType":"uint256"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"string","name":"","internalType":"string"}],"name":"name","inputs":[]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"nonces","inputs":[{"type":"address","name":"","internalType":"address"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint32","name":"","internalType":"uint32"}],"name":"numCheckpoints","inputs":[{"type":"address","name":"","internalType":"address"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"address","name":"","internalType":"address"}],"name":"owner","inputs":[]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"renounceOwnership","inputs":[]},{"type":"function","stateMutability":"view","outputs":[{"type":"string","name":"","internalType":"string"}],"name":"symbol","inputs":[]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"totalSupply","inputs":[]},{"type":"function","stateMutability":"nonpayable","outputs":[{"type":"bool","name":"","internalType":"bool"}],"name":"transfer","inputs":[{"type":"address","name":"dst","internalType":"address"},{"type":"uint256","name":"rawAmount","internalType":"uint256"}]},{"type":"function","stateMutability":"nonpayable","outputs":[{"type":"bool","name":"","internalType":"bool"}],"name":"transferFrom","inputs":[{"type":"address","name":"src","internalType":"address"},{"type":"address","name":"dst","internalType":"address"},{"type":"uint256","name":"rawAmount","internalType":"uint256"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"transferOwnership","inputs":[{"type":"address","name":"newOwner","internalType":"address"}]}]

REWARDS_CONTRACT = [{"type":"function","stateMutability":"view","payable":False,"outputs":[{"type":"uint256","name":""}],"name":"DECIMALS","inputs":[],"constant":True},{"type":"function","stateMutability":"view","payable":False,"outputs":[{"type":"bool","name":""}],"name":"isInitialized","inputs":[],"constant":True},{"type":"function","stateMutability":"view","payable":False,"outputs":[{"type":"uint256","name":""}],"name":"getRewardedOnCycle","inputs":[],"constant":True},{"type":"function","stateMutability":"view","payable":False,"outputs":[{"type":"bool","name":""}],"name":"shouldEmitRewardedOnCycle","inputs":[],"constant":True},{"type":"function","stateMutability":"view","payable":False,"outputs":[{"type":"uint256","name":""}],"name":"getBlockRewardAmount","inputs":[],"constant":True},{"type":"function","stateMutability":"view","payable":False,"outputs":[{"type":"uint256","name":""}],"name":"getBlockRewardAmountPerValidator","inputs":[{"type":"address","name":"_validator"}],"constant":True},{"type":"function","stateMutability":"view","payable":False,"outputs":[{"type":"uint256","name":""}],"name":"INFLATION","inputs":[],"constant":True},{"type":"function","stateMutability":"pure","payable":False,"outputs":[{"type":"uint256","name":""}],"name":"getBlocksPerYear","inputs":[],"constant":True},{"type":"function","stateMutability":"nonpayable","payable":False,"outputs":[],"name":"onCycleEnd","inputs":[],"constant":False},{"type":"function","stateMutability":"view","payable":False,"outputs":[{"type":"uint256","name":""}],"name":"getTotalSupply","inputs":[],"constant":True},{"type":"function","stateMutability":"view","payable":False,"outputs":[{"type":"uint256","name":""}],"name":"BLOCKS_PER_YEAR","inputs":[],"constant":True},{"type":"function","stateMutability":"nonpayable","payable":False,"outputs":[],"name":"emitRewardedOnCycle","inputs":[],"constant":False},{"type":"function","stateMutability":"pure","payable":False,"outputs":[{"type":"uint256","name":""}],"name":"getInflation","inputs":[],"constant":True},{"type":"function","stateMutability":"view","payable":False,"outputs":[{"type":"address","name":""}],"name":"getProxyStorage","inputs":[],"constant":True},{"type":"function","stateMutability":"nonpayable","payable":False,"outputs":[{"type":"address[]","name":""},{"type":"uint256[]","name":""}],"name":"reward","inputs":[{"type":"address[]","name":"benefactors"},{"type":"uint16[]","name":"kind"}],"constant":False},{"type":"function","stateMutability":"nonpayable","payable":False,"outputs":[],"name":"initialize","inputs":[{"type":"uint256","name":"_supply"}],"constant":False},{"type":"event","name":"Rewarded","inputs":[{"type":"address[]","name":"receivers","indexed":False},{"type":"uint256[]","name":"rewards","indexed":False}],"anonymous":False},{"type":"event","name":"RewardedOnCycle","inputs":[{"type":"uint256","name":"amount","indexed":False}],"anonymous":False}]