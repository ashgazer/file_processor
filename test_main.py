import pytest

from main import product_tool




# from load_exmls import fix_price, fix_stock


@pytest.mark.parametrize('data, result',[


('4', '4.00')
,('5','5.00')
,('6.0','6.00')
,('7.','7.00')
 ,('8.00', '8.00')


])
def test_fix_price(data, result):
    assert result == product_tool.fix_price(data)



@pytest.mark.parametrize('data,result', [



    ('y','1'),
    ('n','0'),

])
def test_fix_stock(data,result):
    assert result == product_tool.fix_stock(data)