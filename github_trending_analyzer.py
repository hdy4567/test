#!/usr/bin/env python3
"""
GitHub Trending Repository Analyzer

This tool analyzes trending GitHub repositories and provides detailed insights
focusing on 4 key aspects:
1. Problem Definition
2. Architecture & Tools
3. Data Flow
4. Documentation
"""

import requests
from datetime import datetime
from typing import List, Dict, Optional
import json
import time


class GitHubTrendingAnalyzer:
    """Analyzes GitHub trending repositories."""
    
    def __init__(self, github_token: Optional[str] = None):
        """Initialize the analyzer with optional GitHub token.
        
        Args:
            github_token: GitHub personal access token for higher rate limits
        """
        self.github_token = github_token
        self.headers = {
            'Accept': 'application/vnd.github.v3+json'
        }
        if github_token:
            self.headers['Authorization'] = f'token {github_token}'
    
    def get_trending_repos(self, language: str = '', since: str = 'daily', limit: int = 10) -> List[Dict]:
        """Fetch trending repositories from GitHub.
        
        Args:
            language: Programming language filter (empty for all)
            since: Time range ('daily', 'weekly', 'monthly')
            limit: Number of repositories to fetch
            
        Returns:
            List of repository information dictionaries
        """
        # Using GitHub API to search for recently popular repositories
        # We'll search for repos with high stars gained recently
        query_parts = ['stars:>100', 'sort:stars']
        
        if since == 'daily':
            query_parts.insert(0, f'created:>={self._get_date_ago(1)}')
        elif since == 'weekly':
            query_parts.insert(0, f'created:>={self._get_date_ago(7)}')
        elif since == 'monthly':
            query_parts.insert(0, f'created:>={self._get_date_ago(30)}')
        
        if language:
            query_parts.append(f'language:{language}')
        
        query = ' '.join(query_parts)
        url = f'https://api.github.com/search/repositories?q={query}&sort=stars&order=desc&per_page={limit}'
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            return data.get('items', [])
        except requests.RequestException as e:
            print(f"Error fetching trending repos: {e}")
            return []
    
    def get_repo_details(self, owner: str, repo: str) -> Dict:
        """Get detailed information about a repository.
        
        Args:
            owner: Repository owner
            repo: Repository name
            
        Returns:
            Dictionary with detailed repository information
        """
        url = f'https://api.github.com/repos/{owner}/{repo}'
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching repo details: {e}")
            return {}
    
    def get_repo_issues(self, owner: str, repo: str, state: str = 'open', limit: int = 10) -> List[Dict]:
        """Get repository issues.
        
        Args:
            owner: Repository owner
            repo: Repository name
            state: Issue state ('open', 'closed', 'all')
            limit: Number of issues to fetch
            
        Returns:
            List of issue dictionaries
        """
        url = f'https://api.github.com/repos/{owner}/{repo}/issues'
        params = {'state': state, 'per_page': limit, 'sort': 'comments', 'direction': 'desc'}
        
        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching issues: {e}")
            return []
    
    def get_readme(self, owner: str, repo: str) -> str:
        """Get repository README content.
        
        Args:
            owner: Repository owner
            repo: Repository name
            
        Returns:
            README content as string
        """
        url = f'https://api.github.com/repos/{owner}/{repo}/readme'
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Decode base64 content
            import base64
            content = base64.b64decode(data['content']).decode('utf-8')
            return content
        except requests.RequestException as e:
            print(f"Error fetching README: {e}")
            return ""
    
    def analyze_repository(self, owner: str, repo: str) -> Dict:
        """Perform comprehensive analysis of a repository.
        
        This analyzes the repo based on 4 key aspects:
        1. Problem Definition
        2. Architecture & Tools
        3. Data Flow
        4. Documentation
        
        Args:
            owner: Repository owner
            repo: Repository name
            
        Returns:
            Dictionary with analysis results
        """
        print(f"\nAnalyzing {owner}/{repo}...")
        
        # Get repo details
        details = self.get_repo_details(owner, repo)
        if not details:
            return {}
        
        # Get README
        readme = self.get_readme(owner, repo)
        
        # Get issues for discussions
        issues = self.get_repo_issues(owner, repo, state='all', limit=5)
        
        analysis = {
            'repository': f"{owner}/{repo}",
            'stars': details.get('stargazers_count', 0),
            'forks': details.get('forks_count', 0),
            'description': details.get('description', ''),
            'language': details.get('language', 'N/A'),
            'created_at': details.get('created_at', ''),
            'updated_at': details.get('updated_at', ''),
            'url': details.get('html_url', ''),
            
            # Four key analysis aspects
            'problem_definition': self._analyze_problem_definition(readme, details),
            'architecture_tools': self._analyze_architecture(readme, details),
            'data_flow': self._analyze_data_flow(readme),
            'documentation': self._analyze_documentation(readme, details),
            
            # Hot discussions
            'hot_discussions': self._analyze_discussions(issues[:3])
        }
        
        return analysis
    
    def _analyze_problem_definition(self, readme: str, details: Dict) -> Dict:
        """Analyze problem definition from README and description."""
        return {
            'description': details.get('description', ''),
            'has_problem_statement': 'problem' in readme.lower() or 'solution' in readme.lower(),
            'readme_length': len(readme),
        }
    
    def _analyze_architecture(self, readme: str, details: Dict) -> Dict:
        """Analyze architecture and tech stack."""
        # Common tech keywords
        tech_keywords = [
            'react', 'vue', 'angular', 'python', 'javascript', 'typescript',
            'docker', 'kubernetes', 'aws', 'gcp', 'azure', 'tensorflow',
            'pytorch', 'mongodb', 'postgresql', 'redis', 'node.js', 'go',
            'rust', 'java', 'spring', 'django', 'flask', 'fastapi'
        ]
        
        readme_lower = readme.lower()
        detected_tech = [tech for tech in tech_keywords if tech in readme_lower]
        
        return {
            'primary_language': details.get('language', 'N/A'),
            'detected_technologies': detected_tech[:10],  # Limit to top 10
            'has_architecture_diagram': 'architecture' in readme_lower or 'diagram' in readme_lower,
        }
    
    def _analyze_data_flow(self, readme: str) -> Dict:
        """Analyze data flow information."""
        readme_lower = readme.lower()
        
        return {
            'mentions_api': 'api' in readme_lower,
            'mentions_database': 'database' in readme_lower or 'db' in readme_lower,
            'mentions_async': 'async' in readme_lower or 'asynchronous' in readme_lower,
            'has_flow_diagram': 'flow' in readme_lower or 'pipeline' in readme_lower,
        }
    
    def _analyze_documentation(self, readme: str, details: Dict) -> Dict:
        """Analyze documentation quality."""
        readme_lower = readme.lower()
        
        return {
            'has_readme': len(readme) > 0,
            'readme_length': len(readme),
            'has_installation': 'install' in readme_lower,
            'has_usage': 'usage' in readme_lower or 'example' in readme_lower,
            'has_contributing': 'contribut' in readme_lower,
            'has_license': details.get('license') is not None,
            'open_issues': details.get('open_issues_count', 0),
        }
    
    def _analyze_discussions(self, issues: List[Dict]) -> List[Dict]:
        """Analyze hot discussions from issues."""
        discussions = []
        
        for issue in issues:
            if 'pull_request' not in issue:  # Skip pull requests
                discussions.append({
                    'title': issue.get('title', ''),
                    'number': issue.get('number', 0),
                    'comments': issue.get('comments', 0),
                    'state': issue.get('state', ''),
                    'url': issue.get('html_url', ''),
                    'created_at': issue.get('created_at', ''),
                })
        
        return discussions
    
    def generate_report(self, analyses: List[Dict]) -> str:
        """Generate a formatted analysis report.
        
        Args:
            analyses: List of analysis dictionaries
            
        Returns:
            Formatted report string
        """
        report_lines = []
        report_lines.append("🔥 GitHub Trending Repository Analysis Report")
        report_lines.append("=" * 80)
        report_lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append("\n")
        
        for i, analysis in enumerate(analyses, 1):
            report_lines.append(f"\n{'='*80}")
            report_lines.append(f"📊 Repository {i}: {analysis['repository']}")
            report_lines.append(f"{'='*80}\n")
            
            # Basic Info
            report_lines.append("📌 Basic Information")
            report_lines.append(f"   ⭐ Stars: {analysis['stars']:,}")
            report_lines.append(f"   🔱 Forks: {analysis['forks']:,}")
            report_lines.append(f"   💬 Language: {analysis['language']}")
            report_lines.append(f"   📝 Description: {analysis['description']}")
            report_lines.append(f"   🔗 URL: {analysis['url']}\n")
            
            # Problem Definition
            prob_def = analysis['problem_definition']
            report_lines.append("🎯 #1 Problem Definition")
            report_lines.append(f"   • Has clear problem statement: {'✅' if prob_def['has_problem_statement'] else '❌'}")
            report_lines.append(f"   • README length: {prob_def['readme_length']:,} characters\n")
            
            # Architecture & Tools
            arch = analysis['architecture_tools']
            report_lines.append("🏗️ #2 Architecture & Tools")
            report_lines.append(f"   • Primary language: {arch['primary_language']}")
            if arch['detected_technologies']:
                report_lines.append(f"   • Detected technologies: {', '.join(arch['detected_technologies'])}")
            report_lines.append(f"   • Has architecture diagram: {'✅' if arch['has_architecture_diagram'] else '❌'}\n")
            
            # Data Flow
            flow = analysis['data_flow']
            report_lines.append("🔄 #3 Data Flow")
            report_lines.append(f"   • Mentions API: {'✅' if flow['mentions_api'] else '❌'}")
            report_lines.append(f"   • Mentions Database: {'✅' if flow['mentions_database'] else '❌'}")
            report_lines.append(f"   • Mentions Async: {'✅' if flow['mentions_async'] else '❌'}")
            report_lines.append(f"   • Has flow diagram: {'✅' if flow['has_flow_diagram'] else '❌'}\n")
            
            # Documentation
            docs = analysis['documentation']
            report_lines.append("📚 #4 Documentation")
            report_lines.append(f"   • Has README: {'✅' if docs['has_readme'] else '❌'}")
            report_lines.append(f"   • Has installation guide: {'✅' if docs['has_installation'] else '❌'}")
            report_lines.append(f"   • Has usage examples: {'✅' if docs['has_usage'] else '❌'}")
            report_lines.append(f"   • Has contributing guide: {'✅' if docs['has_contributing'] else '❌'}")
            report_lines.append(f"   • Has license: {'✅' if docs['has_license'] else '❌'}")
            report_lines.append(f"   • Open issues: {docs['open_issues']}\n")
            
            # Hot Discussions
            if analysis['hot_discussions']:
                report_lines.append("💬 Hot Discussions")
                for j, disc in enumerate(analysis['hot_discussions'][:3], 1):
                    report_lines.append(f"   {j}. {disc['title']}")
                    report_lines.append(f"      • Issue #{disc['number']} | {disc['comments']} comments | {disc['state']}")
                    report_lines.append(f"      • {disc['url']}")
                report_lines.append("")
        
        report_lines.append("\n" + "=" * 80)
        report_lines.append("Report generated by GitHub Trending Analyzer")
        report_lines.append("=" * 80)
        
        return "\n".join(report_lines)
    
    def _get_date_ago(self, days: int) -> str:
        """Get date string for N days ago."""
        from datetime import timedelta
        date = datetime.now() - timedelta(days=days)
        return date.strftime('%Y-%m-%d')


