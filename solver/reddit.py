import praw
import re
import ast
from bs4 import BeautifulSoup
from solver import console
from solver.code import Code


class Reddit:
    reddit = praw.Reddit(
        user_agent="ioc-solver",
        client_id="xxxxx",
        client_secret="xxxx"
    )

    def solutions(self, day):
        thread = self.find_thread(day)
        if thread:
            return self.find_solutions(thread)
        return []

    def find_thread(self, day):
        thread = None
        search_term = '2022 Day {} Solutions'.format(day)
        print('Searching reddit for thread: {}'.format(search_term))
        subreddit = self.reddit.subreddit("adventofcode")
        for result in subreddit.search(search_term, limit=1):
            thread = result

        if thread.link_flair_text != 'SOLUTION MEGATHREAD':
            console.print('[bold red]Reddit thread not found![/bold red]')
            return None
        return thread

    @classmethod
    def find_solutions(cls, thread):
        solutions = []
        for top_level_comment in thread.comments:
            if hasattr(top_level_comment, 'body_html'):
                comment_html = top_level_comment.body_html
                if 'python' in comment_html.lower() and not cls.exclude_by_comment(comment_html.lower()):
                    found = re.findall('<code>.+?</code>', comment_html, re.DOTALL)
                    if len(found) == 1:
                        for code in found:
                            code = code.replace("<code>", "").replace("</code>", "")
                            parsed_code = BeautifulSoup(code, "html.parser")
                            solutions.append(Code(parsed_code.text))
        return solutions

    @classmethod
    def exclude_by_comment(cls, comment):
        return 'lisp' in comment \
               or 'c#' in comment \
               or 'cmake' in comment \
               or 'gpt-3' in comment \
               or 'perl' in comment \
               or 'bash' in comment

