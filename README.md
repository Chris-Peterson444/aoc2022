advent of code 2022
===================

https://adventofcode.com/2022


### About

Code for Advent of Code 2022. I copied this repo format from anthonywritescode's [aoc2015](https://github.com/anthonywritescode/aoc2015) repo, to make it easier to work on and submit my own code to aoc2022. All of the original `support` code and terminal submission code is his work. 


### Setup

To use the timing code and terminal submission command you'll need to install the `support` package.

First, I recommend creating a virtual envrionment to work in:
```bash
python3 -m venv venv
```

Next you you can install `support`, along with `pytest`, but running:
```bash
pip install -r requirements.txt
```

### Working with the Terminal

Create a file named `.env` in the root directory of the repo that contains your session cookie. Finding this is browser dependent but you can generally find this out by logging into adventofcode.com, opening your browser's developer tools, and looking for `storage` or `cookies`. **Remember**: Don't share this cookie with anyone or upload it to github.

#### Firefox
Log in to adventofcode.com, open the Web Developer Tools (ctrl+shift+I or press the hamburger/trigam/triple-bar button -> More Tools -> Web Developer tools), click on the `storage` menu, and then click on the `cookies` pane on the left. Finally, the `session` entry contains your session cookie. 

#### Google Chrome
Log in to adventofcode.com, open the Developer Tools (ctrl+alt+I or press the kebab/triple-dots button -> More Tools -> Developer tools), click on the `>>` button and select `application`, and then expand the `cookies` dropdown in the `storage` section on the left pane. Finally, click on the adventofcode.com entry and the `session` entry contains your session cookie.

Your `.env` file should look something like:
```bash
session=123412341234...
```
With the ellipses indicating that it's a particularly long value, not that you should have them in the field!

Then you can submit your code by piping your output to the `aoc-submit` command. Example:

### Timing

- comparing to these numbers isn't necessarily useful
- normalize your timing to day 1 part 1 and compare
- alternate implementations are listed in parens
- these timings are very non-scientific (sample size 1)

```console
$ find -maxdepth 1 -type d -name 'day*' -not -name day00 | sort | xargs --replace bash -xc 'python {}/part1.py {}/input.txt; python {}/part2.py {}/input.txt'
+ python ./day01/part1.py ./day01/input.txt
74
> 1272 μs
```


