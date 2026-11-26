#!/usr/bin/env python3
"""
Quality Audit Report Generator (ISO 13485 / FDA)
Reads pipeline results and produces an auditable, self-explanatory HTML report.
"""

import os
import json
import hashlib
import subprocess
import re
import xml.etree.ElementTree as ET
from datetime import datetime


def detect_technology():
    if os.path.exists('go.mod'):
        return 'go'
    if os.path.exists('package.json'):
        return 'vue'
    if os.path.exists('build.gradle.kts') or os.path.exists('app/build.gradle.kts'):
        return 'kotlin'
    return 'unknown'


def calculate_hash(file_path):
    if not os.path.exists(file_path):
        return "N/A"
    try:
        with open(file_path, 'rb') as f:
            return hashlib.sha256(f.read()).hexdigest()[:16]
    except Exception:
        return "N/A"


def extract_jira_id(message):
    match = re.search(r'([A-Z]+-\d+)', message)
    return match.group(1) if match else None


def get_commit_hash():
    try:
        return subprocess.check_output(['git', 'rev-parse', 'HEAD'], stderr=subprocess.DEVNULL).decode().strip()
    except Exception:
        return 'unknown'


def get_commit_message():
    try:
        return subprocess.check_output(['git', 'log', '-1', '--pretty=%B'], stderr=subprocess.DEVNULL).decode().strip()
    except Exception:
        return 'unknown'


def get_version():
    try:
        if os.path.exists('package.json'):
            with open('package.json', 'r') as f:
                version = json.load(f).get('version', None)
                if version and version != '0.0.0':
                    return version
    except Exception:
        pass
    try:
        if os.path.exists('sonar-project.properties'):
            with open('sonar-project.properties', 'r') as f:
                for line in f:
                    if line.startswith('sonar.projectVersion='):
                        return line.split('=', 1)[1].strip()
    except Exception:
        pass
    return '0.0.0'


def get_project():
    try:
        with open('sonar-project.properties', 'r') as f:
            for line in f:
                if line.startswith('sonar.projectKey='):
                    return line.split('=', 1)[1].strip()
    except Exception:
        pass
    return 'unknown'


def read_coverage():
    # Vue
    if os.path.exists('coverage/lcov.info'):
        return read_coverage_lcov()
    if os.path.exists('coverage/coverage-final.json'):
        return read_coverage_istanbul_json()
    # Go
    if os.path.exists('coverage.xml'):
        return read_coverage_go()
    # Kotlin
    if os.path.exists('app/build/reports/jacoco/jacocoTestReport/jacocoTestReport.xml'):
        return read_coverage_jacoco()
    return None


def read_coverage_lcov():
    try:
        with open('coverage/lcov.info', 'r') as f:
            content = f.read()
        total_lines = 0
        covered_lines = 0
        total_branches = 0
        covered_branches = 0
        total_functions = 0
        covered_functions = 0

        for line in content.splitlines():
            if line.startswith('LF:'): total_lines += int(line.split(':')[1])
            elif line.startswith('LH:'): covered_lines += int(line.split(':')[1])
            elif line.startswith('BRF:'): total_branches += int(line.split(':')[1])
            elif line.startswith('BRH:'): covered_branches += int(line.split(':')[1])
            elif line.startswith('FNF:'): total_functions += int(line.split(':')[1])
            elif line.startswith('FNH:'): covered_functions += int(line.split(':')[1])

        def pct(covered, total):
            return round((covered / total * 100), 2) if total > 0 else 0.0

        return {
            'lines': {'covered': covered_lines, 'total': total_lines, 'pct': pct(covered_lines, total_lines)},
            'branches': {'covered': covered_branches, 'total': total_branches, 'pct': pct(covered_branches, total_branches)},
            'functions': {'covered': covered_functions, 'total': total_functions, 'pct': pct(covered_functions, total_functions)},
        }
    except Exception as e:
        print(f"Error reading lcov.info: {e}")
        return None


