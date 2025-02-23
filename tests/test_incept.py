from oauthmanager import OnePasswordAuthManager
import pandas as pd
import incept

# In a real scenario, you'd provide your Notion API key & Database ID
auth_manager = OnePasswordAuthManager(vault_name="API Keys")
notion_creds = auth_manager.get_credentials("Quantum", "credential")
NOTION_API_KEY = notion_creds.get("credential")
DATABASE_ID = "195a1865-b187-8103-9b6a-cc752ca45874"

def main():
    # Attempt to fetch ALL courses:
    all_courses_df = incept.getCourses(
        api_key=NOTION_API_KEY,
        database_id=DATABASE_ID
    )
    print("=== ALL Courses ===")
    print(all_courses_df)

    # If you want to filter by course name (optional):
    filtered_df = incept.getCourses(
        api_key=NOTION_API_KEY,
        database_id=DATABASE_ID,
        filter="Sample Course A"
    )
    print("\n=== Filtered Courses (Sample Course A) ===")
    print(filtered_df)

if __name__ == "__main__":
    main()

