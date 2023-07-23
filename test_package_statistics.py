"""Unit Tests Module"""
import unittest
from io import BytesIO
import gzip
import requests
from package_statistics import ArchPackageStats

PACKAGE_LIST_SIZE = 10
TARGET_URL = "http://ftp.uk.debian.org/debian/dists/stable/main/"

class TestPackageStats(unittest.TestCase):
    """
    This class is used to test module package_statistics
    """
    def setUp(self):
        self.stats_loader = ArchPackageStats()

    def tearDown(self):
        self.stats_loader = None

    def test_get_all_avalible_archs(self):
        """
        This tests get_avalible_archs() function
        and detect an arch is available
        """
        all_archs = self.stats_loader.get_avalible_archs()
        self.assertTrue("i386" in all_archs)
        self.assertFalse("mipsel64" in all_archs)

    def test_send_invalid_arch(self):
        """This test checks invalid input."""
        with self.assertRaises(Exception) as ex:
            self.stats_loader.get_stats("test123")
        self.assertTrue(
            "test123 is not a valid arch in Debian mirror" in str(ex.exception))

    def test_get_stats_for_amd64(self):
        """
        This test checks return stats after calcutating top 10 packages
        """
        stats = self.stats_loader.get_stats("amd64")
        self.assertEqual(stats[0][0], "piglit")
        self.assertTrue(stats[0][1] > stats[1][1])
        self.assertFalse(stats[-1][1] > stats[-2][1])
        self.assertTrue(len(stats), PACKAGE_LIST_SIZE)

        # verify counts are consistent
        content = BytesIO(requests.get(TARGET_URL + "Contents-amd64.gz", timeout=10).content)
        data = gzip.open(content, 'rt')
        packages = []
        for line in data.readlines():
            packages.append(line.split()[-1].split("/")[-1])
        data.close()
        self.assertEqual(packages.count("piglit"), stats[0][1])

        # verify this is in the package
        content = BytesIO(requests.get(TARGET_URL + "binary-amd64/Packages.gz", timeout=10).content)
        data = gzip.open(content, 'rt')
        info = data.read()
        data.close()
        self.assertTrue("piglit" in info)

if __name__ == "__main__":
    unittest.main()
