#!/usr/bin/env python3
"""
Simple CVE Team Dashboard Generator for GitHub Pages
Usage: python3 generate_dashboard.py [filter_url]
"""

import os
import sys
import requests
import base64
from datetime import datetime
import re
from urllib.parse import urlparse, parse_qs, unquote

# Load .env file manually (same method as verify_on_qa)
env_path = os.path.expanduser("~/.claude/.env")
if os.path.exists(env_path):
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                value = value.strip().strip('"').strip("'")
                os.environ[key.strip()] = value

JIRA_BASE_URL = os.getenv('JIRA_BASE_URL', 'https://redhat.atlassian.net')
JIRA_USER_EMAIL = os.getenv('JIRA_USER_EMAIL')
JIRA_API_TOKEN = os.getenv('JIRA_API_TOKEN')

def get_jira_headers():
    """Get Jira auth headers"""
    if not JIRA_USER_EMAIL or not JIRA_API_TOKEN:
        print("❌ Error: Set JIRA_USER_EMAIL and JIRA_API_TOKEN in ~/.claude/.env")
        sys.exit(1)

    b64_auth = base64.b64encode(f'{JIRA_USER_EMAIL}:{JIRA_API_TOKEN}'.encode()).decode()
    return {
        'Authorization': f'Basic {b64_auth}',
        'Content-Type': 'application/json'
    }

def extract_jql_from_filter_url(filter_url):
    """Extract JQL query from Jira filter URL"""
    parsed = urlparse(filter_url)
    query_params = parse_qs(parsed.query)

    if 'jql' in query_params:
        return unquote(query_params['jql'][0])

    # If no JQL in URL, use default
    return 'assignee = currentUser() AND issuetype = Tracker ORDER BY duedate ASC'

def fetch_tickets(jql):
    """Fetch CVE tracker tickets from Jira"""
    headers = get_jira_headers()

    print(f"🔍 Fetching tickets with JQL: {jql[:100]}...")

    url = f"{JIRA_BASE_URL}/rest/api/3/search/jql"
    params = {
        'jql': jql,
        'fields': 'key,summary,assignee,status,duedate,priority',
        'maxResults': 100
    }

    all_issues = []

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        all_issues.extend(data.get('issues', []))

        # Handle pagination
        while not data.get('isLast', True) and data.get('nextPageToken'):
            params['nextPageToken'] = data['nextPageToken']
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            all_issues.extend(data.get('issues', []))

        print(f"✅ Fetched {len(all_issues)} tickets")
        return all_issues

    except requests.exceptions.HTTPError as e:
        print(f"❌ Error: {e.response.status_code}")
        print(e.response.text)
        sys.exit(1)

def process_data(issues):
    """Process Jira issues into simple data structure"""
    data = []
    for issue in issues:
        fields = issue['fields']
        key = issue['key']
        summary = fields.get('summary', '')

        # Extract CVE ID
        cve_match = re.search(r'CVE-\d{4}-\d+', summary)
        cve_id = cve_match.group(0) if cve_match else 'N/A'

        # Extract version
        version_match = re.search(r'\[cnv-([\d.]+)\]', summary)
        version = version_match.group(1) if version_match else 'N/A'

        # Extract PS Component
        ps_component_match = re.search(r'container-native-virtualization/([\w-]+):', summary)
        ps_component = ps_component_match.group(1) if ps_component_match else 'N/A'

        data.append({
            'assignee': fields.get('assignee', {}).get('displayName', 'Unassigned') if fields.get('assignee') else 'Unassigned',
            'cve_id': cve_id,
            'jira_id': key,
            'jira_link': f"{JIRA_BASE_URL}/browse/{key}",
            'ps_component': ps_component,
            'title': summary,
            'version': version,
            'due_date': fields.get('duedate', 'No Due Date'),
            'status': fields.get('status', {}).get('name', 'Unknown'),
            'priority': fields.get('priority', {}).get('name', 'N/A')
        })

    return data

