# GitHub Stars Export

## Overview

GitHub Stars Export is a Python tool that exports your starred repositories from GitHub to a Notion database. It allows you to easily organize and manage the repositories you have starred, providing a way to store metadata in Notion for easy searching and categorization.

## Features

- Export starred repositories from your GitHub account.
- Save repository information, such as name, URL, and description, to a Notion database.
- Uses environment variables for secure configuration.

## Requirements

- Python 3.8+
- Notion API Key
- GitHub Personal Access Token

## Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/your-username/github-stars-export.git
   cd github-stars-export
   ```

2. Install dependencies using Poetry:

   ```sh
   poetry install
   ```

3. Create a `.env` file to store your API keys:

   ```sh
   touch .env
   ```

   Add the following keys to your `.env` file:

   ```ini
   GITHUB_API_TOKEN=your_github_token
   NOTION_API_TOKEN=your_notion_token
   ```

## Usage

To export your GitHub starred repositories to Notion, run the following command:

```sh
poetry run python -m github_stars_export
```

This command will authenticate using the provided GitHub and Notion tokens and start exporting starred repositories to your Notion database.

### Examples

1. **Basic Export Command**

   To export your GitHub starred repositories to a Notion database, you can run the following command with the required options:

   ```sh
   poetry run python -m github_stars_export --github-api-token YOUR_GITHUB_API_TOKEN --notion-api-token YOUR_NOTION_API_TOKEN --notion-database-id YOUR_NOTION_DATABASE_ID
   ```

   Alternatively, if you have set the required environment variables in your `.env` file (`GITHUB_API_TOKEN`, `NOTION_API_TOKEN`, `NOTION_DATABASE_ID`), you can simplify the command:

   ```sh
   poetry run python -m github_stars_export
   ```

2. **Using Environment Variables**

   You can export the starred repositories without specifying the tokens explicitly in the command if you have the environment variables set:

   ```sh
   export GITHUB_API_TOKEN=your_github_token
   export NOTION_API_TOKEN=your_notion_token
   export NOTION_DATABASE_ID=your_notion_database_id

   poetry run python -m github_stars_export
   ```

3. **Help Command**

   To view all the available options and get help with usage:

   ```sh
   poetry run python -m github_stars_export --help
   ```

   This will display information about required options such as `--github-api-token`, `--notion-api-token`, and `--notion-database-id`.

### Command-line Options

- `--github-api-token` (required): The GitHub API token used to access your starred repositories.
- `--notion-api-token` (required): The Notion API token used to connect to your Notion workspace.
- `--notion-database-id` (required): The ID of the Notion database where the starred repositories will be saved.

These examples show how to configure and run the export using the command-line interface provided by the tool, either by specifying the tokens directly or by using environment variables.


## Scripts

The repository includes several helper scripts:

- `build.sh`: Builds the project for distribution.
- `format.sh`: Formats the code using the preferred code style.
- `lint.sh`: Runs linters to ensure code quality.

## Configuration

The project uses `pyproject.toml` to manage dependencies and configuration for tools like linters and formatters. It also includes a `.pylintrc` for customizing `pylint` behavior.

## Development

For local development:

1. Install dependencies:

   ```sh
   poetry install
   ```

2. Run the code formatter:

   ```sh
   ./format.sh
   ```

3. Run the linter:

   ```sh
   ./lint.sh
   ```

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.

## Contact

If you have any questions or suggestions, feel free to reach out to the repository maintainer.
