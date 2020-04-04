from jira import JIRA
server_options = {"server": "https://cybersoft4u.atlassian.net"}
jira = JIRA(server_options, basic_auth=('<your jira account>','<your jira token>'))