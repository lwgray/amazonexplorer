# coding: utf-8
def get_refund_data(input_file):
    with open(input_file) as infile:
        reader = csv.reader(infile, delimiter='\t')
        reader.next()
        reader.next()
        reader.next()
        header = reader.next()
        print header
	data = [line for line in reader]
    return data
