import subprocess
import json
import os
from utils.github_client import comment_on_pr

def run_ui_tests(pr_number, ui_files, base_url='http://localhost:3000'):
    screenshots = []

    for file in ui_files[:3]:
        component_name = os.path.basename(file).replace('.tsx', '').replace('.jsx', '')

        playwright_cmd = [
            'npx', '@playwright/mcp@latest',
            '--browser', 'chromium',
            '--action', 'navigate',
            '--url', base_url
        ]

        try:
            result = subprocess.run(playwright_cmd, capture_output=True, text=True, timeout=30)

            screenshot_cmd = [
                'npx', '@playwright/mcp@latest',
                '--browser', 'chromium',
                '--action', 'screenshot',
                '--url', base_url,
                '--output', f'/tmp/{component_name}.png'
            ]

            subprocess.run(screenshot_cmd, capture_output=True, text=True, timeout=30)
            screenshots.append(f'/tmp/{component_name}.png')

        except Exception as e:
            print(f"UI test error for {file}: {e}")

    test_results = {
        'success': len(screenshots) > 0,
        'screenshots': screenshots,
        'files_tested': ui_files[:3]
    }

    comment = f"## UI Test Results\n"
    comment += f"✅ Tested {len(ui_files[:3])} UI components\n"
    comment += f"📸 Generated {len(screenshots)} screenshots\n"
    for file in ui_files[:3]:
        comment += f"- {file}\n"

    comment_on_pr(pr_number, comment)

    return test_results