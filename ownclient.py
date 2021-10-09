import sys
import requests

# Данные авторизации в API Trello
auth_params = {
    'key': "a5b16ff550557cef14ef8f287e9dc856",
    'token': "8f4833e5e2deb4e64b0cb55c3fbfebe68e319cc7c156d10d30192ac655c5c5df", }

# Адрес, на котором расположен API Trello, # Именно туда мы будем отправлять HTTP запросы.
base_url = "https://api.trello.com/1/{}"

board_id = "5cInxnwk"

def read():
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()

    for column in column_data:
        task_data = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
        print(column['name'] + ' ' + str(len(task_data)) + 'tasks')
        if not task_data:
            print('No tasks')
            continue
        for task in task_data:
            print(task['name'])
    print("argv[1] = create_task - создать задачу, argv[1] = create_column - создать колонку, argv[1] = move - переместить задачу")
    print("argv[2] - имя задачи, argv[3] - имя колонки")

def create_task(name, column_name):
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()

    for column in column_data:
        column_tasks = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
        for task in column_tasks:
            if task['name']==name:
                print("Данное имя уже использовано! в колонке ", column['name'])
                break
            else:
                if column['name'] == column_name:
                    requests.post(base_url.format('cards'), data={'name': name, 'idList': column['id'], **auth_params})
                    break

def create_column(name):
    board_id = "615e09bbe590c90ea9cdeb0a"
    requests.post(base_url.format('lists'), data={'name': name, 'idBoard': board_id, **auth_params})


def move(name, column_name):
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()

    choose_task=None

    task_id=None

    for column in column_data:
        column_tasks = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
        for task in column_tasks:
            if task['name']==name:
                task_id = task['id']
            if task_id:
                break


    for column in column_data:
        if column['name'] == column_name:
            requests.put(base_url.format('cards') + '/' + task_id + '/idList', data={'value': column['id'], **auth_params})
            break

if __name__ == "__main__":
    if len(sys.argv) == 1:
        read()
    elif sys.argv[1] == 'create':
	    create_task(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'move':
        move(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'create_column':
        create_column(sys.argv[2])
    elif (sys.argv[1] != 'create') and (sys.argv[1] != 'move') and (sys.argv[1] != 'create_column'):
        print('Incorrect argument')