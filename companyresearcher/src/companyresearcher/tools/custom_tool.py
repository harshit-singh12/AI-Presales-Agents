import os
from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
from crewai_tools import SerperDevTool
import requests
from dotenv import load_dotenv
load_dotenv()

class LinkedInSearchtoolInput(BaseModel):
    """Input schema for MyCustomTool."""
    #company_founder: str = Field(..., description="Name of the company founder")
    company_name: str = Field(..., description="Name of the company")

class LinkedInSearchTool(BaseTool):
    name: str = "LinkedIn Profile Search Tool"
    description: str = (
        "Search the founder linkedin profile and return the best suitable profile."
    )
    args_schema: Type[BaseModel] = LinkedInSearchtoolInput
    
    def _run(self, company_name: str) -> str:
        serper_tool=SerperDevTool()
        search_results =  serper_tool.run(query=f"Search LinkedIn profile of the founders who is from company {company_name} and provide the most suitable profiles")
        linkedin_links = [
            result['link']
            for result in search_results.get('results', [])
            if 'linkedin.com' in result.get('link', '')
        ]
        return linkedin_links[0] if linkedin_links else "No LinkedIn profile found."

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
        #query = f"site:linkedin.com/jobs {company_name} careers"
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


'''if __name__ == "__main__":
    tool = LinkedInJobSearchTool()
    print(tool._run("LatentBridge"))'''
