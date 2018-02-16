import pytest
import random
import json

import secondary_func as sf


class TestCheckIP:
    @pytest.mark.parametrize('addr', ['127.0.0.1', '192.168.100.2', '10.0.0.3'])
    def test_check_ip_successful(self, addr):
        assert sf._check_ip(addr)

    @pytest.mark.parametrize('addr', ['1254.0.0.123', 'slovo', '152.0.123.8tyu'])
    def test_check_ip_error(self, addr):
        assert sf._check_ip(addr) == False


class TestConvertData:
    bytes_data = [(json.dumps({i: random.randint(1, 20)})).encode('utf-8') for i in range(10)]
    json_data = [json.loads(i.decode('utf-8')) for i in bytes_data]
    error_data = ['str', 1234, ('tuple', ), ['list',]]

    @pytest.mark.parametrize('j_data', json_data)
    def test_convert_j_data_successful(self, j_data):
        assert sf._convert_data(j_data) == json.dumps(j_data).encode('utf-8')

    @pytest.mark.parametrize('b_data', bytes_data)
    def test_convert_b_data_successful(self, b_data):
        assert sf._convert_data(b_data) == json.loads(b_data.decode('utf-8'))

    @pytest.mark.parametrize('e_data', error_data)
    def test_convert_data_error(self, e_data):
        assert sf._convert_data(e_data) == None