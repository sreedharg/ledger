import os, csv, json
from AccountCSVLoader import AccountCSVLoader

debug = True

class DiscoveryLoader(AccountCSVLoader):
    """Loads Discovery data from a csv file"""

    def __init__(self, dirname, filename, accts_dictionary, data):
        """Create new instance of Discovery Loader"""
        super(DiscoveryLoader, self).__init__(dirname, filename, accts_dictionary, data)
        self._al_accts = ['Liabilities', 'Discovery Credit card']

    def _determine_discovery_pl_acct(self, row):
        txn_data = str.lower(row[3])

        for txn_tag in self._txn_tags:
            if txn_tag['name'] in txn_data:
               return str.split(str(txn_tag['category']), ':')

        self._print_exception(txn_data, row)

        if float(row[1]) > 0:
            return ['Income', 'Unknown']
        else:
            return ['Expense','Unknown']

    def load(self):
        """Loads data into a data structure and returns the same"""
        first_discovery_entry = 0
        opening_bal = 0

        with open(os.path.join(self._dirname, self._filename), 'rt') as f:
            reader = csv.reader(f)
            for row in reader:
                if row[0] in ['', 'ACCOUNT TRANSACTION HISTORY', 'Name:', 'Account:', 'Date']:
                    continue

                if row[0] == 'Balance:':
                    opening_bal = float(row[1])
                    continue

                yyyymm = row[0][6:10] + row[0][3:5]

                if first_discovery_entry == 0:
                    first_discovery_entry = 1
                    self._add_acct(self._al_accts, opening_bal, yyyymm)
                    self._add_acct(['Equity', 'Opening Balances'], opening_bal * -1, yyyymm)

                txn_amt = float(row[1])

                pl_accts = self._determine_discovery_pl_acct(row)
                if 'Assets' in pl_accts:
                    continue

                self._add_acct(pl_accts, txn_amt * -1, yyyymm)
                self._add_acct(self._al_accts, txn_amt, yyyymm)

        return self._data, self._accts_dictionary
