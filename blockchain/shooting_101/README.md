# Shooting 101 (very easy)
In this challenge we need to call some special functions on the contract.

Let's take a look at the target contract:

```solidity
pragma solidity ^0.8.18;

contract ShootingArea {
    bool public firstShot;
    bool public secondShot;
    bool public thirdShot;

    modifier firstTarget() {
        require(!firstShot && !secondShot && !thirdShot);
        _;
    }

    modifier secondTarget() {
        require(firstShot && !secondShot && !thirdShot);
        _;
    }

    modifier thirdTarget() {
        require(firstShot && secondShot && !thirdShot);
        _;
    }

    receive() external payable secondTarget {
        secondShot = true;
    }

    fallback() external payable firstTarget {
        firstShot = true;
    }

    function third() public thirdTarget {
        thirdShot = true;
    }
}
```

The `Setup.sol` just contains the `isSolved()` function like the first challenge, however now it checks all three bolleans of the target contract whether they are true.

We can also see that there are some `modifiers` that are applied to the functions.
This ensures the order in which they are called is first, second, then third.

The first target is the `fallback` method.

I saw that this is different from the other functions we had before, so I went to look for some information on `receive` and `fallback` and have found this [article](https://blog.soliditylang.org/2020/03/26/fallback-receive-split/).

Here it says, that:
> receive() external payable — for empty calldata (and any value)
> fallback() external payable — when no other function matches (not even the receive function). Optionally payable.

Both of these functions are triggered when sending just a transaction to the contract, and not directly calling any functions on it.

The `receive` function is used when empty call data is received, and the `fallback` function is used when no other function on the contract matches.

So to trigger `fallback` first, let's send a transaction, but with a non-empty data field.

Next the second target is the `receive` function, let's send a transaction with empty data field.

And finally the `third` is just a function like in the previous challange, we can just call it in the same way.

`solve.py` performs these steps, although I couldn't make it work with a single invocation of the script.
For each of the step the script is executed once and then I just commented the steps that were already done.

Sending 3 to the other endpoint that is not the RPC we get the flag.
