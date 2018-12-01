from utiltools import *

class ProductFeeds(UtilTools):
    def __init__(self):
        self.files = ('https://s3-eu-west-1.amazonaws.com/pricesearcher-code-tests/python-software-developer/products.csv.gz' \
                 ,'https://s3-eu-west-1.amazonaws.com/pricesearcher-code-tests/python-software-developer/products.json'
                 ,'https://s3-eu-west-1.amazonaws.com/pricesearcher-code-tests/python-software-developer/products.xml.zip')

        super(ProductFeeds, self).__init__()


    def the_writer(self,data, FILE = 'final_product_feed.csv'):
        """
        Method writes the final product feed file as a csv
        1 - check if file already exists if not then create and add headers
        2 - Write data held in the object as lines in csv

        Args:
            data: data as an object usually a list of dicts
            FILE: defaults to final_product_feed.csv can ovewrite with value


        """

        from pathlib import Path

        if not Path(FILE).is_file():
            with open(FILE,'w') as f:
                f.writelines('Id, Name, Brand, Retailer, Price, InStock, Source \n')
        with open(FILE,'a') as f:
            for row in data:
                f.writelines(', '.join(row.values()) + '\n')

    def transformer(self, data):
        """ depending on data source transformations are applied to the data object

            Args:
                data: an iterable object of the product feed

        """

        transformed_data = ''
        if data[1]['source'] == 'json':
            for row in data:
                row['price'] = self.fix_price(row.get('price', 0))
                row['in_stock'] = self.fix_stock(row.get('in_stock', 0))

                if row.get('brand', None) is None:
                    row['brand'] = ' '

                if row.get('retailer', None) is None:
                    row['retailer'] = ' '


            transformed_data = data
        elif data[1]['source'] == 'xml':
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

        elif data[1]['source' == 'csv']:
            for row in data:
                for col in row:
                    if not isinstance(row[col], str):
                        row[col] = str(row[col])

                row['Price'] = self.fix_price(row['Price'])
                row['InStock'] = self.fix_stock(row['InStock'])


            transformed_data = data


        return transformed_data

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
        if val == 'y' or val == 't':
            return '1'
        if val == 'n' or val == 'f':
            return '0'
        else:
            return ''

    def run(self):
        """
        Main execution method
        1 - downloads file
        2 - creates csv, xml , json objects
        3 - apply product feed transformations
        4 - write data to final_product file


        """
        file_list = []
        for url in self.files:
            filename = self.download_file(url)
            file_list.append(filename)
            # file_list.append(self.BUCKET + os.path.basename(url))

        for file in file_list:
            filename , file_extension = os.path.splitext(file)
            file_extension = file_extension[1:]
            if file_extension == 'csv':
                csv_data = self.transformer(self.csv_reader)
                self.the_writer(csv_data)
            elif file_extension == 'json':
                json_data = self.transformer(self.json_reader(file))
                self.the_writer(json_data)
            elif file_extension == 'xml':
                xml_data = self.transformer(self.xml_reader(file))
                self.the_writer(xml_data)



