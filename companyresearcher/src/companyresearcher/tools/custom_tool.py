import os
from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
from crewai_tools import SerperDevTool
import requests
from dotenv import load_dotenv
load_dotenv()

class LinkedInJobSearchtoolInput(BaseModel):
    """Input schema for MyCustomTool."""
    #company_founder: str = Field(..., description="Name of the company founder")
    company_name: str = Field(..., description="Name of the company")

class LinkedInJobSearchTool(BaseTool):
    name: str = "LinkedIn job opening search tool"
    description: str = (
        "Search the job opening on linkedin for the provided company and return all the current opening."
    )
    args_schema: Type[BaseModel] = LinkedInJobSearchtoolInput
    
    def _run(self, company_name: str) -> str:
        api_key = os.getenv("SERPER_API_KEY")  # Replace with your actual key
        url = "https://google.serper.dev/search"
        headers = {
            "X-API-KEY": api_key,
            "Content-Type": "application/json"
        }
        query = f"site:linkedin.com/jobs {company_name} careers"
        payload = {"q": query}
        search_results =  requests.post(url, headers=headers, json=payload)
        search_results.raise_for_status()
        data = search_results.json()
        
        if search_results.status_code == 200:
            data = search_results.json()
            results = data.get("organic", [])
            if not results:
                return "No job listings found."
            return "\n\n".join([f"{item['title']}\n{item['link']}" for item in results])
        else:
            return f"Error: {search_results.status_code}, {search_results.text}"