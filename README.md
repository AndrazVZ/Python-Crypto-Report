# Python-Crypto-Report

## Overview 🔎
This project is made fully with Python and is running on my Raspberry Pi 4 model b. I use crontab to run the main.py every day at 23:59, this gets the daily P/L and writes it into a .txt file. To fully automate this I also run graph.py daily at 10:00, this will create a graph from the data in the .txt file and send me an email with the graph. *More details about each file in the program overview section*


## Tech stack 💻
- Python
  - Binance library (getting crypto and wallet data)
  - Matplotlib (graphs)
  - google email library

## Program overview 👨‍💻
### main.py
In main.py I first get my Binance wallet details, then I also get the transactions I made in the last year. After that for each of the coins that I still own and have purchased in the last year I calculate the P/L based on the coin's current price (at the time of running the program) and I subtract the ammount that I have paid for this coin.. Example:

Let's say I bought 100$ worth of BTC in the past year and I have 0.0001 BTC, today my 0.0001 BTC is worth for example 110$, so my profit is 10$. This then gets written into the .txt file with today's date.

### graph.py
In graph.py I read the .txt file line by line so each line represents one day. Then I seperate the date, currency and P/L per currency and put it all in a graph.. If there are more currencies each currency's line will be a different color. After the graph is created I call a function from smtp.py.

### smtp.py
This file is a standard mailing file with some custom features such as a custom content message and a attachment which is the image of the graph. **NOTE: in order for this to work you must complete Google's verification and put your google account as a trusted tester, you will also be given a token.json file which you need to include in the project's directory! Please see : https://developers.google.com/workspace/gmail/api/quickstart/python for a more in depth guide on how to do this.**


### Known issues
- Since this program is in an unrefined state there is an issue where if I buy one currency additionally, I will have to reset my graph progress so all of my currencies will have the same ammount of entries otherwise matplotlib will throw an error.
- Also if I decide to withdraw or trade some of my tracked currency, the ammount in the program will not change as the withdrawing/trading part is not implemented.
  
