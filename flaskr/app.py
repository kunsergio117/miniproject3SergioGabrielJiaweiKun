from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('github_search.html')

@app.route('/search', methods=['GET'])
def search():
    username = request.args.get('username')
    if username:
        # Fetch user data from GitHub API
        github_api_url = f"https://api.github.com/users/{username}"
        response = requests.get(github_api_url)
        if response.status_code == 200:
            user_data = response.json()

            # Fetch repository data
            repo_api_url = f"https://api.github.com/users/{username}/repos"
            repo_response = requests.get(repo_api_url)
            if repo_response.status_code == 200:
                repositories = repo_response.json()
            else:
                repositories = []

            return render_template('github_profile.html', username=username, user=user_data, repositories=repositories)
        else:
            return f"Failed to fetch user data from GitHub for user {username}"
    else:
        return "Please provide a username."


if __name__ == '__main__':
    app.run(debug=True)
