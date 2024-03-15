Skoða upplýsingar Undir Stock Plan → My Account → Benefit History í ETrade
[https://us.etrade.com/etx/sp/stockplan?accountIndex=0&traxui=tsp_portfolios/#/myAccount/benefitHistory](https://us.etrade.com/etx/sp/stockplan?accountIndex=0&traxui=tsp_portfolios/#/myAccount/benefitHistory)

Gengi: [https://www.exchangerates.org.uk/USD-ISK-spot-exchange-rates-history-2021.html](https://www.exchangerates.org.uk/USD-ISK-spot-exchange-rates-history-2021.html)


# ESPP
Ég hugsaði um þetta eins og þetta væru bara stock optionar sem við værum búin að committa á að exercisea, svo þetta er skráð mikið til eins og stock options.

```
Í 3.19, undir Erlend hlutabréf, setja inn aðra línu fyrir ESPP:
Þrep 1 - info (ath bara við fyrstu uppsetningu): 
  Land = Bandaríkin
  Kennitala eiganda = mín kt
  Nafn félags = <company> - ESPP <ár>
  haka í Fjöldi hluta
Þrep 2 - Kaup:
  Hérna þarf að nota undir Employee Stock Purchase Plan (ESPP) og undir hverju purchase, þá skoða Events.
 Þægilegast að gera View Confirmation of Purchase, og skoða það (ath bara það sem gerðist á einu ári)
 fyrir hvert Confirmation of Purchase, þá setja eina línu:
    Dagsetning = Purchase Date Í Confirmation of Purchase
    Kennitala seljanda = 9999999999
    Fjöldi hluta = Shares Issued
    Kaupverð = Total Price * gengi (USD → ISK) á Purchase Date
   Tekjuskattskvöð = Taxable Gain * gengi (USD → ISK) á Purchase Date
Þrep 3 - Sala:
  Engin sala fyrir exercise 🙂
Þrep 4 - Arður / Tekjuskattskvöð:
  Ekkert 🙂 
```
# RSU
RSU eru leiðinleg útaf skattur er due um leið af þeim, og þau valda sell eventum, sem þarf líka að skrá.
```
Í 3.19 Hlutabréfaeign, undir Erlend hlutabréf, setja inn fyrir RSU:
Þrep 1 - info (ath bara við fyrstu uppsetningu): 
  Land = Bandaríkin
  Kennitala eiganda = mín kt
  Nafn félags = <company> - RSU <ár>
  haka í Fjöldi hluta
Þrep 2 - Kaup:
  Hérna þarf að nota undir Restricted Stock (RS) og undir hverjum grant, þá skoða Events.
 Þægilegast að gera View Confirmation of Release, og skoða það (ath bara það sem gerðist á einu ári)
 Fyrir hvert Confirmation of Release, þarf að gera eina línu í framtalinu:
   Dagsetning = Release Date
   Kennitala seljanda = 9999999999
   Fjöldi hluta = Shares Released
   Kaupverð = Total Gain * gengi (USD → ISK) á Release Date
Þrep 3 - Sala:
  Ef einhver bréf voru seld til að covera skatt (sell to cover), þá þarf líka að gera grein fyrir þeim
 Fyrir hvert confirmation of release þar sem bréf voru seld:
   Dagsetning = Release Date
   Kennitala kaupanda = 9999999999
   Fjöldi hluta = Shares Sold
   Söluverð = Total Sale Price  * gengi (USD → ISK) á Release Date
Þrep 4 - Arður / Tekjuskattskvöð:
  Tómt
```

Ef það var ekki greiddur skattur af RSU bréfum af fyrirtækinu (skráð á launaseðil), þá þarf að passa að skrá það sér:
```
Í 1.01 Tekjusíða, undir 2.2 Önnur hlunnindi:
  Kennitala = mín kt
  Nafn launagreiðenda = Hlutabréfahlunnindi
  Launafjárhæð = Summa af Kaupverð í skrefunum á undan, þar sem Calculation of Taxes í Confirmation of Release er $0. (Þetta ætti að vera allt pre-Desember 2021).
```

Ef það var greiddur tekjuskattur af RSU bréfum af fyrirtækinu, þá þarf að passa að það sé allt afstemmt rétt - bera saman 1.01 Tekjusíða við launaseðla og athuga hvort að sell to cover sé listað þar!

Ef ekki, þá þarf að skrá það í sér lið í 1.01 Tekjusíða:
```
Undir 2.2 Önnur hlunnindi:
  Kennitala = <KT fyrirtækis>
  Nafn launagreiðenda = Hlutabréfahlunnindi
  Launafjárhæð = Summa af Kaupverð í skrefunum á undan, þar sem það var greiddur skattur í Confirmation of Release (post-Desember 2021)

Undir 2.10 Staðgreiðsla af tekjum (öðrum en fjármagnstekjum):
  Kennitala = <KT fyrirtækis>
  Nafn launagreiðenda = Hlutabréfahlunnindi
  Launafjárhæð = Summa af (Total Tax í Confirmation of Release * gengi (USD → ISK) á Release date) fyrir hvert RSU plan sem greiddi skatt.
```

Athuga að leiðrétta stofnverð seldra hlutabréfa fyrir RSU skatt til að passa upp á að það sé summan af `(fjöldi seldra * Market value per share * gengi USD→ISK á Release date)` fyrir hvert Release Confirmation þar sem eitthvað var selt. Semsagt, summan af keyptum bréfum ætti að stemma við hlutabréfahlunnindi á framtalinu, og summan af því sem selt var ætti að stemma við greiddan skatt.

# Stock Options
Fyrir Stock option exercised á árinu
```
Í 3.19, undir Erlend hlutabréf, setja inn aðra línu fyrir Stock Option:
Þrep 1 - info (ath bara við fyrstu uppsetningu): 
  Land = Bandaríkin
  Kennitala eiganda = mín kt
  Nafn félags = <company> - SO <date>
  haka í Fjöldi hluta
Þrep 2 - Kaup:
  Hérna þarf að nota undir Stock Options og undir hverjum grant, þá skoða Events.
 Þægilegast að gera View Confirmation of Exercise, og skoða það (ath bara það sem gerðist á einu ári)
 fyrir hvert Confirmation of Exercise, þá setja eina línu:
    Dagsetning = Exercise date Í Confirmation of Exercise
    Kennitala seljanda = 9999999999
    Fjöldi hluta = Shares Issued
    Kaupverð = Total Price * gengi (USD → ISK) á Exercise Date
   Tekjuskattskvöð = Total Gain * gengi (USD → ISK) á Exercise Date
Þrep 3 - Sala:
  Engin sala fyrir exercise 🙂
Þrep 4 - Arður / Tekjuskattskvöð:
  Ekkert 🙂 
```
Mér fannst þægilegt að brjóta upp optiona eftir exercises - þá er hægt að selja bréf sem voru keypt í einu exercise sér frá öðrum, útaf þau geta haft mismunandi tekjuskattskvaðir. Þá er bara bætt við línu og skrefin að ofan gerð bara fyrir það release, með `Nafn félags = <company - <type> <dags>`


Fyrir sölu, þá þar sem hlutabréf eru fungible, þá er hægt að velja hvar þú skráir söluna / part af sölunni. Hægt að taka út úr RSU, sem þýðir enginn tekjuskattur, bara fjármagnstekjuskattur af hagnaði, en líka hægt að taka út úr ESPP eða options, sem þýðir tekjuskattur skv tekjuskattskvöð, og svo fjármagnstekjuskattur af umfram hagnaði. 



