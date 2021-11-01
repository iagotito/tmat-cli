# Task Manager Automation Tool (TMAT) CLI

Command Line (CLI) Application to automate creation of tasks in
Redmine, issues on Github and the sync process of them.

## How to configure

To start using the TMAT CLI you need to configure the access to the
site that you will perform some action. To do it, run the following
command:

```shell
pyton tmat.py config
```

*Warning:* for now, your loguin information is saved in a local text
file, which is not very recomended. Be careful with this while there
isn't an update to store some access key or something like this.

This will ask you the info to perform the authorization in the site.

> For now, the info asked is about Redmine (link to the project and
> loguin info). When new sites be added to TMAT scope, there will be
> questions about which one you intent to use.

## How to use

TMAT CLI allows to create, read, update and delete tasks and issues on
Redmine (on future, others sites will be added). To see how to use
those functions, check ours tutorials:

- [How to operate on Redmine](./docs/redmine.md)
