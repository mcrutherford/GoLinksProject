"""
File: utilities.py
Author: Mark Rutherford
Created: 10/6/2021 6:02 PM
"""
import flask
import requests
from typing import Optional


class Repository:
    """
    An class representing a single github repository. Fields are None until data is provided.
    """
    def __init__(self, github_json=None):
        """
        Instantiate the Repository object. If passed the json from a github api call, it will create all relevant
        fields.

        Args:
            github_json: (OPTIONAL) The json representing a repository from a github api call
        """
        # Unique id of the repo
        self.id: Optional[int] = github_json['id'] if github_json else None

        # Full name of the repo
        self.full_name: Optional[str] = github_json['full_name'] if github_json else None

        # Whether the repo is a fork
        self.fork: Optional[bool] = github_json['fork'] if github_json else None

        # The amount of stargazers for this repo
        self.stargazers_count: Optional[int] = github_json['stargazers_count'] if github_json else None

        # The amount of forks of this repo
        self.forks: Optional[int] = github_json['forks'] if github_json else None
        self.forks_count: Optional[int] = github_json['forks_count'] if github_json else None  # TODO What is the difference?

        # The languages used in the repo, by number of lines
        #self.languages = requests.get(github_json['languages_url']).json() if github_json else None

        # The size of the repo, in kilobytes
        self.size: Optional[int] = github_json['size'] if github_json else None

    def __str__(self):
        return self.full_name

    def __repr__(self):
        return f'{self.id} {self.full_name}'


def get_request_arg(request: flask.Request, arg_name: str, arg_type, required=False):
    """
    Retrieve an argument of a specific type from a request.

    Args:
        request: The flask request
        arg_name: The parameter name
        arg_type: The parameter type
        required: Whether the argument is mandatory

    Returns: The parameter converted to type arg_type

    """
    if arg_name in request.args:
        arg = request.args[arg_name]
        try:
            arg = arg_type(arg)
            return arg
        except (ValueError, TypeError) as e:
            flask.abort(400)
            return
    elif required:
        flask.abort(400)
        return
    else:
        return None


def get_user_repositories(username: str) -> list[Repository]:
    """
    Retrieve the github repositories for a specific user.

    Args:
        username: The github username

    Returns: The github repositories for the user.

    """
    api_responses_per_page = 100  # Github currently has a max limit of 100 responses per page, though this could change
    api_page = 1  # pages start at 1, not 0
    repos: list[Repository] = []

    response = True  # Initialize to true to start the first loop. Will be a dictionary afterwards
    while response:
        query = {'per_page': api_responses_per_page, 'page': api_page}
        response = requests.get(f"https://api.github.com/users/{username}/repos", params=query).json()

        # Convert to Repository objects and add to repos
        for repo_json in response:
            repos.append(Repository(repo_json))

        api_page += 1  # Move to the next page
    return repos


def get_total_stargazers(repos: list) -> int:
    """
    Retrieve the total number of stargazers for a list of repositories.

    Args:
        repos: The repositories

    Returns: The total number of stargazers

    """
    return 0


def get_total_fork_count(repos: list) -> int:
    """
    Return the total number of forks of a list of repositories.

    Args:
        repos: The repositories

    Returns: The total number of forks

    """
    return 0


def get_average_repo_size(repos: list) -> str:
    """
    Return the average repository size of a list of repositories.

    Args:
        repos: The repositories

    Returns: The average repository size

    """
    return '0GB'


def get_repo_languages(repos: list) -> dict:
    """
    Return the languages used in repositories, sorted by usage.

    Args:
        repos: The repositories

    Returns: The sorted usage of repo languages

    """
    return {}


if __name__ == '__main__':
    get_user_repositories('mcrutherford')
