import datetime

import yaml
import requests

from modules import util


def _check_issues(issues:list[dict]):
    REQUIRED_ISSUE_KEYS = [
        "subject",
    ]
    VALID_ISSUE_KEYS = [
        "description",
        "estimated-hours",
        "suffix",
        "subissues"
    ]
    for i in range(0, len(issues)):
        for required_key in REQUIRED_ISSUE_KEYS:
            assert required_key in issues[i], f"missing key {required_key} in issue {i+1}"

        for key in issues[i].keys():
            assert key in REQUIRED_ISSUE_KEYS or key in VALID_ISSUE_KEYS, f"invalid key in issue {i+1}: {key}"

        # TODO: asserts for types

        if "subissues" in issues[i].keys():
            _check_issues(issues[i].get("subissues")) # type: ignore


def _check_sprint(sprint:dict):
    REQUIRED_SPRINT_KEYS = [
        "sprint",
        "issues-prefix",
        "start-date",
        "due-date",
        "issues"
    ]
    # TODO: documentation of sprint fields
    assert all(key in sprint.keys() for key in REQUIRED_SPRINT_KEYS), "Malformed sprint."
    assert type(sprint.get("sprint")) is int, "sprint must be an int"
    assert type(sprint.get("issues-prefix")) is str, "issues-prefic must be a string"
    assert type(sprint.get("start-date")) is datetime.date, "start-date must be a datetime"
    assert type(sprint.get("due-date")) is datetime.date, "due-date must be a datetime"
    assert type(sprint.get("issues")) is list, "issues must be a list"

    _check_issues(sprint.get("issues")) # type: ignore


def post_issue(issue:dict, config:dict) -> requests.Response:
    project_url = str(config.get("project-url"))
    username = str(config.get("username"))
    password = str(config.get("password"))

    url = f"{project_url}/issues.json"
    json = { "issue": issue }
    headers = {
        "Contnt-Type": "application/json"
    }
    auth = (username, password)

    res = requests.post(url, json=json, headers=headers, auth=auth)

    return res


def create(filepath:str, config_path:str):
    with open(filepath, "r") as f:
        sprint = yaml.load(f, Loader=yaml.FullLoader)
    with open(config_path, "r") as c:
        config = yaml.load(c, Loader=yaml.FullLoader)

    _check_sprint(sprint)

    sprint["start-date"] = sprint.get("start-date").strftime("%Y-%m-%d")
    sprint["due-date"] = sprint.get("due-date").strftime("%Y-%m-%d")

    issues:list[dict] = sprint.get("issues")
    for i in range(len(issues)):
        issue = issues[i]
        issue_prefix = f"{sprint.get('issues-prefix')}{i+1:02d}: "
        issue["subject"] = f"{issue_prefix}{issue.get('subject')}"
        issue["start-date"] = sprint.get("start-date")
        issue["due-date"] = sprint.get("due-date")

        issue = util._replace_hyphen_with_underscore(issue)

        res = post_issue(issue, config)
        print(res.json())

    print(f"Create from {filepath}")
    return True
