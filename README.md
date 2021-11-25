# FTX Autocompounder

If more than 95% of lendable money is lending, reset to 100%.

# How to run

1. Get a key, secret
2. Manually run `python3 lend.py` and see
3. Config crontab like this
```
3,15,30,55 * * * * cd ftx; echo "$(tail -1000 output.txt)" > output.txt; python3 lend.py | tee -a output.txt
```
