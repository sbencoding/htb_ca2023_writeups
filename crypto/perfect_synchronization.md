# Perfect synchronization (very easy)
This challenge is about using frequency analysis to break encryption.

The flag is encrypted, such that each character is passed to AES ECB encryption.
This means that the same letters will generate the same cipher text as well.
Further more the range of input is limited to upper case letters, curly braces `_`, and space.

Now the challenge did drop the hint to use the `quipqiup` tool, however I couldn't manage to figure out during the contest how to make it work so I just did it by hand.

I wrote a simple script to analyse the frequency of the strings.
Here I have found 2 strings with frequency of 1, these must be the curly braces for the flag!

Then we also know that before the opening brace the strings must correspond to HTB

From here it was a matter of substituting all occurrences of a string with the letter we know it corresponds to, and then finding words we can guess the letters of, for example: `THE`, `THAT` already had most letters revealed, just by knowing `HTB`.

I continued this process until enough letters were revealed so that the flag is completely known.
