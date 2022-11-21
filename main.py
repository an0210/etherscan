import requests
from time import sleep
from pprint import pprint
import json
from math import fabs
import winsound

key = "XENZBWU22W1U25YM2I23CTA8SUNC1QVVQY"
wallets = []


def get_acc_balance(addr):
    req = requests.get(f"https://api.etherscan.io/api?module=account&action=balance&address={addr}&tag=latest&apikey={key}")
    return int(req.json()["result"]) / 10**18


def get_accs_balances(addrs):
    req = requests.get(f"https://api.etherscan.io/api?module=account&action=balancemulti&address={addrs}&tag=latest&apikey={key}")
    addresses = req.json()["result"]
    for x in addresses:
        x["balance"] = int(x["balance"]) / 10**18
    return addresses


def create_ftx_dict():
    balances = []
    with open("ftx_drainer.txt", 'r') as file:
        for x in file.readlines():
            balances.append({"account": x.split()[0], "balance": x.split()[1]})
    return balances


def continuos_monitoring(addrs):
    balances = get_accs_balances(addrs)
    old_balances = create_ftx_dict()
    with open("ftx_drainer.txt", "w") as f:
        for i, x in enumerate(balances):
            cur_bal = x["balance"]
            old_bal = float(old_balances[i]["balance"])
            diff = fabs(cur_bal / old_bal - 1)
            if diff > 0.05:
                print("ALERT ALERT ALERT")
                print(f"cur_bal: {cur_bal}, old_bal: {old_bal}, {diff}")
                winsound.PlaySound("openingsound.wav", winsound.SND_FILENAME)
            f.write(f"{x['account']} {x['balance']}\n")


def infinite_monitoring(addrs):
    while True:
        continuos_monitoring(addrs)
        print("No changes so far")
        sleep(5)


if __name__ == '__main__':
    wallets = ""
    with open("wallets.txt", 'r') as file:
        for x in file.readlines():
            wallets += x.strip() + ","
    wallets = wallets[:-1]

    infinite_monitoring(wallets)
    # create_ftx_dict()
    # get_accs_balances(wallets)
    # for x in wallets:
    #     print(f"{x}     {get_acc_balance(x)}")
    #     sleep(0.3)
