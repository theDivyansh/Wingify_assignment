## Importing libraries and files
import os
import re
from dotenv import load_dotenv
load_dotenv()

from crewai_tools import tool
from crewai_tools import SerperDevTool
from langchain_community.document_loaders import PyPDFLoader

## Creating search tool
search_tool = SerperDevTool()

## Creating custom pdf reader tool
class BloodTestReportTool:
    def __init__(self):
        pass
    
    @tool("Blood Test Report Reader")
    def read_data_tool(self, path: str = 'data/sample.pdf') -> str:
        """Tool to read and extract data from a blood test PDF file.

        Args:
            path (str, optional): Path of the PDF file. Defaults to 'data/sample.pdf'.

        Returns:
            str: Full Blood Test report file
        """
        try:
            # Check if file exists
            if not os.path.exists(path):
                return f"Error: File not found at path {path}"
            
            # Load PDF using PyPDFLoader
            docs =PyPDFLoader(path).load()
            
            if not docs:
                return "Error: No content found in the PDF file"
            
            full_report = ""
            for doc in docs:
                # Clean and format the report data
                content = doc.page_content
                
                # Remove excessive whitespaces and format properly
                content = re.sub(r'\n\s*\n', '\n', content)  # Remove empty lines
                content = re.sub(r'\s+', ' ', content)  # Replace multiple spaces with single space
                content = content.strip()
                
                full_report += content + "\n"
            
            # Additional cleaning for blood test reports
            full_report = self._clean_blood_report(full_report)
            
            return full_report
            
        except Exception as e:
            return f"Error reading PDF file: {str(e)}"
    

## Creating Nutrition Analysis Tool
class NutritionTool:
    def __init__(self):
        pass
    
    @tool("Nutrition Analysis Tool")
    def analyze_nutrition_tool(self, blood_report_data: str) -> str:
        """Analyze blood test data to provide nutritional insights and recommendations.

        Args:
            blood_report_data (str): Blood test report content

        Returns:
            str: Nutritional analysis and recommendations
        """
        try:
            # Extract key nutritional markers from blood report
            nutritional_markers = self._extract_nutritional_markers(blood_report_data)
            
            # Analyze the markers
            analysis = self._analyze_markers(nutritional_markers)
            
            return analysis
            
        except Exception as e:
            return f"Error in nutrition analysis: {str(e)}"
    
    def _extract_nutritional_markers(self, data: str) -> dict:
        """Extract nutritional markers from blood report data."""
        markers = {}
        
        # Common nutritional markers to look for
        marker_patterns = {
            'vitamin_d': r'vitamin\s*d.*?(\d+\.?\d*)',
            'vitamin_b12': r'vitamin\s*b12.*?(\d+\.?\d*)',
            'folate': r'folate.*?(\d+\.?\d*)',
            'iron': r'iron.*?(\d+\.?\d*)',
            'ferritin': r'ferritin.*?(\d+\.?\d*)',
            'glucose': r'glucose.*?(\d+\.?\d*)',
            'cholesterol': r'cholesterol.*?(\d+\.?\d*)',
            'hdl': r'hdl.*?(\d+\.?\d*)',
            'ldl': r'ldl.*?(\d+\.?\d*)',
            'triglycerides': r'triglycerides.*?(\d+\.?\d*)',
        }
        
        for marker, pattern in marker_patterns.items():
            match = re.search(pattern, data.lower())
            if match:
                markers[marker] = float(match.group(1))
        
        return markers
    
    def _analyze_markers(self, markers: dict) -> str:
        """Analyze nutritional markers and provide recommendations."""
        analysis = "NUTRITIONAL ANALYSIS BASED ON BLOOD MARKERS:\n\n"
        
        if not markers:
            return "Unable to extract nutritional markers from the blood report. Please ensure the report contains standard nutritional biomarkers."
        
        # Analyze each marker
        for marker, value in markers.items():
            analysis += f"{marker.upper().replace('_', ' ')}: {value}\n"
            analysis += self._get_marker_analysis(marker, value) + "\n"
        
        analysis += "\nGENERAL RECOMMENDATIONS:\n"
        analysis += "- Consult with a registered dietitian for personalized nutrition advice\n"
        analysis += "- Consider follow-up testing as recommended by your healthcare provider\n"
        analysis += "- Focus on a balanced, whole-food diet rich in nutrients\n"
        
        return analysis
    
    def _get_marker_analysis(self, marker: str, value: float) -> str:
        """Get analysis for specific nutritional markers."""
        analyses = {
            'vitamin_d': self._analyze_vitamin_d(value),
            'vitamin_b12': self._analyze_b12(value),
            'iron': self._analyze_iron(value),
            'glucose': self._analyze_glucose(value),
            'cholesterol': self._analyze_cholesterol(value),
        }
        
        return analyses.get(marker, "Analysis not available for this marker.")
    
    def _analyze_vitamin_d(self, value: float) -> str:
        if value < 20:
            return "Low vitamin D levels. Consider vitamin D supplementation and increased sun exposure."
        elif value < 30:
            return "Insufficient vitamin D. Consider moderate supplementation."
        else:
            return "Adequate vitamin D levels."
    
    def _analyze_b12(self, value: float) -> str:
        if value < 200:
            return "Low B12 levels. Consider B12 supplementation and B12-rich foods."
        else:
            return "Adequate B12 levels."
    
    def _analyze_iron(self, value: float) -> str:
        if value < 60:
            return "Low iron levels. Consider iron-rich foods and evaluate for deficiency."
        elif value > 170:
            return "Elevated iron levels. Consult healthcare provider."
        else:
            return "Normal iron levels."
    
    def _analyze_glucose(self, value: float) -> str:
        if value < 70:
            return "Low glucose levels. Monitor for hypoglycemia."
        elif value > 100:
            return "Elevated glucose levels. Consider dietary modifications."
        else:
            return "Normal glucose levels."
    
    def _analyze_cholesterol(self, value: float) -> str:
        if value > 200:
            return "Elevated cholesterol. Consider heart-healthy diet modifications."
        else:
            return "Normal cholesterol levels."

