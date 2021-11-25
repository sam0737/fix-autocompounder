from ftx import *
from datetime import datetime

offers = call_ftx('GET', 'spot_margin/offers')['result']
lending_info = call_ftx('GET', 'spot_margin/lending_info')['result']

"""
b'{"result":[{"coin":"BNB","rate":5.65e-06,"size":210.416505},{"coin":"USD","rate":5.71e-06,"size":64761.763794}],"success":true}\n'
b'{"result":[{"coin":"USD","lendable":64761.76379470817,"locked":64761.763794,"minRate":5.71e-06,"offered":64761.763794},{"coin":"BNB","lendable":210.41650546,"locked":210.416505,"minRate":5.65e-06,"offered":210.416505},{"coin":"USDT","lendable":0.0,"locked":0.0,"minRate":null,"offered":0.0}],"success":true}\n'
"""

lending_info_dicts = dict((v["coin"], v) for v in lending_info)

print(f'Now: {datetime.now().isoformat()}')
for offer in offers:
    coin = offer["coin"]
    if coin not in lending_info_dicts: break
    info = lending_info_dicts[coin]
    if offer["size"]/info["lendable"] > 0.95 and \
       info["lendable"] - offer["size"] > 1e-7:
        print(f'Refreshing {coin} to {info["lendable"]}')
        call_ftx('POST', 'spot_margin/offers', {
            "coin": coin, "size": info["lendable"]-1e-4, "rate": offer["rate"]
            })
    else:
        print(f'{coin} offer not updated. Current size {offer["size"]}, lendable {info["lendable"]}')
    # print('    ', info["lendable"], offer["size"], offer["size"]/info["lendable"] > 0.95, info["lendable"] - offer["size"] > 1e-5)
