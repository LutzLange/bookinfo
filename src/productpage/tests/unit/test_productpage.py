#
# Copyright 2018 Istio Authors
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# Run from the top level productpage directory with:
#
# pip install -r test-requirements.txt
# python -m unittest discover tests/unit

import unittest

import requests_mock

import productpage


class ApplianceTest(unittest.TestCase):

    def setUp(self):
        self.app = productpage.app.test_client()

    @requests_mock.Mocker()
    def test_header_propagation_reviews(self, m):
        """ Check that non-trace headers and trace context are forwarded correctly """
        product_id = 0
        # Register mock - we check specific non-trace headers and that trace
        # context exists (trace ID preserved, span ID may change as child spans are created)
        def check_headers(request):
            # Non-trace headers should be forwarded exactly
            self.assertEqual(request.headers.get('x-request-id'), '34eeb41d-d267-9e49-8b84-dde403fc5b72')
            self.assertEqual(request.headers.get('sw8'), '40c7fdf104e3de67')
            # Trace ID should be preserved (same trace)
            self.assertEqual(request.headers.get('x-b3-traceid'), '80f198ee56343ba864fe8b2a57d3eff7')
            # Span ID may be different (child span) but should exist
            self.assertIsNotNone(request.headers.get('x-b3-spanid'))
            return True

        m.get("http://reviews:9080/reviews/%d" % product_id, text='{}',
              additional_matcher=check_headers)

        uri = "/api/v1/products/%d/reviews" % product_id
        headers = {
            'x-request-id': '34eeb41d-d267-9e49-8b84-dde403fc5b72',
            'x-b3-traceid': '80f198ee56343ba864fe8b2a57d3eff7',
            'x-b3-spanid': 'e457b5a2e4d86bd1',
            'x-b3-sampled': '1',
            'sw8': '40c7fdf104e3de67'
        }
        actual = self.app.get(uri, headers=headers)
        self.assertEqual(200, actual.status_code)

    @requests_mock.Mocker()
    def test_header_propagation_ratings(self, m):
        """ Check that non-trace headers and trace context are forwarded correctly """
        product_id = 0
        # Register mock - we check specific non-trace headers and that trace
        # context exists (trace ID preserved, span ID may change as child spans are created)
        def check_headers(request):
            # Non-trace headers should be forwarded exactly
            self.assertEqual(request.headers.get('x-request-id'), '34eeb41d-d267-9e49-8b84-dde403fc5b73')
            self.assertEqual(request.headers.get('sw8'), '40c7fdf104e3de67')
            # Trace ID should be preserved (same trace)
            self.assertEqual(request.headers.get('x-b3-traceid'), '80f198ee56343ba864fe8b2a57d3eff7')
            # Span ID may be different (child span) but should exist
            self.assertIsNotNone(request.headers.get('x-b3-spanid'))
            return True

        m.get("http://ratings:9080/ratings/%d" % product_id, text='{}',
              additional_matcher=check_headers)

        uri = "/api/v1/products/%d/ratings" % product_id
        headers = {
            'x-request-id': '34eeb41d-d267-9e49-8b84-dde403fc5b73',
            'x-b3-traceid': '80f198ee56343ba864fe8b2a57d3eff7',
            'x-b3-spanid': 'e457b5a2e4d86bd1',
            'x-b3-sampled': '1',
            'sw8': '40c7fdf104e3de67'
        }
        actual = self.app.get(uri, headers=headers)
        print(actual.data)
        self.assertEqual(200, actual.status_code)
