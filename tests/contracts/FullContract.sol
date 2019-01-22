pragma solidity ^0.4.24;

/**
    Comments
 */
contract FirstContract {
    function foo() external pure returns (uint256) {
        return 1;
    }
}

/**
    Some other comments
    { }
 */
contract SecondContract {
    function bar() external pure returns (uint256) {
        return 2;
    }

    function foo() external pure returns (uint256) {
        return 1;
    }
}

/**
    contract TheContract {} should do nothing
 */
contract ThirdContract is SecondContract { }

library MyLibrary {
    // Test { some harmlesss braces }
}


// Some more {{ }}
interface MyInterface {

}