def generate_html(data, output_file='index.html'):
    """Generate standalone HTML dashboard"""

    total = len(data)
    by_assignee = {}
    by_status = {}
    overdue = 0

    today = datetime.now().date()

    for item in data:
        by_assignee[item['assignee']] = by_assignee.get(item['assignee'], 0) + 1
        by_status[item['status']] = by_status.get(item['status'], 0) + 1

        if item['due_date'] != 'No Due Date':
            try:
                due = datetime.strptime(item['due_date'], '%Y-%m-%d').date()
                if due < today and item['status'] not in ['Verified', 'Closed']:
                    overdue += 1
            except:
                pass

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CVE Team Dashboard</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif; background: #f5f7fa; padding: 20px; }}
        .container {{ max-width: 1400px; margin: 0 auto; }}
        h1 {{ color: #2c3e50; margin-bottom: 10px; }}
        .updated {{ color: #7f8c8d; font-size: 14px; margin-bottom: 30px; }}
        .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 30px; }}
        .stat-card {{ background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
        .stat-card h3 {{ color: #7f8c8d; font-size: 14px; margin-bottom: 10px; text-transform: uppercase; }}
        .stat-number {{ font-size: 32px; font-weight: bold; color: #2c3e50; }}
        .stat-number.red {{ color: #e74c3c; }}
        .filters {{ background: white; padding: 15px; border-radius: 8px; margin-bottom: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
        .filters input, .filters select {{ padding: 8px 12px; border: 1px solid #ddd; border-radius: 4px; margin-right: 10px; }}
        .table-container {{ background: white; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); overflow: hidden; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th {{ background: #34495e; color: white; padding: 12px; text-align: left; font-weight: 600; position: sticky; top: 0; }}
        td {{ padding: 12px; border-bottom: 1px solid #ecf0f1; font-size: 14px; }}
        tr:hover {{ background: #f8f9fa; }}
        .status {{ padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: 600; display: inline-block; }}
        .status-ON_QA {{ background: #fff3cd; color: #856404; }}
        .status-MODIFIED {{ background: #d4edda; color: #155724; }}
        .status-Verified {{ background: #d1ecf1; color: #0c5460; }}
        .status-NEW {{ background: #f8d7da; color: #721c24; }}
        .status-ASSIGNED {{ background: #cce5ff; color: #004085; }}
        a {{ color: #3498db; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
        .priority-Blocker, .priority-Critical {{ color: #e74c3c; font-weight: bold; }}
        .priority-Major {{ color: #f39c12; }}
        @media print {{ body {{ background: white; }} .filters {{ display: none; }} }}
    </style>
</head>
<body>
    <div class="container">
        <h1>CVE Team Dashboard</h1>
        <div class="updated">Last updated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</div>

        <div class="stats">
            <div class="stat-card">
                <h3>Total Tickets</h3>
                <div class="stat-number">{total}</div>
            </div>
            <div class="stat-card">
                <h3>Overdue</h3>
                <div class="stat-number red">{overdue}</div>
            </div>
"""

    for assignee, count in sorted(by_assignee.items(), key=lambda x: x[1], reverse=True)[:4]:
        html += f"""            <div class="stat-card">
                <h3>{assignee}</h3>
                <div class="stat-number">{count}</div>
            </div>
"""

    html += """        </div>

        <div class="filters">
            <input type="text" id="search" placeholder="Search..." onkeyup="filterTable()">
            <select id="assigneeFilter" onchange="filterTable()">
                <option value="">All Assignees</option>
"""

    for assignee in sorted(by_assignee.keys()):
        html += f'                <option value="{assignee}">{assignee}</option>\n'

    html += """            </select>
            <select id="statusFilter" onchange="filterTable()">
                <option value="">All Statuses</option>
"""

    for status in sorted(by_status.keys()):
        html += f'                <option value="{status}">{status}</option>\n'

    html += """            </select>
        </div>

        <div class="table-container">
            <table id="dataTable">
                <thead>
                    <tr>
                        <th>Assignee</th>
                        <th>CVE ID</th>
                        <th>Jira ID</th>
                        <th>PS Component</th>
                        <th>Version</th>
                        <th>Due Date</th>
                        <th>Status</th>
                        <th>Priority</th>
                    </tr>
                </thead>
                <tbody>
"""

    for item in data:
        status_class = item['status'].replace(' ', '_')
        priority_class = item['priority'].replace(' ', '_')

        html += f"""                    <tr>
                        <td>{item['assignee']}</td>
                        <td>{item['cve_id']}</td>
                        <td><a href="{item['jira_link']}" target="_blank">{item['jira_id']}</a></td>
                        <td>{item['ps_component']}</td>
                        <td>{item['version']}</td>
                        <td>{item['due_date']}</td>
                        <td><span class="status status-{status_class}">{item['status']}</span></td>
                        <td class="priority-{priority_class}">{item['priority']}</td>
                    </tr>
"""

    html += """                </tbody>
            </table>
        </div>
    </div>

    <script>
        function filterTable() {
            const search = document.getElementById('search').value.toLowerCase();
            const assignee = document.getElementById('assigneeFilter').value;
            const status = document.getElementById('statusFilter').value;
            const rows = document.querySelectorAll('#dataTable tbody tr');

            rows.forEach(row => {
                const text = row.textContent.toLowerCase();
                const rowAssignee = row.cells[0].textContent;
                const rowStatus = row.cells[6].textContent;

                const matchSearch = !search || text.includes(search);
                const matchAssignee = !assignee || rowAssignee === assignee;
                const matchStatus = !status || rowStatus === status;

                row.style.display = matchSearch && matchAssignee && matchStatus ? '' : 'none';
            });
        }
    </script>
</body>
</html>
"""

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"✅ Dashboard created: {output_file}")
    return os.path.abspath(output_file)

def main():
    print("=" * 60)
    print(" CVE Team Dashboard Generator")
    print("=" * 60)

    # Get filter URL from command line, env var, or use default
    if len(sys.argv) > 1:
        filter_url = sys.argv[1]
    elif os.getenv('JIRA_DASHBOARD_FILTER_URL'):
        filter_url = os.getenv('JIRA_DASHBOARD_FILTER_URL')
        print(f"📋 Using JIRA_DASHBOARD_FILTER_URL from .env")
    elif os.getenv('JIRA_FILTER_URL'):
        filter_url = os.getenv('JIRA_FILTER_URL')
        print(f"📋 Using JIRA_FILTER_URL from .env")
    else:
        # Default: all your tracker tickets
        filter_url = None
        print(f"📋 Using default JQL for your tickets")

    if filter_url:
        print(f"📋 Filter URL: {filter_url}")
        # Extract JQL from filter URL
        jql = extract_jql_from_filter_url(filter_url)
    else:
        # Default JQL
        jql = 'assignee = currentUser() AND issuetype = Tracker ORDER BY duedate ASC'

    # Fetch tickets
    issues = fetch_tickets(jql)

    if not issues:
        print("\n⚠️  No tickets found. The dashboard will be empty.")
        print("💡 Try a different filter URL or check your permissions.")

    # Process and generate
    data = process_data(issues)
    output_path = generate_html(data)

    print("\n" + "=" * 60)
    print("✅ Done!")
    print("=" * 60)
    print(f"\n📄 File: {output_path}")
    print(f"\n💡 To view: Open in browser or upload to GitHub Pages")
    print(f"\n💡 To update: python3 generate_dashboard.py [filter_url]")

if __name__ == '__main__':
    main()
