# Enviroment 
* Python3.8

# install dependencies
```
    virtualenv -p python venv
    source venv/bin/activate
    pip3 install -r requirements.txt
```


# file structure
* venv/ = virtual enviroment
* debian_package_state.py = package stats class
* test_debian_package_state.py = testing  script


# how to use class
```
    # create
    stat = DebianPackageStats()

    # get all avalible archs
    # array of strings
    all_arch = stat.get_avalible_archs()
    
    
    # get top 10 for arch
    top = stat.get_stats("amd64")


    # get list of all with counts
    all = stat.get_package_list()
```


## how to run test
``` 
    python3 test_debian_package_stats.py
```

## how to start simple cli
```
    chmod +x debian_package_stats.bash
    ./debian_package_stats.bash
```

## python cli
```
    python3 debian_package_stats.py amd64
```


## how long this took me
* around 2.5 to 3 hrs


# coding test instructions

* Debian uses deb packages to deploy and upgrade software. The packages are stored in repositories and each repository contains the so called "Contents index". The format of that file is well described here https://wiki.debian.org/RepositoryFormat#A.22Contents.22_indices

* Your task is to develop a Python command line tool that takes the architecture (amd64, arm64, mips etc.) as an argument and downloads the compressed Contents file associated with it from a Debian mirror. The program should parse the file and output the statistics of the top 10 packages that have the most files associated with them.

* An example output could be:
```
./package_statistics.py amd64
1. <package name 1>         <number of files> 2. <package name 2>         <number of files> ......
10. <package name 10>         <number of files>
```

* You can use the following Debian mirror
    * http://ftp.uk.debian.org/debian/dists/stable/main/. Please do try to follow Python's best practices in your solution. Hint: there are tools that can help you verify your code is compliant. In-line comments are appreciated.
* It will be good if the code is accompanied by a 1-page report of the work that you have done including the time you actually spent working on it.

