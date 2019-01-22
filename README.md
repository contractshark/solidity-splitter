# Solidity splitter
[![CircleCI](https://circleci.com/gh/tinchoabbate/solidity-splitter.svg?style=svg)](https://circleci.com/gh/tinchoabbate/solidity-splitter)

Because nothing is more boring than manually splitting a set of smart contracts contained in a single file.

This is a simple python script to split a set of Solidity smart contracts. Whether by providing an address of a verified contract in Etherscan or a local Solidity file containing multiple contracts, the script will attempt to split all contracts found, into as many files as contracts are detected. It also works with interfaces and libraries.

## Requirements
- Python 3

## Usage
~~~bash
$ python3 run.py --help
usage: run.py [-h] (-a ADDRESS | -f FILE)

optional arguments:
  -h, --help            show this help message and exit
  -a ADDRESS, --address ADDRESS
                        Address of the contract (source code must be verified
                        in Etherscan)
  -f FILE, --file FILE  Solidity file containing several contracts to
                        split
~~~

## Test
~~~bash
$ python3 -m unittest
~~~

## Limitations
- The necessary `import` statements, after splitting into multiple files, are not included.
- The script naively looks for opening and closing curly braces to detect a contract / library / interface. It is known to fail if a multiline comment includes the beginning of a contract / interface / library declaration, such as:

~~~solidity
/**
contract ContractInsideAComment {
*/
contract ContractOutsideAComment { ... }
~~~

## Maintainers
[@tinchoabbate](https://github.com/tinchoabbate)
