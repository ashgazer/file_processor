import pytest

from ProductFeed import ProductFeeds


@pytest.mark.parametrize('data, result',[


('4', '4.00')
, ('5','5.00')
, ('6.0','6.00')
, ('7.','7.00')
, ('8.00', '8.00')


])
def test_fix_price(data, result):
    assert result == ProductFeeds.fix_price(data)



@pytest.mark.parametrize('data,result', [



    ('y', '1'),
    ('n', '0'),

])
def test_fix_stock(data, result):
    assert result == ProductFeeds.fix_stock(data)


@pytest.mark.parametrize('data,result', [

    (
  , [{
    "id": "c5bd1c1bc2da4f8d",
    "name": "amnesic",
    "brand": "tetriodide",
    "retailer": "bagonet",
    "price": 9.19,
    "in_stock": "y"
  }])

])

def test_json_reader(data,result):
    assert result == ProductFeeds.json_reader(data)


# from io import StringIO
#
# in_mem_csv = StringIO("""Id, Name, Brand, Retailer, Price, InStock, source
# "5860865", "deflorescence", "balsamroot", "redecline", "320", "n", "csv"
#  """)
#
#
# @pytest.mark.parametrize('data, result', [
#     (in_mem_csv, { 'Id' : '5860865'
#                    ,'Name' : 'deflorescence'
#                    , 'Brand' : 'balsamroot'
#                    , 'Retailer' : 'redecline'
#                    , 'Price' : '320.00'
#                    , 'InStock' : '0'
#                    , 'source' : 'csv'
#
#
#
#
#     } )
#
#
# ])
#
# def test_csv(data, result):
#     assert result == ProductFeeds.csv_reader(data)