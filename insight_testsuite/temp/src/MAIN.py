#!/usr/bin/python -tt

"""
Insight Data Engineering Fellowship Program, starting Jan. 2017 in New York City.
Coding Challenge: develop features to prevent fraudulent payment requests for PayMo. 

Shanyun Gao

"""

import sys

import transfer_verify

def main():
    if len(sys.argv) != 4:
        print 'usage: ./MAIN.py  --transferverify file1 file2'
        sys.exit(1)

    option = sys.argv[1]
    filename1 = sys.argv[2]
    filename2 = sys.argv[3]
    if option == '--transferverify':
        transfer_verify.transfer_verify(filename1, filename2)
    else:
        print 'unknown option: ' + option
        sys.exit(1)

if __name__ == '__main__':
    main()