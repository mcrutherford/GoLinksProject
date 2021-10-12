"""
File: app.py
Author: Mark Rutherford
Created: 10/6/2021 5:29 PM

Flask entrypoint. Contains all routes.
"""
import flask

import utilities

app = flask.Flask(__name__)


# Index
@app.route('/', methods=['GET'])
def get_index():
    """
    Serve the static index.html form to test the /getuserstats route.

    Returns: static/index.html

    """
    return flask.current_app.send_static_file('index.html')


# GitHub user aggregated stats API
@app.route('/getuserstats', methods=['GET'])
def get_user_stats():
    """
    Provided a GitHub username, calculate and return aggregated statistics about the user's repositories.

    Returns: The aggregated statistics

    """
    username = utilities.get_request_arg(request=flask.request, arg_name='username', required=True)
    show_forked = utilities.get_request_arg(request=flask.request, arg_name='forked')

    # Return HTTP 400 if forked is set but not a boolean. Otherwise convert to boolean
    if show_forked is None:
        show_forked = True
    elif show_forked.lower() != 'true' and show_forked.lower() != 'false':
        flask.abort(400)
        return
    else:
        show_forked = show_forked.lower() == 'true'

    # Get all of the user's repositories
    repositories = utilities.get_user_repositories(username, show_forked=show_forked)

    # Create and return the statistics
    user_stats = {
        'Repositories': len(repositories),
        'TotalStargazers': sum([repo.stargazers_count for repo in repositories]),
        'TotalForkCount': sum([repo.forks_count for repo in repositories]),
        'AverageRepoSize': utilities.get_average_repo_size(repositories),
        'Languages': utilities.get_repo_languages(repositories),
    }
    return flask.jsonify(user_stats)


if __name__ == '__main__':
    app.run()
