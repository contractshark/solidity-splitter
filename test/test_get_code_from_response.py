import unittest
import json
from splitter import get_code_from_response


class TestGetCodeFromResponse(unittest.TestCase):
    def setUp(self):
        self.expected_code = "pragma solidity ^0.4.25; contract Test {{}}"
        self.success_response_string = json.dumps({
            "status": 1,
            "result": [{"SourceCode": f"{self.expected_code}"}]
        })
        self.failure_response_string = json.dumps({
            "status": 0,
            "result": [{"SourceCode": ""}]
        })
    
    def test_extracts_source(self):
        code = get_code_from_response(self.success_response_string)
        self.assertEqual(code, self.expected_code)

    def test_raises_exception_when_code_not_found(self):
        self.assertRaises(
            Exception,
            get_code_from_response,
            self.failure_response_string
        )
