import re
class JiraMarkdownHelper:
    def __init__(self, raw_markdown):
        self.raw_markdown = raw_markdown
    def get_insert_point(self, title):
        pattern1 = '^\* .*{}.*'.format(title)
        pattern2 = '^\*\* .*'
        title_presented = False
        for index, line in enumerate(self.raw_markdown.split('\n')):
            if title_presented and not re.match(pattern2, line):
                return index
            if re.match(pattern1, line):
                title_presented = True
        return len(self.raw_markdown.split('\n')) if title_presented else None
    def insert_content(self, content, insert_line=-1):
        fragments = self.raw_markdown.split('\n')
        return '\n'.join(fragments[:insert_line] + [content] + fragments[insert_line:])
    def squash_content(self, title, squash_size=None):
        pattern1 = '^\* .*{}.*'.format(title)
        pattern2 = '^\*\* .*'
        title_presented_index = -1
        for index, line in enumerate(self.raw_markdown.split('\n')):
            if title_presented_index != -1 and not re.match(pattern2, line):
                index = index -1
                break
            if re.match(pattern1, line):
                title_presented_index = index
        if squash_size is None or index - title_presented_index > squash_size:
            fragments = self.raw_markdown.split('\n')
            new_title = fragments[title_presented_index]+ ' **({})**'.format(str(squash_size)+'+' if squash_size else 'squashed') 
            return '\n'.join(
                fragments[:title_presented_index]+
                [new_title]+ 
                fragments[index+1:]
            )
        else:
            return self.raw_markdown
