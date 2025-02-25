# test_incept_addcourse.py

import pandas as pd
from oauthmanager import OnePasswordAuthManager
from incept.courses import addCourse

def main():
    # 1) Fetch credentials
    auth_manager = OnePasswordAuthManager(vault_name="API Keys")
    notion_creds = auth_manager.get_credentials("Quantum", "credential")
    api_key = notion_creds["credential"]
    database_id = "195a1865-b187-8103-9b6a-cc752ca45874"  # Adjust to your DB

    # 2) Build a DataFrame with a single row for your new course
    df_single = pd.DataFrame([{
        "name": "KitchenTestCourse", 
        "description": "Testing addCourse from pythonKitchen environment",
        "tags": ["Test", "Kitchen"],
        "cover": "https://example.com/kitchen_cover.jpg",
        "icon": "https://example.com/kitchen_icon.png",
        "course_link": "https://example.com/kitchen",
        "path": "/kitchen/test/path"
    }])

    # 3) Call addCourse from the 'incept' package
    result = addCourse(
        db="notion",
        template="default",
        df=df_single,
        api_key=api_key,
        database_id=database_id
    )

    # 4) Print the result
    print("addCourse result:", result)

if __name__ == "__main__":
    main()
