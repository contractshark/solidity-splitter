#!/usr/bin/python3
import os, re, sys, json, argparse
import urllib.request
import urllib.parse


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


def load_contract_lines(filepath):
    source_code_lines = []
    with open(filepath, "r") as source_file:
        source_code_lines = source_file.readlines()
    return source_code_lines


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


def persist_contracts(names, contracts_code, pragma, output_dir="contracts"):
    """
    Takes a list of names and a list of source codes,
    and writes each contract to a separate file in the given directory
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for name, code in zip(names, contracts_code):
        with open(f"{os.path.join(output_dir, name)}.sol", "w") as out_file:
            if len(pragma):
                out_file.write(pragma + "\n")
            out_file.writelines(code)


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
    

def run(address=None, filename=None):
    source_code_lines = []
    
    if address:
        try:
            source_code_lines = fetch_source_code(address).split("\n")            
        except Exception as exc:
            print(exc)
            exit(-1)
    elif filename:
        source_code_lines = load_contract_lines(filename)

    pragma_statement = extract_pragma(source_code_lines)

    persist_contracts(
        *extract_contracts(source_code_lines),
        pragma_statement
    )


def get_args_parser():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument("-a", "--address",
        help="Address of the contract (source code must be verified in Etherscan)",
        type=str,
        default=None
    )

    group.add_argument("-f", "--file",
        help="Solidity file containing several contracts to split",
        type=str,
        default=None
    )

    return parser


if __name__ == "__main__":
    args = get_args_parser().parse_args()
    if args.address:
        run(address=args.address)
    elif args.file:
        run(filename=args.file)
