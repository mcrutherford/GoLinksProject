"""
File: app.py
Author: Mark Rutherford
Created: 10/6/2021 5:29 PM
"""
import flask

import utilities

app = flask.Flask(__name__)


@app.route('/getuserstats', methods=['GET'])
def get_user_stats():
    username = utilities.get_request_arg(request=flask.request, arg_name='username', arg_type=str, required=True)
    forked = utilities.get_request_arg(request=flask.request, arg_name='forked', arg_type=bool)
    if forked is None:
        forked = False

    repos = []
    user_stats = {
        'Username': username,
        'Forked': forked,
        'Repositories': utilities.get_total_repositories(username),
        'TotalStargazers': utilities.get_total_stargazers(repos),
        'TotalForkCount': utilities.get_total_fork_count(repos),
        'AverageRepoSize': utilities.get_average_repo_size(repos),
        'Languages': utilities.get_repo_languages(repos),
    }
    return flask.jsonify(user_stats)


if __name__ == '__main__':
    app.run()
