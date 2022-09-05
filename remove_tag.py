from config import *
from pathlib import Path

def delete_tag(folder):
    for item in projects.iterdir():
        if item.is_file():
            with open(item,"r") as f:
                content = f.read()
            content = content.replace("#Projects","")
            with open(item,"w") as f:
                f.write(content)
            print(f"Updated file: {item.name}")
        # else:
        #     delete_tag(item)

delete_tag(projects)


