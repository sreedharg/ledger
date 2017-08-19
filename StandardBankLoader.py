import os, csv, json
from AccountCSVLoader import AccountCSVLoader

debug = False

class StandardBankLoader(AccountCSVLoader):
    """Loads StandardBank data from a csv file"""

    def __init__(self, dirname, filename, accts_dictionary, data):
        """Create new instance of StandardBank Loader"""
        super(StandardBankLoader, self).__init__(dirname, filename, accts_dictionary, data)
        self._al_accts = ['Assets', 'SB Cheque Account']

    def _determine_sb_pl_acct(self, row):
        txn_data = str.lower(row[5])

        for txn_tag in self._txn_tags:
            if txn_tag['name'] in txn_data:
               return str.split(str(txn_tag['category']), ':')

        txn_data = str.lower(row[4])
        for txn_tag in self._txn_tags2:
            if txn_tag['name'] in txn_data:
               return str.split(str(txn_tag['category']), ':')

        self._print_exception(txn_data, row)
        if float(row[3]) > 0:
            return ['Income', 'Unknown']
        else:
            return ['Expense','Unknown']

    def load(self):
        """Loads data into a data structure and returns the same"""
        first_sb_entry = 0
        opening_bal = 0

        with open(os.path.join(self._dirname, self._filename), 'rt') as f:
            reader = csv.reader(f)
            for row in reader:
                if row[0] in ['0']:
                    continue

                if row[2] == 'OPEN':
                    opening_bal = float(row[3])
                    continue

                if row[0] in ['']:
                    continue

                yyyymm = row[1][0:6]

                if first_sb_entry == 0:
                    first_sb_entry = 1
                    self._add_acct(self._al_accts, opening_bal, yyyymm)
                    self._add_acct(['Equity', 'Opening Balances'], opening_bal * -1, yyyymm)

                txn_amt = float(row[3])

                pl_accts = self._determine_sb_pl_acct(row)

                self._add_acct(pl_accts, txn_amt * -1, yyyymm)
                self._add_acct(self._al_accts, txn_amt, yyyymm)

        return self._data, self._accts_dictionary
