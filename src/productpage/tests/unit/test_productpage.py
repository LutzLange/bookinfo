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
        """ Check that non-trace headers are forwarded correctly """
        product_id = 0
        # Register mock for the reviews endpoint
        m.get("http://reviews:9080/reviews/%d" % product_id, text='{}')

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

        # Verify headers on the outgoing request using request_history
        self.assertEqual(1, len(m.request_history))
        outgoing_headers = m.request_history[0].headers

        # Non-trace headers should be forwarded exactly
        self.assertEqual(outgoing_headers.get('x-request-id'), '34eeb41d-d267-9e49-8b84-dde403fc5b72')
        self.assertEqual(outgoing_headers.get('sw8'), '40c7fdf104e3de67')

        # Trace context is handled by OpenTelemetry instrumentation which creates child spans.
        # The trace ID should be preserved but span ID will be different (child span).
        # OpenTelemetry may inject either B3 or W3C TraceContext headers depending on the
        # propagator configuration. We just verify some form of trace context exists.
        has_trace_context = (
            outgoing_headers.get('x-b3-traceid') is not None or
            outgoing_headers.get('traceparent') is not None
        )
        self.assertTrue(has_trace_context, "Expected trace context headers to be present")

    @requests_mock.Mocker()
    def test_header_propagation_ratings(self, m):
        """ Check that non-trace headers are forwarded correctly """
        product_id = 0
        # Register mock for the ratings endpoint
        m.get("http://ratings:9080/ratings/%d" % product_id, text='{}')

        uri = "/api/v1/products/%d/ratings" % product_id
        headers = {
            'x-request-id': '34eeb41d-d267-9e49-8b84-dde403fc5b73',
            'x-b3-traceid': '80f198ee56343ba864fe8b2a57d3eff7',
            'x-b3-spanid': 'e457b5a2e4d86bd1',
            'x-b3-sampled': '1',
            'sw8': '40c7fdf104e3de67'
        }
        actual = self.app.get(uri, headers=headers)
        self.assertEqual(200, actual.status_code)

        # Verify headers on the outgoing request using request_history
        self.assertEqual(1, len(m.request_history))
        outgoing_headers = m.request_history[0].headers

        # Non-trace headers should be forwarded exactly
        self.assertEqual(outgoing_headers.get('x-request-id'), '34eeb41d-d267-9e49-8b84-dde403fc5b73')
        self.assertEqual(outgoing_headers.get('sw8'), '40c7fdf104e3de67')

        # Trace context is handled by OpenTelemetry instrumentation which creates child spans.
        # The trace ID should be preserved but span ID will be different (child span).
        # OpenTelemetry may inject either B3 or W3C TraceContext headers depending on the
        # propagator configuration. We just verify some form of trace context exists.
        has_trace_context = (
            outgoing_headers.get('x-b3-traceid') is not None or
            outgoing_headers.get('traceparent') is not None
        )
        self.assertTrue(has_trace_context, "Expected trace context headers to be present")
