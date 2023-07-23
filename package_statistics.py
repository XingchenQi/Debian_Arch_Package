"""
This module takes the architecture (amd64, arm64, mips etc.) as an argument, parse the file
and output the statistics of the top 10 packages that have the most files associated with them

Usage example:

python3 debian_package_stats.py ppc64el

output example:
----------------------------------------------------------------------------------------------------
Id                  Package Name                                                              Number
----------------------------------------------------------------------------------------------------
1.                  piglit                                                                     53007
2.                  esys-particle                                                              18408
3.                  acl2-books                                                                 16907
4.                  libboost1.81-dev                                                           15456
5.                  racket                                                                      9599
6.                  zoneminder                                                                  8161
7.                  horizon-eda                                                                 8130
8.                  libtorch-dev                                                                8089
9.                  liboce-modeling-dev                                                         7458
10.                 paraview-dev                                                                6468
"""
import sys
import re
from io import BytesIO
import gzip
import requests


PACKAGE_LIST_SIZE = 10
TARGET_URL = "http://ftp.uk.debian.org/debian/dists/stable/main/"

class ArchPackageStats:
    """
    This class is used to get all the archs by parsing the contents from
    TARGET_URL, extracting contents file names and analyze statistics
    """
    def __init__(self):
        self.mirror_url = TARGET_URL
        self.archs_dict = self._get_archs_details()
        self.package_full_list = []

    # public
    def get_stats(self, arch):
        """
        This function calculates the stats with the input arch.
        @param arch is the input arch e.g. amd64
        @return list of top PACKAGE_LIST_SIZE packages and counts
        """
        self._check_valid_arch(arch)
        file_data = self._get_arch_data(arch)
        self.package_full_list = self._create_package_counts(file_data)
        file_data.close()
        return self.package_full_list[:PACKAGE_LIST_SIZE]

    def get_package_list(self):
        """
        This function returns the full package-counts list
        @return
        """
        return self.package_full_list

    def get_avalible_archs(self):
        """
        This function returns a list of archs from the mirror url
        """
        return self.archs_dict.keys()

    # private
    def _check_valid_arch(self, arch):
        """
        check to see if input arch is valid
        """
        if arch not in self.archs_dict.keys():
            raise Exception(
                arch
                + " is not a valid arch in Debian mirror, please choose an arch in the following: "
                + ' '.join(self.get_avalible_archs()))

    def _get_archs_details(self):
        """
        This function makes an HTTP request and return response
        data in dict format.
        """
        res_text = requests.get(self.mirror_url, timeout=10).text
        return self._build_arch_dict(res_text.splitlines())


    def _build_arch_dict(self, data):
        """
        This function creates a dictionary of arch-related
        file information from api data array
        """
        data_dict = {}
        for row in data:
            if re.search(r"Contents-.*\.gz",row):
                file_name = row[row.rfind("Contents-"): row.rfind(".gz")+3]
                arch = file_name[file_name.rfind("-")+1: file_name.find(".gz")]
                data_dict = self._update_data_dic(arch, file_name, data_dict)
        return data_dict

    def _update_data_dic(                  #pylint: disable=no-self-use
            self, arch, info, data_dict):
        """
        This function starts creating dictionary data by arch
        """
        if arch not in data_dict:
            data_dict[arch] = {}
        if re.search("Contents-udeb",info):
            data_dict[arch]['udeb_file'] = info
        else:
            data_dict[arch]['file_name'] = info
        return data_dict

    def _get_arch_data(self, arch):
        """
        make api call to download contents data associated with arch
        """
        url = (self.mirror_url +
               self.archs_dict[arch]['file_name'])
        return gzip.open(BytesIO(requests.get(url, timeout=10).content), 'rt', encoding='UTF-8')

    def _extract_file_and_package(self, line):  #pylint: disable=no-self-use
        """
        this function returns file name and package name
        """
        split_colomns = line.split()
        if len(split_colomns) == 2:
            return split_colomns[0], split_colomns[1].split("/")[-1]
        if len(split_colomns) > 2:
            return ' '.join(split_colomns[:-1]), split_colomns[-1].split("/")[-1]
        return False, False

    def _create_package_counts(
            self, data):
        """
        this function builds a package-count dictionary and
        sorts dict by package count number
        """
        package_dict = {}
        for line in data.readlines():
            file_name, package_name = self._extract_file_and_package(line)
            if file_name:
                if package_name not in package_dict:
                    package_dict[package_name] = 1
                else:
                    package_dict[package_name] += 1
        return sorted(
            package_dict.items(), key=lambda x: x[1], reverse=True)

#  Main func declaration is to avoid being executed when this module is
#  imported by another on top level
if __name__ == "__main__":
    stats_loader = ArchPackageStats()
    package_list = stats_loader.get_stats(sys.argv[1])
    dash_line = '-' * 110  # pylint: disable=invalid-name
    print(dash_line)
    print(f"{'Id':<20s}{'Package Name':<55s}{'Number':>35s}")
    print(dash_line)
    for i, package in enumerate(package_list):
        idx = f"{i+1}."
        print(f"{idx:<20s}{package[0]:<55s}{str(package[1]):>35s}")
