# ledger
Mini ledger app / command line based with .csv input

The app currently handles csv files from the following banks:
1. Capitec bank
   - file contains 'extr' in its name
   - sample format: 1999999999,05/01/2017,0412047,FINANCIAL,"","*SMS FEE",0.40,,"",100.00

2. Standard bank
  - file contains 'statement' in its name
  - sample format: HIST,20170331,##,-100,SERVICE FEE,FIXED MONTHLY FEE 099999999,1112,0

3. Discovery credit card
  - file contains '490137' in its name - this might be different to different accounts
  - sample format: 03/01/2017,-591.26,0, PNP CAPE TOWN       

Reports and exceptions are produced under reports.

Transaction data must be under txn-data.
