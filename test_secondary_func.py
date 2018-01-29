import pytest
import os
import random
import json

import secondary_func as sf


class TestCLclientOptions:
    def test_cl_client_options_successful(self):
        assert sf.cl_client_options([os.getcwd()]) == {'addr': '127.0.0.1', 'port': 7777}
        assert sf.cl_client_options([os.getcwd(), '192.0.1.12']) == {'addr': '192.0.1.12', 'port': 7777}
        assert sf.cl_client_options([os.getcwd(), '152.12.125.23', '8888']) == {'addr': '152.12.125.23', 'port': 8888}


    def test_cl_client_options_error(self):
        assert sf.cl_client_options([os.getcwd(), '15236.2456.fvf']) == ['!!!ip address is incorrect!!!']
        assert sf.cl_client_options([os.getcwd(), '192.16.3.15', '9999999999']) == [
            '!!!port is incorrect, maximum allowable value 65535!!!', ]
        assert sf.cl_client_options([os.getcwd(), '192.16.3.15', 'hjkfs]fds']) == [
            '!!!port is incorrect, the value must consist of digits!!!']
        assert sf.cl_client_options([os.getcwd(), '192.16.3.1t', '9999999999']) == [
            '!!!ip address is incorrect!!!',
            '!!!port is incorrect, maximum allowable value 65535!!!']
        assert sf.cl_client_options([os.getcwd(), '192.16.3.15.89', 'hjkfs]fds']) == [
            '!!!ip address is incorrect!!!',
            '!!!port is incorrect, the value must consist of digits!!!']


class TestCLsrvOptions:
    def test_cl_srv_options_successful(self):
        assert sf.cl_srv_options([os.getcwd()]) == {'addr': '0.0.0.0', 'port': 7777}
        assert sf.cl_srv_options([os.getcwd(), '192.0.1.12']) == {'addr': '0.0.0.0', 'port': 7777}
        assert sf.cl_srv_options([os.getcwd(), '-a', '152.12.125.23', '-p', '8888']) == {'addr': '152.12.125.23', 'port': 8888}


    def test_cl_srv_options_error(self):
        assert sf.cl_srv_options([os.getcwd(), '-a']) == ['!!!enter the ip address!!!']
        assert sf.cl_srv_options([os.getcwd(), '-a', '15236.2456.fvf']) == ['!!!ip address is incorrect!!!']
        assert sf.cl_srv_options([os.getcwd(), '-p']) == ['!!!enter the port!!!']
        assert sf.cl_srv_options([os.getcwd(), '-p', '15236.2456.fvf']) == [
            '!!!port is incorrect, the value must consist of digits!!!']
        assert sf.cl_srv_options([os.getcwd(), '-p', '152362456']) == [
            '!!!port is incorrect, maximum allowable value 65535!!!']

        assert sf.cl_srv_options([os.getcwd(), '-p', '15236cds2456dd', '-a']) == [
            '!!!port is incorrect, the value must consist of digits!!!',
            '!!!enter the ip address!!!']
        assert sf.cl_srv_options([os.getcwd(), '-p', '152362456', '-a']) == [
            '!!!port is incorrect, maximum allowable value 65535!!!',
            '!!!enter the ip address!!!']
        assert sf.cl_srv_options([os.getcwd(), '-p', '15236cds2456dd', '-a', '999999999fgdf']) == [
            '!!!port is incorrect, the value must consist of digits!!!',
            '!!!ip address is incorrect!!!']

        assert sf.cl_srv_options([os.getcwd(), '-a', '15236cds2456dd', '-p']) == [
            '!!!ip address is incorrect!!!',
            '!!!enter the port!!!']
        assert sf.cl_srv_options([os.getcwd(), '-a', '152362456', '-p', '999999999fgdf']) == [
            '!!!ip address is incorrect!!!',
            '!!!port is incorrect, the value must consist of digits!!!']
        assert sf.cl_srv_options([os.getcwd(), '-a', '15236cds2456dd', '-p', '999999999']) == [
            '!!!ip address is incorrect!!!',
            '!!!port is incorrect, maximum allowable value 65535!!!']

        assert sf.cl_srv_options([os.getcwd(), '-a', '-p']) == [
            '!!!ip address is incorrect!!!',
            '!!!enter the port!!!']
        assert sf.cl_srv_options([os.getcwd(), '-p', '-a']) == [
            '!!!port is incorrect, the value must consist of digits!!!',
            '!!!enter the ip address!!!']


class TestCheckIP:
    @pytest.mark.parametrize('addr', ['127.0.0.1', '192.168.100.2', '10.0.0.3'])
    def test_check_ip_successful(self, addr):
        assert sf.check_ip(addr)

    @pytest.mark.parametrize('addr', ['1254.0.0.123', 'slovo', '152.0.123.8tyu'])
    def test_check_ip_error(self, addr):
        assert sf.check_ip(addr) == False


class TestConvertData:
    bytes_data = [(json.dumps({i: random.randint(1, 20)})).encode('utf-8') for i in range(10)]
    json_data = [json.loads(i.decode('utf-8')) for i in bytes_data]
    error_data = ['str', 1234, ('tuple', ), ['list',]]

    @pytest.mark.parametrize('j_data', json_data)
    def test_convert_j_data_successful(self, j_data):
        assert sf.convert_data(j_data) == json.dumps(j_data).encode('utf-8')

    @pytest.mark.parametrize('b_data', bytes_data)
    def test_convert_b_data_successful(self, b_data):
        assert sf.convert_data(b_data) == json.loads(b_data.decode('utf-8'))

    @pytest.mark.parametrize('e_data', error_data)
    def test_convert_data_error(self, e_data):
        assert sf.convert_data(e_data) == None