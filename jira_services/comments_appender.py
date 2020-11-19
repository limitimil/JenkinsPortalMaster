from jira_services.core import jira
from jira_services.jira_markdown_helper import JiraMarkdownHelper
def append_url_references(issue_key, reference_url, customized_title):
    issue = jira.issue(issue_key)
    last_comment = issue.fields.comment.comments[-1]
    raw_markdown = last_comment.body
    jmh = JiraMarkdownHelper(raw_markdown)
    insert_point = jmh.get_insert_point(customized_title)
    if insert_point is not None:
        raw_markdown = jmh.insert_content(
            '** [{url}|{url}|smart-link]'.format(title=customized_title,url=reference_url),
            insert_point
        )
        last_comment.update(body=raw_markdown)
    else:
        new_url_references(issue_key, reference_url, customized_title)

def new_url_references(issue_key, reference_url, customized_title):
    issue = jira.issue(issue_key)
    jira.add_comment(issue, '* *{title}:*\n** [{url}|{url}|smart-link] '.format(title=customized_title,url=reference_url))

def append_ci_reference(issue_key, reference_url):
    issue = jira.issue(issue_key)
    jira.add_comment(issue, '* *CI:*\n** [{url}|{url}|smart-link] '.format(url=reference_url))

def append_change_log(issue_key, change_logs: list):
    title = "Change Log"
    issue = jira.issue(issue_key)
    last_comment = issue.fields.comment.comments[-1]
    raw_markdown = last_comment.body
    jmh = JiraMarkdownHelper(raw_markdown)
    raw_markdown = jmh.squash_content(title)
    jmh = JiraMarkdownHelper(raw_markdown)
    insert_point = jmh.get_insert_point(title)

    raw_change_logs = ""
    for log in change_logs:
        raw_change_logs = raw_change_logs + '** ' + '{{{{{}}}}} '.format(log[0]) + ''.join(log[1:]) + '\n'
    if insert_point is not None:
        raw_markdown = jmh.insert_content(
            raw_change_logs,
            insert_point
        )
        last_comment.update(body=raw_markdown)
    else:
        jira.add_comment(issue, '* *{}:*\n'.format(title) + raw_change_logs)

class CommentAppender():
    def __init__(self, issue_key):
        self.issue = jira.issue(issue_key)
        self.last_comment = self.issue.fields.comment.comments[-1]
        self.raw_markdown = self.last_comment.body

    def append_url_references(self, reference_url, customized_title):
        jmh = JiraMarkdownHelper(self.raw_markdown)
        insert_point = jmh.get_insert_point(customized_title)
        if insert_point is not None:
            raw_markdown = jmh.insert_content(
                '** [{url}|{url}|smart-link]'.format(title=customized_title,url=reference_url),
                insert_point
            )
            self.last_comment.update(body=raw_markdown)
        else:
            self.new_url_references(reference_url, customized_title)
    def new_url_references(self, reference_url, customized_title):
        jira.add_comment(self.issue, '* *{title}:*\n** [{url}|{url}|smart-link] '.format(title=customized_title,url=reference_url))
    def aggregate_by_title(self, customized_title):
        jmh = JiraMarkdownHelper(self.raw_markdown)
        new_content = jmh.squash_content(customized_title, 10)
        self.raw_markdown = new_content

    def push_message_to_the_last_comment(self, message):
        self.last_comment.update( 
            body=( self.raw_markdown + message))
