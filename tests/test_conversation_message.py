import unittest
from datetime import datetime
from messagebird import ConversationClient

try:
    from unittest.mock import Mock
except ImportError:
    # mock was added to unittest in Python 3.3, but was an external library
    # before.
    from mock import Mock


class TestConversationMessage(unittest.TestCase):

    def test_conversation_list_messages(self):
        http_client = Mock()
        http_client.request.return_value = '{"count":1,"items":[{"id":"54445534","conversationId":"54345543543","channelId":"4535434354","type":"text","content":{"text":"Hello"},"direction":"sent","status":"delivered","createdDatetime":"2019-04-02T08:54:54.608157775Z","updatedDatetime":"2019-04-02T08:54:54.63910221Z"}],"limit":10,"offset":0,"totalCount":1}'

        msg = ConversationClient('', http_client).list_messages(54567)

        self.assertEqual(1, msg.count)
        self.assertEqual('54445534', msg.items[0].id)

        http_client.request.assert_called_once_with('conversations/54567/messages', 'GET', None)

    def test_create_message(self):
        http_client = Mock()
        http_client.request.return_value = '{"id":"id","conversationId":"conversation-id","channelId":"channel-id","type":"text","content":{"text":"Example Text Message"},"direction":"sent","status":"pending","createdDatetime":"2019-04-02T11:57:52.142641447Z","updatedDatetime":"2019-04-02T11:57:53.142641447Z"}'

        data = {
            'channelId':  1234,
            'type': 'text',
            'content': {
                'text': 'this is a message'
            },
        }

        msg = ConversationClient('', http_client).create_message('conversation-id', data)

        self.assertEqual(datetime(2019, 4, 2, 11, 57, 53), msg.updatedDatetime)
        self.assertEqual(datetime(2019, 4, 2, 11, 57, 52), msg.createdDatetime)

        http_client.request.assert_called_once_with('conversations/conversation-id/messages', 'POST', data)