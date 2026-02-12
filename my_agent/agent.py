from google.adk.agents.llm_agent import Agent

# Phase 2: This agent will be responsible for generating the scrum update.
# Its tools will be provided by the JiraToolAgent.
scrum_update_agent = Agent(
    name='scrum_update_agent',
    model='gemini-1.5-flash',
    instruction='You are a scrum assistant. Your goal is to generate a daily scrum update summary for the user. '
                'First, determine what the user worked on yesterday. Then, determine what they have in progress for today. '
                'Finally, format it as: "Yesterday I worked on [Task A] and [Task B]. Today I am focusing on [Task C]. No blockers."',
)

# Phase 3: This agent will be responsible for creating a daily plan.
# Its tools will also be provided by the JiraToolAgent.
daily_planner_agent = Agent(
    name='daily_planner_agent',
    model='gemini-1.5-flash',
    instruction='You are a productivity planner. Your goal is to create a prioritized to-do list for the user for the current day. '
                'Analyze the user\'s open Jira tickets, considering their priority, status, and due dates. '
                'List the tasks in the order the user should approach them.',
)

# Phase 4: The root_agent acts as an orchestrator.
root_agent = Agent(
    name='root_agent',
    model='gemini-1.5-flash',
    description='An intelligent assistant that helps software engineers with daily scrum updates and planning.',
    instruction='You are an orchestrator agent. Your job is to understand the user\'s request and delegate it to the appropriate specialized agent. '
                'If the user asks for a scrum update, use the scrum_update_agent. If the user asks for a daily plan, use the daily_planner_agent.',
    tools=[scrum_update_agent, daily_planner_agent]
)
