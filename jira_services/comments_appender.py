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
            '** [{url}|{url}]'.format(title=customized_title,url=reference_url),
            insert_point
        )
        last_comment.update(body=raw_markdown)
    else:
        new_url_references(issue_key, reference_url, customized_title)

def new_url_references(issue_key, reference_url, customized_title):
    issue = jira.issue(issue_key)
    jira.add_comment(issue, '* *{title}:*\n** [{url}|{url}] '.format(title=customized_title,url=reference_url))

def append_ci_reference(issue_key, reference_url):
    issue = jira.issue(issue_key)
    jira.add_comment(issue, '* *CI:*\n** [{url}|{url}] '.format(url=reference_url))

