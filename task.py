## Importing libraries and files
from crewai import Task
from agents import doctor, verifier, nutritionist, exercise_specialist
from tools import search_tool, BloodTestReportTool

## Creating a task to help solve user's query
help_patients = Task(
    description=(
        "Provide comprehensive medical analysis and interpretation of blood test results for the user's query: {query}.\n"
        "Carefully analyze the uploaded blood test report using the available tools.\n"
        "Interpret blood test values in the context of normal reference ranges and clinical significance.\n"
        "Identify any abnormal values and explain their potential clinical implications.\n"
        "Provide evidence-based medical insights while emphasizing the need for professional medical consultation.\n"
        "Search for current medical literature and guidelines when necessary to support your analysis.\n"
        "Always maintain professional medical standards and avoid making definitive diagnoses."
    ),
    expected_output=(
        "A comprehensive medical analysis report including:\n"
        "- Summary of key blood test findings\n"
        "- Interpretation of abnormal values with clinical context\n"
        "- Potential health implications and areas of concern\n"
        "- Recommendations for follow-up testing if appropriate\n"
        "- Clear emphasis on the need for professional medical consultation\n"
        "- References to relevant medical guidelines or literature\n"
        "- Professional medical language with clear explanations for patient understanding"
    ),
    agent=doctor,
    tools=[BloodTestReportTool().read_data_tool, search_tool],
    async_execution=False,
)

## Creating a nutrition analysis task
nutrition_analysis = Task(
    description=(
        "Analyze blood test results to provide evidence-based nutritional recommendations for the user's query: {query}.\n"
        "Examine blood markers related to nutritional status including vitamins, minerals, lipids, glucose, and other relevant biomarkers.\n"
        "Identify any nutritional deficiencies or imbalances indicated by the blood test results.\n"
        "Provide specific, practical dietary recommendations based on established nutritional science.\n"
        "Focus on whole food sources and evidence-based nutritional interventions.\n"
        "Only recommend supplements when there is clear evidence of deficiency and established benefit.\n"
        "Consider individual health conditions and potential dietary restrictions."
    ),
    expected_output=(
        "A detailed nutritional analysis including:\n"
        "- Assessment of nutritional biomarkers from blood test results\n"
        "- Identification of any nutritional deficiencies or concerns\n"
        "- Specific food recommendations to address identified issues\n"
        "- Practical meal planning suggestions\n"
        "- Evidence-based supplement recommendations only when clinically indicated\n"
        "- Dietary modifications based on blood lipids, glucose, and other relevant markers\n"
        "- References to established nutritional guidelines and research\n"
        "- Clear explanation of the connection between blood markers and nutritional needs"
    ),
    agent=nutritionist,
    tools=[BloodTestReportTool().read_data_tool, search_tool],
    async_execution=False,
)

## Creating an exercise planning task
exercise_planning = Task(
    description=(
        "Develop a safe, medically-appropriate exercise plan based on blood test results and the user's query: {query}.\n"
        "Analyze blood markers relevant to exercise capacity including cardiovascular health, metabolic markers, and inflammatory indicators.\n"
        "Consider any health limitations or contraindications indicated by the blood test results.\n"
        "Create a progressive, evidence-based exercise program appropriate for the individual's health status.\n"
        "Ensure all recommendations prioritize safety and align with medical guidelines for exercise prescription.\n"
        "Include modifications for any identified health concerns or contraindications.\n"
        "Emphasize the importance of medical clearance for exercise programs when appropriate."
    ),
    expected_output=(
        "A comprehensive exercise plan including:\n"
        "- Assessment of exercise-relevant blood markers (cardiovascular, metabolic, inflammatory)\n"
        "- Safe exercise recommendations based on health status\n"
        "- Progressive training plan with appropriate intensity levels\n"
        "- Specific exercise modifications for any identified health concerns\n"
        "- Guidelines for monitoring exercise response and safety\n"
        "- Recommendations for medical clearance if indicated\n"
        "- Evidence-based rationale for exercise prescriptions\n"
        "- Clear safety guidelines and warning signs to watch for during exercise"
    ),
    agent=exercise_specialist,
    tools=[BloodTestReportTool().read_data_tool, search_tool],
    async_execution=False,
)

## Creating a verification task
verification = Task(
    description=(
        "Thoroughly verify and validate that the uploaded document is a legitimate blood test report containing proper medical laboratory data.\n"
        "Examine the document structure, formatting, and content to confirm it contains authentic blood test results.\n"
        "Check for essential elements of a blood test report including patient information, test dates, laboratory values, reference ranges, and laboratory identification.\n"
        "Identify any missing critical information or formatting inconsistencies that might indicate an invalid document.\n"
        "Verify that the document contains medically relevant blood biomarkers and laboratory values.\n"
        "Ensure the document is complete and suitable for medical analysis."
    ),
    expected_output=(
        "A verification report including:\n"
        "- Confirmation of document type and authenticity\n"
        "- Assessment of document completeness and quality\n"
        "- Identification of key blood test components present\n"
        "- List of blood markers and tests included in the report\n"
        "- Assessment of reference ranges and laboratory standards\n"
        "- Any concerns about document validity or completeness\n"
        "- Recommendation on whether the document is suitable for medical analysis\n"
        "- Clear documentation of verification process and findings"
    ),
    agent=verifier,
    tools=[BloodTestReportTool().read_data_tool],
    async_execution=False
)