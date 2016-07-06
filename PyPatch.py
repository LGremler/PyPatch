# This is a lightweight script used to update files in a directory based off their MD5 sum
# or download them if they do not exist.
#
# Author: Logan Gremler 7/1/16
# Remote MD5 Sum Code Author: Brian Ewing 5/26/11 (https://gist.github.com/brianewing/994303)(Modified)

import os
import hashlib
import urllib
import urllib2
import optparse

class PyPatch():
    def __init__(self):
        self.client1 = ''
        self.server1 = ''
        self.client2 = ''
        self.server2 = ''

    def fetch_server_md5(self, url, max_file_size=100*1024*1024):
        self.remote = urllib2.urlopen(url)
        self.hash = hashlib.md5()
        
        self.total_read = 0
        while True:
            self.data = self.remote.read(4096)
            self.total_read += 4096

            if not self.data or self.total_read > max_file_size:
                break

            self.hash.update(self.data)

        return self.hash.hexdigest()

    def check_server_md5(self):
        # Create individual Option Parsers for each file
        self.options = optparse.OptionParser()
        self.options2 = optparse.OptionParser()

        # Add Options
        self.options.add_option('--url', '-u', default='https://raw.githubusercontent.com/LGremler/citrus/master/Menu.py')
        self.options2.add_option('--url', '-u', default='https://github.com/LGremler/Apartment-Calculator/raw/master/ApartmentCalculator.py')

        # Parse the arguments
        self.options, self.args = self.options.parse_args()
        self.options2, self.args = self.options2.parse_args()

        # Store the MD5s
        self.server1 = self.fetch_server_md5(self.options.url)
        self.server2 = self.fetch_server_md5(self.options2.url)

    def fetch_client_md5(self):
        # Define files
        self.file1 = 'sample/Menu.py'
        self.file2 = 'ApartmentCalculator.py'

        # Open files for reading or download them if they dont exist
        try:
            self.open1 = open(self.file1)
        except IOError:
            print "Downloading" ,str(self.file1)
            urllib.urlretrieve ("https://raw.githubusercontent.com/LGremler/citrus/master/Menu.py", "sample/Menu.py")
            print str(self.file1), "has been downloaded."
            print ""
            self.open1 = open(self.file1)
        try:
            self.open2 = open(self.file2)
        except IOError:
            print "Downloading" ,str(self.file2)
            urllib.urlretrieve ("https://github.com/LGremler/Apartment-Calculator/raw/master/ApartmentCalculator.py", "ApartmentCalculator.py")
            print str(self.file2), "has been downloaded."
            print ""
            self.open2 = open(self.file2)

        # Read files
        self.content1 = self.open1.read()
        self.content2 = self.open2.read()

        # Store the MD5s
        self.client1 = hashlib.md5(self.content1).hexdigest()
        self.client2 = hashlib.md5(self.content2).hexdigest()

    def downloader(self):
        # Get the MD5s for the client files and the server files
        self.check_server_md5()
        self.fetch_client_md5()

        # Check to see if updates are available. Download if necessary
        if self.client1 != self.server1:
            print "Updating " ,str(self.file1)
            urllib.urlretrieve ("https://raw.githubusercontent.com/LGremler/citrus/master/Menu.py", "sample/Menu.py")
            print str(self.file1), "has been updated."
            print ""
        else:
            print str(self.file1), "is up to date."
            print ""
        if self.client2 != self.server2:
            print "Updating " ,str(self.file2)
            urllib.urlretrieve ("https://github.com/LGremler/Apartment-Calculator/raw/master/ApartmentCalculator.py", "ApartmentCalculator.py")
            print str(self.file2), "has been updated."
        else:
            print str(self.file2), "is up to date."
