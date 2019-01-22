import unittest
from unittest.mock import mock_open, patch
from splitter.helpers import load_contract_lines

class TestLoadContractLines(unittest.TestCase):    
    def test_raises_exception_when_file_not_found(self):
        self.assertRaises(
            FileNotFoundError,
            load_contract_lines,
            "SomeFakeFile.sol"
        )
    

    def test_raises_exception_when_filename_is_empty_string(self):
        self.assertRaises(
            FileNotFoundError,
            load_contract_lines,
            ""
        )

    def test_raises_exception_when_filename_is_not_string(self):
        self.assertRaises(
            FileNotFoundError,
            load_contract_lines,
            0
        )

    def test_returns_list_of_string_lines(self):
        pass
