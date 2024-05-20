from functools import partial

from requests import HTTPError
from unittest import TestCase
from urllib3_mock import Responses

from poeg.libs import slevomat

responses = Responses(package='requests.packages.urllib3')
responses.add = partial(responses.add, method='GET', url='/api/vouchercheck',
                        content_type='application/json')


class SlevomatClientTests(TestCase):

    def setUp(self):
        self.c = slevomat.Client('asd')

    @responses.activate
    def test_one(self):
        responses.add(body="""{
                          "result": false,
                          "data": {},
                          "error": {
                            "code": 1204,
                            "message": "The order was not paid yet."
                          }
                        }""",
                      status=400)
        with self.assertRaises(HTTPError) as cm:
            self.c.check_voucher('123')
        e = cm.exception
        self.assertEqual(400, e.response.status_code)
        js = e.response.json()
        self.assertEqual(js['error']['code'], 1204)
        self.assertIn('result', js)
