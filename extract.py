import PyPDF2
import glob
import re
from datetime import datetime
from decimal import Decimal
from collections import namedtuple
import os.path

ESPPData = namedtuple('ESPPData', ['issued', 'total', 'taxablegain'])
RSUData= namedtuple('RSUData', ['issued', 'totalgain', 'sold', 'totalsale'])



dateRe = re.compile("\d{2}-\d{2}-\d{4}")
numRe = re.compile("[\d\.]+")
priceRe = re.compile("\$[\d\.,]+")


esppList = glob.glob("getEsppConfirmation*.pdf")
esppdata = {}
for x in esppList:
    date = ""
    issued = -1
    total = -1
    taxablegain = -1
    with open(x, "rb") as f:
        pdf = PyPDF2.PdfReader(f)
        t = pdf.pages[0].extract_text()
        for line in t.splitlines():
            if line.startswith("Purchase Date"):
                m = dateRe.search(line)
                if m is not None:
                    date = datetime.strptime(m.group(0), '%m-%d-%Y').isoformat()
            elif line.startswith("Shares Purchased"):
                m = numRe.search(line)
                if m is not None:
                    issued = int(float(m.group(0)))
            elif line.startswith("Total Price") and total == -1:
                m = priceRe.search(line)
                if m is not None:
                    total = Decimal(m.group(0)[1:].replace(",", ""))
            elif line.startswith("Taxable Gain"):
                m = priceRe.search(line)
                if m is not None:
                    taxablegain = Decimal(m.group(0)[1:].replace(",", ""))
    assert(date != "" and issued != -1 and total != -1 and taxablegain != -1)
    esppdata[date] = ESPPData(issued, total, taxablegain)

esppdata = sorted(list(esppdata.items()), key=lambda k: k[0])

rates = {}
if os.path.exists("exchange.txt"):
    with open("exchange.txt") as f:
        for line in f:
            a,b = line.strip().split()
            rates[a]=Decimal(b)

print("==================ESPP KAUP=================")
for k, v in esppdata:
    date = datetime.fromisoformat(k)
    d = date.strftime("%d.%m.%Y")
    y = date.strftime("%Y")
    
    if d not in rates:
        print(f"Please fill in {d} in exchange.txt! You can get this info from https://www.exchangerates.org.uk/USD-ISK-spot-exchange-rates-history-{y}.html")
        total = "UNKNOWN"
        taxablegain = "UNKNOWN"
    else:
        rate = rates[d]
        total = str(round(v.total * rate))
        taxablegain = str(round(v.taxablegain * rate))

    print("Dagsetning", d)
    print("Kennitala seljanda", "9999999999")
    print("Fjöldi hluta", str(v.issued))
    print("Kaupverð", total)
    print("Tekjuskattskvöð", taxablegain)
    print("")
    print("- Kaupverð (USD)", v.total)
    print("- Tekjuskattskvöð (USD)", v.taxablegain)
    print("")
    print("")




rsuList = glob.glob("getReleaseConfirmation*.pdf")
rsudata = {}
for x in rsuList:
    date = ""
    issued = -1
    totalgain = -1
    sold = -1
    totalsale = -1
    with open(x, "rb") as f:
        pdf = PyPDF2.PdfReader(f)
        t = pdf.pages[0].extract_text()
        for line in t.splitlines():
            if "Release Date" in line:
                idx = line.index("Release Date")
                line = line[idx:]
                m = dateRe.search(line)
                if m is not None:
                    date = datetime.strptime(m.group(0), '%m-%d-%Y').isoformat()
            elif line.startswith("Shares Released"):
                m = numRe.search(line)
                if m is not None:
                    issued = int(float(m.group(0)))
            elif line.startswith("Total Gain") and totalgain == -1:
                m = priceRe.search(line)
                if m is not None:
                    totalgain = Decimal(m.group(0)[1:].replace(",", ""))
            elif line.startswith("Shares Sold"):
                m = numRe.search(line)
                if m is not None:
                    sold = int(float(m.group(0)))
            elif line.startswith("Total Sale Price") and totalsale == -1:
                m = priceRe.search(line)
                if m is not None:
                    totalsale = Decimal(m.group(0)[1:].replace(",", ""))
    assert(date != "" and issued != -1 and totalgain != -1 and sold != -1 and totalsale != -1)
    if date not in rsudata:
        rsudata[date] = RSUData(0, 0, 0, 0)
    cur = rsudata[date]
    rsudata[date] = RSUData(cur.issued + issued, cur.totalgain + totalgain, cur.sold + sold, cur.totalsale + totalsale)

rsudata = sorted(list(rsudata.items()), key=lambda k: k[0])

rsutable = {}
if os.path.exists("rsutable.txt"):
    with open("rsutable.txt") as f:
        for line in f:
            a,b = line.strip().split()
            rsutable[a]=Decimal(b)

print("==================RSU KAUP==================")
for k, v in rsudata:
    date = datetime.fromisoformat(k)
    mo = date.strftime("%m")
    if mo not in rsutable:
        print(f"Please fill in {mo} in rsutable.txt! You can get this info from your payslip for that month or the month after")
        iskgain = "UNKNOWN"
    else:
        iskgain = str(rsutable[mo])
    print("Dagsetning", date.strftime("%d.%m.%Y"))
    print("Kennitala seljanda", "9999999999")
    print("Fjöldi hluta", str(v.issued))
    print("Kaupverð", iskgain)
    print("")
    print("- Kaupverð (USD)", str(v.totalgain))
    print("")
    print("")

print("==================RSU SALA==================")
for k, v in rsudata:
    date = datetime.fromisoformat(k)
    mo = date.strftime("%m")
    if mo not in rsutable:
        print(f"Please fill in {mo} in rsutable.txt! You can get this info from your payslip for that month or the month after")
        sale = "UNKNOWN"
        rate = "UNKNOWN"
    else:
        iskgain = rsutable[mo]
        rate = iskgain / v.totalgain
        sale = str(round(v.totalsale * rate))
    print("Dagsetning", date.strftime("%d.%m.%Y"))
    print("Kennitala kaupanda", "9999999999")
    print("Fjöldi hluta", str(v.sold))
    print("Söluverð", sale)
    print("")
    print("- Gengi (USD -> ISK)", str(round(rate, 2)))
    print("- Söluverð (USD)", str(v.totalsale))
    print("")
    print("")



print("================HLUNNINDI===================")
print("Launafjárhæð", sum(rsutable.values()))
