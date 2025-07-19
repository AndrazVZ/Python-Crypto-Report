from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
import smtp
from datetime import datetime
FULL_PATH_TO_PROJECT = "your_path"
colors = [
    "blue", "green", "red", "orange", "purple", "cyan", "magenta", "brown", "olive", "teal",
    "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"
]
dates = []
profit_by_currency = defaultdict(list)
try:
    with open(FULL_PATH_TO_PROJECT+"/crypto-report.txt", "r") as f:
        lines = f.read().splitlines()

    for line in lines:
        if line.strip() == "":
            continue

        parts = line.split(";")
        
        #skip line if it's not in the correct format
        if len(parts) < 3 or len(parts) % 2 == 0:
            continue

        date = parts[0]
        dates.append(date)

        # Parse each currency and its P/L
        for i in range(1, len(parts), 2):
            currency = parts[i]
            profit = float(parts[i + 1])
            profit_by_currency[currency].append(profit)

    for idx,(currency,profits) in enumerate(profit_by_currency.items()):
        plt.plot(dates,profits,label=currency,color=colors[idx])

    plt.title("Daily P/L")
    plt.xlabel("Dates")
    plt.ylabel("P/L (€)")

    # plt.show()
    #instead of displaying it, save it
    full_path = FULL_PATH_TO_PROJECT+"/weekly_graph.jpg"
    plt.savefig(full_path)
    smtp.send_email(full_path)
except Exception as e:
    date_time = datetime.now()
    with open(FULL_PATH_TO_PROJECT+"/errors.log","a") as f:
        f.write(f"[{date_time.strftime('%d.%m.%Y %H:%M:%S')}] graph.py error: {e}")
