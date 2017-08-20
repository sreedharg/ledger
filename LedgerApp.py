import sys, getopt
import os

from CapitecLoader import CapitecLoader
from DiscoveryLoader import DiscoveryLoader
from StandardBankLoader import StandardBankLoader

class LedgerApp(object):
    def __init__(self):
        print ('Ledger v0.1')
        self._data = {}
        self._accts_dictionary = {}
        self._count = 0
        self._report_file = open('./reports/report.txt', 'w')
        self._csv_report_file = open('./reports/report.csv', 'w')
        self._level = 2

        argv = sys.argv[1:]
        try:
            opts, args = getopt.getopt(argv,"hl:",["level="])
        except getopt.GetoptError:
            print ('ledger_app.py -l <level> ')
            sys.exit(2)

        for opt, arg in opts:
            if opt == '-h':
                print ('ledger_app.py -l <level> ')
                sys.exit()
            elif opt in ("-l", "--level"):
                self._level = int(arg)
                if self._level <= 0:
                    print ('level must be greater than 0')
                    sys.exit()

    def _print_item_name(self, item, tab, csv_flag=False):
        format_string = (75 - tab) * ' ' + '{0:<' + str(tab) + '}'
        self._report_file.write(format_string.format(item))

        if csv_flag:
            self._csv_report_file.write(format_string.format(child2) + ',')

    def _pretty_print_monthly_detail(self):
        tab = 75
        format_string_1 = '{0:>20,.2f}'
        format_string_2 = '{0:>15,.2f}'
        csv_format_string_1 = '{0:>20.2f}'
        csv_format_string_2 = '{0:>15.2f}'

        for item in sorted(self._accts_dictionary):
            item_total = 0
            self._print_item_name(item, tab)

            for yyyy in sorted(self._data):
                for mm in sorted(self._data[yyyy]):
                    if mm not in [  'monthly' , 'yearly' , 'bal']:
                        try:
                            self._report_file.write(format_string_1.format(self._data[yyyy][mm][item]['bal']))
                            item_total = self._data[yyyy][mm][item]['bal'] + item_total
                        except:
                            self._report_file.write(format_string_1.format(0))

            self._report_file.write(' |' + format_string_2.format(item_total))
            self._report_file.write('\n' + (' ' * 80) + ('-' * 15+ '     ') * (self._count + 1) + '\n')

            if self._level <= 1:
                continue

            tab = tab - 10
            for child in sorted(self._accts_dictionary[item]):
                child_total = 0
                self._print_item_name(child, tab)

                for yyyy in sorted(self._data):
                    for mm in sorted(self._data[yyyy]):
                        if mm not in [  'monthly' , 'yearly' , 'bal']:
                            in_front=item + ',' + child + ',' + str(yyyy) + str(mm) + ','
                            try:
                                self._report_file.write(format_string_1.format(self._data[yyyy][mm][item][child]['bal']))
                                self._csv_report_file.write( in_front + csv_format_string_1.format(self._data[yyyy][mm][item][child]['bal']) + '\n')
                                child_total = child_total + self._data[yyyy][mm][item][child]['bal']
                            except:
                                self._report_file.write(format_string_1.format(0))
                                self._csv_report_file.write( in_front  + csv_format_string_1.format(0) + '\n')
                self._report_file.write(' |')
                self._report_file.write(format_string_2.format(child_total))
                self._report_file.write('\n')

                if self._level <= 2:
                   continue
                tab = tab -10
                for child2 in sorted(self._accts_dictionary[item][child]):
                    child2_total = 0
                    self._print_item_name(child2, tab, True)

                    for yyyy in sorted(self._data):
                        for mm in sorted(self._data[yyyy]):
                            if mm not in [  'monthly' , 'yearly' , 'bal']:
                                try:
                                    self._report_file.write(format_string_1.format(self._data[yyyy][mm][item][child][child2]['bal']))
                                    self._csv_report_file.write(csv_format_string_1.format(self._data[yyyy][mm][item][child][child2]['bal']) + ',')
                                    child2_total = child2_total + self._data[yyyy][mm][item][child][child2]['bal']
                                except:
                                    self._report_file.write(format_string_1.format(0))
                                    self._csv_report_file.write(csv_format_string_1.format(0) + ',')
                    self._report_file.write('         |' + format_string_2.format(child2_total) + '\n')
                    self._csv_report_file.write(csv_format_string_2.format(child2_total) + ',\n')

                tab = tab + 10

            self._report_file.write('\n' * 2)
            tab = tab + 10

    def pretty_print_monthly(self):
        for yyyy in sorted(self._data):
            for mm in sorted(self._data[yyyy]):
                if mm not in [  'monthly' , 'yearly' , 'bal']:
                    self._count = self._count + 1

        self._report_file.write('\n' + '-' * 80 + '-' * 20 * (self._count + 1) + '\n' + ' ' * 75)

        for yyyy in sorted(self._data):
            for mm in sorted(self._data[yyyy]):
                if mm not in [  'monthly' , 'yearly' , 'bal']:
                    yyyymm_str = '             ' + str(yyyy) + '/' + str(mm)
                    self._report_file.write(yyyymm_str)

        self._report_file.write('\n' + '-' * 80 + '-' * 20 * (self._count + 1) + '\n')
        self._pretty_print_monthly_detail()

    def read_files(self):
        for dirname, dirnames, filenames in os.walk('./txn-data'):
            for filename in filenames:
                if 'extr' in filename:
                    capitec_loader = CapitecLoader(dirname, filename, self._accts_dictionary, self._data)
                    self._data, self._accts_dictionary = capitec_loader.load()

                if '490137' in filename:
                    discovery_loader = DiscoveryLoader(dirname, filename, self._accts_dictionary, self._data)
                    self._data, self._accts_dictionary = discovery_loader.load()

                if 'statement' in filename:
                    standard_bank_loader = StandardBankLoader(dirname, filename, self._accts_dictionary, self._data)
                    self._data, self._accts_dictionary = standard_bank_loader.load()

    def cleanup(self):
        self._report_file.close()
        self._csv_report_file.close()

if __name__ == '__main__':
    ledger_app = LedgerApp()

    ledger_app.read_files()
    ledger_app.pretty_print_monthly()
    ledger_app.cleanup()
