Advent of Code 2022
===================

https://adventofcode.com/2022


### About

Code for Advent of Code 2022. I copied this repo format from anthonywritescode's [aoc2015](https://github.com/anthonywritescode/aoc2015) repo, to make it easier to work on and submit my own code to aoc2022. All of the original `support` code and terminal submission code is his work. 


## Setup

The `support` package in the repo contains tools that allow you to download your specific problem input as well as submit your solution, all via the terminal. After setting up, the only thing you'll need your browser for is reading the prompt and copying over your test input. This package also contains some timing code that you can optionally use.

First, I recommend creating a virtual envrionment to work in:
```bash
python3 -m venv venv
```

Next you you can install `support`, along with `pytest`, but running:
```bash
pip install -r requirements.txt
```

The directory `day00` is a template directory you can copy for each day with `cp -r day00 day0X` which has boilerplate code.

### Getting Your Session Cookie

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

## Working With the Terminal

The primary commands from support you'll want to use are `aoc-download-input` and `aoc-submit` for downloading the problem input and submitting your answers, respectively.

### Downloading your input

To download your input for a specific day, `cd` into the directory for the day you want and run the `aoc-download-input` command. Example:

```bash
# download input for day 1
cp -r day00 day01
cd day01
aoc-download-input
```

A new file named `input.txt` will appear in your directory, and you'll see a preview of the first few lines in the terminal.

### Submitting Your Code

Once you're satisfied with your code and you'd like to submit your answer, you can pipe the output of your program to `aoc-submit --part [1|2]`. Example:

```bash
# submitting answers to day 01 part 1
python part1.py input.txt | aoc-submit --part 1
```

The terminal will then give you a response (the same as the website's) depending on the correctness of your answer. If you are correct, you can refresh the page on adventofcode.com and you will see part 2 of the answer. 

## Timing

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


## aactivator

I found this project to be particularly useful for trying out `aactivator`. This tool will automatically source your virtual environment upon `cd`ing into a directory that has a `.activate.sh` file in the root folder, as well as deactivating it when you `cd` out of the project folder and have a `.deactivate.sh` file in the root directory. You can find more about the project [here](https://github.com/Yelp/aactivator).

One particular issue I kept encountering with `aactivator` is: `aactivator: Cowardly refusing to source .activate.sh because writeable by others: .`
If you are like me and didn't understand what it means right away: it means that the current project directory is writable to other users/groups that aren't you (`.` being the current directory). To fix this, you need to change the permissions on the project directory (using chmod) so that you are the only user with write access. 