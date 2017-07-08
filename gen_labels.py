#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Label creator for issues in github."""

import argparse
import json

import requests


def setup_args_parser():
    parser = argparse.ArgumentParser(description="Generates GitHub issue " +
                                                 "labels.")
    parser.add_argument('-u', '--user', dest='username', required=True,
                        help="github username")
    parser.add_argument('-p', '--pass', dest='password', required=True,
                        help="github password, or application token for 2FA")
    parser.add_argument('-o', '--owner', dest='owner', required=True,
                        help="the owner of the repository to update")
    parser.add_argument('-r', '--repo', dest='repository',
                        help="the repository to update")
    parser.add_argument('--all', action='store_true')
    parser.add_argument('-d', '--def', dest='definitions',
                        help="location of json file containing label " +
                             "definitions. Defaults to definitions.json",
                        default='definitions.json')
    parser.add_argument('-t', '--test', dest='test', action='store_true',
                        help="If true, performs a dry run without actually " +
                             "making request to github")
    return parser


def parse_args():
    return setup_args_parser().parse_args()


def read_definitions(file_):
    with open(file_, 'r') as stream:
        return json.load(stream)


def create_request(args, label_def, repo_name=None):
    if repo_name is None:
        repo_name = args.repository

    url = "https://api.github.com/repos/{}/{}/labels".format(args.owner,
                                                             repo_name)
    body = json.dumps({'name': label_def['name'], 'color': label_def['color']})
    return (url, body)


def make_request(args, label=None, request_url=None, repo_name=None):
    auth = (args.username, args.password)
    header = {
        'X-GitHub-OTP': str(two_factor)
    }
    if request_url is None:
        http_request = create_request(args, label, repo_name)
        request_url = http_request[0]
        response = requests.post(request_url, headers=header,
                                 data=http_request[1], auth=auth, timeout=10)
    else:
        response = requests.get(request_url, headers=header, auth=auth,
                                 timeout=10)

    return response, request_url


def get_all_repos(args):
    """Get all repos for a user."""
    all_repos = list()
    all_repos_url = 'https://api.github.com/users/{}/repos'.format(args.owner)

    # get a list of all the repositories for the owner
    response, request_url = make_request(args, request_url=all_repos_url)

    if response.ok:
        repos = json.loads(response.text)
        for repo in repos:
            all_repos.append(repo['name'])
    else:
        raise RuntimeError("Unable to get a list of repositories for the " +
                           "owner using the url: {}".format(request_url))

    return all_repos


def issue_requests(args, label_defs):
    # populate a list of the repos we would like to update
    repositories = list()

    if args.all:
        repositories.extend(get_all_repos(args))
    elif args.repository is not None:
        repositories.append(args.repository)

    print(repositories)

    if len(repositories) > 0:
        print("Creating labels:")

    for label_def in label_defs['label']:
        for repo in repositories:
            if args.test:
                print("  would create label {} with color {} here: {}/{}".format(label_def['name'], label_def['color'], args.owner, repo))
            else:
                response, request_url = make_request(args, label=label_def, repo_name=repo)

                if (response.status_code != 200 and response.status_code != 201):
                    print("  failed request to {}: ({}) {}".format(request_url, response.status_code, response.text))
                else:
                    print("  done (%s)" % (response.status_code))


if __name__ == '__main__':
    args = parse_args()
    two_factor = None

    # check to see if either 'all' is set to True (meaning we will add these)
    # labels for all of the owner's repos or -r is set specifying the specific
    # repo to which the labels will be added
    if not args.all and args.repository is None:
        raise RuntimeError("You need to either specify a repo using the -r " +
                           "flag or use the --all flag to add the labels to " +
                           "all repos for the current owner.")

    label_defs = read_definitions(args.definitions)

    if not args.test or args.all:
        two_factor = input("Enter two factor code: ")

    issue_requests(args, label_defs)
