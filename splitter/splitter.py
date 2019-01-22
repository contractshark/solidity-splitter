import re, sys, json
import urllib.request
import urllib.parse
from .helpers import load_contract_lines, get_args_parser


def extract_pragma(source_lines):
    """
    Takes a list of Solidity source code lines and looks for a pragma statement.
    When found, returns the statement, removing it from the list.
    Returns an empty string otherwise.
    """
    PRAGMA_REGEX = r"^\s*pragma\ssolidity\s+.*?\s*;"
    pragma_pattern = re.compile(PRAGMA_REGEX)

    pragma_statement = ""
    pragma_at = 0

    for n, line in enumerate(source_lines):
        match = re.match(pragma_pattern, line)
        if match:
            pragma_at = n
            pragma_statement = match.group(0)
            break
    
    if len(pragma_statement):
        del source_lines[pragma_at]

    return pragma_statement


def extract_contracts(source_lines):
    """
    Takes a list of Solidity source code lines and naively attempts to extract
    all different contracts/libraries/interfaces detected, including docstrings outside them.
    Returns two lists of strings, the first one containing the names of the contracts found,
    and the second one containing the actual code (as a single string) for each contract.
    """
    CONTRACT_DEFINITION_REGEX = r"^(?:contract|library|interface)\s{1,}(\w{1,}).*{"
    contract_pattern = re.compile(CONTRACT_DEFINITION_REGEX, re.DOTALL)
    
    contracts = [""]
    contract_names = []   
    
    # Keep track of open / closed curly braces.
    # 0 means that we're outside a contract
    brace_counter = 0 

    for line in source_lines:
        contracts[-1] += line

        if brace_counter == 0:
            match = re.match(contract_pattern, line)
            if match:
                name = match.group(1)
                contract_names.append(name)

                # Add a new contract if this one is closed in the same line
                # Otherwise just count the opening brace that matched in the regex
                if "}" in line:
                    contracts.append("")
                else:
                    brace_counter += 1
        
        else: # We're inside a contract, so count opening vs. closing brackets
            if "{" in line:
                brace_counter += 1
            
            if "}" in line:
                brace_counter -= 1
                if brace_counter == 0:
                    # After last contract, there'll be one additional element that must be cleaned
                    contracts.append("")

    # Don't return last element in contracts list, it's empty
    return contract_names, contracts[:-1]


def prepare_etherscan_request(contract_address):
    params = {
        "module": "contract",
        "action": "getsourcecode",
        "address": contract_address
    }
    return urllib.request.Request(
        f"https://api.etherscan.io/api?{urllib.parse.urlencode(params)}",
        headers={
            "User-Agent":
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"
        }
    )


def get_code_from_response(response):
    """Returns the source code from a JSON-formatted response string from Etherscan's API"""
    response = json.loads(response, encoding='utf-8')
    if not int(response["status"]):
        raise Exception("The given address does not have a verified source code.")

    return response["result"][0]["SourceCode"]


def fetch_source_code(contract_address):
    """Retrieves the verified source code of the given address from Etherscan's public API"""    
    r = prepare_etherscan_request(contract_address)
    return get_code_from_response(urllib.request.urlopen(r).read())
