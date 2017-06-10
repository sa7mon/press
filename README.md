      ########  ########  ########  ######   ######
      ##     ## ##     ## ##       ##    ## ##    ##
      ##     ## ##     ## ##       ##       ##
      ########  ########  ######    ######   ######
      ##        ##   ##   ##             ##       ##
      ##        ##    ##  ##       ##    ## ##    ##
      ##        ##     ## ########  ######   ######

usage: press.py [-h] -u USERS -p PASSWORDS -s SITE [-r RESUME] [-l LOGFILE]
                [-t THREADS]

press -- A multi-threaded tool for resumable Wordpress bruteforcing

optional arguments:
  -h, --help            show this help message and exit
  -u USERS, --users USERS
                        File with usernames to try
  -p PASSWORDS, --passwords PASSWORDS
                        File of passwords to try
  -s SITE, --site SITE  Site to target. Full path to /wp-login.php
  -r RESUME, --resume RESUME
                        Username to resume bruteforcing at
  -l LOGFILE, --logfile LOGFILE
                        Name of log file. Default: ./log.txt
  -t THREADS, --threads THREADS
                        Number of threads to use. Default: 10