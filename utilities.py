"""
File: utilities.py
Author: Mark Rutherford
Created: 10/6/2021 6:02 PM

Utility functions to support the main flask routes.
"""
import flask
import requests
import os
from typing import Optional
from statistics import mean
from collections import defaultdict
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv


# Load the .env variables
load_dotenv()
GITHUB_USERNAME = os.getenv('GITHUB_USERNAME')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')


class Repository:
    """
    An class representing a single github repository. Fields are None until data is provided.

    If the GitHub API changes, the only alterations needed will be here.
    """
    def __init__(self, github_json=None):
        """
        Instantiate the Repository object. If passed the json from a github api call, it will populate all relevant
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
        self.forks_count: Optional[int] = github_json['forks_count'] if github_json else None

        # The languages used in the repo, by number of lines
        self.languages = requests.get(github_json['languages_url'], auth=HTTPBasicAuth(username=GITHUB_USERNAME, password=GITHUB_TOKEN)).json() if github_json else None

        # The size of the repo, in kilobytes
        self.size: Optional[int] = github_json['size'] if github_json else None

    def __str__(self):
        """
        Get a string representation of the repository.

        Returns: The repository name

        """
        return self.full_name

    def __repr__(self):
        """
        Get a detailed representation of the repository.

        Returns: The repository name and ID

        """
        return f'{self.id} {self.full_name}'


def get_request_arg(request: flask.Request, arg_name: str, required=False):
    """
    Retrieve an argument from a request.

    Args:
        request: The flask request
        arg_name: The parameter name
        required: Whether the argument is mandatory

    Returns: The request parameter

    """
    if arg_name in request.args:
        return request.args[arg_name]
    elif required:
        flask.abort(400)

    return None


def get_user_repositories(username: str, show_forked: bool) -> list[Repository]:
    """
    Retrieve the github repositories for a specific user.

    Args:
        username: The github username
        show_forked: Whether to keep or discard forked repos

    Returns: The github repositories for the user.

    """
    api_responses_per_page = 100  # Github currently has a max limit of 100 responses per page, though this could change
    api_page = 1  # pages start at 1, not 0
    repos: list[Repository] = []

    response_json = True  # Initialize to true to start the first loop. Will be a dictionary afterwards
    while response_json:
        query = {'per_page': api_responses_per_page, 'page': api_page}
        response = requests.get(f"https://api.github.com/users/{username}/repos", params=query, auth=HTTPBasicAuth(username=GITHUB_USERNAME, password=GITHUB_TOKEN))
        response_json = response.json()

        if response.status_code != 200:
            flask.abort(response.status_code)
            return []
        # Convert to Repository objects and add to repos
        for repo_json in response_json:
            if show_forked or not repo_json['fork']:
                repos.append(Repository(repo_json))

        api_page += 1  # Move to the next page
    return repos


def get_average_repo_size(repositories: list[Repository]) -> str:
    """
    Return the average repository size of a list of repositories. Uses 1024 KiB per 1MiB, etc.

    Args:
        repositories: The repositories

    Returns: The average repository size

    """
    avg_in_kb = mean([repo.size for repo in repositories])
    avg_in_unit = avg_in_kb

    # Iterate over units to find one where the size is under 1024 of the unit
    for unit in ["KiB", "MiB", "GiB", "TiB", "PiB"]:
        if avg_in_unit < 1024.0:
            return f"{avg_in_unit:3.1f}{unit}"
        avg_in_unit /= 1024.0

    # Default to KiB if a suitable unit isn't found
    return f'{avg_in_kb}KiB'


def get_repo_languages(repositories: list) -> list[list[str, int]]:
    """
    Return the languages used in repositories.

    Args:
        repositories: The repositories

    Returns: The sorted usage of repo languages

    """
    # Using a defaultdict avoids having to use if statements to avoid KeyErrors
    languages = defaultdict(int)

    # Sum all of the repository languages
    for repo in repositories:
        for language, usage in repo.languages.items():
            languages[language] += usage

    # Convert to a list (which has order) and sort it. More compatible than sorting a dictionary
    language_list = list(languages.items())
    language_list.sort(key=lambda x: x[1], reverse=True)

    return language_list
