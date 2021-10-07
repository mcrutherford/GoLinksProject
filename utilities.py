"""
File: utilities.py
Author: Mark Rutherford
Created: 10/6/2021 6:02 PM
"""
import flask


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


def get_total_repositories(username: str) -> int:
    """
    Retrieve the total github repositories for a specific user.

    Args:
        username: The github username

    Returns: The number of github repositories for a user.

    """
    return 0


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
