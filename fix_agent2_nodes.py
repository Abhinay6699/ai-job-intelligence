import sqlite3
import json
import os

def fix_nodes(nodes):
    changed = False
    for node in nodes:
        if node.get('name') in ['Store Resume', 'Store ATS Report']:
            params = node.get('parameters', {})
            if 'specifyBody' not in params:
                params['specifyBody'] = 'json'
                params['jsonBody'] = '={{ $json.github_payload }}'
                if 'bodyParameters' in params:
                    del params['bodyParameters']
                changed = True
    return changed

# 1. Update SQLite DB
db_path = r"C:\Users\nagna\.n8n\database.sqlite"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("SELECT id, nodes FROM workflow_entity")
rows = cursor.fetchall()

updated = 0
for row in rows:
    wf_id = row[0]
    nodes_json = row[1]
    
    if nodes_json:
        nodes = json.loads(nodes_json)
        if fix_nodes(nodes):
            new_nodes_json = json.dumps(nodes)
            cursor.execute("UPDATE workflow_entity SET nodes = ? WHERE id = ?", (new_nodes_json, wf_id))
            updated += 1

conn.commit()
conn.close()
print(f"Updated {updated} workflows in n8n SQLite DB.")

# 2. Update JSON files in Desktop repo
workflows_dir = r"C:\Users\nagna\OneDrive\Desktop\ai job intelligence\workflows"
for f in os.listdir(workflows_dir):
    if f.endswith('.json'):
        path = os.path.join(workflows_dir, f)
        with open(path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            
        if 'nodes' in data and fix_nodes(data['nodes']):
            with open(path, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=2)
            print(f"Updated {f} in repo.")
