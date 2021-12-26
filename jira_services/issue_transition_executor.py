from jira_services.core import jira

from jira_services.core.issue_grabber import IssueGrabber

def get_verification_message(assigneeId):
    return f"請 [~accountid:{assigneeId}] 協助驗證此議題"

class IssueTransitionExecutor(IssueGrabber):
    def transit_to_default_verifier(self):
        reporterId = self.issue.fields.reporter.accountId
        transition_id = self.get_transition_id_by_status_name(status_name='Verification')
        jira.add_comment(self.issue, get_verification_message(reporterId))
        jira.transition_issue(self.issue, transition_id , fields={'assignee':{'accountId': reporterId}})
        

    def get_transition_id_by_status_name(self, status_name):
        transitions = jira.transitions(self.issue)
        transition =  next(( t for t in transitions if t['to']['name'] == status_name), None)
        return transition['id']

