import time
import sys
from random import randrange

from solver import console
from solver.solve import Solve
from datetime import datetime

if __name__ == "__main__":
    solve = Solve()

    if len(sys.argv) > 1:
        day = sys.argv[1]
        solve.run(int(day))
    else:
        while True:
            today = datetime.now()
            current_day = today.day
            latest_solved = solve.get_progress()

            console.print('Current day: {}'.format(current_day))
            console.print('Latest Solved: {}'.format(latest_solved))

            while latest_solved != current_day:
                try:
                    solve.run(latest_solved + 1)
                    latest_solved += 1
                except Exception as ex:
                    console.print(ex)
            else:
                console.print('All problems solved...')

            delay = 240 + randrange(120)
            console.print('Thinking for {} seconds'.format(delay))
            time.sleep(delay)
