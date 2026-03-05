from typing import List, Dict, Any
from google.adk.tools import FunctionTool
import json
import os
 
# Simulated current user - change this to test different users
 # Options: Sarah Chen, Marcus Johnson, Priya Patel, Alex Rodriguez, Emma Williams
 
# Load the mock data from the JSON file
MOCK_JIRA_DATA = {}
file_path = os.path.join(os.path.dirname(__file__), 'mockJiraData.json')
with open(file_path, 'r') as f:
    MOCK_JIRA_DATA = json.load(f)
 
def get_assigned_jira_tickets(name: dict) -> dict:
    """
    Queries mock Jira data for all issues assigned to the current user
    that are not in a 'Done' or 'Closed' status.
 
    Returns:
        A list of dictionaries, where each dictionary represents a Jira ticket
        with its key, summary, status, and priority. Returns an empty list
        if no tickets are found.
    """
    uname = name.get("user")  # Default to CURRENT_USER if no name provided
    print(f"Fetching Jira tickets for user: {uname}")
    try:
        # Find the current user's tasks
        user_data = None
        for person in MOCK_JIRA_DATA["jiraTasks"]:
            if person["assignee"] == uname:
                user_data = person
                break
       
        if not user_data:
            return [{"error": f"No user found with name: {uname}"}]
       
        # Filter out Done and Closed tasks, and format the response
        filtered_tickets = []
        for task in user_data["tasks"]:
            if task["status"] not in ["Done", "Closed", "Won't Do"]:
                filtered_tickets.append({
                    "key": task["taskId"],
                    "summary": task["title"],
                    "status": task["status"],
                    "priority": task["priority"],
                    "dueDate": task["dueDate"],
                    "description": task["description"],
                    "storyPoints": task["storyPoints"]
                })
       
        # Sort by priority (Critical > High > Medium > Low) and then by due date
        priority_order = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}
        filtered_tickets.sort(key=lambda x: (priority_order.get(x["priority"], 4), x["dueDate"]))
       
        print(filtered_tickets)
        return filtered_tickets
       
    except Exception as e:
        return [{"error": f"Failed to fetch Jira tickets. Error: {str(e)}"}]
 
jira_tool = FunctionTool(func=get_assigned_jira_tickets)

if __name__ == "__main__":
    result = get_assigned_jira_tickets({"user": CURRENT_USER})
    print(f"Found {len(result)} tickets")
    print(json.dumps(result, indent=2))