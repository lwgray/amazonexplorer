#!/usr/bin/python
# coding: utf-8
""" Tool to find discrepancies in Amazon returns and reimbursements """
import csv
import sys
from datetime import datetime


def get_return_report(input_file):
    """ parse report of returned goods
        Input: Amazon Return Report
        Output: Dict Object
            Keys: Order_ID(s)
            Value : List of Dict(s)
                Key --> detailed_disposition : Value --> product state
                Key --> reason : Value --> reason for return
                Key --> status : Value --> current status
                Key --> sku : Value --> product sku
                Key --> asin : Value -->  Amazon Asin
                Key --> date : Value --> product return date
    """
    data = {}
    with open(input_file) as in_file:
        return_reader = csv.reader(in_file, delimiter='\t')
        return_reader.next()
        for index, line in enumerate(return_reader):
            order_id = line[1]
            detailed_disposition = line[-3]
            reason = line[-2]
            status = line[-1]
            sku = line[2]
            asin = line[3]
            return_date = line[0]
            if order_id not in data:
                data[order_id] = [{'detailed_disposition': detailed_disposition,
                                  'reason': reason, 'status': status, 'sku': sku, 'asin': asin, 'date': return_date}]
            else:
                data[order_id].append({'detailed_disposition': detailed_disposition,
                                       'reason': reason, 'status': status, 'sku': sku, 'asin': asin, 'date': return_date})
        return data


def find_damaged_goods(returned_products):
    """ Find damaged and non-reimbursed products """
    damaged = {}
    for key, value in returned_products.iteritems():
        for index in value:
            if index['detailed_disposition'] == 'SELLABLE' or index['detailed_disposition'] == 'CUSTOMER_DAMAGED'\
                    or index['detailed_disposition'] == 'DEFECTIVE':
                continue
            elif index['status'] == 'Reimbursed':
                continue
            elif key not in damaged:
                damaged[key] = [index]
            else:
                damaged[key].append(index)
    return damaged


def get_reimbursement_report(input_file):
    """ parse report of reimbursed transactions
        Input: Amazon Reimbursement Report
        Output: Dict Object
            Key : Order_ID(s)
            Value : List of Dict(s)
                Key --> date : Value --> Reimbursement Date
                Key --> quantity_reimbursed_cash : Value --> Quantity Reimbursed with Cash
                Key --> sku : Value --> Product SKU
                Key --> asin : Value --> Product ASIN
    """
    data = {}
    with open(input_file) as in_file:
        reader = csv.reader(in_file, delimiter='\t')
        reader.next()
        for index, line in enumerate(reader):
            order_id = line[3]
            date = line[0]
            quantity_reimbursed_cash = line[13]
            sku = line[5]
            asin = line[7]
            if order_id not in data:
                data[order_id] = [{'date': date,
                                   'quantity_reimbursed_cash': quantity_reimbursed_cash,
                                   'sku': sku, 'asin': asin}]
            else:
                data[order_id].append({'date': date,
                                       'quantity_reimbursed_cash': quantity_reimbursed_cash,
                                       'sku': sku, 'asin': asin})
        # remove items without order_id - these products were damaged in warehouse
        data.pop('')
        return data


def verify_reimbursement(damaged, reimbursed):
    """ Verify that the damaged item was not reimbursed """
    data = [(key, damaged[key]) for key in damaged if key not in reimbursed]
    # If not reimbursed - make sure that the time to file has not exceeded reimbursement policy time-line
    # data = [value for value in data if check_days(value[1]['date'], 18, 'months')]
    return data


def write_report(verified):
    with open('c:\\users\\lwgra\\desktop\\final_report.txt', 'w') as report:
        writer = csv.writer(report)
        writer.writerow(['AMAZON ORDER ID', 'ASIN', "SELLER SKU", 'DATE'])
        for items in verified:
            order_id = items[0]
            for item in items[1]:
                writer.writerow([order_id, item['asin'], item['sku'], item['date']])


def import_removal_report(filename):
    with open(filename) as in_file:
        reader = csv.reader(in_file, delimiter='\t')
        reader.next()
        for line in reader:
            print line
    return


def check_days(date, limit, unit):
    """ Return True or False if time passed is greater than required """
    # refund_date = datetime.strptime(date, '%b %d, %Y %I:%M:%S %p PST')
    refund_date = date
    today = datetime.now()
    time_diff = today - refund_date
    num_days = time_diff.days
    if unit == 'days':
        if num_days < limit:
            return True
        else:
            return False
    if unit == 'months':
        months = num_days/31
        if months < limit:
            return True
        else:
            return False
    return


def get_refund_data(input_file):
    """ parse report of refunded goods
        Input: Amazon Refund Report
        Output: Dict Object
            Keys: Order_ID(s)
            Value : List of Dict(s)
                Key --> detailed_disposition : Value --> product state
                Key --> reason : Value --> reason for return
                Key --> status : Value --> current status
                Key --> sku : Value --> product sku
                Key --> asin : Value -->  Amazon Asin
                Key --> date : Value --> product return date
    """
    with open(input_file) as infile:
        reader = csv.reader(infile, delimiter='\t')
        reader.next()
        reader.next()
        reader.next()
        reader.next()
        data = dict([(line[1], line) for line in reader])
    return data


def find_problems(returned, refunded, reimbursed):
    for key, value in refunded.iteritems():
        if key not in returned:
            if key not in reimbursed:
                date = datetime.strptime(value[0], '%b %d, %Y')
                if check_days(date, 18, 'months'):
                    print key, value
    return


def find_non_reimbursed_damaged_goods_before_deadline():
    """

    :return: 
    """
    returned_goods = get_return_report('c:\\users\\lwgra\\desktop\\returns.txt')
    refunded_goods = get_refund_data('c:\\users\\lwgra\\desktop\\refunds.txt')
    reimbursed_goods = get_reimbursement_report('c:\\users\\lwgra\\desktop\\reimbursements.txt')
    find_problems(returned_goods, refunded_goods, reimbursed_goods)
    return


def find_non_reimbursed_damaged_goods():
    ''' Find Damaged Goods that were not reimbursed
    :rtype: object
    '''
    returned_goods = get_return_report('c:\\users\\lwgra\\desktop\\returns.txt')
    reimbursed_goods = get_reimbursement_report('c:\\users\\lwgra\\desktop\\reimbursements.txt')
    damaged_goods = find_damaged_goods(returned_goods)
    verified = verify_reimbursement(damaged_goods, reimbursed_goods)
    write_report(verified)
    return

'''
def main():
    reimbursed_goods = get_reimbursement_report('c:\\users\\lwgra\\desktop\\reimbursements.txt')
    returned_goods = get_return_report('c:\\users\\lwgra\\desktop\\returns.txt')
    while True:
        returned = True
        reimbursed = True
        order_id = raw_input("Enter Order ID: ")
        order_id = order_id.strip()
        if order_id:
            try:
                if returned_goods[order_id]:
                    print "This Item was returned"
                    returned = True
            except KeyError:
                print "This Item has not been returned"
                returned = False
            try:
                if reimbursed_goods[order_id]:
                    print "This item was reimbursed"
                    reimbursed = True
            except KeyError:
                print "This Item has not been reimbursed"
                reimbursed = False
        if not returned and not reimbursed:
            print "Oh Yea"
            check_days()

if __name__ == '__main__':
    sys.exit(main())
'''

