import logging.handlers
import os
from typing import Any

import requests
import rich_click as click
from dotenv import load_dotenv
from notion_client import Client

from github_stars_export import __project__

# Load environment variables
load_dotenv()

GITHUB_API_TOKEN = os.getenv("GITHUB_API_TOKEN")
NOTION_API_TOKEN = os.getenv("NOTION_API_TOKEN")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")
# GitHub API URL
GITHUB_API_URL = "https://api.github.com/user/starred"

# Initialize Notion client
notion_client = Client(auth=NOTION_API_TOKEN)




@click.group("cli", help="Run the export operation.")
@click.option("--github-api-token", envvar="GITHUB_API_TOKEN", default=None, required=True,
              help="The GitHub API token.")
@click.option("--notion-api-token", envvar="NOTION_API_TOKEN", default=None, required=True,
              help="The Notion API token.")
@click.option("--notion-database-id", envvar="NOTION_DATABASE_ID", default=None, required=True,
              help="The Notion database ID.")
@click.pass_context
def cli(context: click.Context, github_api_token: str, notion_api_token: str, notion_database_id: str):
    """
    The base command-line interface
    :type notion_database_id: str
    :type notion_api_token: str
    :type github_api_token: str
    :param github_api_token: The API token for GitHub
    :param notion_api_token: The API token for Notion
    :param notion_database_id: The database ID for Notion
    :param context:
    :return:
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


@cli.command("run", help="Run the export operation.")
@click.pass_context
def cli_run(context: click.Context):
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
    sync_starred_projects_to_notion(github_api_token, notion_api_token, notion_database_id)


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
    Add the project to Notion
    :param notion_api_token: The API token for interfacing with Notion
    :param notion_database_id: The Notion database ID
    :type repository: object
    :param repository:
    :return:
    """
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
    properties = {
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

    # Send the data to Notion
    try:
        notion_client.pages.create(
            parent={"database_id": NOTION_DATABASE_ID},
            properties=properties
        )
        print(f"Added project: {title}")
    except Exception as e:
        _logger.exception("Failed: Unable to create the database page.", exc_info=e)


# Main function to sync GitHub starred projects to Notion
def sync_starred_projects_to_notion(github_api_url: str, github_api_token: str, notion_database_id: str):
    """
    Get the list of starred repositories and add it to the Notion database.
    :return:
    """
    repos: list[dict] = get_starred_repos(github_api_url, github_api_token)
    if repos:
        for repo in repos:
            add_project_to_notion(repo, notion_database_id)
    else:
        print("No starred projects found.")


try:
    cli()
except Exception as e:
    pass
