import re
from utils.github_client import get_pr_info, get_pr_diff

def analyze(pr_ref):
    pr_info = get_pr_info(pr_ref)
    pr_diff = get_pr_diff(pr_info['number'])

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

    summary = f"PR #{pr_info['number']}: {pr_info['title']}\n"
    summary += f"Files changed: {len(pr_info.get('files', []))}\n"
    summary += f"UI files: {len(ui_files)}, API files: {len(api_files)}"

    return {
        'pr_number': pr_info['number'],
        'summary': summary,
        'change_type': change_type,
        'ui_files': ui_files,
        'api_files': api_files,
        'base_branch': pr_info['baseRefName']
    }