import re
class JiraMarkdownHelper:
    def __init__(self, raw_markdown):
        self.raw_markdown = raw_markdown
    def get_insert_point(self, title):
        pattern1 = '^\* .*{}.*'.format(title)
        pattern2 = '^\*\* .*'
        title_presented = False
        for index, line in enumerate(self.raw_markdown.split('\n')):
            if title_presented and not re.match(pattern1, line):
                return index
            if re.match(pattern1, line):
                title_presented = True
        return None
    def insert_content(self, content, insert_line=-1):
        fragments = self.raw_markdown.split('\n')
        return '\n'.join(fragments[:insert_line] + [content] + fragments[insert_line:])
