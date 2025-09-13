import os
from pydantic_ai import Agent
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.google import GoogleProvider
from utils.github_client import get_pr_info, get_pr_diff

# Initialize Gemini 2.5 Pro model - API key comes from MCP config env vars
def get_gemini_model():
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key or api_key == 'your-gemini-api-key-here':
        raise ValueError("GEMINI_API_KEY must be set in MCP config. Please update .mcp/config.json with your actual API key.")
    provider = GoogleProvider(api_key=api_key)
    return GoogleModel('gemini-2.5-pro', provider=provider)

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
        
        Provide a single paragraph summary that gives developers good context about what this PR accomplishes.
        Be specific about the changes but keep it concise and readable."""
    )

def analyze(pr_ref):
    """Analyze a PR using AI to generate an intelligent summary."""
    pr_info = get_pr_info(pr_ref)
    pr_diff = get_pr_diff(pr_info['number'])
    
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
        result = pr_analyzer.run_sync(context)
        ai_summary = result.data
    except Exception as e:
        # Fallback to basic summary if AI fails
        ai_summary = f"PR #{pr_info['number']}: {pr_info['title']} - {len(pr_info.get('files', []))} files changed"
    
    # Categorize files for compatibility
    ui_files = []
    api_files = []
    
    for file in pr_info.get('files', []):
        name = file['path']
        if name.endswith(('.tsx', '.jsx', '.js')) and not name.endswith('.test.js'):
            ui_files.append(name)
        elif name.endswith('.py'):
            api_files.append(name)
    
    change_type = 'none'
    if ui_files and api_files:
        change_type = 'both'
    elif ui_files:
        change_type = 'ui'
    elif api_files:
        change_type = 'api'
    
    return {
        'pr_number': pr_info['number'],
        'summary': ai_summary,
        'change_type': change_type,
        'ui_files': ui_files,
        'api_files': api_files,
        'base_branch': pr_info['baseRefName']
    }