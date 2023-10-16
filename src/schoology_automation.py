import asyncio
import config
import requests
from bs4 import BeautifulSoup
import todoist
import json

# Load the configuration settings
schoology_api_token = config.SCHOOLOGY_API_TOKEN
todoist_api_token = config.TODOIST_API_TOKEN
schoology_course_ids = config.SCHOOLOGY_COURSE_IDS
todoist_project_id = config.TODOIST_PROJECT_ID


# Get the list of assignments from Schoology
async def get_assignments():
    session = requests.Session()
    session.headers["Authorization"] = f"Bearer {schoology_api_token}"

    response = await session.get("https://app.schoology.com/api/v1/assignments")
    assignments = json.loads(response.content)
    return assignments


# Create a new task in Todoist
async def create_todoist_task(assignment):
    todoist_client = todoist.TodoistAPI(todoist_api_token)

    task = todoist.Task(
        content=assignment["title"],
        due_date=assignment["due_date"],
        project_id=todoist_project_id
    )
    await todoist_client.items.add(task)


# Update the Todoist list with Schoology assignments
async def update_todoist_list():
    assignments = await get_assignments()

    for assignment in assignments:
        await create_todoist_task(assignment)


# Async main function
async def main():
    await update_todoist_list()

    print("Successfully updated Todoist list with Schoology assignments!")


if __name__ == "__main__":
    asyncio.run(main())
