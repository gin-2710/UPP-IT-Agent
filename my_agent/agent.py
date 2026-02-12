from google.adk.agents.llm_agent import Agent
from .jira_tool import jira_tool

jira_agent = Agent(
    model='gemini-2.5-flash',
    name='scrum_update_agent',
    description='You are a JIRA agent. You can use the provided tool to query JIRA tickets assigned to the user. Your goal is to generate a daily scrum update summary for the user. ',
    instruction= 'First, determine what the user worked on yesterday. Then, determine what they have in progress for today. Finally, format it as: "Yesterday I worked on [Task A] and [Task B]. Today I am focusing on [Task C]. No blockers."',
    tools=[jira_tool]
)

root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction='Answer user questions to the best of your knowledge',
    sub_agents=[jira_agent]
)
