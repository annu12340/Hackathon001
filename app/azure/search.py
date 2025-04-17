from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import Vector
import os
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class RunbookSearch:
    def __init__(self):
        self.endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
        self.key = os.getenv("AZURE_SEARCH_KEY")
        self.index_name = "runbooks"
        self.credential = AzureKeyCredential(self.key)
        self.search_client = SearchClient(
            endpoint=self.endpoint,
            index_name=self.index_name,
            credential=self.credential
        )

    async def search_runbooks(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """Search for relevant runbooks using semantic search."""
        try:
            # Convert query to vector (placeholder - implement actual vectorization)
            vector = self._get_query_vector(query)
            
            # Perform vector search
            results = self.search_client.search(
                search_text=query,
                vector=vector,
                top=top_k,
                select=["title", "content", "category", "severity"]
            )
            
            return [result for result in results]
        except Exception as e:
            logger.error(f"Error searching runbooks: {str(e)}")
            raise

    def _get_query_vector(self, query: str) -> Vector:
        """Convert query text to vector representation."""
        # TODO: Implement actual vectorization using Azure OpenAI
        # This is a placeholder implementation
        return Vector(
            value=[0.1] * 1536,  # Assuming 1536-dimensional vectors
            fields="content_vector"
        )

    def format_runbook_response(self, runbook: Dict[str, Any]) -> str:
        """Format runbook content for Slack response."""
        return f"""
*{runbook['title']}*
Category: {runbook['category']}
Severity: {runbook['severity']}

{runbook['content']}
""" 