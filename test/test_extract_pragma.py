import unittest
from splitter import extract_pragma


class TestExtractPragma(unittest.TestCase):
    def setUp(self):
        self.expected_pragma = "pragma solidity 0.4.0;"
        self.test_data = [
            self.expected_pragma,
            "//pragma solidity 0.4.0;",
            "/*pragma solidity 0.4.0;*/",
            "pragma",
            "pragma solidity 0.4.0"    
        ]
    
    def test_finds_correct_pragma_statement(self):
        pragma_statement = extract_pragma(self.test_data)
        self.assertEqual(pragma_statement, self.expected_pragma)

    def test_deletes_pragma_statement_from_list_after_found(self):
        original_data = list(self.test_data)
        pragma_statement = extract_pragma(self.test_data)
        self.assertEqual(pragma_statement, self.expected_pragma)
        self.assertEqual(self.test_data, original_data[1:])

    def test_returns_empty_string_when_not_found(self):
        pragma_statement = extract_pragma(self.test_data[1:])
        self.assertEqual(pragma_statement, "")
    
