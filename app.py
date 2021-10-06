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
    if 'user' in flask.request.args:
        user = flask.request.args['user']
    else:
        flask.abort(404)
        return

    user_stats = {
        'Repositories': utilities.get_total_repositories(user),
        'TotalStargazers': utilities.get_total_stargazers(user),
        'TotalForkCount': utilities.get_total_fork_count(user),
        'AverageRepoSize': utilities.get_average_repo_size(user),
        'Languages': utilities.get_repo_languages(user),
    }
    return flask.jsonify(user_stats)


if __name__ == '__main__':
    app.run()
