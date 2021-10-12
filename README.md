# GoLinksProject

This is a programming task for a position at go/links. Running this code starts an API 
that aggregates GitHub user repository statistics, with the ability to filter out forked 
repositories.

This code is easily extensible to add other features with relative ease, and will 
only require minor alterations if the GitHub API changes.

## Installation

This project has been tested and validated on Python 3.9 using Windows, though it should work on 
Python 3.7+ platform agnostic. Certain libraries are required to run this API, listed in 
[requirements.txt](./requirements.txt). The easiest way to add these to your python install is using 
pip.

```bash
pip install -r requirements.txt
```

This repository also provides a [.env-sample](./.env-sample) file, which should be copied and renamed 
to `.env`. Add a github username and corresponding 
[personal access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token#creating-a-token)
with no permissions to the `.env` file. For example

```dotenv
GITHUB_USERNAME=mcrutherford
GITHUB_TOKEN=ghp_abcdefghijklmnopqrstuvwxyz
```

## Usage

### App
Run app.py using Python

```bash
python ./app.py
```

Flask defaults to running the web server on port 5000, though the exact link and port should be in the console 
after the web server starts. The index page (with an API form) is likely at 
[http://127.0.0.1:5000/](http://127.0.0.1:5000/) with the API endpoint hosted at 
[http://127.0.0.1:5000/getuserstats](http://127.0.0.1:5000/getuserstats).

### API
The /getuserstats API endpoint expects a GET request with the parameter `username`, and an optional `forked` parameter. 
When `forked` is false, the API will ignore forked repositories. Default is true.

```
http://127.0.0.1:5000/getuserstats?username=mcrutherford&forked=false
```

This will return a json formatted response with
- Total count of repositories
- Total stargazers for all repositories
- Total fork count for all repositories
- Average size of a repository in the appropriate KiB, MiB, GiB, etc
- A list of languages with their counts, sorted by most used to least used


## Disclaimer

This code should NOT be used directly in production. The following decisions were made in order to reduce 
unnecessary complexity and improve ease of installation given the scope of this project.

Flask is run using the development `app.run()` call, which will not be able to handle production-level load. 
A production WSGI server would be needed.

GitHub authentication is done through a personal access token. A GitHub App token should be used when in production 
because the app doesn't need access to a specific GitHub account.

## License
[MIT](./LICENSE)