## Creating Exercise Planning Tool
class ExerciseTool:
    def __init__(self):
        pass
    
    @tool("Exercise Planning Tool")
    def create_exercise_plan_tool(self, blood_report_data: str) -> str:
        """Create a safe exercise plan based on blood test results.

        Args:
            blood_report_data (str): Blood test report content

        Returns:
            str: Personalized exercise recommendations
        """
        try:
            # Extract relevant markers for exercise planning
            exercise_markers = self._extract_exercise_markers(blood_report_data)
            
            # Create exercise recommendations
            plan = self._create_exercise_recommendations(exercise_markers)
            
            return plan
            
        except Exception as e:
            return f"Error creating exercise plan: {str(e)}"
    
    def _extract_exercise_markers(self, data: str) -> dict:
        """Extract markers relevant to exercise planning."""
        markers = {}
        
        # Exercise-relevant markers
        marker_patterns = {
            'hemoglobin': r'hemoglobin.*?(\d+\.?\d*)',
            'heart_rate': r'heart\s*rate.*?(\d+\.?\d*)',
            'blood_pressure': r'blood\s*pressure.*?(\d+\.?\d*)',
            'glucose': r'glucose.*?(\d+\.?\d*)',
            'creatinine': r'creatinine.*?(\d+\.?\d*)',
            'ldl': r'ldl.*?(\d+\.?\d*)',
            'hdl': r'hdl.*?(\d+\.?\d*)',
        }
        
        for marker, pattern in marker_patterns.items():
            match = re.search(pattern, data.lower())
            if match:
                markers[marker] = float(match.group(1))
        
        return markers
    
    def _create_exercise_recommendations(self, markers: dict) -> str:
        """Create exercise recommendations based on blood markers."""
        plan = "EXERCISE RECOMMENDATIONS BASED ON BLOOD MARKERS:\n\n"
        
        if not markers:
            plan += "GENERAL EXERCISE RECOMMENDATIONS:\n"
            plan += "- Start with light to moderate exercise\n"
            plan += "- Aim for 150 minutes of moderate activity per week\n"
            plan += "- Include both cardio and strength training\n"
            plan += "- Always consult your healthcare provider before starting any exercise program\n"
            return plan
        
        plan += "MARKER ANALYSIS:\n"
        for marker, value in markers.items():
            plan += f"{marker.upper().replace('_', ' ')}: {value}\n"
        
        plan += "\nEXERCISE RECOMMENDATIONS:\n"
        
        # Basic recommendations based on common markers
        if 'glucose' in markers:
            if markers['glucose'] > 100:
                plan += "- Focus on aerobic exercise to help with glucose control\n"
                plan += "- Consider post-meal walks to help manage blood sugar\n"
        
        if 'ldl' in markers:
            if markers['ldl'] > 100:
                plan += "- Include regular cardio exercise to help improve cholesterol\n"
                plan += "- Aim for 30-45 minutes of moderate exercise most days\n"
        
        if 'hemoglobin' in markers:
            if markers['hemoglobin'] < 12:
                plan += "- Start with low-intensity exercise due to low hemoglobin\n"
                plan += "- Monitor energy levels and avoid overexertion\n"
        
        plan += "\nGENERAL SAFETY GUIDELINES:\n"
        plan += "- Always warm up before exercising and cool down afterward\n"
        plan += "- Stay hydrated during exercise\n"
        plan += "- Stop exercising if you feel dizzy, short of breath, or experience chest pain\n"
        plan += "- Get medical clearance before starting any new exercise program\n"
        plan += "- Consider working with a certified exercise physiologist\n"
        
        return plan