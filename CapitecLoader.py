import os, csv, json
from AccountCSVLoader import AccountCSVLoader

debug = True

class CapitecLoader(AccountCSVLoader):
    """Loads Capitec data from a csv file"""

    def __init__(self, dirname, filename, accts_dictionary, data):
        """Create new instance of Capitec Loader"""
        super(CapitecLoader, self).__init__(dirname, filename, accts_dictionary, data)
        self._al_accts = ['Assets', 'Capitec']

    def _determine_capitec_pl_acct(self, row):
        txn_data = str.lower(row[8])

        for txn_tag in self._txn_tags:
            if txn_tag['name'] in txn_data:
                print str.split(str(txn_tag['category']), ':')
                return str.split(str(txn_tag['category']), ':')

        for txn_tag in self._txn_tags2:
            if txn_tag['name'] in str.lower(row[5]):
                print str.split(str(txn_tag['category']), ':')
                return str.split(str(txn_tag['category']), ':')

        self._print_exception(txn_data, row)

        if row[7] != '':
            return ['Income', 'Unknown']
        else:
            return ['Expense','Unknown']

    def load(self):
        """Loads data into a data structure and returns the same"""
        first_capitec_entry = 0

        with open(os.path.join(self._dirname, self._filename), 'rt') as f:
            reader = csv.reader(f)
            for row in reader:
                if debug:
                    print '-' * 100
                    print row
                    print json.dumps(self._data , sort_keys=True,
                        indent=4, separators=(',', ': '))
                    print json.dumps(self._accts_dictionary, sort_keys=True,
                        indent=4, separators=(',', ': '))
                    print '-' * 100
                if row[0] == 'Account':
                    continue

                yyyymm = row[1][6:10] + row[1][3:5]

                if first_capitec_entry == 0:
                    first_capitec_entry = 1
                    if row[6] != '':
                        txn_amt = float(row[9]) + float(row[6])
                    else:
                        txn_amt = float(row[9]) - float(row[7])

                    self._add_acct(self._al_accts, txn_amt, yyyymm)
                    self._add_acct(['Equity', 'Opening Balances'], txn_amt * -1, yyyymm)
                    continue

                if row[6] != '':
                    txn_amt = float(row[6]) * -1
                else:
                    txn_amt = float(row[7])

                pl_accts = self._determine_capitec_pl_acct(row)

                if 'Assets' in pl_accts and 'Shares' not in pl_accts:
                    continue

                self._add_acct(pl_accts, txn_amt * -1, yyyymm)
                self._add_acct(self._al_accts, txn_amt, yyyymm)

        return self._data, self._accts_dictionary
