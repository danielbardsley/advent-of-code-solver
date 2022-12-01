from rich.syntax import Syntax
from solver import console
import re
import contextlib
import sys
import ast
from io import StringIO


@contextlib.contextmanager
def stdout_io(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old


class Code:
    banned_code = [
        "open(0)",
        "import fileinput",
        "sys.stdin",
        "sys.exit()",
        "import os",
        "raise SystemExit",
        "input(...)",
        "N = int(input())",
        "stdin.readline()",
        "quit()",
        "eval()",
        "\\n",
        ".py",
        "heapq"
    ]

    def __init__(self, parsed_code):
        self.local = {}
        self.code = self.process_input(parsed_code)
        self.syntax = Syntax(self.code, "python", theme="monokai", line_numbers=True)
        self.output = ""
        self.result = []

    def is_valid(self):
        for banned in self.banned_code:
            if banned in self.code:
                return False
        return self.is_valid_python()

    def is_valid_python(self):
        try:
            ast.parse(self.code)
        except SyntaxError:
            return False
        return True

    def is_solved(self):
        return len(self.result) == 2

    def print_code(self):
        console.print(self.syntax)

    def print_output(self):
        console.print(self.output)

    def print_answer(self):
        console.print(self.result)

    @classmethod
    def process_input(cls, parsed_code):
        return re.sub('open\\(.+?\\)', "open('input.txt', 'r')", parsed_code, re.DOTALL)

    def process_output(self, output):
        found = re.findall('[1-9]\d{2,}|9[6-9]\d|9[5-9]{2}', output, re.DOTALL)
        if len(found) == 2:
            self.result = found

    def execute(self):
        try:
            if self.is_valid():
                with stdout_io() as s:
                    exec(self.code, self.local)
                    self.output = s.getvalue()
                self.process_output(self.output)
            else:
                console.print("Skipping since code contains banned instructions")
        except Exception as ex:
            console.print(ex)


