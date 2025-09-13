import subprocess
import json
import os

def run_gh(args, cwd=None):
    """Run gh command with optional working directory."""
    if cwd is None:
        cwd = os.getcwd()
    
    result = subprocess.run(['gh'] + args, capture_output=True, text=True, cwd=cwd)
    if result.returncode != 0:
        raise Exception(f"gh command failed: {result.stderr}")
    return result.stdout

def get_pr_info(pr_ref, cwd=None):
    if pr_ref.isdigit():
        return json.loads(run_gh(['pr', 'view', pr_ref, '--json', 'number,title,body,headRefName,baseRefName,files'], cwd=cwd))
    else:
        return json.loads(run_gh(['pr', 'view', '--json', 'number,title,body,headRefName,baseRefName,files'], cwd=cwd))

def get_pr_diff(pr_number, cwd=None):
    return run_gh(['pr', 'diff', str(pr_number)], cwd=cwd)

def comment_on_pr(pr_number, body, cwd=None):
    return run_gh(['pr', 'comment', str(pr_number), '--body', body], cwd=cwd)