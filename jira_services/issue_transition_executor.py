from jira_services.core import jira

from jira_services.core.issue_grabber import IssueGrabber

class IssueTransitionExecutor(IssueGrabber):
    def transit_to_default_verifier(self):
        raise NotImplementedError

    def get_transition_id_by_status_name(self, status_name='Verification'):
        transitions = jira.transitions(self.issue)
        return next(( t for t in transitions if t['to']['name'] == status_name), None)

