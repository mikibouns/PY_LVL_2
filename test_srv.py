import pytest


from srv import Srv

account_name_from_list = ['igor', 'vasia', 'elena']
account_name_out_of_list = ['123', 'galia', 'seva', 'sasha']

passwd_409 = ['hjfdsklfa', '45658456', 4562315]
passwd_200 = ['12345678']

users_list = {
              'igor': {'passwd': '12345678',
                       'status': 'authorized',
                       'state': 'offline'},
              'maria': {'status': 'unauthorized',
                        'state': 'online'},
              'vasia': {'passwd': '12345678',
                        'status': 'authorized',
                        'state': 'offline'},
              'elena': {'passwd': '12345678',
                        'status': 'authorized',
                        'state': 'online'}
}

presence_msg = {'action': 'presence',
                'type': 'status',
                'user': {
                    'account_name': '',
                    'status': 'online'}
                }

authenticate_msg = {'action': 'authenticate',
                    'user': {'account_name': '',
                             'password': ''}
                    }


@pytest.fixture()
def srv_fixture(request):
    print('setup_fixture')
    srv = Srv()
    def resource_teardpwn():
        print('teardown_fixture')
    request.addfinalizer(resource_teardpwn)
    return srv


class TestSrv:
    @pytest.mark.parametrize('account_name', account_name_out_of_list)
    def test_check_auth_data_presence_msg_successful(self, srv_fixture, account_name):
        presence_msg['user']['account_name'] = account_name
        assert srv_fixture.check_auth_data(presence_msg) == {'response': 200, 'alert': 'OK'}


    @pytest.mark.parametrize('account_name', account_name_from_list)
    @pytest.mark.parametrize('passwd', passwd_200)
    def test_check_auth_data_authenticate_msg_successful(self, srv_fixture, account_name, passwd):
        authenticate_msg['user']['account_name'] = account_name
        authenticate_msg['user']['password'] = passwd
        assert srv_fixture.check_auth_data(authenticate_msg) == {'response': 200, 'alert': 'OK'}


    @pytest.mark.parametrize('account_name', account_name_from_list)
    def test_check_auth_data_presence_msg_error(self, srv_fixture, account_name):
        presence_msg['user']['account_name'] = account_name
        assert srv_fixture.check_auth_data(presence_msg) == {'response': 409,
                                                             'error': 'Someone​ is​ already​ connected​ with​ the​ given​ user​ name'}


    @pytest.mark.parametrize('account_name', account_name_out_of_list)
    @pytest.mark.parametrize('passwd', passwd_409 + passwd_200)
    def test_check_auth_data_authenticate_msg_error1(self, srv_fixture, account_name, passwd):
        authenticate_msg['user']['account_name'] = account_name
        authenticate_msg['user']['password'] = passwd
        assert srv_fixture.check_auth_data(authenticate_msg) == {'response': 402,
                                                                 'error': 'incorrect login or password'}

    @pytest.mark.parametrize('account_name', account_name_from_list)
    @pytest.mark.parametrize('passwd', passwd_409)
    def test_check_auth_data_authenticate_msg_error2(self, srv_fixture, account_name, passwd):
        authenticate_msg['user']['account_name'] = account_name
        authenticate_msg['user']['password'] = passwd
        assert srv_fixture.check_auth_data(authenticate_msg) == {'response': 402,
                                                                 'error': 'incorrect login or password'}

    def test_disabling_user(self, srv_fixture):
        assert srv_fixture.disabling_user({'action': 'quit', 'account_name': 'user'}) == {'action': 'quit'}


if __name__ == '__main__':
    pass