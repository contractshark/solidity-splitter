import unittest
import urllib.request
from splitter.splitter import prepare_etherscan_request


class TestPrepareEtherscanRequest(unittest.TestCase):
    def setUp(self):
        self.address = "0x0000000000000000000000000000000000001234"
        self.base_url = "https://api.etherscan.io/api"
    
    def test_returns_request_object(self):
        self.assertEqual(
            type(prepare_etherscan_request(self.address)),
            urllib.request.Request
        )
    
    def test_request_has_custom_user_agent_header(self):
        user_agent_header_name = "User-agent"
        
        r = prepare_etherscan_request(self.address)

        self.assertTrue(r.has_header(user_agent_header_name))
        self.assertNotIn(
            "Python-urllib",
            r.get_header(user_agent_header_name)
        )

    def test_address_is_set_in_url_query_params(self):
        params = {
            "module": "contract",
            "action": "getsourcecode",
            "address": self.address
        }
        
        r = prepare_etherscan_request(self.address)
        
        self.assertEqual(
            r.full_url,
            f"{self.base_url}?{urllib.parse.urlencode(params)}"
        )
