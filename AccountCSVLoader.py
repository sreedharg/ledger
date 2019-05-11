import os, csv, json

class AccountCSVLoader(object):
    """Loads data from a csv file"""

    def __init__(self, dirname, filename, accts_dictionary, data):
        """Create new instance of Capitec Loader"""
        self._dirname = dirname
        self._filename = filename
        self._data = data
        self._accts_dictionary = accts_dictionary
        self._exception_file = open('./reports/exceptions_' + filename + '.txt', 'w')

        with open('config.json') as json_data_file:
            config_data = json.load(json_data_file)
        self._txn_tags = config_data["txn_tags"]
        self._txn_tags2 = config_data["txn_tags2"]

    def _print_exception(self, txn_data, row):
        self._exception_file.write(', '.join(row) + '\n')


    def _update_dict(self, acct, accts_dictionary):
        if acct in accts_dictionary:
            return
        else:
            accts_dictionary[acct] = {}

    def _add_acct_cat(self, al_accts, data, amount, yyyymm, accts_dictionary):
        yyyy = yyyymm[0:4]
        mm = yyyymm[4:]

        if al_accts[0] in data:
            data[al_accts[0]]['bal'] = data[al_accts[0]]['bal'] + amount
        else:
            data[al_accts[0]] = {'bal': amount, 'monthly': False, 'yearly': False}
            self._update_dict(al_accts[0], accts_dictionary)

        if len(al_accts) > 1:
            self._add_acct_cat(al_accts[1:], data[al_accts[0]], amount, yyyymm, accts_dictionary[al_accts[0]])

    def _add_acct(self, al_accts, amount, yyyymm):
        yyyy = yyyymm[0:4]
        mm = yyyymm[4:]

        if yyyy in self._data:
            if mm in self._data[yyyy]:
                self._data[yyyy]['bal'] = self._data[yyyy]['bal'] + amount
                self._data[yyyy][mm]['bal'] = self._data[yyyy][mm]['bal'] + amount

                if al_accts[0] in self._data[yyyy][mm]:
                    self._data[yyyy][mm][al_accts[0]]['bal'] = self._data[yyyy][mm][al_accts[0]]['bal'] + amount
                else:
                    self._data[yyyy][mm][al_accts[0]] = {'bal': amount, 'monthly': False, 'yearly': False}
                    self._update_dict(al_accts[0], self._accts_dictionary)

            else:
                self._data[yyyy]['bal'] = self._data[yyyy]['bal'] + amount
                self._data[yyyy][mm] = {al_accts[0]: {'bal': amount, 'monthly': False, 'yearly': False}, 'bal': amount, 'monthly': True, 'yearly': False}
                self._data[yyyy][mm][al_accts[0]] = {'bal': amount, 'monthly': False, 'yearly': False}
                self._update_dict(al_accts[0], self._accts_dictionary)

        else:
            self._data[yyyy] = {mm: {al_accts[0]: {'bal': amount, 'monthly': False, 'yearly': False}, 'bal': amount, 'monthly': True, 'yearly': False}, 'bal': amount, 'yearly': True , 'monthly': False}
            self._update_dict(al_accts[0], self._accts_dictionary)

        if len(al_accts) > 1:
            self._add_acct_cat(al_accts[1:], self._data[yyyy][mm][al_accts[0]], amount, yyyymm, self._accts_dictionary[al_accts[0]])
