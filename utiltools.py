import csv
import json
from csv import DictReader
import requests
import os
import gzip
from zipfile import ZipFile
import xml.etree.ElementTree as ET


class UtilTools(object):

    def __init__(self):
        self.BUCKET = 'data_bucket/'

    def _write_data(self,filepath, data):
        """Private method to write an data object to the DATA Bucket location

         Args:
            filepath (str): location of file on s3
            data : object from requests library containing parsed data

         """
        with open(self.BUCKET + os.path.basename(filepath), 'wb') as f:
            f.write(data)


        return self.BUCKET + os.path.basename(filepath)

    def download_file(self, url):
        """
        Method that downlaods the a file from a url that is based to it.
        1 - uses request to get the contents from s3 and saves to Data Bucket folder
        2 - if file extension of the file is gz or zip additional step to uncompress file
        3 - returns location of newly created file

        Args:
            url (str): location of file on S3 bucket
        """
        filename , file_extension = os.path.splitext(url)
        r = requests.get(url, allow_redirects=True)
        open(self.BUCKET+os.path.basename(url), 'wb').write(r.content)

        if file_extension  == '.gz':
            print('gz zipped')
            filedata = gzip.open(self.BUCKET+os.path.basename(url)).read()
            self._write_data(filename, filedata)
            return self.BUCKET + os.path.basename(url)


        elif file_extension == '.zip':
            print('zip zipped')
            with ZipFile(self.BUCKET+os.path.basename(url)) as zp:

                self._write_data(filename, zp.read('products.xml'))
                return self.BUCKET+os.path.basename(url)
        else:
            return self.BUCKET + os.path.basename(url)

    @staticmethod
    def csv_reader(file_location):
        """
        1 - open products csv from data_bucket folder
        2 - carry out tranformation on price and stock columns
        3 - Append to a list of dicts
        4 - return a list object containing dicts


        """
        new_dict = []
        with open(file_location, newline='') as csvfile:
            data_t: DictReader = csv.DictReader(csvfile, delimiter=',', quotechar='"', skipinitialspace=True)

            for row in data_t:
                row['source'] = 'csv'

                new_dict.append(dict(row))

            return new_dict

    @staticmethod
    def json_reader(filelocation):
        """
        json reader hardcoded to look for products.json file and return a dict object

        1 - read json file from data_bucket folder
        2 - carry out manipulation on columns
        3 - return Dict object

        """
        json_data = open(filelocation).read()
        data = json.loads(json_data)
        for row in data:
            row['source'] = 'json'

        return data

    @staticmethod
    def xml_reader(file_location):
        """"
                1 - open products XML product from data_bucket folder and parse
                2 - get set of elements found in xml object
                3 - loop through object and append to a dict
                4 - carry out transformation on price and available fields
                5 - append dict to a list
                6 - return list of dicts

        """

        tree = ET.parse(file_location)
        root = tree.getroot()
        elements = set(elem.tag for elem in root.iter())

        data_list = []
        i = 0
        while i < len(root):
            row_dict = {}
            for elem in elements:
                for col in root[i].iter(elem):
                    row_dict[elem] = str(col.text) or ''

            row_dict['xml'] = 'xml'

            data_list.append(row_dict)

            i += 1

        return data_list
