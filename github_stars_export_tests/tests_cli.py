import unittest

import click.testing
from click import Context

from github_stars_export.__main__ import cli


class TestCli(unittest.TestCase):
    """
    Initializes the test setup by creating a CliRunner and Context instances.

    :return: None
    """
    def setUp(self):
        """
        Initializes the test setup by creating a CliRunner and Context instances.

        :return: None
        """
        self.runner = click.testing.CliRunner()
        self.ctx = Context(cli)
        self.ctx.obj = {}

    def test_valid_arguments(self):
        """
        :return: Validates that the CLI accepts and correctly assigns the provided GitHub API token,
                 Notion API token, and Notion database ID. Asserts that the respective values in the
                 context object match the expected values and no exceptions are raised in the CLI output.
        """
        result = self.runner.invoke(cli, ['--github-api-token', 'github_token', '--notion-api-token', 'notion_token',
                                          '--notion-database-id', 'database_id'], obj=self.ctx)

        self.assertEqual(self.ctx.obj['github_api_token'], 'github_token')
        self.assertEqual(self.ctx.obj['notion_database_id'], 'database_id')
        self.assertEqual(self.ctx.obj['notion_api_token'], 'notion_token')
        self.assertTrue(result.exception is None)

    def test_empty_context(self):
        """
        Tests the invocation of the CLI without a proper context object and confirms that a ValueError is raised.

        :return: None
        """
        with self.assertRaises(ValueError) as context:
            self.runner.invoke(cli, ['--github-api-token', 'github_token', '--notion-api-token', 'notion_token',
                                     '--notion-database-id', 'database_id'], obj=None)
        self.assertTrue("The context specified is invalid or null" in str(context.exception))

    def test_empty_github_token(self):
        """
        Tests the behavior of the CLI when the GitHub API token is empty.

        :return: None
        """
        with self.assertRaises(ValueError) as context:
            self.runner.invoke(cli,
                               ['--github-api-token', '', '--notion-api-token', 'notion_token', '--notion-database-id',
                                'database_id'], obj=self.ctx)
        self.assertTrue("The GitHub API token is invalid" in str(context.exception))

    def test_empty_notion_token(self):
        """
        Validates that the CLI properly raises a ValueError when an empty Notion API token is provided.

        :return: None
        """
        with self.assertRaises(ValueError) as context:
            self.runner.invoke(cli,
                               ['--github-api-token', 'github_token', '--notion-api-token', '', '--notion-database-id',
                                'database_id'], obj=self.ctx)
        self.assertTrue("The Notion API token is invalid" in str(context.exception))

    def test_empty_database_id(self):
        """
        Test the behavior when an empty database ID is provided.

        :return: None. Raises a ValueError if the database ID is invalid.
        """
        with self.assertRaises(ValueError) as context:
            self.runner.invoke(cli, ['--github-api-token', 'github_token', '--notion-api-token', 'notion_token',
                                     '--notion-database-id', ''], obj=self.ctx)
        self.assertTrue("The database ID is invalid" in str(context.exception))


if __name__ == '__main__':
    unittest.main()