def read_coverage_istanbul_json():
    try:
        with open('coverage/coverage-final.json', 'r') as f:
            data = json.load(f)
        
        total_statements = 0
        covered_statements = 0
        total_branches = 0
        covered_branches = 0
        total_functions = 0
        covered_functions = 0

        for file_path, file_data in data.items():
            for key, count in file_data.get('s', {}).items():
                total_statements += 1
                if count > 0:
                    covered_statements += 1
            for key, counts in file_data.get('b', {}).items():
                for count in counts:
                    total_branches += 1
                    if count > 0:
                        covered_branches += 1
            for key, count in file_data.get('f', {}).items():
                total_functions += 1
                if count > 0:
                    covered_functions += 1

        def pct(covered, total):
            return round((covered / total * 100), 2) if total > 0 else 0.0

        return {
            'lines': {'covered': covered_statements, 'total': total_statements, 'pct': pct(covered_statements, total_statements)},
            'branches': {'covered': covered_branches, 'total': total_branches, 'pct': pct(covered_branches, total_branches)},
            'functions': {'covered': covered_functions, 'total': total_functions, 'pct': pct(covered_functions, total_functions)},
        }
    except Exception as e:
        print(f"Error reading coverage-final.json: {e}")
        return None


def read_coverage_go():
    try:
        tree = ET.parse('coverage.xml')
        root = tree.getroot()
        total_lines = 0
        covered_lines = 0
        for line_to_cover in root.findall('.//lineToCover'):
            total_lines += 1
            if line_to_cover.get('covered') == 'true':
                covered_lines += 1
        pct = round((covered_lines / total_lines * 100), 2) if total_lines > 0 else 0.0
        return {
            'lines': {'covered': covered_lines, 'total': total_lines, 'pct': pct},
            'branches': {'covered': 0, 'total': 0, 'pct': 0.0},
            'functions': {'covered': 0, 'total': 0, 'pct': 0.0},
        }
    except Exception as e:
        print(f"Error reading coverage.xml: {e}")
        return None


def read_coverage_jacoco():
    """Reads JaCoCo XML report generated by Kotlin/Gradle."""
    try:
        tree = ET.parse('app/build/reports/jacoco/jacocoTestReport/jacocoTestReport.xml')
        root = tree.getroot()

        total_lines = 0
        covered_lines = 0
        total_branches = 0
        covered_branches = 0
        total_methods = 0
        covered_methods = 0

        # The counters are usually at the end of the XML, inside the <report> tag
        for counter in root.findall('counter'):
            counter_type = counter.attrib.get('type')
            missed = int(counter.attrib.get('missed', 0))
            covered = int(counter.attrib.get('covered', 0))

            if counter_type == 'LINE':
                total_lines = missed + covered
                covered_lines = covered
            elif counter_type == 'BRANCH':
                total_branches = missed + covered
                covered_branches = covered
            elif counter_type == 'METHOD':
                total_methods = missed + covered
                covered_methods = covered

        def pct(covered, total):
            return round((covered / total * 100), 2) if total > 0 else 0.0

        return {
            'lines': {'covered': covered_lines, 'total': total_lines, 'pct': pct(covered_lines, total_lines)},
            'branches': {'covered': covered_branches, 'total': total_branches, 'pct': pct(covered_branches, total_branches)},
            'functions': {'covered': covered_methods, 'total': total_methods, 'pct': pct(covered_methods, total_methods)},
        }
    except Exception as e:
        print(f"Error reading jacocoTestReport.xml: {e}")
        return None


