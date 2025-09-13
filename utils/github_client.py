import subprocess
import json

def run_gh(args):
    result = subprocess.run(['gh'] + args, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"gh command failed: {result.stderr}")
    return result.stdout

def get_pr_info(pr_ref):
    if pr_ref.isdigit():
        return json.loads(run_gh(['pr', 'view', pr_ref, '--json', 'number,title,body,headRefName,baseRefName,files']))
    else:
        return json.loads(run_gh(['pr', 'view', '--json', 'number,title,body,headRefName,baseRefName,files']))

def get_pr_diff(pr_number):
    return run_gh(['pr', 'diff', str(pr_number)])

def comment_on_pr(pr_number, body):
    return run_gh(['pr', 'comment', str(pr_number), '--body', body])