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

AcountManager = Agent(
    role='Romanian Account Manager',
    goal='Develop an template offer based on previous offers in the Romanian language',
    backstory='You work at a leading Romanian tech company. Your expertise lies in identifying patterns. You have a '
              'knack for dissecting complex data and presenting it as actionable insights',
    verbose=True,
    allow_delegation=False,
    tools=[search_tool],
    llm=ChatOpenAI(model_name='gpt-3.5-turbo-instruct', temperature=0.7)  # gpt-4-turbo-preview
)

SalesRepresentative = Agent(
    role='Romanian Sales Representative',
    goal='Develop a custom client oriented offer, in the Romanian language, based on the template offer developed by '
         'the Account Manager in the Romanian language',
    backstory='you are a renowned Romanian Sales Representative known for your wit, empathy and expertise. You can '
              'match what the client wants to what the company can offer and convince the client it was their idea',
    verbose=True,
    allow_delegation=True,
    tools=[search_tool],
    llm=ChatOpenAI(model_name='gpt-3.5-turbo-instruct', temperature=0.7)
)

i = 1
offer = ''
offers = []

try:
    while i:
        offer = DOCXSearchTool(docx=f'Oferta - Test {i}.docx')
        offers.append(offer)
        i += 1
except Exception as e:
    print('nu mai am documente', e)

task1 = Task(
    description=f'Conduct comprehensive analysis of {offers}. Identify key patterns with regards to price strategy, '
                f'used technologies in stack, back-end, front-end, data bases as well as the required task necessary '
                f'to build the app with regards to team size, time spent on development and per unit of labour cost',
    expected_output='full analysis report in bullet points in the Romanian language',
    agent=AcountManager,
    tool=offers
)

task2 = Task(
    description='write a competitive and attractive sales offer based on the template provided by the Acount Manager. '
                'follow the template but be willing to modify it to match client expectations and requirements',
    expected_output='a 2 page offer with articulate and comprehensive descriptions of the services, prices and '
                    'timetable our company is willing to provide in the Romanian language ',
    agent=SalesRepresentative
)

# initiate crew and agents
crew = Crew(
    agents=[AcountManager, SalesRepresentative],
    tasks=[task1, task2],
    verbose=1,
)

result = crew.kickoff()

print('########')
print(result)
