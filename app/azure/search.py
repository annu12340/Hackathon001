import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

# Mock runbook data
MOCK_RUNBOOKS = [
    {
        "id": "rb-001",
        "title": "Database Connection Timeout",
        "content": "1. Check database connection pool\n2. Verify network connectivity\n3. Restart database service",
        "category": "Database",
        "severity": "high",
        "tags": ["database", "connection", "timeout"]
    },
    {
        "id": "rb-002",
        "title": "API Rate Limit Exceeded",
        "content": "1. Check current rate limits\n2. Verify API key usage\n3. Implement rate limiting\n4. Contact API provider if needed",
        "category": "API",
        "severity": "medium",
        "tags": ["api", "rate-limit", "throttling"]
    },
    {
        "id": "rb-003",
        "title": "Memory Leak in Application",
        "content": "1. Monitor memory usage\n2. Check for memory leaks in code\n3. Review recent code changes\n4. Restart affected services",
        "category": "Application",
        "severity": "critical",
        "tags": ["memory", "performance", "application"]
    }
]

class RunbookSearch:
    def __init__(self):
        logger.info("Initializing RunbookSearch")
    
    def search_runbooks(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """Search for relevant runbooks using keyword matching."""
        try:
            # Remove "PagerDuty:" prefix if present
            query = query.replace("PagerDuty:", "").strip()
            query_lower = query.lower()
            
            results = []
            for runbook in MOCK_RUNBOOKS:
                # Check if query matches any part of the runbook
                if (query_lower in runbook["title"].lower() or
                    query_lower in runbook["content"].lower() or
                    query_lower in runbook["category"].lower() or
                    any(query_lower in tag.lower() for tag in runbook["tags"])):
                    results.append(runbook)
                    if len(results) >= top_k:
                        break
            
            logger.info(f"Search found {len(results)} results for query: {query}")
            return results
        except Exception as e:
            logger.error(f"Error searching runbooks: {str(e)}")
            raise

    def format_runbook_response(self, runbook: Dict[str, Any]) -> str:
        """Format runbook content for Slack response."""
        return f"""
*{runbook['title']}*
Category: {runbook['category']}
Severity: {runbook['severity']}

{runbook['content']}
""" 