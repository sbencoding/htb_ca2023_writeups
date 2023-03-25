# Navigating the unkown (very easy)
In this challenge we need to call a function on the blockchain.

The readme of this challenge tells us that the goal is for the `isSolved()` function to return true.
The setup function tells us how that can be achieved.
```solidity
pragma solidity ^0.8.18;

import {Unknown} from "./Unknown.sol";

contract Setup {
    Unknown public immutable TARGET;

    constructor() {
        TARGET = new Unknown();
    }

    function isSolved() public view returns (bool) {
        return TARGET.updated();
    }
}
```

We just need to make sure that the `update` variable in the other contract is true.

```solidity
pragma solidity ^0.8.18;

contract Unknown {
    
    bool public updated;

    function updateSensors(uint256 version) external {
        if (version == 10) {
            updated = true;
        }
    }

}
```

Here we see that to make the `updated` variable true, we need to call the `updateSensors` function the blockchain.

The `solve.py` script will do precisely this.

Calling functions requires the ABI of the contract. For this I have used an online IDE called *remix* where I placed the contract source code.
Then I compiled the code and clicked on the ABI button to copy it to my clipboard

After that we can use the other endpoint the challenge gives us when spawning the docker intsance and send option 3 to get the flag.
