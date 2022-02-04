from jira_services.core import jira

class IssueGrabber:
    def __init__(self, issue_key):
        self.issue = jira.issue(issue_key)
        self.last_comment = self.issue.fields.comment.comments[-1]
        self.raw_markdown = self.last_comment.body
        self.summary = self.issue.fields.summary
        self.description = self.issue.fields.description
        self.issue_key = issue_key
    def toJSON(self):
        return {
                "last_comment": self.raw_markdown,
                "summary": self.summary,
                "description": self.description,
                "issue_key": self.issue_key
                }
