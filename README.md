# My Favorite Coworker

AI-powered PR review assistant that automatically analyzes pull requests, detects change types, and runs appropriate tests.

## Features

- **Automatic PR Analysis**: Detects UI (React) and API (Python) changes
- **UI Testing**: Screenshots via Playwright MCP integration
- **API Testing**: Endpoint testing with OpenAPI spec support
- **GitHub Integration**: Comments results directly on PRs

## Quick Start for Engineers

### Prerequisites

- Python 3.8+
- GitHub CLI (`gh`) authenticated
- Node.js 18+ (for Playwright MCP)

### Installation

1. Clone and setup:
```bash
git clone https://github.com/yourusername/myfav-coworker.git
cd myfav-coworker
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. Configure GitHub CLI:
```bash
gh auth login
```

3. Install in your IDE:

**For Claude Desktop:**
```bash
cp .mcp/config.json ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

**For Cursor/Windsurf:**
Add to settings.json:
```json
{
  "mcpServers": {
    "myfav-coworker": {
      "command": "python3",
      "args": ["/path/to/myfav-coworker/server.py"],
      "env": {
        "PYTHONPATH": "/path/to/myfav-coworker"
      }
    }
  }
}
```

## Usage

In your IDE with MCP support:

1. **Analyze a PR:**
   - "Review PR #123"
   - "Check the changes in PR 45"
   - "Test my current branch PR"

2. **The assistant will:**
   - Analyze the PR diff
   - Detect UI vs API changes
   - Run appropriate tests
   - Comment results on the PR

## How It Works

1. **analyze_pr**: Fetches PR info via `gh pr view`, categorizes changes
2. **test_ui_changes**: Uses Playwright MCP to capture screenshots
3. **test_api_changes**: Tests endpoints based on OpenAPI spec
4. **GitHub Comments**: Posts results using `gh pr comment`

## Project Structure

```
myfav-coworker/
├── server.py              # Main MCP server
├── tools/
│   ├── analyze_pr.py     # PR analysis
│   ├── ui_tester.py      # UI testing
│   └── api_tester.py     # API testing
├── utils/
│   ├── github_client.py  # GitHub CLI wrapper
│   └── openapi_parser.py # OpenAPI utilities
└── .mcp/config.json      # MCP configuration
```

## Troubleshooting

- **"gh command failed"**: Run `gh auth login`
- **UI tests fail**: Ensure app is running on localhost:3000
- **API tests fail**: Ensure API is running on localhost:8000
- **MCP not found**: Restart your IDE after configuration

## Contributing

PRs welcome! The codebase is minimal (~300 lines) and focused.