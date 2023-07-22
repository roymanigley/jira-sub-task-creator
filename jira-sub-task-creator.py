import requests
import sys
import re


JIRA_HOME = 'https://flow.sbb.ch'
JIRA_PROJECT = 'CAPRE'
COOKIE_FILE = 'cookie.txt'
TASKS_FILE = 'tasks.md'

with open(COOKIE_FILE) as f:
    cookie = f.read()

HEADERS = {
    'Cookie': cookie.replace('\n', ''),
    'Content-Type': 'application/json'
}


class SubTask:

    def __init__(self, parent: str, title: str, description: str):
        self.parent = parent
        self.title = title
        self.description = description

    def create(self):
        description = self.description.replace('\n', '\\n').replace('** ', '* ')
        body = f'''{{
    "fields":
    {{
        "project":
        {{
            "key": "{JIRA_PROJECT}"
        }},
        "parent":
        {{
            "key": "{self.parent}"
        }},
        "summary": "{self.title}",
        "description": "{description}",
        "issuetype":
        {{
"self": "https://flow.sbb.ch/rest/api/2/issuetype/10003",
            "id": "10003",
            "description": "The sub-task of the issue",
            "iconUrl": "https://flow.sbb.ch/secure/viewavatar?size=xsmall&avatarId=10316&avatarType=issuetype",
            "name": "Sub-task",
            "subtask": true,
            "avatarId": 10316
        }}
    }}
}}'''
        print(f'[+] creating sub_task: {self.parent} - {self.title}')
        # print(body)
        response = requests.post(f"{JIRA_HOME}/rest/api/2/issue", data=body, headers=HEADERS)
        print(f'[>] {response.text}')

def create_sub_tasks_from_file(file_name):
    print(f'[+] parsing sub_tasks from file: {file_name}')
    sub_tasks = []
    with open(file_name) as f:
        parent = ''
        title = ''
        description = ''
        for line in f.readlines():
            if re.match('^#\s*', line):
                if parent != '':
                    sub_tasks.append(SubTask(parent, title, description))
                parent = re.sub('^#\s*', '', line[:-1])
                title = ''
                description = ''
            if re.match('^\s*\*\s+', line):
                if title != '':
                    sub_tasks.append(SubTask(parent, title, description))
                title = re.sub('^\s*\*\s+', '', line[:-1])
                description = ''
            if re.match('^\s*\*\*\s+', line):
                description += re.sub('^\s*', '', line)
        sub_tasks.append(SubTask(parent, title, description))
    print(f'[+] {len(sub_tasks)} found')
    previous_parent = ''
    for sub_task in sub_tasks:
        if sub_task.parent != previous_parent:
            print('__________________________\n')
            print(f'# {sub_task.parent}')
            previous_parent = sub_task.parent
        print(f'* {sub_task.title}')
        print(f'{sub_task.description}')
    print('__________________________\n')

    create_sub_tasks = input('[?] create those sub_tasks [y/N]: ')
    if create_sub_tasks.lower() == 'y':
        print('[+] creating sub_tasks')
        for sub_task in sub_tasks:
            sub_task.create()
        print("[+] completed")
        print('''.===================================================================.
||                            ___                                  ||
||                          .'   '.  Cheers!                       ||
||                         /       \           oOoOo               ||
||                        |         |       ,==|||||               ||
||                         \       /       _|| |||||               ||
||                          '.___.'    _.-'^|| |||||               ||
||                        __/_______.-'     '==HHHHH               ||
||                   _.-'` /                   """""               ||
||                .-'     /   oOoOo                                ||
||                `-._   / ,==|||||                                ||
||                    '-/._|| |||||                                ||
||                     /  ^|| |||||                                ||
||                    /    '==HHHHH                                ||
||                   /________"""""                                ||
||                   `\       `\                                   ||
||                     \        `\   /                             ||
||                      \         `\/                              ||
||                      /                                          ||
||                     /                                           ||
||         by royman  /_____                                       ||
||                                                                 ||
'==================================================================='''')


if __name__ == '__main__':
    create_sub_tasks_from_file(TASKS_FILE)
