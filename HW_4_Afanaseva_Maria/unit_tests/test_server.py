import unittest
import sys
import os
sys.path.append(os.path.join(os.getcwd(), '..'))
from server import get_addr_port, valid_client_msg
from common.variables import *


class TestServer(unittest.TestCase):
    def setUp(self):
        self.arg = [sys.argv[0]]

    def test_get_addr_port(self):
        sys.argv = self.arg
        self.assertEqual(get_addr_port(), ('', 7777))

    def test_get_addr_port_args(self):
        sys.argv = self.arg
        args = ['-p', '8542', '-a', '78.12.12.45', ]
        for i in args:
            sys.argv.append(i)
        # print(sys.argv)
        self.assertEqual(get_addr_port(), ('78.12.12.45', 8542))

    def test_get_addr_port_wrong_ip(self):
        sys.argv = self.arg
        args = ['-p', '8542', '-a', '78.12.12.454', ]
        for i in args:
            sys.argv.append(i)
        # print(sys.argv)
        self.assertRaises(SystemExit, get_addr_port)

    def test_get_addr_port_wrong_port(self):
        sys.argv = self.arg
        args = ['-p', '88', '-a', '127.0.0.0', ]
        for i in args:
            sys.argv.append(i)
        # print(sys.argv)
        self.assertRaises(SystemExit, get_addr_port)

    def test_valid_client_msg_200(self):
        self.assertEqual(valid_client_msg({ACTION: PRESENCE, TIME: 1.1, USER: {ACCOUNT_NAME:'Guest'}}), {RESPONSE: 200})

    def test_valid_client_msg_400(self):
        self.assertEqual(valid_client_msg(
            {ACTION: AUTHENTICATE, TIME: 1.1, USER: {ACCOUNT_NAME:'Maria'}}),
            {RESPONSE: 400, ERROR: 'Bad Request'}
        )

    def test_valid_client_msg_wrong_msg(self):
        self.assertEqual(valid_client_msg(
            {ACTION: PRESENCE, TIME: 1.1}),
            {RESPONSE: 400, ERROR: 'Bad Request'}
        )


if __name__ == '__main__':
    unittest.main()
