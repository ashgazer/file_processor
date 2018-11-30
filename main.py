import csv
import json
import requests
import os
import gzip
from zipfile import ZipFile
import xml.etree.ElementTree as ET






class product_tool:

    def __init__(self):
        self.files = ('https://s3-eu-west-1.amazonaws.com/pricesearcher-code-tests/python-software-developer/products.csv.gz' \
                 ,'https://s3-eu-west-1.amazonaws.com/pricesearcher-code-tests/python-software-developer/products.json'
                 ,'https://s3-eu-west-1.amazonaws.com/pricesearcher-code-tests/python-software-developer/products.xml.zip')


        self.BUCKET = 'data_bucket/'




    def _write_data(self,filepath, data):
        """Private method to write an data object to the DATA Bucket location

         Args:
            filepath (str): location of file on s3
            data : object from requests library containing parsed data

         """
        with open(self.BUCKET + os.path.basename(filepath), 'wb') as f:
            f.write(data)




    def download_file(self):
        """
        Method that downlaods the 3 product feed files
        1 - loops through file locations in the self.files tupple
        2 - uses request to get the contents from s3 and saves to Data Bucket folder
        3 - if file extension of the file is gz or zip additional step to uncompress file


        """
        #TODO: maybe take out loop and put into main
        for file in self.files:
            filename , file_extension = os.path.splitext(file)
            r = requests.get(file, allow_redirects=True)
            open(self.BUCKET+os.path.basename(file), 'wb').write(r.content)

            if file_extension  == '.gz':
                print('gz zipped')
                filedata = gzip.open(self.BUCKET+os.path.basename(file)).read()
                self._write_data(filename, filedata)

            elif file_extension == '.zip':
                print('zip zipped')
                with ZipFile(self.BUCKET+os.path.basename(file)) as zp:

                    self._write_data(filename, zp.read('products.xml'))


    def json_reader(self):
        """
        json reader hardcoded to look for products.json file and return a dict object

        1 - read json file from data_bucket folder
        2 - carry out manipulation on columns
        3 - return Dict object

        """
        json_data = open('data_bucket/products.json').read()
        data = json.loads(json_data)
        for row in data:
            row['source'] = 'json'
            row['price'] = self.fix_price(row.get('price', 0))
            row['in_stock'] = self.fix_stock(row.get('in_stock', 0))

            if row.get('brand', None) is None:
                row['brand'] = ' '

            if row.get('retailer', None) is None:
                row['retailer'] = ' '


        return data

    def csv_reader(self):
        """
        1 - open products csv from data_bucket folder
        2 - carry out tranformation on price and stock columns
        3 - Append to a list of dicts
        4 - return a list object containing dicts


        """
        new_dict = []
        with open('data_bucket/products.csv', newline='') as csvfile:
            data_t = csv.DictReader(csvfile, delimiter=',', quotechar='"', skipinitialspace=True)

            for row in data_t:
                row['source'] = 'csv'
                row['Price'] = self.fix_price(row['Price'])
                row['InStock'] = self.fix_stock(row['InStock'])

                new_dict.append(dict(row))

            return new_dict

    def xml_reader(self):
        """"
                1 - open products XML product from data_bucket folder and parse
                2 - get set of elements found in xml object
                3 - loop through object and append to a dict
                4 - carry out transformation on price and available fields
                5 - append dict to a list
                6 - return list of dicts

        """

        tree = ET.parse('data_bucket/products.xml')
        root = tree.getroot()
        elements = set(elem.tag for elem in root.iter())

        data_list = []
        i = 0
        while i < len(root):
            row_dict = {}
            for elem in elements:
                for col in root[i].iter(elem):
                    row_dict[elem] = str(col.text) or ''

            row_dict['latest_price'] = self.fix_price(row_dict['latest_price'])
            row_dict['available'] = self.fix_stock(row_dict['available'])

            data_list.append({'id': row_dict['id']
                             , 'name': row_dict['name']
                             , 'brand': row_dict['brand']
                             , 'retailer': row_dict['retailer']
                             , 'latest_price': row_dict['latest_price']
                             , 'available': row_dict['available']
                             , 'source': 'xml'
                             })


            i += 1

        return data_list



    @staticmethod
    def fix_price(val):
        """
        the method evaluates the data passed in and returns a numeric value
        to two decimal places.

         Args:
            val: this is the price value passed into the function


        """
        if val == False:
            return ''
        elif val == True:
            return ''
        elif val == '':
            return '0.00'
        if hasattr(val,'find') == False:
            return ''

        start = val.find('.')
        if start == -1:
            val += '.00'
            return val
        if len(val[start + 1:]) == 1:
            val += '0'
            return val
        elif len(val[start + 1:]) == 0:
            val += '00'
            return val
        else:
            return val

    @staticmethod
    def fix_stock(val):
        """
        the method evaluates the data passed in and returns a string value
        either 1 to indication true and 0 for false that the item is in stock

         Args:
            val: this is the indication if an item is in stock


        """
        if val == False:
            return '0'
        elif val == True:
            return '1'

        val = val[0].lower()
        if val == 'y':
            return '1'
        if val == 'n':
            return '0'
        else:
            return ''


    def the_writer(self,data, FILE = 'final_product_feed.csv'):

        from pathlib import Path

        if not Path(FILE).is_file():
            with open(FILE,'w') as f:
                f.writelines('Id, Name, Brand, Retailer, Price, InStock, Source \n')
        with open(FILE,'a') as f:
            for row in data:
                f.writelines(', '.join(row.values()) + '\n')



    def transformer(self, data):
        if data['source'] == 'json':
            for row in data:
                row['price'] = self.fix_price(row.get('price', 0))
                row['in_stock'] = self.fix_stock(row.get('in_stock', 0))

                if row.get('brand', None) is None:
                    row['brand'] = ' '

                if row.get('retailer', None) is None:
                    row['retailer'] = ' '


            transformed_data = data
        elif data['source'] == 'xml':
            transformed_data = []

            for row in data:
                row['latest_price'] = self.fix_price(row['latest_price'])
                row['available'] = self.fix_stock(row['available'])

                transformed_data.append({'id': row['id']
                                 , 'name': row['name']
                                 , 'brand': row['brand']
                                 , 'retailer': row['retailer']
                                 , 'latest_price': row['latest_price']
                                 , 'available': row['available']
                                 , 'source': 'xml'
                                 })

        elif data['source' == 'csv']:
            for row in data:
                row['Price'] = self.fix_price(row['Price'])
                row['InStock'] = self.fix_stock(row['InStock'])
            transformed_data = data


        return data


    def run(self):
        """
        Main execution method
        1 - downloads file
        2 - creates csv, xml , json objects
        3 - write data to final_product file


        :return:
        """
        self.download_file()
        csv_data = self.csv_reader()
        json_data = self.json_reader()
        xml_data = self.xml_reader()

        self.the_writer(csv_data)
        self.the_writer(json_data)
        self.the_writer(xml_data)



#
# data_feed = product_tool()
# data_feed.run()

