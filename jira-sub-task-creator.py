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

    def create(self) -> bool:
        body = {
            "fields":
            {
                "project":
                {
                    "key": JIRA_PROJECT
                },
                "parent":
                {
                    "key": self.parent
                },
                "summary": self.title,
                "description": self.description.replace('**', '*'),
                "issuetype":
                {
        "self": "https://flow.sbb.ch/rest/api/2/issuetype/10003",
                    "id": "10003",
                    "description": "The sub-task of the issue",
                    "iconUrl": "https://flow.sbb.ch/secure/viewavatar?size=xsmall&avatarId=10316&avatarType=issuetype",
                    "name": "Sub-task",
                    "subtask": True,
                    "avatarId": 10316
                }
            }
        }
        print(f'[+] creating sub_task: {self.parent} - {self.title}')
        response = requests.post(f"{JIRA_HOME}/rest/api/2/issue", json=body, headers=HEADERS)
        success = False
        if response.status_code == 201:
            success = True
        reason = response.text
        if response.headers['Content-Type'].find('application/json') < 0:
            reason = '{"error": "invalid cookie"}'
            success = False
        return {'success': success, 'reason': reason, 'sub_task': self }

def create_sub_tasks_from_file(file_name):
    print(f'[+] parsing sub_tasks from file: {file_name}')
    sub_tasks = []
    with open(file_name) as f:
        parent = ''
        title = ''
        description = ''
        for line in f.readlines():
            line = line.strip()
            if re.match('^#\s*', line):
                if parent != '':
                    sub_tasks.append(SubTask(parent, title, description))
                parent = re.sub('^#\s*', '', line)
                title = ''
                description = ''
            if re.match('^\s*\*\s+', line):
                if title != '':
                    sub_tasks.append(SubTask(parent, title, description))
                title = re.sub('^\s*\*\s+', '', line)
                description = ''
            if re.match('^\s*\*\*\s+', line):
                description += (re.sub('^\s*', '', line) + '\n')
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
        responses = []
        for sub_task in sub_tasks:
            responses.append(sub_task.create())
        print('__________________________\n')
        print("RESPONSES")
        print('__________________________\n')
        for response in responses:
            if response['success']:
                sub_task = response['sub_task']
                reason = response['reason']
                print(f'✅ {reason}')
                print(f'# {sub_task.parent}')
                print(f'* {sub_task.title}')
                print(f'{sub_task.description}')
        has_error = False
        for response in responses:
            if not response['success']:
                sub_task = response['sub_task']
                reason = response['reason']
                print(f'❌ {reason}')
                print(f'# {sub_task.parent}')
                print(f'* {sub_task.title}')
                print(f'{sub_task.description}')
                has_error = True
        print("[+] completed")
        if not has_error:
            print('''.===================================================================.
||                            ____    No errors                    ||
||                          .'    '.  Cheers!                      ||
||                         /   |  | \          oOoOo               ||
||                        |          |      ,==|||||               ||
||                         \ '.___.'/      _|| |||||               ||
||                          '.____.'   _.-'^|| |||||               ||
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
.===================================================================.''')


if __name__ == '__main__':
    create_sub_tasks_from_file(TASKS_FILE)
