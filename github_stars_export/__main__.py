import logging.handlers
from typing import Any

import requests
import rich_click as click
from dotenv import load_dotenv
from notion_client import Client

from github_stars_export.helpers.logging.helpers_logging import get_or_create_logging

# Load environment variables
load_dotenv()

# GitHub API URL
GITHUB_API_URL = "https://api.github.com/user/starred"

_logger: logging.Logger = get_or_create_logging()


@click.group("cli", help="Run the export operation.")
@click.option("--github-api-token", envvar="GITHUB_API_TOKEN", default=None, required=True,
              help="The GitHub API token.")
@click.option("--notion-api-token", envvar="NOTION_API_TOKEN", default=None, required=True,
              help="The Notion API token.")
@click.option("--notion-database-id", envvar="NOTION_DATABASE_ID", default=None, required=True,
              help="The Notion database ID.")
@click.pass_context
def cli(context: click.Context, github_api_token: str, notion_api_token: str, notion_database_id: str) -> int:
    """
    :param context: The Click context object providing access to the command line context.
    :param github_api_token: The GitHub API token for authenticating GitHub API requests.
    :param notion_api_token: The Notion API token for authenticating Notion API requests.
    :param notion_database_id: The ID of the Notion database to be accessed or modified.
    :return: None
    """
    if not context:
        raise ValueError("The context specified is invalid or null")

    if not github_api_token:
        raise ValueError("The GitHub API token is invalid")

    if not notion_api_token:
        raise ValueError("The Notion API token is invalid")

    if not notion_database_id:
        raise ValueError("The database ID is invalid")

    context.obj['github_api_token'] = github_api_token
    context.obj['notion_database_id'] = notion_database_id
    context.obj['notion_api_token'] = notion_api_token

    return 0


@cli.command("run", help="Run the export operation.")
@click.pass_context
def cli_run(context: click.Context) -> int:
    """
    Run the export tool
    :param context:
    :return:
    """
    if not context:
        raise ValueError("The context specified is invalid or null")
    github_api_token = context.obj['github_api_token']
    notion_database_id = context.obj['notion_database_id']
    notion_api_token = context.obj['notion_api_token']
    if not github_api_token:
        raise ValueError("The GitHub API token is invalid or null")
    if not notion_api_token:
        raise ValueError("The Notion API token is invalid or null")
    if not notion_database_id:
        raise ValueError("The Notion database ID is invalid or null")
    try:
        sync_starred_projects_to_notion(github_api_token, notion_api_token, notion_database_id)
    except Exception as exc:
        print(exc)

    return 0


# Function to get starred repositories from GitHub
def get_starred_repos(github_api_url: str, github_api_token: str) -> list[dict]:
    """
    Get the list of starred repositories from the user account
    :param github_api_token:
    :type github_api_url: str
    :return:
    """
    if not github_api_token:
        raise ValueError("The GitHub API token is invalid or null")
    if not github_api_url:
        raise ValueError("The GitHub API url is invalid or null")
    headers = {"Authorization": f"token {github_api_token}"}
    response = requests.get(github_api_url, headers=headers)
    repositories: list[dict] = []

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve starred repositories: {response.status_code}")
        return repositories


# Function to add a GitHub project to Notion
def add_project_to_notion(repository: dict[str, Any], notion_api_token: str, notion_database_id: str):
    """
    Add a GitHub project to Notion database.
    :param repository: Dictionary containing the project details such as name, description, topics, and html_url
    :param notion_api_token: Notion API token for authentication
    :param notion_database_id: Notion database ID where the project will be added
    :return: None
    """

    if not notion_api_token:
        raise ValueError("The Notion API token is invalid or null")

    if not notion_database_id:
        raise ValueError("The database ID is invalid or null")

    if not repository:
        raise ValueError("The repository is invalid or null")

    # Initialize Notion client
    notion_client = Client(auth=notion_api_token)

    title: str = repository.get("name")
    description: str = repository.get("description", "No description provided.")
    topics: list[str] = repository.get("topics", [])
    url: str = repository.get("html_url")

    if not title:
        raise ValueError("The title is invalid or null")
    if not description:
        raise ValueError("The description is invalid or null")
    if not topics:
        raise ValueError("The topics is invalid or null")
    if not url:
        raise ValueError("The url is invalid or null")

    # Prepare the request payload for Notion
    properties = generate_notion_payload(description, title, topics, url)

    # Send the data to Notion
    try:
        notion_client.pages.create(
            parent={"database_id": notion_database_id},
            properties=properties
        )
        print(f"Added project: {title}")
    except Exception as add_proj_exc:
        _logger.exception("Failed: Unable to create the database page.", exc_info=add_proj_exc)


def generate_notion_payload(description: str, title: str, topics: list[str], url: str):
    """
    Generate the payload for invoking the Notion API
    :param description: The description.
    :param title: The title of the Notion payload.
    :param topics:
    :param url:
    :return:
    """
    if not description:
        raise ValueError("The description is invalid or null")

    if not title:
        raise ValueError("The title is invalid or null")

    if not topics:
        raise ValueError("The topics is invalid or null")

    if not isinstance(topics, list):
        raise TypeError("The topics is invalid or null")

    properties: dict[str, any] = {
        "Name": {
            "title": [
                {
                    "text": {
                        "content": title
                    }
                }
            ]
        },
        "Description": {
            "rich_text": [
                {
                    "text": {
                        "content": description
                    }
                }
            ]
        },
        "URL": {
            "url": url
        },
        "Topics": {
            "multi_select": [{"name": topic} for topic in topics]
        }
    }
    return properties


# Main function to sync GitHub starred projects to Notion
def sync_starred_projects_to_notion(github_api_url: str, github_api_token: str, notion_database_id: str):
    """
    Get the list of starred repositories and add it to the Notion database.
    :return:
    """
    repos: list[dict] = get_starred_repos(github_api_url, github_api_token)
    if repos:
        for repo in repos:
            add_project_to_notion(repo, github_api_token, notion_database_id)
    else:
        print("No starred projects found.")


try:
    cli(auto_envvar_prefix="GITHUB_STARS_EXPORT")
except Exception as exc:
    _logger.exception("Failed: Unable to run command-line tool.", exc_info=exc)
