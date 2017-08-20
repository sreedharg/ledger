# ledger
Mini ledger app / command line based with .csv input

##Input
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

Transaction data must be under txn-data.

##How to run?

Run <code>python LedgerApp.py</code> 

##Output
Reports and exceptions are produced under reports.

Sample:

--------------------------------------------------------------------------------------------------------------------
                                                                                        2017/01          Total
--------------------------------------------------------------------------------------------------------------------

Expense                                                                                 4672.45  |     4672.45
                                                                                ---------------     ---------------     
          Banking-fees                                                                   249.65              249.65 
          Comms                                                                        2,078.87             2078.87 
          Cosmetics                                                                        0.00                0.00 
          Eating-out                                                                   2,218.95             2218.95 
          Electronics                                                                    124.98              124.98 