def main():
    """Main function to run the analyzer."""
    print("🚀 GitHub Trending Repository Analyzer")
    print("=" * 80)
    
    # Initialize analyzer
    # You can set GITHUB_TOKEN environment variable for higher rate limits
    import os
    token = os.environ.get('GITHUB_TOKEN')
    analyzer = GitHubTrendingAnalyzer(github_token=token)
    
    # Get trending repositories
    print("\n📊 Fetching trending repositories...")
    trending_repos = analyzer.get_trending_repos(language='', since='daily', limit=5)
    
    if not trending_repos:
        print("❌ No trending repositories found.")
        return
    
    print(f"✅ Found {len(trending_repos)} trending repositories\n")
    
    # Analyze top 2 repositories
    analyses = []
    for repo in trending_repos[:2]:
        owner = repo['owner']['login']
        name = repo['name']
        
        # Avoid rate limiting
        time.sleep(1)
        
        analysis = analyzer.analyze_repository(owner, name)
        if analysis:
            analyses.append(analysis)
    
    # Generate report
    if analyses:
        report = analyzer.generate_report(analyses)
        print("\n" + report)
        
        # Save to file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'github_trending_analysis_{timestamp}.txt'
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"\n💾 Report saved to: {filename}")
        
        # Save JSON version
        json_filename = f'github_trending_analysis_{timestamp}.json'
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(analyses, f, indent=2, ensure_ascii=False)
        print(f"💾 JSON data saved to: {json_filename}")
    else:
        print("❌ No analyses completed.")


if __name__ == '__main__':
    main()
