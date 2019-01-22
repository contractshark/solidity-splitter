import argparse, os


def load_contract_lines(filepath):
    source_code_lines = []
    with open(str(filepath), "r") as source_file:
        source_code_lines = source_file.readlines()
    return source_code_lines


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
