#!/usr/bin/env python3

from splitter.helpers import get_args_parser, load_contract_lines, persist_contracts
from splitter.splitter import fetch_source_code, extract_pragma, extract_contracts

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

if __name__ == "__main__":
    args = get_args_parser().parse_args()
    if args.address:
        run(address=args.address)
    elif args.file:
        run(filename=args.file)
