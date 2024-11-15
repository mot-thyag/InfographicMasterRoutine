from openai import OpenAI
import json
import os
from typing import Dict

class ReportParser:
    def __init__(self, api_key: str = None):
        self.client = OpenAI(api_key='xxxx')

    def extract_report_info(self, report_text: str) -> Dict[str, str]:
        """Extract relevant information from a company analysis report using OpenAI."""
        
        prompt = """
        Extract the following information from the company analysis report in a JSON format:
        1. company_name: The name of the company
        2. report_type: The type of financial report (e.g., "FY2024Q3 Income Statement")
        3. citation: The source document reference
        4. report_date: The date or period of the report
        5. key_insight: A one-line key insight or conclusion from the report (5-6 words)

        Format the response as a JSON object with these exact keys.
        If any information is not found, use null as the value.
        """

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",  # or another appropriate model
                messages=[
                    {"role": "system", "content": "You are a financial report parser. Extract specific information and return it in JSON format."},
                    {"role": "user", "content": prompt + "\n\nReport text:\n" + report_text}
                ],
                response_format={ "type": "json_object" }
            )
            
            parsed_data = json.loads(response.choices[0].message.content)
            
            # Format the data to match the imageMerge.py requirements
            return {
                "company_name_text": parsed_data.get("company_name"),
                "type_text_value": parsed_data.get("report_type"),
                "citation_text": parsed_data.get("citation"),
                "description_text": parsed_data.get("report_date"),
                "center_description_text": parsed_data.get("key_insight")
            }
            
        except Exception as e:
            print(f"Error parsing report: {e}")
            return None 
