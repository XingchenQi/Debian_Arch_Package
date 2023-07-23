# coding test instructions

* Debian uses *deb packages to deploy and upgrade software. The packages are stored in repositories and each repository contains the so called "Contents index". The format of that file is well described here https://wiki.debian.org/RepositoryFormat#A.22Contents.22_indices

* Your task is to develop a python command line tool that takes the architecture (amd64, arm64, mips etc.) as an argument and downloads the compressed Contents file associated with it from a Debian mirror. The program should parse the file and output the statistics of the top 10 packages that have the most files associated with them. An example output could be:

```
    ./package_statistics.py amd64

    
    <package name 1>         <number of files>
    <package name 2>         <number of files>
    ......

    <package name 10>         <number of files>
```

* You can use the following Debian mirror: http://ftp.uk.debian.org/debian/dists/stable/main/. Please try to follow Python's best practices in your solution.

* Please do your work in a local Git repository. Your repo should contain a README that explains your thought process and approach to the problem, and roughly how much time you spent on the exercise. When you are finished, create a tar.gz of your repo and submit it to the link included in this email. Please do not make the repository publicly available.

# Enviroment 
* Python 3.8.8

# Intuition 
* First I parse all the file names from the mirror url and store valid arch names in a dictionary, then it downloads the related arch content file with the valid input and use gzip library to open zip-compressed file. Later it reads this file by line and create a dictionary that store the package as the key and the incremented count as value. Finally we sort the dict by value and extract the top 10 pairs as a list.
* After the code implementation, I used pylint library to check code quality and see whether it has followed the Python's best practices.
* A short bash script is also introduced as a simple CLI interface for users to interact with.

## how long this took me
* 3 hrs

# class and public methods
```
    # create class object
    stats_loader = ArchPackageStats()

    # get all avalible archs
    all_archs = stats_loader.get_avalible_archs()
    
    
    # entrance function to get top 10 for arm64
    top = stats_loader.get_stats("arm64")


    # get full list packages of all with counts
    all = stats_loader.get_package_list()
```

# file structure
* venv/ = virtual enviroment
* package_statistics.py = feature implementation class
* package_stats_cli.bash = bash script
* test_package_statistics.py = unit tests


# install dependencies
```
    virtualenv -p python venv
    source venv/bin/activate
    pip3 install -r requirements.txt
```



## python command line example
```
    python3 package_statistics.py amd64
```

## start bash script
```
    chmod +x package_stats_cli.bash
    ./package_stats_cli.bash
```


## run tests
``` 
    python3 test_package_statistics.py
```





