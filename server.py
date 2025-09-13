#!/usr/bin/env python3
from mcp.server.fastmcp import FastMCP
from tools.analyze_pr import analyze
from tools.ui_tester import run_ui_tests
from tools.api_tester import run_api_tests

mcp = FastMCP("My Favorite Coworker")

@mcp.tool()
async def analyze_pr(pr_ref: str, repo_path: str = None) -> dict:
    """Analyze a GitHub PR to determine change types and files affected.
    Args:
        pr_ref: PR number or current branch
        repo_path: Path to the git repository (defaults to current directory)
    """
    return await analyze(pr_ref, repo_path)

@mcp.tool()
def test_ui_changes(pr_number: int, ui_files: list[str], base_url: str = "http://localhost:3000") -> dict:
    """Run UI tests on changed components using Playwright.
    Args:
        pr_number: GitHub PR number
        ui_files: List of UI files changed
        base_url: Base URL of the application
    """
    return run_ui_tests(pr_number, ui_files, base_url)

@mcp.tool()
def test_api_changes(pr_number: int, api_files: list[str], base_url: str = "http://localhost:8000") -> dict:
    """Test API endpoints affected by changes.
    Args:
        pr_number: GitHub PR number
        api_files: List of API files changed
        base_url: Base URL of the API
    """
    return run_api_tests(pr_number, api_files, base_url)

if __name__ == "__main__":
    mcp.run(transport="stdio")