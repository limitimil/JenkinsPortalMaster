from jira_services.core import jira

class IssueGrabber:
    def __init__(self, issue_key):
        self.issue = jira.issue(issue_key)
        self.last_comment = self.issue.fields.comment.comments[-1]
        self.raw_markdown = self.last_comment.body
        self.summary = self.issue.fields.summary
        self.description = self.issue.fields.description
        self.issue_key = issue_key
