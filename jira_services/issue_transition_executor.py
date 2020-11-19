from jira_services.core.issue_grabber import IssueGrabber

class IssueTransitionExecutor(IssueGrabber):
    def transit_to_default_verifier(self):
        raise NotImplementedError

