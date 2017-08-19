import sys, getopt
import csv
from time import strptime
from time import mktime
from datetime import datetime, timedelta
from datetime import date
import os
import json
from configparser import ConfigParser

from CapitecLoader import CapitecLoader
from DiscoveryLoader import DiscoveryLoader
from StandardBankLoader import StandardBankLoader

accounts = {}
accts_dictionary = {}

count = 0
level = 2

report_file = open('./reports/report.txt', 'w')
csv_report_file = open('./reports/report.csv', 'w')

def pretty_print_monthly_detail():
    tab = 75
    for item in sorted(accts_dictionary):
        item_total = 0
        format_string = (75 - tab) * ' ' + '{0:<' + str(tab) + '}'
        report_file.write(format_string.format(item))
        #csv_report_file.write(item + ',')

        for yyyy in sorted(accounts):
            for mm in sorted(accounts[yyyy]):
                if mm not in [  'monthly' , 'yearly' , 'bal']:
                    format_string = '{0:>20,.2f}'
                    csv_format_string = '{0:>20.2f}'
                    try:
                        report_file.write(format_string.format(accounts[yyyy][mm][item]['bal']))
                        #csv_report_file.write(csv_format_string.format(accounts[yyyy][mm][item]['bal']) + ',')

                        item_total = accounts[yyyy][mm][item]['bal'] + item_total
                    except:
                        report_file.write(format_string.format(0))
                        #csv_report_file.write(csv_format_string.format(0) + ',')

        report_file.write('         |')
        format_string = '{0:>15,.2f}'
        csv_format_string = '{0:>15.2f}'
        report_file.write(format_string.format(item_total))
        #csv_report_file.write(csv_format_string.format(item_total)+ ',')

        report_file.write('\n')
        #csv_report_file.write('\n')
        report_file.write((' ' * 80) + ('-' * 15) + ('     ') + ('-' * 15) + ('     ') + ('-' * 15 ) + '\n')

        if level <= 1:
            continue

        tab = tab - 10
        for child in sorted(accts_dictionary[item]):
            child_total = 0
            format_string = (75 - tab) * ' ' + '{0:<' + str(tab) + '}'
            report_file.write(format_string.format(child))
            #csv_report_file.write(item + ',' + child + ',')

            for yyyy in sorted(accounts):
                for mm in sorted(accounts[yyyy]):
                    if mm not in [  'monthly' , 'yearly' , 'bal']:

                        in_front=item + ',' + child + ',' + str(yyyy) + str(mm) + ','
                        format_string = '{0:>20,.2f}'
                        csv_format_string = '{0:>20.2f}'
                        try:
                            report_file.write(format_string.format(accounts[yyyy][mm][item][child]['bal']))
                            csv_report_file.write( in_front + csv_format_string.format(accounts[yyyy][mm][item][child]['bal']) + '\n')
                            child_total = child_total + accounts[yyyy][mm][item][child]['bal']
                        except:
                            report_file.write(format_string.format(0))
                            csv_report_file.write( in_front  + csv_format_string.format(0) + '\n')
            report_file.write('         |')
            format_string = '{0:>15,.2f}'
            csv_format_string = '{0:>15.2f}'
            report_file.write(format_string.format(child_total))
            report_file.write('\n')
            #csv_report_file.write(csv_format_string.format(child_total) + ',')
            #csv_report_file.write('\n')

            if level <= 2:
               continue
            tab = tab -10
            for child2 in sorted(accts_dictionary[item][child]):
                child2_total = 0
                format_string = (75 - tab) * ' ' + '{0:<' + str(tab) + '}'
                report_file.write(format_string.format(child2))
                csv_report_file.write(format_string.format(child2) + ',')
                for yyyy in sorted(accounts):
                    for mm in sorted(accounts[yyyy]):
                        if mm not in [  'monthly' , 'yearly' , 'bal']:
                            format_string = '{0:>20,.2f}'
                            csv_format_string = '{0:>20.2f}'
                            try:
                                report_file.write(format_string.format(accounts[yyyy][mm][item][child][child2]['bal']))
                                csv_report_file.write(csv_format_string.format(accounts[yyyy][mm][item][child][child2]['bal']) + ',')
                                child2_total = child2_total + accounts[yyyy][mm][item][child][child2]['bal']
                            except:
                                report_file.write(format_string.format(0))
                                csv_report_file.write(csv_format_string.format(0) + ',')
                report_file.write('         |')
                format_string = '{0:>15,.2f}'
                csv_format_string = '{0:>15.2f}'
                report_file.write(format_string.format(child2_total))
                csv_report_file.write(csv_format_string.format(child2_total) + ',')

                report_file.write('\n')
                csv_report_file.write('\n')

            tab = tab +10


        report_file.write('\n')
        report_file.write('\n')
        csv_report_file.write('\n')
        csv_report_file.write('\n')
        tab = tab + 10

def pretty_print_monthly(accounts):
    count = 0
    for yyyy in sorted(accounts):
        for mm in sorted(accounts[yyyy]):
            if mm not in [  'monthly' , 'yearly' , 'bal']:
                count = count + 1

    report_file.write('\n')
    csv_report_file.write('\n')
    report_file.write('-' * 80 + '-' * 20 * (count + 1) + '\n')

    report_file.write(' ' * 75)

    for yyyy in sorted(accounts):
        for mm in sorted(accounts[yyyy]):
            if mm not in [  'monthly' , 'yearly' , 'bal']:
                yyyymm_str = '             ' + str(yyyy) + '/' + str(mm)
                report_file.write(yyyymm_str)
                csv_report_file.write(',' + yyyymm_str)

    report_file.write('\n')
    csv_report_file.write('\n')
    report_file.write('-' * 80 + '-' * 20 * (count + 1) + '\n')

    tab = 75
    pretty_print_monthly_detail()

def read_files():
    global accts_dictionary, accounts

    for dirname, dirnames, filenames in os.walk('./txn-data'):
        for filename in filenames:
            if 'extr' in filename:
                capitec_loader = CapitecLoader(dirname, filename, accts_dictionary, accounts)
                accounts, accts_dictionary = capitec_loader.load()

            if '490137' in filename:
                discovery_loader = DiscoveryLoader(dirname, filename, accts_dictionary, accounts)
                accounts, accts_dictionary = discovery_loader.load()

            if 'statement' in filename:
                standard_bank_loader = StandardBankLoader(dirname, filename, accts_dictionary, accounts)
                accounts, accts_dictionary = standard_bank_loader.load()

    pretty_print_monthly(accounts)

if __name__ == '__main__':
    print ('Ledger v0.1')

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
            level = int(arg)
            if level <= 0:
                print ('level must be greater than 0')
                sys.exit()

    read_files()

    report_file.close()
    csv_report_file.close()
