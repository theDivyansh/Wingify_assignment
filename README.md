# Project Setup and Execution Guide

## Getting Started

### Install Required Libraries
```sh
pip install -r requirement.txt
```

# You're All Not Set!
🐛 **Debug Mode Activated!** The project has bugs waiting to be squashed - your mission is to fix them and bring it to life.

## Debugging Instructions

1. **Identify the Bug**: Carefully read the code and understand the expected behavior.
2. **Fix the Bug**: Implement the necessary changes to fix the bug.
3. **Test the Fix**: Run the project and verify that the bug is resolved.
4. **Repeat**: Continue this process until all bugs are fixed.


"""
## File-by-File Bug Analysis

## agents.py 

Import Error
python BROKEN
from crewai.agents import Agent

# FIXED
from crewai import Agent


Circular LLM Definition
python BROKEN
llm = llm

# FIXED
llm = LLM(
    model="gpt-4o-mini",
    temperature=0.7
)


Tools Parameter Error
python BROKEN
tool=[BloodTestReportTool().read_data_tool]

# FIXED
tools=[BloodTestReportTool().read_data_tool]



## tasks.py 


python BROKEN
tools=[BloodTestReportTool.read_data_tool]

# FIXED
tools=[BloodTestReportTool().read_data_tool]


python BROKEN - All tasks assigned to doctor
agent=doctor

# FIXED 
nutrition_analysis.agent = nutritionist
exercise_planning.agent = exercise_specialist
 

## tools.py 

python BROKEN
from crewai_tools import tools
from crewai_tools.tools.serper_dev_tool import SerperDevTool

# FIXED
from crewai_tools import tool
from crewai_tools import SerperDevTool
from langchain_community.document_loaders import PyPDFLoader



PDF Loader Class Error
python BROKEN
docs = PDFLoader(file_path=path).load()

# FIXED
loader = PyPDFLoader(path)
docs = loader.load()


Missing Tool Decorators
python BROKEN
async def read_data_tool(path='data/sample.pdf'):

# FIXED
@tool("Blood Test Report Reader")
def read_data_tool(self, path: str = 'data/sample.pdf') -> str:



## main.py - API and Orchestration Issues

python BROKEN
from task import help_patients

# FIXED
from tasks import help_patients, verification, nutrition_analysis, exercise_planning



Incomplete Crew Configuration
python BROKEN - Only doctor agent
agents=[doctor]
tasks=[help_patients]

# FIXED
agents=[verifier, doctor, nutritionist, exercise_specialist]
tasks=[verification, help_patients, nutrition_analysis, exercise_planning]

