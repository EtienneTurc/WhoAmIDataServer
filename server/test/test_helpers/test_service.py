import unittest
from unittest.mock import Mock
import json

from helpers.service import dispatch, is_callback
from test.utils import call_counter


@call_counter
@is_callback(["message1"])
def mock_callback_1(payload):
    return 'callback_1'


@call_counter
@is_callback(["message1", "message2"])
def mock_callback_2(payload):
    return 'callback_2'


class TestService(unittest.TestCase):

    def test_dispatch(self):
        callbacks = [mock_callback_1, mock_callback_2]
        mock_message = Mock()
        calls_mock_callback_1 = mock_callback_1.calls
        calls_mock_callback_2 = mock_callback_2.calls
        mock_message.topic = "message1"
        mock_message.payload = json.dumps({"token": "token"})
        dispatch(mock_message, callbacks)
        self.assertEqual(mock_callback_1.calls, calls_mock_callback_1 + 1)
        self.assertEqual(mock_callback_2.calls, calls_mock_callback_2 + 1)


if __name__ == '__main__':
    unittest.main()
