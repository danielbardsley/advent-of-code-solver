from solver import console
from collections import Counter
from rich.style import Style

from solver.advent import Advent
from solver.reddit import Reddit

highlight_style = Style(color="green", bold=True)


class Solve:
    def __init__(self):
        self.advent = Advent('xxxx')

    def run(self, day):
        self.advent.write_input(day)
        solutions = Reddit().solutions(day)

        for solution in solutions:
            self.execute_solution(solution)

        solved = [solution for solution in solutions if solution.is_solved()]

        if len(solved) > 0:
            answer1, answer2 = self.find_answer(solved)
            console.print('[bold red]Submitting answers: {}, {}[/bold red]'.format(answer1, answer2))
            self.advent.solve(day, answer1, answer2)
        else:
            console.print('[bold red]No solutions found![/bold red]')

    @classmethod
    def find_answer(cls, solved):
        answers1 = Counter([x.result[0] for x in solved])
        answers2 = Counter([x.result[1] for x in solved])
        answer1 = answers1.most_common(1)[0][0]
        answer2 = answers2.most_common(1)[0][0]
        return answer1, answer2

    def get_progress(self):
        return self.advent.get_progress()

    @classmethod
    def execute_solution(cls, solution):
        console.print("-----starting solution execution----", style=highlight_style)
        console.print('--code-- ')
        solution.print_code()
        console.print('--execution--')
        solution.execute()
        solution.print_output()
        console.print('--Answer--')
        solution.print_answer()
        console.print("-----ending solution execution----\n", style=highlight_style)
