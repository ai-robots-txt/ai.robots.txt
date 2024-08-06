import json
from pathlib import Path

import requests
from bs4 import BeautifulSoup

session = requests.Session()
response = session.get("https://darkvisitors.com/agents")
soup = BeautifulSoup(response.text, "html.parser")

existing_content = json.loads(Path("./robots.json").read_text())

for section in soup.find_all("div", {"class": "agent-links-section"}):
    category = section.find("h2").get_text()
    for agent in section.find_all("a", href=True):
        name = agent.find("div", {"class": "agent-name"}).get_text().strip()
        desc = agent.find("p").get_text().strip()
        
        if name in existing_content:
            print(f"{name} already exists in robots.json")
            continue
        # Template:
        # "Claude-Web": {
        #     "operator": "[Anthropic](https:\/\/www.anthropic.com)",
        #     "respect": "Unclear at this time.",
        #     "function": "Scrapes data to train Anthropic's AI products.",
        #     "frequency": "No information. provided.",
        #     "description": "Scrapes data to train LLMs and AI products offered by Anthropic."
        # }
        existing_content[name] = {
            "operator": "Unclear at this time.",
            "respect": "Unclear at this time.",
            "function": "Unclear at this time.",
            "frequency": "Unclear at this time.",
            "description": f"{desc} More info can be found at https://darkvisitors.com/agents{agent['href']}"
        }

Path("./robots.json").write_text(json.dumps(existing_content, indent=4))