import pytest

from client import Client


class TestClient:
    def setup(self):
        self.user = Client()
        self.user._send_message = self.sub_send_message
        self.user.account_name = 'Vasia'
        self.user.room = 'room'
        self.user.to_user = 'Igor'

    def sub_send_message(self, data):
        message = 'Hello Vasia!'
        return message

    def test_user_to_user(self):
        assert self.user.user_to_user() == {'action': 'msg',
                                            'to': 'Igor',
                                            'from': 'Vasia',
                                            'encoding': 'utf-8',
                                            'message': 'Hello Vasia!'}

    def test_user_to_chat(self):
        assert self.user.user_to_chat() == {'action': 'msg',
                                            'to': '#room',
                                            'from': 'Vasia',
                                            'encoding': 'utf-8',
                                            'message': 'Hello Vasia!'}

    # def test_join_chat(self):
    #     assert self.user.join_chat() == {'action': 'join',
    #                                      'room': '#{}'.format(self.user.room)}

    def test_leave_chat(self):
        assert self.user.leave_chat() == {'action': 'leave',
                                          'room': '#{}'.format(self.user.room)}