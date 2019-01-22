import unittest
import argparse
from splitter import get_args_parser


class TestGetArgsParser(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser = get_args_parser()


    def test_returns_parser_object(self):
        self.assertIsInstance(self.parser, argparse.ArgumentParser)


    def test_parser_has_one_mutually_exclusive_group(self):
        parser_groups = self.parser._mutually_exclusive_groups
        self.assertEqual(len(parser_groups), 1)
    

    def test_parser_mutually_exclusive_group_requires_one_argument(self):
        parser_groups = self.parser._mutually_exclusive_groups
        self.assertTrue(parser_groups[0].required)


    def test_parser_defines_address_string_argument(self):
        actions_dict = self.parser._option_string_actions
        self.assertIn("-a", actions_dict)
        self.assertListEqual(actions_dict["-a"].option_strings, ["-a", "--address"])
        self.assertEqual(str, actions_dict["-a"].type)


    def test_parser_defines_address_argument_help_description(self):
        actions_dict = self.parser._option_string_actions
        self.assertEqual(
            actions_dict["-a"].help,
            "Address of the contract (source code must be verified in Etherscan)"
        )


    def test_parser_defaults_address_argument_to_none(self):
        actions_dict = self.parser._option_string_actions
        self.assertIsNone(actions_dict["-a"].default)


    def test_parser_defines_file_string_argument(self):
        actions_dict = self.parser._option_string_actions
        self.assertIn("-f", actions_dict)
        self.assertListEqual(actions_dict["-f"].option_strings, ["-f", "--file"])
        self.assertEqual(str, actions_dict["-f"].type)


    def test_parser_defines_file_argument_help_description(self):
        actions_dict = self.parser._option_string_actions
        self.assertEqual(
            actions_dict["-f"].help,
            "Solidity file containing several contracts to split"
        )


    def test_parser_defaults_file_argument_to_none(self):
        actions_dict = self.parser._option_string_actions
        self.assertIsNone(actions_dict["-f"].default)
