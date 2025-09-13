import httpx
import json
import os
from utils.openapi_parser import load_spec, generate_test_data
from utils.github_client import comment_on_pr

def run_api_tests(pr_number, api_files, base_url='http://localhost:8000'):
    results = []

    openapi_path = None
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file in ['openapi.json', 'openapi.yaml', 'swagger.json']:
                openapi_path = os.path.join(root, file)
                break

    endpoints_to_test = []

    if openapi_path and os.path.exists(openapi_path):
        spec = load_spec(openapi_path)
        paths = spec.get('paths', {})

        for api_file in api_files[:3]:
            module_name = os.path.basename(api_file).replace('.py', '')
            for path, methods in paths.items():
                if module_name.lower() in path.lower():
                    for method in ['get', 'post', 'put', 'delete']:
                        if method in methods:
                            endpoints_to_test.append((method.upper(), path))

    if not endpoints_to_test:
        endpoints_to_test = [('GET', '/health'), ('GET', '/api/status')]

    with httpx.Client(base_url=base_url, timeout=5.0) as client:
        for method, path in endpoints_to_test[:5]:
            try:
                response = client.request(method, path)
                results.append({
                    'endpoint': f"{method} {path}",
                    'status': response.status_code,
                    'success': 200 <= response.status_code < 400
                })
            except Exception as e:
                results.append({
                    'endpoint': f"{method} {path}",
                    'status': 0,
                    'success': False,
                    'error': str(e)
                })

    comment = f"## API Test Results\n"
    comment += f"✅ Tested {len(results)} endpoints\n\n"
    for result in results:
        status_icon = "✅" if result['success'] else "❌"
        comment += f"{status_icon} {result['endpoint']}: {result['status']}\n"

    comment_on_pr(pr_number, comment)

    return {
        'success': any(r['success'] for r in results),
        'results': results
    }