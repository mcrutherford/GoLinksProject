"""
File: app.py
Author: Mark Rutherford
Created: 10/6/2021 5:29 PM
"""
import flask
from statistics import mean

import utilities

app = flask.Flask(__name__)


@app.route('/getuserstats', methods=['GET'])
def get_user_stats():
    username = utilities.get_request_arg(request=flask.request, arg_name='username', arg_type=str, required=True)
    forked = utilities.get_request_arg(request=flask.request, arg_name='forked', arg_type=bool)
    if forked is None:
        forked = False

    # Get all of the user's repositories
    repositories = utilities.get_user_repositories(username)

    # Filter out forked repositories if necessary
    if forked is False:
        repos = [repo for repo in repositories if repo.fork is False]

    # Create and return the statistics
    user_stats = {
        'Repositories': len(repositories),
        'TotalStargazers': mean([repo.stargazers_count for repo in repositories]),
        'TotalForkCount': sum([repo.fork for repo in repositories]),
        'AverageRepoSize': utilities.get_average_repo_size(repositories),
        'Languages': utilities.get_repo_languages(repositories),
    }
    return flask.jsonify(user_stats)


if __name__ == '__main__':
    app.run()
