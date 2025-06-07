import os
import requests
import json
import pandas as pd
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "notion_sync_token.env"))

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
print(NOTION_TOKEN)
HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

def fetch_database_all(database_id):
    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    results = []
    has_more = True
    next_cursor = None

    while has_more:
        try:
            payload = {"start_cursor": next_cursor} if next_cursor else {}
            response = requests.post(url, headers=HEADERS, json=payload)
            response.raise_for_status()
            data = response.json()
            results.extend(data["results"])
            has_more = data.get("has_more", False)
            next_cursor = data.get("next_cursor")
        except requests.exceptions.HTTPError as e:
            error_message = f"HTTP Error: {e.response.status_code} - {e.response.text}"
            if e.response.status_code == 401:
                error_message += "\n認証エラー: Notionトークンが無効か、データベースへのアクセス権限がありません。"
            elif e.response.status_code == 404:
                error_message += "\nデータベースが見つかりません: データベースIDが正しいか、インテグレーションにアクセス権限があるか確認してください。"
            elif e.response.status_code == 429:
                error_message += "\nレート制限: しばらく待ってから再試行してください。"
            raise Exception(error_message)
        except requests.exceptions.RequestException as e:
            raise Exception(f"リクエストエラー: {str(e)}")

    return {"results": results}

def save_as_csv(data, filename):
    rows = []
    for result in data["results"]:
        row = {}
        for prop, value in result["properties"].items():
            if value["type"] == "title":
                row[prop] = value["title"][0]["plain_text"] if value["title"] else ""
            elif value["type"] == "rich_text":
                row[prop] = value["rich_text"][0]["plain_text"] if value["rich_text"] else ""
            elif value["type"] == "select":
                row[prop] = value["select"]["name"] if value["select"] else ""
            elif value["type"] == "multi_select":
                row[prop] = ", ".join([v["name"] for v in value["multi_select"]])
            elif value["type"] == "date":
                row[prop] = value["date"]["start"] if value["date"] else ""
            elif value["type"] == "checkbox":
                row[prop] = value["checkbox"]
            elif value["type"] == "number":
                row[prop] = value["number"]
            elif value["type"] == "relation":
                row[prop] = ", ".join([r["id"] for r in value["relation"]])
            else:
                row[prop] = str(value.get(value["type"], ""))
        rows.append(row)

    df = pd.DataFrame(rows)
    df.to_csv(filename, index=False)

if __name__ == "__main__":
    notion_dbs = {
        "daily_logs": "20b30729ab3980229ac3c7bf7cd795ea",
        "tasks": "20b30729ab3981bfbeffc166388f6707",
        "learning_logs": "20b30729ab39817da602f4b50e01663e"
    }

    os.makedirs("notion_sync", exist_ok=True)

    for name, db_id in notion_dbs.items():
        print(f"[INFO] Fetching data from '{name}'...")
        data = fetch_database_all(db_id)
        os.makedirs("notion_sync/synced_db", exist_ok=True)
        save_as_csv(data, f"notion_sync/synced_db/{name}.csv")
        print(f"[INFO] Saved to 'notion_sync/synced_db/{name}.csv'")
