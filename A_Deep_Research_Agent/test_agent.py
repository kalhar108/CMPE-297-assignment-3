#!/usr/bin/env python3
"""
Test script for Deep Research Agent
Runs a quick test with sample data
"""

import os
from research_agent import ResearchAgent

def test_agent():
    """Run a quick test of the research agent"""
    print("Testing Deep Research Agent...")
    print("-" * 60)
    
    # Initialize agent
    agent = ResearchAgent()
    print("✓ Agent initialized")
    
    # Test company search
    print("\nTest 1: Searching for companies...")
    companies = agent.search_companies("AI startups", "California")
    print(f"✓ Found {len(companies)} companies")
    
    if companies:
        print(f"  Sample: {companies[0].get('name', 'N/A')}")
    
    # Test deep research on one company
    print("\nTest 2: Deep research on a company...")
    if companies:
        company_name = companies[0].get('name', 'OpenAI')
    else:
        company_name = "OpenAI"
    
    research = agent.deep_research_company(company_name)
    print(f"✓ Researched {company_name}")
    print(f"  Data length: {len(research['research_data'])} characters")
    
    # Test contact extraction
    print("\nTest 3: Extracting contact information...")
    contacts = agent.extract_contact_info(research['research_data'])
    print(f"✓ Extracted contacts:")
    for key, value in contacts.items():
        print(f"  {key}: {value}")
    
    # Test report generation
    print("\nTest 4: Generating reports...")
    test_data = [{
        'company_name': company_name,
        'website': 'https://example.com',
        'researched_at': research['researched_at'],
        'contacts': contacts,
        'research_data': research['research_data']
    }]
    
    csv_path, json_path = agent.generate_lead_report(test_data, output_dir="outputs/test")
    print(f"✓ CSV saved: {csv_path}")
    print(f"✓ JSON saved: {json_path}")
    
    print("\n" + "=" * 60)
    print("All tests passed! ✓")
    print("=" * 60)

if __name__ == "__main__":
    test_agent()
