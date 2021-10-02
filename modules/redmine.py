import datetime
import re

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


def _build_subissue_suffix(subissue, parent_issue):
    p = f"{parent_issue.get('prefix')}".removesuffix(": ")
    suffix = subissue.get("suffix").replace("%p", p)
    return suffix


def get_issues_names_by_prefix(issues_prefix:str, config:dict) -> list[str]:
    # TODO: how to avoid this code repetition here and in post_issue?
    project_url = str(config.get("project-url"))
    username = str(config.get("username"))
    password = str(config.get("password"))

    url = f"{project_url}/issues.json?subject=~{issues_prefix}&limit=99"
    headers = {
        "Contnt-Type": "application/json"
    }
    auth = (username, password)

    res = requests.get(url, headers=headers, auth=auth)
    issues = res.json().get("issues")
    issues_names = []
    for issue in issues:
        issues_names.append(re.sub(fr"{issues_prefix}[\d]*: ", "", issue.get("subject")))

    return issues_names


def post_issue(issue:dict, config:dict):
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
    status_code = res.status_code
    assert status_code == 201, f"Status Code {status_code} during creation of: {issue.get('subject')}"

    created_issue = res.json().get("issue")
    created_issue_id = created_issue.get("id")
    created_issue_name = created_issue.get("subject")
    print(f"Issue {created_issue_id} created: {created_issue_name}")

    return created_issue


def create_sprint_issues(sprint_filepath:str, config_filepath:str):
    with open(sprint_filepath, "r") as f:
        sprint = yaml.load(f, Loader=yaml.FullLoader)
    with open(config_filepath, "r") as c:
        config = yaml.load(c, Loader=yaml.FullLoader)

    _check_sprint(sprint)

    sprint["start-date"] = sprint.get("start-date").strftime("%Y-%m-%d")
    sprint["due-date"] = sprint.get("due-date").strftime("%Y-%m-%d")

    registered_issues:list[str] = get_issues_names_by_prefix(sprint.get("issues-prefix"), config)

    registered_issues_count = len(registered_issues)

    issues:list[dict] = sprint.get("issues")
    for issue in issues:
        if issue.get("subject") in registered_issues: continue
        registered_issues_count += 1
        issue_prefix = f"{sprint.get('issues-prefix')}{registered_issues_count:02d}: "
        issue["subject"] = f"{issue_prefix}{issue.get('subject')}"

        issue["start-date"] = sprint.get("start-date")
        issue["due-date"] = sprint.get("due-date")

        issue = util._replace_hyphen_with_underscore(issue)

        created_issue = post_issue(issue, config)
        created_issue["prefix"] = issue_prefix

        subissues = issue.get("subissues")
        if subissues is None: continue
        for subissue in subissues:
            registered_issues_count += 1

            subissue_prefix = f"{sprint.get('issues-prefix')}{registered_issues_count:02d}: "
            subissue_suffix = _build_subissue_suffix(subissue, created_issue)
            subissue["subject"] = f"{subissue_prefix}{subissue.get('subject')} {subissue_suffix}"

            subissue["start-date"] = sprint.get("start-date")
            subissue["due-date"] = sprint.get("due-date")

            subissue = util._replace_hyphen_with_underscore(subissue)

            post_issue(subissue, config)

    print(f"Create from {sprint_filepath}")
    return True
