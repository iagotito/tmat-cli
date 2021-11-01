# TMAT Redmine Documentation

> How to use the TMAT's Redmine functionalities

## Create new Tasks

As in a software development process is common to separate the
development in sprints, the _TMAT CLI_ was tought to create a set of
the sprint tasks.

To do it, you need to specify them in a file, then run the command:

```
$ python tmat.py redmine create <file name>
```

TMAT support the following filetypes to specify tasks:

### YAML

The yaml structure must follow this sctructure:

```yaml
---
sprint: 1
issues-prefix: S01-T
start-date: 2021-10-22
due-date: 2021-10-22
issues:
  - subject: "Task 1"
    description: "This is the first task"
    estimated-hours: 4
    subissues:
      - subject: "Task 1 subissues"
        description: "This is a description"
      - subject: "Another task 1 subissue"

  - subject: "Task 2"
    ...
```

All the fields (sprint, issues-prefix, start-date, due-date and issues)
are requiered. In the issues, only the "subject" field is required, the
others are optional. The subissues can have the same fields as a normal
issue, but not another nested subissues.
