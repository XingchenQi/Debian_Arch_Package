"""This module Alls you to run the CLI Package Statistics for Debian"""
from io import BytesIO
import gzip
import sys
import requests


class DebianPackageStats:
    """
    This class is used to get package and file name statistics for Debian
    """
    def __init__(self):
        self.mirror_url = "http://ftp.uk.debian.org/debian/dists/stable/main/"
        self.package_details = self._get_package_details()
        self.package_list = None

    # public
    def get_stats(self, arch):
        """
        This function gets the stats associated with a package.
        @param arch  is string of package ex. amd64
        @return list of top 10 packages and file counts
        """
        self._check_valid_package(arch)
        data = self._get_debian_package_data(arch)
        self.package_list = self._build_package_counts_json(data, arch)
        data.close()
        return self.package_list[:10]

    def get_package_list(self):
        """
        This function returns the pack list build
        with all packages and file counts
        @return
        """
        return self.package_list

    def get_avalible_archs(self):
        """
        This function returns a list of avalible packages
        """
        archs = []
        for key in self.package_details:
            archs.append(key)
        return archs

    # private
    def _check_valid_package(self, package):
        """
        check to see if package is valid
        """
        if package not in self.get_avalible_archs():
            raise Exception(
                "{} not valid Debian package".format(package))

    def _get_package_details(self):
        """
        This function gets debian information and returns
        data in json format.
        """
        data = self._get_package_details_data()
        return self._build_package_json(data)

    def _get_package_details_data(self):
        """
        This function makes api call to get debian information
        and returns it in arrray
        """
        res = requests.get(self.mirror_url)
        return res.text.split("\r\n")

    def _build_package_json(self, data):
        """
        This function creates json debian
        information from array of api data
        """
        filtered_data = []
        for row in data:
            if "Contents-" in row and ".gz" in row:
                filtered_data.append(row)
        return self.build_json_data_with_filtered_data(filtered_data)

    def build_json_data_with_filtered_data(self, filtered_data):
        """
        This function gathers information for builiding debian json data
        """
        data_info = {}
        for row in filtered_data:
            info = row[row.rfind("Contents-"): row.rfind(".gz")]
            arch = info[info.rfind("-")+1: len(info)]
            data_info = self.add_to_data_json(arch, info, data_info)
        return data_info

    def add_to_data_json(  # pylint: disable=no-self-use
            self, arch, info, data_info):
        """
        This function starts builiding debian json data
        """
        if arch not in data_info:
            data_info[arch] = {}
        if "Contents-udeb" in info:
            data_info[arch]['udeb_filename'] = info+".gz"
        else:
            data_info[arch]['fileName'] = info+".gz"
        return data_info

    def _get_debian_package_data(self, package):
        """
        make api call to get contents data associated with package
        """
        url = (self.mirror_url +
               self.package_details[package]['fileName'])
        content = BytesIO(requests.get(url).content)
        return gzip.open(content, 'rt')

    def _get_file_name_package(self, line):   # pylint: disable=no-self-use
        """
        this fumnction returns package and filename
        """
        info = line.split()
        if len(info) > 2:
            return info[:-1], info[-1].split("/")[-1]
        if len(info) == 2:
            return info[0],  info[1].split("/")[-1]
        return False, False

    def _get_add_value_from_filename(  # pylint: disable=no-self-use
            self, file_name):
        """
        this function determins how much to add
        to the package file count
        """
        add = 1
        if file_name == "EMPTY_PACKAGE":
            add = 0
        return add

    def _package_list_modification(   # pylint: disable=no-self-use
            self, add, arch, package_list):
        """
        this functions calculates the files per package
        """
        if arch not in package_list:
            package_list[arch] = add
        else:
            package_list[arch] += add
        return package_list

    def _build_package_counts_json(  # pylint: disable=no-self-use
            self, data, package):
        """
        this function builds and sorts json
        of packages and file counts
        """
        package_list = {}
        for line in data.readlines():
            file_name, package = self._get_file_name_package(line)
            add = self._get_add_value_from_filename(file_name)
            if file_name and add:
                package_list = self._package_list_modification(
                    add, package, package_list)
        return sorted(
            package_list.items(), key=lambda x: x[1], reverse=True)


if __name__ == "__main__":
    stats = DebianPackageStats()
    answer = stats.get_stats(sys.argv[1])
    i = -1
    dash = '-' * 60  # pylint: disable=invalid-name
    while i < len(answer):
        if i == -1:
            print(dash)
            print('{:<20s}{:<20s}{:>20s}'.format("#", "Package", "Count"))
            print(dash)
        else:
            print('{:<20s}{:<20s}{:>20s}'.format(
                "{}.".format(i+1),  answer[i][0],  str(answer[i][1])))
        i += 1
