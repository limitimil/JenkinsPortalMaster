from jira_services.core import jira
def append_ci_reference(issue_key, reference_url):
    issue = jira.issue(issue_key)
    jira.add_comment(issue, '* *CI:*\n** [{url}|{url}] '.format(url=reference_url))

