import os
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool
from crewai_tools import DOCXSearchTool
from langchain_openai import ChatOpenAI
import ollama

search_tool = SerperDevTool()

# with open('Oferta - Test 1.docx', 'r') as file:
#     data = file.readlines()

# agents definition

researcher = Agent(
    role='Senior Research Assistant',
    goal='Look up the latest advancements in AI agents',
    backstory='You work at a leading tech think tank. Your expertise lies in identifying emerging trends. You have a '
              'knack for dissecting complex data and presenting it as actionable insights',
    verbose=False,
    allow_delegation=False,
    tools=[search_tool],
    llm=ChatOpenAI(model_name='gpt-3.5-turbo-instruct', temperature=0.7)  # gpt-4-turbo-preview
)

writer = Agent(
    role='Tech Content Strategist',
    goal='Craft compelling content on tech advancements',
    backstory='you are renowned Content Strategist, known for your insights. You transform complex concepts into '
              'compelling narratives',
    verbose=False,
    allow_delegation=True,
    tools=[search_tool],
    llm=ChatOpenAI(model_name='gpt-3.5-turbo-instruct', temperature=0.7)
)

i = 1
tool = ''
try:
    while i:
        tool = DOCXSearchTool(docx=f'Oferta - Test {i}.docx')
        i += 1
except Exception as e:
    print('nu mai am documente', e)

task1 = Task(
    description='Conduct comprehensive analysis of the latest advanced tech in AI. Identify key trends, breakthrough '
                'technologies and potential industry disruptors',
    expected_output='full analysis report in bullet points',
    agent=researcher,
    tool=tool
)

task2 = Task(
    description='write a short article that highlights the most significant AI Agent advancements',
    expected_output='full blogpost of at least 3 paragraphs',
    agent=writer
)

# initiate crew and agents
crew = Crew(
    agents=[researcher, writer],
    tasks=[task1, task2],
    verbose=1,
)

result = crew.kickoff()

print('########')
print(result)
