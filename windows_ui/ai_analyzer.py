import google.generativeai as genai
from config import GEMINI_API_KEY
import json
import time

class AIAnalyzer:
    def __init__(self):
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-pro')
        
    def analyze_logs(self, tool_name, log_data):
        try:
            # Create a prompt for the AI
            prompt = f"""
            Analyze the following {tool_name} log data for potential security threats.
            Focus on identifying:
            1. Suspicious activities
            2. Potential security breaches
            3. Unusual patterns
            4. Security vulnerabilities
            
            Log data:
            {log_data}
            
            Provide a detailed analysis and suggest appropriate actions if threats are detected.
            """
            
            # Get AI response
            response = self.model.generate_content(prompt)
            
            # Parse the response
            analysis = response.text
            
            # Check if there are threats
            if any(keyword in analysis.lower() for keyword in ["threat", "vulnerability", "suspicious", "warning", "risk"]):
                return {
                    "threat_detected": True,
                    "analysis": analysis,
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                }
            else:
                return {
                    "threat_detected": False,
                    "analysis": "No immediate threats detected.",
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                }
                
        except Exception as e:
            return {
                "threat_detected": False,
                "analysis": f"Error in AI analysis: {str(e)}",
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            
    def get_solution(self, threat_analysis):
        try:
            # Create a prompt for solution
            prompt = f"""
            Based on the following threat analysis, provide detailed steps to mitigate or resolve the security issues.
            Include both immediate actions and long-term preventive measures.
            
            Threat Analysis:
            {threat_analysis}
            
            Provide a step-by-step solution.
            """
            
            # Get AI response
            response = self.model.generate_content(prompt)
            
            return {
                "solution": response.text,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            
        except Exception as e:
            return {
                "solution": f"Error generating solution: {str(e)}",
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            } 