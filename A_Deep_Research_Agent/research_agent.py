#!/usr/bin/env python3
"""
Deep Research Agent for Lead Generation
Based on Google ADK Deep Research Agent pattern
"""

import os
import json
import csv
from datetime import datetime
from typing import List, Dict, Any
from dotenv import load_dotenv

from google import genai
from google.genai import types

# Load environment variables
load_dotenv()

# Configuration
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
MODEL_NAME = os.getenv("MODEL_NAME", "gemini-2.5-flash-exp")


class ResearchAgent:
    """Deep research agent for lead generation"""
    
    def __init__(self):
        """Initialize the research agent with ADK client"""
        self.client = genai.Client(
            vertexai=True,
            project=PROJECT_ID,
            location=LOCATION
        )
        self.model_id = MODEL_NAME
        self.research_history = []
        
    def search_companies(self, industry: str, location: str = None) -> List[Dict[str, Any]]:
        """
        Search for companies in a specific industry
        
        Args:
            industry: Target industry (e.g., "AI startups", "SaaS companies")
            location: Optional location filter
            
        Returns:
            List of company information dictionaries
        """
        search_query = f"Find top companies in {industry}"
        if location:
            search_query += f" located in {location}"
            
        prompt = f"""You are a lead generation research assistant. 
        
Task: {search_query}

Please provide a list of 5 companies with the following information:
- Company name
- Website URL
- Brief description (1-2 sentences)
- Industry category
- Estimated company size
- Key products/services

Format your response as a structured list."""

        response = self.client.models.generate_content(
            model=self.model_id,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.7,
                max_output_tokens=2048,
            )
        )
        
        # Log the research step
        self.research_history.append({
            "step": "company_search",
            "query": search_query,
            "timestamp": datetime.now().isoformat()
        })
        
        return self._parse_company_list(response.text)
    
    def deep_research_company(self, company_name: str) -> Dict[str, Any]:
        """
        Perform deep research on a specific company
        
        Args:
            company_name: Name of the company to research
            
        Returns:
            Detailed company research data
        """
        prompt = f"""You are a B2B lead research specialist.

Research the company: {company_name}

Provide detailed information:
1. Company Overview (founding year, headquarters, mission)
2. Key Decision Makers (CEO, CTO, VP Sales - with LinkedIn if possible)
3. Recent News & Developments (last 6 months)
4. Technology Stack (if available)
5. Funding & Financial Info
6. Contact Information (general email, phone, social media)
7. Lead Score (1-10 based on engagement potential)
8. Recommended Outreach Strategy

Be specific and factual. If information is not available, state "Not available"."""

        response = self.client.models.generate_content(
            model=self.model_id,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.4,
                max_output_tokens=3072,
            )
        )
        
        # Log the research step
        self.research_history.append({
            "step": "deep_research",
            "company": company_name,
            "timestamp": datetime.now().isoformat()
        })
        
        return {
            "company_name": company_name,
            "research_data": response.text,
            "researched_at": datetime.now().isoformat()
        }
    
    def extract_contact_info(self, research_data: str) -> Dict[str, str]:
        """
        Extract structured contact information from research data
        
        Args:
            research_data: Raw research text
            
        Returns:
            Structured contact information
        """
        prompt = f"""Extract contact information from this research data and return ONLY a JSON object:

{research_data}

Return format (valid JSON only):
{{
    "email": "contact email or 'Not found'",
    "phone": "phone number or 'Not found'",
    "linkedin": "company LinkedIn URL or 'Not found'",
    "twitter": "Twitter handle or 'Not found'",
    "decision_maker": "name of key decision maker or 'Not found'",
    "decision_maker_title": "title or 'Not found'"
}}"""

        response = self.client.models.generate_content(
            model=self.model_id,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.1,
                max_output_tokens=512,
            )
        )
        
        try:
            # Extract JSON from response
            text = response.text.strip()
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0].strip()
            elif "```" in text:
                text = text.split("```")[1].split("```")[0].strip()
            return json.loads(text)
        except:
            return {
                "email": "Not found",
                "phone": "Not found",
                "linkedin": "Not found",
                "twitter": "Not found",
                "decision_maker": "Not found",
                "decision_maker_title": "Not found"
            }
    
    def _parse_company_list(self, response_text: str) -> List[Dict[str, Any]]:
        """Parse the LLM response into structured company data"""
        # Use LLM to structure the data
        prompt = f"""Convert this company list into a JSON array. Return ONLY valid JSON:

{response_text}

Format:
[
    {{
        "name": "Company Name",
        "website": "URL",
        "description": "Brief description",
        "industry": "Industry",
        "size": "Company size"
    }}
]"""

        response = self.client.models.generate_content(
            model=self.model_id,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.1,
                max_output_tokens=2048,
            )
        )
        
        try:
            text = response.text.strip()
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0].strip()
            elif "```" in text:
                text = text.split("```")[1].split("```")[0].strip()
            return json.loads(text)
        except:
            # Fallback to basic parsing
            return [{
                "name": f"Company {i+1}",
                "website": "Not available",
                "description": "Research data available in detailed report",
                "industry": "Various",
                "size": "Unknown"
            } for i in range(3)]
    
    def generate_lead_report(self, companies_data: List[Dict[str, Any]], 
                           output_dir: str = "outputs") -> tuple:
        """
        Generate CSV and JSON reports from research data
        
        Args:
            companies_data: List of researched company data
            output_dir: Directory to save reports
            
        Returns:
            Tuple of (csv_path, json_path)
        """
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_path = os.path.join(output_dir, f"leads_report_{timestamp}.csv")
        json_path = os.path.join(output_dir, f"research_summary_{timestamp}.json")
        
        # Generate CSV
        with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['company_name', 'website', 'email', 'phone', 
                         'decision_maker', 'title', 'linkedin', 'researched_at']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for company in companies_data:
                contacts = company.get('contacts', {})
                writer.writerow({
                    'company_name': company.get('company_name', 'N/A'),
                    'website': company.get('website', 'N/A'),
                    'email': contacts.get('email', 'Not found'),
                    'phone': contacts.get('phone', 'Not found'),
                    'decision_maker': contacts.get('decision_maker', 'Not found'),
                    'title': contacts.get('decision_maker_title', 'Not found'),
                    'linkedin': contacts.get('linkedin', 'Not found'),
                    'researched_at': company.get('researched_at', '')
                })
        
        # Generate JSON
        with open(json_path, 'w', encoding='utf-8') as jsonfile:
            json.dump({
                'generated_at': datetime.now().isoformat(),
                'total_leads': len(companies_data),
                'companies': companies_data,
                'research_history': self.research_history
            }, jsonfile, indent=2)
        
        return csv_path, json_path


