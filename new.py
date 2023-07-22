#!/usr/bin/env python"""Automation CodeYour task is to develop a python command line tool that takes thearchitecture (amd64, arm64, mips etc.) as an argument and downloads thecompressed Contents file associated with it from a Debian mirror. Theprogram should parse the file and output the statistics of the top 10packages that have the most files associated with them.- This script downloads a Contents architecture file, reads its contents andreturns top 10 packages in terms of associated number of files.Contents file.- Python3 was used in this scripting.https://wiki.ubuntu.com/Python/FoundationsXPythonVersions- Time spent: about 1.5 hours due to office deadlines, I could not spendanymore on this script.TODO: use some try catch blocks for parsingTODO: Add unit tests.TODO: Move utility functions to a utility file.TODO: Move parser to a parser file- Data structure used: heapqhttps://docs.python.org/3.0/library/heapq.html#heapq.nlargestUsage example:Use help switch for options:python3 package_statistics.py --helptime python3 package_statistics.py --arch amd64******************************************************Downloading Content Index file: Contents-amd64.gzDownloading from: http://ftp.uk.debian.org/debian/dists/stable/main/Contents-amd64.gzReading Content Index file: Contents-amd64.gz    numix-icon-theme                68920flightgear-data-base                 64707 texlive-fonts-extra                45910            rust-doc                45641        trilinos-doc                45567      widelands-data                34985     moka-icon-theme                32533            vtk6-doc                29464   faenza-icon-theme                29400fonts-mathjax-extras                29035real    0m12.318suser    0m11.748ssys     0m0.491s"""import argparsefrom argparse import RawTextHelpFormatterimport osimport gzipfrom heapq import nlargestimport io# ConstantsDEBIAN_MIRROR_URL = "http://ftp.uk.debian.org/debian/dists/stable/main/"NUMBER_OF_RESULTS = 10# Dictionary for Packagespackage_dict = {}def download_content_indice_file(file):    wget_command = "wget {} --no-check-certificate".format(file)    os.system(wget_command)def read_content_indice_file(file):    gz = gzip.open(file, 'rb')    f = io.BufferedReader(gz)    for line in f:        line = line.decode("utf-8")        line = line.rstrip()        file_name, space, package_name = line.rpartition(' ')        # Case admin/molly-guard,admin/systemd-sysv,admin/sysvinit-core        package_name = package_name.split(',')        for package in package_name:            # Grab package name After last /            package = package.rpartition('/')[2]            # Uniquessness in keys            if package not in package_dict.keys():                package_dict[package] = []            package_dict[package].append(file_name)    gz.close()    for package in nlargest(NUMBER_OF_RESULTS,                            package_dict, key=lambda e: len(package_dict[e])):            print(                "{: >20} {: >20}".format(package, len(package_dict[package]))            )parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter)parser.add_argument('--arch',                    help="Enter the architecture, e.g. amd64, arm64 etc.")args = parser.parse_args()if args.arch:    content_indice_file = "Contents-{arch}.gz".format(        arch=args.arch    )    content_indice_file_url = "{deb_mirror}{content_indice_file}".format(        content_indice_file=content_indice_file,        deb_mirror=DEBIAN_MIRROR_URL,    )    print("******************************************************")    print("Downloading Content Index file: %s" % content_indice_file)    print("Downloading from: %s" % content_indice_file_url)    download_content_indice_file(content_indice_file_url)    print("Reading Content Index file: %s " % content_indice_file)    read_content_indice_file(content_indice_file)