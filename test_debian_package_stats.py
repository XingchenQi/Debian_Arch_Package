"""This module does blah blah."""
import unittest
from io import BytesIO
import gzip
import requests
from debian_package_stats import DebianPackageStats


class TestDebianPackageStats(unittest.TestCase):
    """This module does blah blah."""

    def setUp(self):
        self.stats = DebianPackageStats()
        self.mirror_url = "http://ftp.uk.debian.org/debian/dists/stable/main/"

    def tearDown(self):
        self.stats = None

    def test_get_all_avalible_archs(self):
        """This test avalible archs"""
        all_archs = self.stats.get_avalible_archs()
        self.assertTrue("amd64" in all_archs)
        self.assertTrue("arm64" in all_archs)
        self.assertTrue("armel" in all_archs)
        self.assertTrue("mips" in all_archs)

    def test_send_bad_arch(self):
        """This test checks if a bad arch is given."""
        with self.assertRaises(Exception) as context:
            self.stats.get_stats("bad")
        self.assertTrue(
            "bad not valid Debian package" in str(context.exception))

    def test_get_stats_for_amd64(self):
        """This test checks if a bad arch is given."""
        stats = self.stats.get_stats("amd64")
        self.assertEqual(stats[0][0], "fonts-cns11643-pixmaps")
        self.assertTrue(stats[0][1] > stats[1][1])
        self.assertTrue(stats[9][1] < stats[8][1])
        self.assertTrue(len(stats), 10)

        # verify this is infact a package
        url = self.mirror_url + "binary-amd64/Packages.gz"
        content = BytesIO(requests.get(url).content)
        data = gzip.open(content, 'rt')
        info = data.read()
        data.close()
        self.assertTrue(
            "Package: fonts-cns11643-pixmaps" in info)

        # verify count occurance is the same
        url = self.mirror_url + "Contents-amd64.gz"
        content = BytesIO(requests.get(url).content)
        data = gzip.open(content, 'rt')
        info = data.read()
        data.close()
        self.assertEqual(
            info.count(" fonts/fonts-cns11643-pixmaps"), stats[0][1])

    def test_get_stats_for_arm64(self):
        """This test checks if a bad arch is given."""
        stats = self.stats.get_stats("arm64")

        self.assertEqual(stats[0][0], "fonts-cns11643-pixmaps")
        self.assertTrue(stats[0][1] > stats[1][1])
        self.assertTrue(stats[9][1] < stats[8][1])
        self.assertTrue(len(stats), 10)

        # verify this is infact a package
        url = self.mirror_url + "binary-arm64/Packages.gz"
        content = BytesIO(requests.get(url).content)
        data = gzip.open(content, 'rt')
        info = data.read()
        data.close()
        self.assertTrue(
            "Package: fonts-cns11643-pixmaps" in info)

        # verify count occurance is the same
        url = self.mirror_url + "Contents-arm64.gz"
        content = BytesIO(requests.get(url).content)
        data = gzip.open(content, 'rt')
        info = data.read()
        data.close()
        self.assertEqual(
            info.count(" fonts/fonts-cns11643-pixmaps"), stats[0][1])

    def test_get_stats_for_mips4(self):
        """This test checks if a bad arch is given."""
        stats = self.stats.get_stats("mips")

        self.assertEqual(stats[0][0], "fonts-cns11643-pixmaps")
        self.assertTrue(stats[0][1] > stats[1][1])
        self.assertTrue(stats[9][1] < stats[8][1])
        self.assertTrue(len(stats), 10)

        # verify this is infact a package
        url = self.mirror_url + "binary-mips/Packages.gz"
        content = BytesIO(requests.get(url).content)
        data = gzip.open(content, 'rt')
        info = data.read()
        data.close()
        self.assertTrue(
            "Package: fonts-cns11643-pixmaps" in info)

        # verify count occurance is the same
        url = self.mirror_url + "Contents-mips.gz"
        content = BytesIO(requests.get(url).content)
        data = gzip.open(content, 'rt')
        info = data.read()
        data.close()
        self.assertEqual(
            info.count(" fonts/fonts-cns11643-pixmaps"), stats[0][1])


if __name__ == "__main__":
    unittest.main()
