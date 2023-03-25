# The chasm's crossing conundrum (hard)
First I get the instructions of the game

```
☠ ☠ ☠ ☠ ☠ ☠ ☠ ☠ ☠ ☠ ☠ ☠ ☠ ☠ ☠ ☠ ☠ ☠ ☠ ☠ ☠ ☠ ☠ ☠ ☠ ☠ ☠ ☠ ☠ ☠ ☠ ☠ ☠ ☠ ☠ ☠ ☠ ☠ ☠ ☠
☠                                                                             ☠️
☠  [*] The path ahead is treacherous.                                         ☠️
☠  [*] You have to find a viable strategy to get everyone across safely.      ☠️
☠  [*] The bridge can hold a maximum of two persons.                          ☠️
☠  [*] The chasm lurks on either side of the bridge waiting for those         ☠️
☠      who think they can get across in total darkness.                       ☠️
☠  [*] If two persons get across, one must come back with the flashlight.     ☠️
☠  [*] The flashlight has energy only for a limited amount of time.           ☠️
☠  [*] The time required for two persons to cross, is dictated by the slower. ☠️
☠  [*] The answer must be given in crossing and returning pairs. For example, ☠️
☠      [1,2],[2],... . This means that persons 1 and 2 cross and 2 gets back  ☠️
☠       with the flashlight so others can cross.                              ☠️
☠                                                                             ☠️
☠ ☠ ☠ ☠ ☠ ☠ ☠ ☠ ☠ ☠ ☠ ☠ ☠ ☠ ☠ ☠ ☠ ☠ ☠ ☠ ☠ ☠ ☠ ☠ ☠ ☠ ☠ ☠ ☠ ☠ ☠ ☠ ☠ ☠ ☠ ☠ ☠ ☠ ☠ ☠
```

Basically:
* cross a bridge
* only one flashlight is available which is limited
* flashlight is required to cross
* at most 2 people can cross
* each person has a different time to cross
* the crossing speed is that of the slowest person on the bridge

First I have thought that a greedy solution would be good for this challenge.
This would mean that I find the fastest person and then always send from one side the fastest person and someone, and then only the fastest person on the way back.

After trying and failing a couple of times I started to question whether this was truly the best approach.

I had a slight intuition that we could send the 2 slowest people across, because that would essentially delete the time penalty of the second slowest person, whereas with my approach we always take the time penalty of every person.

The basic 4 person version of this problem is quite popular as internet browsing suggests.

1. Send 2 fastest
2. Send fastest back
3. Send 2 slowest
4. Send 2nd fastest back
5. Make 2 fastest cross together
6. win

However extending this to multiple people, or having an algorithm to give the ordering of people and not just the shortest time was not so popular anymore.

Still I have tried going with this approach and hard coding sending some fastest and slowest pairs.

In the end my algorithm doesn't always produce the perfect solution, however for some instance of the problem it does, and that resulted in the flag.

```python
# algorithm incorrect, but works some of the time
# greedy not a good solution
# known solution is DP but without who crosses when, only the min cross time
# solution wants optimal cross time
ppl = {
    1: 66,
    2: 43,
    3: 33,
    4: 1,
    5: 62,
    6: 17,
    7: 68,
    8: 40,
}

battery = 232

ppl_sorted = {k: v for k, v in sorted(ppl.items(), key=lambda item: item[1])}
print(ppl_sorted)
ppl_sorted = list(ppl_sorted.items())

ans = []
ans.append(f'[{ppl_sorted[0][0]},{ppl_sorted[1][0]}]')
ans.append(f'[{ppl_sorted[0][0]}]')
ans.append(f'[{ppl_sorted[-1][0]},{ppl_sorted[-2][0]}]')
ans.append(f'[{ppl_sorted[1][0]}]')
ans.append(f'[{ppl_sorted[0][0]},{ppl_sorted[1][0]}]')
ans.append(f'[{ppl_sorted[0][0]}]')
ans.append(f'[{ppl_sorted[-3][0]},{ppl_sorted[-4][0]}]')
ans.append(f'[{ppl_sorted[1][0]}]')

cost = (ppl_sorted[1][1] * 2 + ppl_sorted[0][1]) * 2 + ppl_sorted[-1][1] + ppl_sorted[-3][1]
for i in range(1, len(ppl)-4):
    ans.append(f'[{ppl_sorted[0][0]},{ppl_sorted[i][0]}]')
    cost += ppl_sorted[i][1]
    if i != len(ppl) - 5:
        ans.append(f'[{ppl_sorted[0][0]}]')
        cost += ppl_sorted[0][1]

print(','.join(ans))
print(cost)
```

I print the `cost` which is the time spent so that I can immediately see if a solution will be accepted by the remote. I never made a script that does this automatically instead I just copied the input values by hand.
