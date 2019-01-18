import unittest
import os
from splitter import extract_contracts, load_contract_lines


class TestExtractContracts(unittest.TestCase):
    def join_lines(self, lines, with_pragma=False):
        if with_pragma:
            return "".join(lines)
        
        return "".join(lines[1:])
    

    @classmethod
    def load_test_contract(cls, filename):
        filepath = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'contracts',
            filename
        )
        return load_contract_lines(filepath)


    @classmethod
    def setUpClass(cls):
        cls.full_lines = cls.load_test_contract('FullContract.sol')


    def setUp(self):
        self.names = [
            "FirstContract",
            "SecondContract",
            "ThirdContract",
            "MyLibrary",
            "MyInterface"
        ]
        self.pragma_statement = "pragma solidity ^0.4.0;"  


    def test_returns_two_empty_lists_for_empty_input(self):
        names, contracts = extract_contracts([])
        self.assertListEqual(names, [])
        self.assertListEqual(contracts, [])


    def test_detects_contracts(self):
        first_contract_lines = self.load_test_contract('FirstContract.sol')
        second_contract_lines = self.load_test_contract('SecondContract.sol')
        third_contract_lines = self.load_test_contract('ThirdContract.sol')
        library_lines = self.load_test_contract('MyLibrary.sol')
        interface_lines = self.load_test_contract('MyInterface.sol')

        names, contracts = extract_contracts(self.full_lines)

        self.assertListEqual(names, self.names)
        self.assertListEqual(
            contracts,
            [
                self.join_lines(first_contract_lines, with_pragma=True),
                self.join_lines(second_contract_lines),
                self.join_lines(third_contract_lines),
                self.join_lines(library_lines),
                self.join_lines(interface_lines)
            ]
        )
