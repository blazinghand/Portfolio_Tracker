#!/usr/bin/env python

'''
Note 1:
Problems: 1. The symbol needs to be instered precisely, otherwise the program does not find it and writes N/A in the .txt file,
which needs to be opened manually in order to fix the problem.;
2. if I add a stock that I already have it deletes the previous entries and replace them with the new ones.

Note 2:
There are two versions of ystockquote, the one used here is the version 0.2.4 (which is the one you can get with pip).
Version 0.2.5 is the developing version which is on github. Functions are given different names and, as it is,
this script would not work with the dev version. The changes, though are trivial.

'''


import string
from prettytable import PrettyTable
import os
import sys
import ystockquote



def dict_from_file(file):
	'''
	This function reads from a file and writes a dictionary from it.
	The file needs to have on each line the structure:
	name of the company, title, number of shares, purchase price, latest price.
	Separated by a comma
	'''
	dictionary = {}
	f = open(file,'r')
	for line in f:
		x = line.strip('\n').split(',')
		dictionary[x[0]] = []
		dictionary[x[0]].append(x[0])
		dictionary[x[0]].append(x[1])
		dictionary[x[0]].append(round(float(x[2]),1))
		dictionary[x[0]].append(round(float(x[3]),2))
		#dictionary[x[0]].append(round(float(x[4]),2))
		dictionary[x[0]].append(float(ystockquote.get_price(x[1])))
		#print stocks[x[1]]
	f.close()
	return dictionary


def show_portfolio(dict):
	'''
	This works only for dictionary defined in such a way that for each key there is an array structured like this:
	title, name of the company, number of shares, purchase price, latest price
	'''
	portfolio = PrettyTable(['Company','Shares','Purchase','Latest','Value','Gain'])
	portfolio.align['Company'] = 'l'
	portfolio.padding_width = 1
	tot_latest = 0
	tot_purchase = 0
	for x in dict:
		portfolio.add_row([dict[x][0]+' ('+dict[x][1]+')',\
			dict[x][2],\
			dict[x][3],\
			dict[x][4],\
			dict[x][2]*dict[x][4],\
			str(round((-dict[x][3]+dict[x][4])/dict[x][3]*100,2))+'%'])
		tot_latest += dict[x][2]*dict[x][4]
		tot_purchase += dict[x][2]*dict[x][3]
	portfolio.add_row(['','','','','',''])
	if tot_purchase==0:
		portfolio.add_row(['TOT','',tot_purchase,'',tot_latest,'-'])
	else:
		portfolio.add_row(['TOT','','','',tot_latest,str(round((tot_latest-tot_purchase)/tot_purchase*100,2))+'%'])
	print portfolio

def write_dict_to_file(dict,file):
	'''
	Writes the dictionary to file the way I would like to.
	'''
	f = open(file,'w')
	for key in dict:
		f.write(dict[key][0]+','+dict[key][1]+','+str(dict[key][2])+','+str(dict[key][3])+','+str(dict[key][4])+'\n')
	f.close()


def add_stock(dict):
	'''
	Function to add a stock to portfolio, work with the same dictionary structure as above
	'''
	new_stock = str(raw_input('Company Name: '))
	new_symbol = str(raw_input('Symbol: '))
	num_share = raw_input('Number of stocks purchased: ')
	purch_price = ystockquote.get_price(new_symbol) #raw_input('Purchase Price: ')
	latest_price = purch_price #raw_input('Latest Price: ')
	dict[new_stock]=[]
	dict[new_stock].append(new_stock)
	dict[new_stock].append(new_symbol)
	dict[new_stock].append(num_share)
	dict[new_stock].append(purch_price)
	dict[new_stock].append(latest_price)


def del_stock(dict):
	'''
	Function to delete stock from portfolio
	'''
	while True:
		del_stock = raw_input('Which company have you sold? ')
		if del_stock not in dict:
			print 'Can you repeat? (company name, capitalize correctly) '
			#exit()
		else:
			del dict[del_stock]
			break


