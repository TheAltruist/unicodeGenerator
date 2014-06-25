#! usr/bin/python

'''
Copyright (c) 2014 Marcelino Jorge Romero Karavia

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import platform
import os
import time


def isWindows():
	return platform.system() == 'Windows'


def clear_screen():
	if isWindows():
		os.system('cls')
	else:
		os.system('clear')


def separator(colCounter):
	if colCounter == 25:
		separateChar = "<br /><br />"
	else:
		separateChar = "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
	return separateChar


class Menu(object):
	
	def __init__(self, *args, **kwargs):
		self._menu = []
		self._str_menu = ''
		self._construct_menu()

	@property #read only
	def menu(self):
		return self._menu

	def _construct_menu(self):
		with open("menu_char_sets", "r") as menu_char_sets:
			str_menu = menu_char_sets.read()

		with open("range_char_sets", "r") as range_char_sets:
			str_ranges = range_char_sets.read()

		'''menu_list and ranges_list must have the exact same number of lines'''
		menu_list = str_menu.split('\n')
		ranges_list = str_ranges.split('\n')
		
		del str_menu
		
		counter = 0
		for item in menu_list:
			
			number = item[ 0 : item.find('.') ]
			description = item[ item.find('.') + 2 : ]

			self._menu.append(
				{
					number : description,
					'range_start' : ranges_list[counter][ 0 : ranges_list[counter].find('\t') ], #range_start and range_end are stored in hex format
					'range_end' : ranges_list[counter][ ranges_list[counter].find('\t') + 1 : ],
				}
			)

			self._str_menu = '{}\n{}. {}'.format(self._str_menu, counter, self._menu[counter].get(str(counter)))
			counter += 1

		#Add additional options
		self._menu.append(
			{
				str(counter) : 'Eveything (really slow)',
				'range_start' : self._menu[0].get('range_start'),
				'range_end' : self._menu[counter - 1].get('range_end')
			}
		)

		self._str_menu = '{}\n{}. {}\n... For quit press q: '.format(self._str_menu, counter, self._menu[counter].get(str(counter)))
		
	def __str__(self):
		return self._str_menu


def generate_unicode_file(range_start, range_end, file_name):
	charByte = bytearray()
	strChars = str();
	colCounter = 0;

	for i in xrange(range_start, range_end):
		if i > 127:
			charByte = bytes('&#{:04d}'.format(i))
			strChars += str(charByte).encode('utf_8') + separator(colCounter)
		else:
			strChars += str(chr(i) + separator(colCounter))

		if colCounter == 25:
			colCounter = 0 
		
		colCounter += 1
		
	htmlStruct = "<html>\n<head>\n<title></title>\n\
	<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\" />\n</head>\n<body>\n{}\n</body>\n</html>"

	retValue = {
		'isSuccessful' : True,
		'error' : None
	}
	try:
		fOut = open(file_name, 'w')
		fOut.write(htmlStruct.format(strChars))
	except IOError as err:
		retValue = {
			'isSuccessful' : False,
			'error' : err
		}
	else:
		fOut.close()

	return retValue


def main():
	'''
	In Python 2.x all strings and unicode are bytearrays.
	In Python 3.x strings are strings.

	The list of unicode codes and names has been taken from:
	http://www.fileformat.info/info/unicode/block/index.htm
	'''
	def print_wrong_input():
		clear_screen()
		print "\nSelected option could not be found. Please Try again...\n"

	
	menu = Menu()
	
	while True:
		clear_screen()
		input_option = raw_input('Please select an option:\n{}'.format(menu))

		if input_option.lower() == 'q':
			print '\nProgram is exiting...\n'
			break

		try:
			input_option = int(input_option)
		except ValueError, e:
			print_wrong_input()
			continue

		if input_option > len(menu.menu) or input_option < 0:
			print_wrong_input()
			continue

		filename = "{} {}_{}.html".format(input_option, menu.menu[input_option].get(str(input_option)), time.strftime("%Y%m%d%H%M%S"))
		print('\nGenerating file "{}" . . .\n'.format(filename))

		"range_start and range_end are in hex format and must be converted to int"
		result = generate_unicode_file(int(menu.menu[input_option].get('range_start'), 16), int(menu.menu[input_option].get('range_end'), 16), filename)

		if result.get('isSuccessful'):
			print('File generated successfully!\n')
		else:
			print("Oh crap! An Error ocurred: {}\n".format(result.get('error').strerror))

		raw_input('\nPress enter to continue...')


if __name__ == "__main__": main()
