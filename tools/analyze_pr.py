import os
import json
from pathlib import Path
from pydantic_ai import Agent
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.google import GoogleProvider
from utils.github_client import get_pr_info, get_pr_diff
import logging

# Initialize Gemini 2.5 Pro model - API key comes from Windsurf MCP config
def get_gemini_model():
    # Try to read API key from Windsurf MCP config
    windsurf_config_path = Path.home() / ".codeium" / "windsurf" / "mcp_config.json"
    api_key = None
    
    try:
        if windsurf_config_path.exists():
            with open(windsurf_config_path, 'r') as f:
                config = json.load(f)
                # Look for Gemini API key in the config
                # Common patterns: GEMINI_API_KEY, GOOGLE_API_KEY, or in server configs
                if 'env' in config:
                    api_key = config['env'].get('GEMINI_API_KEY')
                elif 'mcpServers' in config:
                    for server_name, server_config in config['mcpServers'].items():
                        if 'env' in server_config:
                            api_key = server_config['env'].get('GEMINI_API_KEY')
                            if api_key:
                                break
    except Exception as e:
        logging.warning(f"Warning: Could not read Windsurf MCP config: {e}")
    
    # Fallback to environment variable
    if not api_key:
        api_key = os.getenv('GEMINI_API_KEY')
    
    if not api_key or api_key == 'your-gemini-api-key-here':
        raise ValueError("GEMINI_API_KEY must be set in Windsurf MCP config or environment variables.")
    
    provider = GoogleProvider(api_key=api_key)
    logging.info("gemini 2.0 flash model initialized")
    return GoogleModel('gemini-2.0-flash', provider=provider)

# Create PydanticAI agent for PR analysis (initialized lazily)
def get_pr_analyzer():
    model = get_gemini_model()
    return Agent(
        model,
        system_prompt="""You are an expert code reviewer analyzing pull request diffs. 
        Your job is to provide a concise, informative summary of what the PR is doing.
        
        Focus on:
        - The main purpose and goal of the changes
        - Key functionality being added, modified, or removed
        - Impact on the codebase (new features, bug fixes, refactoring, etc.)
        - Any notable patterns or architectural changes
        - Only code changes that are relevant, not comments or formatting changes
        
        Provide a single paragraph summary that gives developers good context about what this PR accomplishes.
        Be specific about the changes but keep it concise and readable."""
    )

async def analyze(pr_ref, repo_path=None):
    """Analyze a PR using AI to generate an intelligent summary."""
    pr_info = get_pr_info(pr_ref, cwd=repo_path)
    pr_diff = get_pr_diff(pr_info['number'], cwd=repo_path)
    
    # Prepare context for the AI agent
    context = f"""
    PR Title: {pr_info['title']}
    PR Description: {pr_info.get('body', 'No description provided')}
    
    Files Changed: {[file['path'] for file in pr_info.get('files', [])]}
    
    Diff Content:
    {pr_diff}
    """
    
    # Get AI-generated summary
    try:
        pr_analyzer = get_pr_analyzer()
        result = await pr_analyzer.run(context)
        ai_summary = result.output
    except Exception as e:
        # Fallback to basic summary if AI fails
        logging.warning(f"AI analysis failed: {e}")
        ai_summary = f"PR #{pr_info['number']}: {pr_info['title']} - {len(pr_info.get('files', []))} files changed"
    
    return {
        'pr_number': pr_info['number'],
        'summary': ai_summary,
        'base_branch': pr_info['baseRefName']
    }