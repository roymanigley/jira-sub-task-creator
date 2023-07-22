# JIRA SubTask Creator
> Creates SubTasks in JIRA according to a `markdown` file

## Initial Setup

    python3 -m venv .env
    source .env/bin/activate
    pip install -r requirements.txt

## Usage

1. copy the `cookie` from your browser and paste it to the `cookie.txt` file
2. run the python script  

```
python3 jira-sub-task-creator.py
```

## Example

### `tasks.md`

    # CAPRE-1234
    * SUB_TASK_TITLE 1
      ** DESCRIPTION 1
      ** DESCRIPTION 2

    * SUB_TASK_TITLE 2
      ** DESCRIPTION 1
    * SUB_TASK_TITLE 3
      ** DESCRIPTION 1


    # CAPRE-5678
    * SUB_TASK_TITLE 1
      ** DESCRIPTION 1
      ** DESCRIPTION 2

    * SUB_TASK_TITLE 2
      ** DESCRIPTION 1
    * SUB_TASK_TITLE 3
      ** DESCRIPTION 1

