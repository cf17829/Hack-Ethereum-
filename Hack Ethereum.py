import requests
import time
from eth_account import Account
from mnemonic import Mnemonic

# Enable the Mnemonic features
Account.enable_unaudited_hdwallet_features()

def generate_mnemonic():
    mnemo = Mnemonic("english")
    return mnemo.generate()

def generate_eth_address(mnemonic):
    account = Account.from_mnemonic(mnemonic)
    address = account.address
    private_key = account.key.hex()
    return address, private_key

def check_balance(address, api_key):
    try:
        url = f"https://api.etherscan.io/api?module=account&action=balance&address={address}&tag=latest&apikey={api_key}"
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad response status
        balance = int(response.json()["result"]) / 10**18  # Convert from Wei to Ether
        return balance
    except requests.exceptions.RequestException as e:
        print("Error occurred during balance check:", e)
        return None
    except KeyError:
        print("Error: Could not retrieve balance from API response")
        return None

def write_to_file(address, mnemonic, balance):
    with open("addresses_with_balance.txt", "a") as file:
        file.write(f"Address: {address}\nMnemonic: {mnemonic}\nBalance: {balance} ETH\n\n")

api_key = "YOUR_ETHERSCAN.IO_API_KEY"
num_addresses = 10  # Number of addresses to generate

try:
    for i in range(num_addresses):
        start_time = time.time()
        mnemonic = generate_mnemonic()
        address, _ = generate_eth_address(mnemonic)
        balance = check_balance(address, api_key)

        print(f"Generated Ethereum Address {i+1}:")
        print("Address:", address)
        print("Mnemonic:", mnemonic)

        if balance is not None:
            print("Balance:", balance, "ETH")
            if balance > 0:
                write_to_file(address, mnemonic, balance)
        else:
            print("Failed to check balance for the address")

        print("-" * 50)

        # Introduce a delay of 0.33 seconds between each mnemonic generation (3 mnemonics per second)
        time.sleep(max(0, 0.33 - (time.time() - start_time)))
except Exception as e:
    print("An error occurred:", e)
    print("Saving discovered addresses with non-zero balances to the file before exiting...")
    # Add code here to save discovered addresses with non-zero balances to the file
    print("Exiting...")