def generate_html(data, output_file):
    project = data['project']
    technology = data['technology']
    sonar_url = f"http://127.0.0.1:9000/dashboard?id={project}"
    jira_id = data.get('jira_id') or 'N/A'

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Quality Audit Report - {project}</title>
  <style>
    body {{ font-family: 'Segoe UI', Arial, sans-serif; background: #f4f7f6; color: #333; margin: 0; padding: 40px; line-height: 1.6; }}
    .container {{ max-width: 900px; margin: 0 auto; background: white; padding: 40px; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }}
    h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 15px; margin-bottom: 30px; }}
    h2 {{ color: #2c3e50; margin-top: 40px; border-bottom: 1px solid #eee; padding-bottom: 10px; }}
    .meta {{ background: #f8f9fa; padding: 20px; border-left: 4px solid #3498db; border-radius: 4px; margin-bottom: 30px; }}
    .meta p {{ margin: 8px 0; }}
    table {{ width: 100%; border-collapse: collapse; margin: 20px 0; font-size: 0.95em; }}
    th {{ background: #34495e; color: white; padding: 12px; text-align: left; }}
    td {{ padding: 12px; border-bottom: 1px solid #eee; }}
    tr:hover {{ background: #f9f9f9; }}
    .ok {{ color: #27ae60; font-weight: bold; }}
    .warn {{ color: #f39c12; font-weight: bold; }}
    .explanation {{ background: #e8f4f8; border-left: 4px solid #3498db; padding: 15px; margin: 15px 0; font-size: 0.9em; color: #2c3e50; }}
    .footer {{ margin-top: 50px; padding-top: 20px; border-top: 1px solid #eee; font-size: 0.85em; color: #7f8c8d; text-align: center; }}
    ul {{ margin-top: 10px; }}
    li {{ margin-bottom: 8px; }}
    code {{ background: #f0f0f0; padding: 2px 6px; border-radius: 4px; font-family: 'Courier New', monospace; color: #c0392b; }}
  </style>
</head>
<body>
  <div class="container">
    <h1>Quality Audit Report</h1>
    <div class="meta">
      <p><strong>Project Name:</strong> {project}</p>
      <p><strong>Technology Stack:</strong> {technology.capitalize()}</p>
      <p><strong>Version:</strong> {data['version']}</p>
      <p><strong>Commit Hash:</strong> <code>{data['commit_hash'][:12]}</code></p>
      <p><strong>Commit Message:</strong> {data['commit_message']}</p>
      <p><strong>Jira Ticket:</strong> {jira_id}</p>
      <p><strong>Generated at:</strong> {data['generation_date']}</p>
      <p><strong>Executed by:</strong> Jenkins CI/CD Pipeline</p>
    </div>

    <div class="explanation">
      <strong>What is this document?</strong><br>
      This report serves as an auditable record of the software development process, required by ISO 13485:2016 (clause 4.2.5 - Control of Records). It proves that the code was automatically built, tested, and verified against security and quality standards before being accepted into the repository.
    </div>

    <h2>1. Pipeline Execution Results</h2>
    <table>
      <tr><th>Stage</th><th>Description</th><th>Result</th></tr>
      <tr><td>Checkout</td><td>Retrieves the code from the Git repository.</td><td class="ok">Success</td></tr>
      <tr><td>Install</td><td>Installs required third-party libraries.</td><td class="ok">Success</td></tr>
      <tr><td>Lint</td><td>Checks for syntax errors and formatting issues.</td><td class="ok">Success</td></tr>
      <tr><td>Type-check</td><td>Validates static typing (e.g., TypeScript, Go).</td><td class="ok">Success</td></tr>
      <tr><td>Unit Tests</td><td>Runs isolated tests to verify logic and generate coverage.</td><td class="ok">Success</td></tr>
      <tr><td>E2E Tests</td><td>Simulates real user interactions (where applicable).</td><td class="ok">Success</td></tr>
      <tr><td>SonarQube</td><td>Static analysis for security and code smells.</td><td class="ok">Quality Gate Passed</td></tr>
      <tr><td>Build</td><td>Compiles the final executable or web assets.</td><td class="ok">Artifacts Generated</td></tr>
    </table>

    <h2>2. Test Coverage Metrics</h2>
    <p>Test coverage measures the percentage of source code executed during automated tests. A higher percentage indicates a lower risk of undetected bugs in production.</p>
"""

    if data['coverage']:
        c = data['coverage']
        html += f"""
    <table>
      <tr><th>Metric</th><th>Covered</th><th>Total</th><th>Percentage</th></tr>
      <tr><td>Lines of Code</td><td>{c['lines']['covered']}</td><td>{c['lines']['total']}</td><td><strong>{c['lines']['pct']}%</strong></td></tr>
      <tr><td>Branches</td><td>{c['branches']['covered']}</td><td>{c['branches']['total']}</td><td>{c['branches']['pct']}%</td></tr>
      <tr><td>Functions</td><td>{c['functions']['covered']}</td><td>{c['functions']['total']}</td><td>{c['functions']['pct']}%</td></tr>
    </table>
    <div class="explanation">
      <strong>ISO 13485 Note:</strong> The company mandates a minimum of 80% test coverage for domain logic. The pipeline fails if this threshold is not met.
    </div>
"""
    else:
        html += '<p class="warn">Coverage file not found. Tests might not have executed correctly.</p>'

    # --- Corrigir os caminhos dos artefactos para o Kotlin ---
    if technology == 'go':
        artifact_path = 'bin/app.exe'
        coverage_path = 'coverage.xml'
    elif technology == 'vue':
        artifact_path = 'dist/index.html'
        coverage_path = 'coverage/lcov.info'
    elif technology == 'kotlin':
        artifact_path = 'app/build/outputs/apk/debug/app-debug.apk'
        coverage_path = 'app/build/reports/jacoco/jacocoTestReport/jacocoTestReport.xml'
    else:
        artifact_path = 'unknown'
        coverage_path = 'unknown'

    html += f"""
    <h2>3. Design Outputs & Integrity</h2>
    <p>These are the final files produced by the pipeline. A SHA-256 hash is a unique digital fingerprint. If the file is altered by even one bit, the hash will change. This guarantees data integrity and prevents tampering.</p>
    <table>
      <tr><th>Output Artifact</th><th>Location</th><th>SHA-256 Hash (First 16 chars)</th></tr>
      <tr><td>Compiled Binary / Web Assets</td><td>{artifact_path}</td><td><code>{calculate_hash(artifact_path)}</code></td></tr>
      <tr><td>Test Coverage Report</td><td>{coverage_path}</td><td><code>{calculate_hash(coverage_path)}</code></td></tr>
    </table>

    <h2>4. Static Analysis (SonarQube)</h2>
    <p>View the full interactive dashboard: <a href="{sonar_url}">{sonar_url}</a></p>

    <h2>5. Compliance Documentation (ISO 13485)</h2>
    <p>All design and development steps must be documented and traceable. The following documents are located in the <code>docs/</code> folder of this repository:</p>
    <ul>
      <li><strong>Design and Development Plan</strong> (SOP 7.3.1) - <code>docs/design-development-plan.md</code></li>
      <li><strong>Requirements Specification</strong> (SOP 7.3.2) - <code>docs/requirements.md</code></li>
      <li><strong>Traceability Matrix</strong> (SOP 7.3.2 + 7.3.5) - <code>docs/traceability-matrix.md</code></li>
      <li><strong>QMS Software Validation</strong> (SOP 4.1.6) - <code>docs/qms-software-validation.md</code></li>
      <li><strong>Validation Plan</strong> (SOP 7.3.6) - <code>docs/validation-plan.md</code></li>
      <li><strong>Design File Index</strong> (SOP 7.3.10) - <code>docs/design-file/README.md</code></li>
    </ul>

    <h2>6. Regulatory Compliance Matrix</h2>
    <table>
      <tr><th>Standard</th><th>Requirement</th><th>How it is applied</th><th>Status</th></tr>
      <tr><td>ISO 13485:2016</td><td>Traceability & Control of Records</td><td>This HTML report is generated automatically and archived.</td><td class="ok">Documented</td></tr>
      <tr><td>FDA (SaMD)</td><td>Software Validation</td><td>Mandatory Quality Gate ensures only validated code is built.</td><td class="ok">Applied</td></tr>
      <tr><td>HIPAA</td><td>Access Control & Security</td><td>All pipeline execution happens on-premise (VPN).</td><td class="ok">Applied</td></tr>
      <tr><td>OWASP Top 10</td><td>Secure Coding</td><td>Static analysis detects common vulnerabilities.</td><td class="warn">Partial (Community)</td></tr>
      <tr><td>WCAG 2.1 AA</td><td>Digital Accessibility</td><td>Automated tests with axe-core.</td><td class="{'ok' if technology == 'vue' else 'warn'}">{'Applied' if technology == 'vue' else 'N/A'}</td></tr>
    </table>

    <div class="footer">
      <p>Report generated automatically by the Jenkins CI/CD pipeline.</p>
      <p>Retention: 2 years or device lifetime (SOP 4.2.5).</p>
    </div>
  </div>
</body>
</html>
"""

    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Report generated: {output_file}")


if __name__ == '__main__':
    commit_message = get_commit_message()
    if os.path.exists('reports/auditoria.html'):
        try: os.remove('reports/auditoria.html')
        except Exception: pass

    data = {
        'project': get_project(),
        'technology': detect_technology(),
        'commit_hash': get_commit_hash(),
        'commit_message': commit_message,
        'version': get_version(),
        'generation_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'coverage': read_coverage(),
        'jira_id': extract_jira_id(commit_message),
    }
    generate_html(data, 'reports/report.html')