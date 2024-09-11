import os
from multiprocessing.managers import Value
from typing import Any

from github_stars_export import __project__
import requests
import rich_click as click
from dotenv import load_dotenv
from notion_client import Client
import logging
import logging.handlers

# Load environment variables
load_dotenv()

GITHUB_API_TOKEN = os.getenv("GITHUB_API_TOKEN")
NOTION_API_TOKEN = os.getenv("NOTION_API_TOKEN")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")
# GitHub API URL
GITHUB_API_URL = "https://api.github.com/user/starred"

# Initialize Notion client
notion_client = Client(auth=NOTION_API_TOKEN)


def get_time_formatted() -> str:
    """
    Get the formatted time stamp
    :return: Returns the formatted time stamp
    """
    from datetime import datetime

    # Get the current date and time
    current_datetime = datetime.now()

    # Format the date and time as dd-MM-YYYY_HHmmss
    formatted_datetime = current_datetime.strftime("%d-%m-%Y_%H%M%S")
    return formatted_datetime


_logger = logging.getLogger(__name__)
_logger.addHandler(logging.StreamHandler())
_logger.addHandler(
    logging.handlers.RotatingFileHandler(os.path.join(os.getcwd(), f"{__project__}_{get_time_formatted()}.log")))


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
    :param github_api_token: The API token for GitHub
    :param notion_api_token: The API token for Notion
    :param notion_database_id: The database ID for Notion
    :param context:
    :return:
    """
    if not context:
        raise ValueError("The context specified is invalid or null")

    context.obj['github_api_token'] = github_api_token
    context.obj['notion_database_id'] = notion_database_id
    context.obj['notion_api_token'] = notion_api_token


@cli.command("run", help="Run the export operation.")
@click.pass_context
def cli_run(context: click.Context):
    """

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
    sync_starred_projects_to_notion(notion_database_id)


# Function to get starred repositories from GitHub
def get_starred_repos() -> list[object]:
    """
    Get the list of starred repositories
    :return:
    """
    headers = {"Authorization": f"token {GITHUB_API_TOKEN}"}
    response = requests.get(GITHUB_API_URL, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve starred repositories: {response.status_code}")
        return []


# Function to add a GitHub project to Notion
def add_project_to_notion(repository: dict[str, Any], notion_database_id: str):
    """

    :param notion_database_id:
    :type repository: object
    :param repository:
    :return:
    """
    title = repository.get("name")
    description = repository.get("description", "No description provided.")
    topics = repository.get("topics", [])
    url = repository.get("html_url")

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
        print(f"Failed to add project {title}: {e}")


# Main function to sync GitHub starred projects to Notion
def sync_starred_projects_to_notion(notion_database_id: str):
    """
    Get the list of starred repositories and add it to the Notion database.
    :return:
    """
    repos = get_starred_repos()
    if repos:
        for repo in repos:
            add_project_to_notion(repo, notion_database_id)
    else:
        print("No starred projects found.")


try:
    cli()
except Exception as e:
    pass
