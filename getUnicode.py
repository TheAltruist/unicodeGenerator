
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

'''
This script does not work on windows console
because win console does not support unicode.
'''
import string

def getUnicodeByCode(code):
	if isinstance(code, str):
		if all(c in string.hexdigits for c in code):
			uchar = unichr(int(code, 16))
		else:
			return -1
	elif isinstance(code, int):
			uchar = unichr(code)
	else:
		return -1

	return uchar

def main():
	codeChr = '0376' #Hex or integer value
	print u'Unicode char of {0} is: {1}'.format(codeChr, getUnicodeByCode(codeChr))


if __name__ == "__main__":
	main()