def main():
    """Main execution function"""
    print("=" * 60)
    print("Deep Research Agent for Lead Generation")
    print("Powered by Google ADK")
    print("=" * 60)
    print()
    
    # Initialize agent
    agent = ResearchAgent()
    
    # Get user input
    industry = input("Enter target industry (e.g., 'AI startups', 'SaaS companies'): ").strip()
    if not industry:
        industry = "AI and machine learning startups"
    
    location = input("Enter location (optional, press Enter to skip): ").strip()
    
    print(f"\n🔍 Searching for companies in: {industry}")
    if location:
        print(f"📍 Location filter: {location}")
    print()
    
    # Step 1: Search for companies
    print("Step 1: Searching for companies...")
    companies = agent.search_companies(industry, location)
    print(f"✓ Found {len(companies)} companies\n")
    
    # Step 2: Deep research on each company
    print("Step 2: Performing deep research on each company...")
    researched_companies = []
    
    for i, company in enumerate(companies[:5], 1):  # Limit to 5 companies
        company_name = company.get('name', f'Company {i}')
        print(f"  [{i}/5] Researching {company_name}...")
        
        research = agent.deep_research_company(company_name)
        contacts = agent.extract_contact_info(research['research_data'])
        
        researched_companies.append({
            **company,
            **research,
            'contacts': contacts
        })
        
    print("✓ Deep research completed\n")
    
    # Step 3: Generate reports
    print("Step 3: Generating reports...")
    csv_path, json_path = agent.generate_lead_report(researched_companies)
    
    print(f"✓ CSV report saved: {csv_path}")
    print(f"✓ JSON report saved: {json_path}")
    print()
    
    print("=" * 60)
    print("Research Complete!")
    print(f"Total leads generated: {len(researched_companies)}")
    print("=" * 60)


if __name__ == "__main__":
    main()
