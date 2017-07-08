# GitHub Issue Label Generator

The code in this repository is a modified version of the code here: [https://github.com/martinpeck/gh-issue-label-generator](https://github.com/martinpeck/gh-issue-label-generator). This version of the script works even if you have two factor enabled on your account (and why would you not???).

This python script will generate the standard set of labels that we use in all of our GitHub issues databases.

The definition of the labels you want to create is set within `definitions.json`. The script expects all existing labels to have already been deleted. Errors will be generated if the label it's trying to create already exists. The script will carry on, but it won't overwrite/modify the existing label.

## Usage ##

- set up a virtual environment (because I said so) with:
  
  ```
  virtualenv ~/.virtualenvs/gh_issue_label_generator
  source ~/.virtualenvs/gh_issue_label_generator/bin/activate
  ```

- install the requirements with `pip install -r requirements.txt`
- make sure that ALL of the existing labels in the repository are deleted (or, be prepared to put up with some errors)
- run `gen_labels.py` in the following manner...

```
python gen_labels.py -u USERNAME -p PASSWORD -o REPOSITORY-OWNER -r REPOSITORY
```

For example...

```
python gen_labels.py -u martinpeck -p 1234$abcd -o martinpeck -r plinky

```

Full usage can be obtained by using `-h` command line arg...

```
usage: gen_labels.py [-h] -u USERNAME -p PASSWORD -o OWNER -r REPOSITORY
                     [-d DEFINITIONS] [-t]

Generates GitHub issue labels.

optional arguments:
  -h, --help            show this help message and exit
  -u USERNAME, --user USERNAME
                        github username
  -p PASSWORD, --pass PASSWORD
                        github password, or application token for 2FA
  -o OWNER, --owner OWNER
                        the owner of the repository to update
  -r REPOSITORY, --repo REPOSITORY
                        the repository to update
  -d DEFINITIONS, --def DEFINITIONS
                        location of json file containing label definitions.
                        Defaults to definitions.json
  -t, --test            If true, performs a dry run without actually making
                        request to github
```