def update_price(dict):
	'''
	Updates portfolio with new prices
	'''
	print 'Updating portfolio...'
	for key in dict:
		dict[key][4] = ystockquote.get_price(dict[key][1])


def create_file():
	'''
	Creates a new .txt file
	'''
	print 'Creating a new text file...'
	name = raw_input('Name of file: ')+'.txt'
	new_file = open(name,'a')
	new_file.close()
	return name


def delete_file():
	'''
	Deletes a .txt file
	'''
	while True:
		file_name = raw_input('Which file do you want to delete? ')+'.txt'
		sure = raw_input('Are you sure you want to delete the file? (Y/N) ').upper()
		if sure == 'Y' :
			if os.path.isfile(file_name):
				os.remove(file_name)
				print 'File deleted'
				print ''
				break
			else:
				print ''
				print 'The file does not exist'
				print ''
				redo = raw_input('(R)e-type or (H)appy this way and get out? ').upper()
				if redo == 'R':
					print 'OK'
				elif redo == 'H':
					break
				else:
					print 'You fucked up and I am shutting down now...'
					break
		elif sure == 'N':
			print ''
			print 'OK, good we stopped you in time...'
			print ''
			break
		else:
			print 'Please repeat what you want to do'


def print_file():
	'''
	Print .txt files in folder
	'''
	pathname = os.path.dirname(sys.argv[0])
	for file in os.listdir(os.path.abspath(pathname)):
		if file.endswith(".txt"):
			print file.strip('.txt')


def file_manager():
	'''
	Manages files
	'''
	print ''
	while True:
		#print ''
		print 'These are your current stock files:'
		#print ''
		print_file()
		#print ''
		choice = raw_input('(W)rite a new file, (D)elete an existing one, (U)pload an existing one or (Q)uit: ').upper()
		if choice == 'U':
			upload = raw_input('Which file do you want to upload? ')+'.txt'
			if os.path.isfile(upload):
				return upload
				break
			else:
				print ''
				print 'The file you requested does not exist, here are your options again '
				print ''
		elif choice == 'W':
			upload = create_file()
			return upload
			break
		elif choice == 'Q':
			exit()
		elif choice == 'D':
			delete_file()
		else:
			print ''
			print 'Please repeat what you want to do, here are the options again'
			print ''


def write_new_line(file):
	'''
	This function writes a new line in the file with the info for the portfolio. It will substitute add_stock
	'''
	new_stock = str(raw_input('Company Name: '))
	new_symbol = str(raw_input('Symbol: '))
	num_share = raw_input('Number of stocks purchased: ')
	purch_price = raw_input('Purchase Price: ')
	latest_price = raw_input('Latest Price: ')
	f = open(file,'a')
	f.write(new_stock+','+new_symbol+','+num_share+','+purch_price+','+latest_price+'\n')
	f.close()


def test_getMarketData():
	assert 0<float(ystockquote.get_price('GOOG'))<10000


def main():
	'''
	Main function
	'''
	upload = file_manager()
	while True:
		stocks = dict_from_file(upload)
		print ''
		print 'This is your portfolio now'
		print ''
		show_portfolio(stocks)
		UpDate = raw_input('(A)dd/(D)elete stock, (U)pdate portfolio, (M)anage files, (Q)uit. ').upper()
		if UpDate == 'A':
			add_stock(stocks)
			write_dict_to_file(stocks,upload)
		elif UpDate == 'D':
			del_stock(stocks)
			write_dict_to_file(stocks,upload)
		elif UpDate == 'U':
			update_price(stocks)
			write_dict_to_file(stocks,upload)
		elif UpDate == 'M':
			upload = file_manager()
		elif UpDate == 'Q':
			exit()
		else:
			print ''
			print 'Sorry, I did not understand what you want to do, here are your options again.'



if __name__ == "__main__":
	main()


