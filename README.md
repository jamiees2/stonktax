# Stonktax

A quick helper script to generate the info for the tax return from ETRADE trade confirmations.

## Disclaimer
If you use this tool and do your taxes wrong, that's on you. Contact a proper accountant if you want real help.

## Usage
Download all the files into one directory, then enter that directory and run the script.

```sh
cd ~/Downloads/taxes2023
python3 ~/projects/stonktax/extract.py
```

This may complain about two files not existing in your directory, exchange.txt, and rsutable.txt

`exchange.txt` contains the exchange rate USD->ISK for filing ESPP information. Running the script once should tell you which dates to fetch the exchange rate for.

An example of this is the following
```
15.03.2023 141.8054
15.09.2023 136.1201
```

`rsutable.txt` is used to calculate the exchange rate of RSUs from your payslips, since they have already been taxed as income for you. This is so that their valuation matches what the evaulation was. This is keyed by month, and is just the total sale for that month. The script assumes that you have provided as input the complete set of trades that happened during the fiscal year. Note that if you do not do this, the valuation will be way off. Use your discretion!

An example of this file is the following
```
03 123456
06 123456
09 123456
12 123456
```



## Fetching the PDFs
To download all the confirmations, you can use the following script in the console on the my account page: [Benefit History](https://us.etrade.com/etx/sp/stockplan#/myAccount/benefitHistory)

First use the following script to expand everything
```js
Array.from(document.querySelectorAll("button[aria-label='expand all rows'].et-icon-plus")).forEach(e => e.click());
```

Then use the following script to extract all the links and replace the page with just that info
```js
year = 2023;
yearStart = new Date(`${year}-01-01`);
yearEnd = new Date(`${year}-12-31`);

links = []
for (const [name, selector] of [["espp", "#ESPPTable"], ["rsu", "#rsBhTable"], ["stockoptions", "#SOTable"]]) {
    links.push([name, Array.from(document.querySelectorAll(`${selector} table.eventsTable tbody tr`)).map(e => [new Date(e.querySelector("td[tableheaddata=Date]").innerText), e.querySelector("td[tableheaddata='Event Type']").innerText, e.querySelector("td[tableheaddata=Action] a")?.href]).filter(e => e[0] >= yearStart && e[0] <= yearEnd).filter(e => e[2] && !e[1].includes("granted"))])
}

document.write(links.map(e => e[1].map(f => `<a href=${f[2]}>${e[0]} ${f[1]}</a>`)).flat()).join("\n")
```

Now you can use some downloader such as DownThemAll to download all the files.
