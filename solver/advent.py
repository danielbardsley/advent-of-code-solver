import requests
import time
from solver import console
from random import randrange
import re


class Advent:
    progress_token = '<span class="leaderboard-daydesc-both">    Time   Rank  Score</span>'

    def __init__(self, session):
        self.cookies = {'session': session}
        self.current_input_day = 0

    def write_input(self, day):
        if day != self.current_input_day:
            headers = {'User-Agent': 'daniel.bardsley https://github.com/danielbardsley/advent-of-code-solver'}
            input_url = 'https://adventofcode.com/2022/day/{}/input'.format(day)
            console.print('Getting input values from advent of code: {}'.format(input_url))
            r = requests.get(input_url, cookies=self.cookies, headers=headers, timeout=10)
            with open('input.txt', 'w') as file:
                file.write(r.text)
                self.current_input_day = day

    def solve(self, day, answer1, answer2):
        submission_url = "https://adventofcode.com/2022/day/{}/answer".format(day)
        headers = {'content-type': 'application/x-www-form-urlencoded',
                   'User-Agent': 'daniel.bardsley https://github.com/danielbardsley/advent-of-code-solver'}

        console.print("Submitting solution 1")
        payload = 'level=1&answer={}'.format(answer1)
        requests.post(submission_url, cookies=self.cookies, data=payload, headers=headers, timeout=10)

        delay = self.calculate_delay()
        console.print("Delaying for {} seconds before posting answer 2...".format(delay))
        time.sleep(delay)

        console.print("Submitting solution 2")
        payload = 'level=2&answer={}'.format(answer2)
        requests.post(submission_url, cookies=self.cookies, data=payload, headers=headers, timeout=10)

    def get_progress(self):
        headers = {'User-Agent': 'daniel.bardsley https://github.com/danielbardsley/advent-of-code-solver'}
        url = 'https://adventofcode.com/2022/leaderboard/self'
        r = requests.get(url, cookies=self.cookies, headers=headers, timeout=10)
        found = re.findall(self.progress_token + '.+?</pre>', r.text, re.DOTALL)
        if len(found) == 0:
            return 0
        latest_day = found[0][len(self.progress_token)+2:].lstrip().split(' ')[0]
        return int(latest_day)

    @classmethod
    def calculate_delay(cls):
        return randrange(120)


