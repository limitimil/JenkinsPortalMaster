import click
import json
import requests
from git import Repo
from itertools import compress
TRIM_COMMIT_HEX= 8
MAX_COMMIT_TRACE_BACK = 20
API_BASE_URL= "http://192.168.107.135:9002"
API_PATH= "append_comment/change_log"
@click.command()
@click.option('-i', '--issue-key', 'issue_key', required=True)
@click.option('-f', '--from', 'from_commit_id', required=True)
@click.option('-t', '--to', 'to_commit_id', default='HEAD')
def main(issue_key, from_commit_id, to_commit_id='HEAD'):
    change_logs = get_change_logs(from_commit_id, to_commit_id)
    payload = get_api_payload(issue_key, change_logs)
    response = requests.put("{base}/{api}".format(
        base= API_BASE_URL,
        api= API_PATH
        ),
            json= payload)
    assert response.status_code == 200
    print("Summary:")
    print("*"* 20)
    print("Jira Issue: {}".format(issue_key))
    print("*"* 20)
    print("\n".join([' '.join(elems) for elems in change_logs]))
    return


def get_api_payload(issue_key, change_logs):
    payload =  {"issue_key":issue_key, "change_logs": change_logs}
    return payload


def get_change_logs(from_commit_id, to_commit_id):
    repo = Repo('./')
    commits = repo.iter_commits('HEAD')
    commits = list(commits)
    result = []
    for c in compress(commits, [1]*MAX_COMMIT_TRACE_BACK ):
        if not result:
            if to_commit_id == 'HEAD' or c.hexsha.startswith(to_commit_id):
                result.append((c.hexsha[:TRIM_COMMIT_HEX], trim_first_line(c.message)))
        else:
            result.append((c.hexsha[:TRIM_COMMIT_HEX], trim_first_line(c.message)))
        if c.hexsha.startswith(from_commit_id):
            break
    assert len(result) > 0
    return result


def trim_first_line(lines :str):
    return lines.split('\n')[0]

if __name__ == '__main__':
    main()

