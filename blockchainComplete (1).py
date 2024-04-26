import os
import json
import operator
from sort_functions import bubble_sort, selection_sort

def find_fork_start(input_list):
    input_list = input_list.copy()  # копируем
    output = []  # список для  форков
    
    # цикл по элементам
    for _ in range(len(input_list)):
        current_element = input_list.pop()  # берем текущ элемент 
        
        matching_element = None
        # ищем элемент 
        for x in input_list:
            if x['index'] == current_element['index'] and x['pre_hash'] == current_element['pre_hash']:
                matching_element = x
                break
        
        # условия для тру
        if matching_element is not None:
            parent_node = None
            # находим родительский узел для текущего элемента
            for x in input_list:
                if x['hash'] == current_element['pre_hash']:
                    parent_node = x
                    break
            # флажок
            current_element['is_main'] = True if current_element['timestamp'] < matching_element['timestamp'] else False
            matching_element['is_main'] = True if current_element['timestamp'] > matching_element['timestamp'] else False
            # добавляем информацию о форке в вывод
            output.append({'fork_pair': [current_element, matching_element], 'parent_node': parent_node})
    
    return output



def build_fork(start, lst):
    return_obj = {'main_path': None, 'fork': None}
    lst = lst.copy()
    prev_item = lst.pop(lst.index(start)) 
    out = [prev_item]  # список для хранения пути ветки
    for _ in range(0, len(lst)):
        try:
            # проверка прихэшов с хэшэм
            next_item = next(item for item in lst if item['pre_hash'] == prev_item['hash'])
            prev_item = next_item
            out.append(next_item)
        except:
            pass
    # main fork / path
    if start['is_main']:
        return_obj['main_path'] = out
    else:
        return_obj['fork'] = out
    return return_obj
  

transaction_list = []

# цикл для транзакций
directory = "transactions"
for file_name in os.listdir(directory):
    file_path = os.path.join(directory, file_name)
    with open(file_path, "r") as file:
        try:
            data = json.load(file)
            transaction_list.append(data)
        finally:
            print("")

# Задание номер 1 сортировки пузырьком и не пузырьком
# Сортировка пузырьком списка transaction_list
transaction_list = bubble_sort(transaction_list)

# Сортировка отбором списка transaction_list
transaction_list = selection_sort(transaction_list)
            
# transaction_list = sorted(transaction_list, key=operator.itemgetter('index'))

start_fork_array = find_fork_start(transaction_list)
start_fork_array.reverse()

repo_path = {'main_branch': [], 'forks': []}

# pathes
for item in start_fork_array:
    for el in item['fork_pair']:
        paths = build_fork(el, transaction_list)
        repo_path['main_branch'].extend(paths['main_path']) if paths['main_path'] is not None else None
        repo_path['forks'].append(paths['fork']) if paths['fork'] is not None else None

# Проверка дупликатов
        
unique_main_branch = list({v['index']: v for v in repo_path['main_branch']}.values())
first_path = transaction_list[1:17]

first_path.extend(unique_main_branch)
repo_path['main_branch'] = first_path

total_blocks = len(repo_path['main_branch'])
for el in repo_path['forks']:
    total_blocks += len(el)
print("Total number of blocks: %s" % (total_blocks + 1))

total_blocks = 0
for el in transaction_list:
    total_blocks += len(el)
print("Total number of blocks: %s" % (total_blocks + 1))

# ex1
for element in transaction_list:
    if element['hash'].endswith('000'):
        print("ex 1. Block index: %d, Author: %s" % (element['index'], element['transactions'][-1]['to']))

# ex 7
print("ex 7 - Reward amount for creating block 71:", transaction_list[89]['transactions'][4]['value'])

# ex 8
current_reward_amount = repo_path['main_branch'][0]['transactions'][-1]['value']
chain_length = 1
for i in repo_path['main_branch']:
    if i['transactions'][-1]['value'] == current_reward_amount:
        chain_length += 1
    else:
        break
print("ex 8 - Chain length where Reward remains the same: %d" % chain_length)

# ex 9
reward_ratio = repo_path['main_branch'][chain_length - 1]['transactions'][-1]['value'] / repo_path['main_branch'][chain_length - 2]['transactions'][-1]['value']
print("ex 9 - Reward reduction ratio: %0.2f" % reward_ratio)

# ex 10
if repo_path['main_branch'][-1]['transactions'][-1]['value'] <= 0.09:
    tmp_main_branch = repo_path['main_branch']
    tmp_main_branch.reverse()
    for i in tmp_main_branch:
        if i['transactions'][-1]['value'] == 0.09:
            block_index = i['index']
            break
else:
    current_last_reward = repo_path['main_branch'][-1]['transactions'][-1]['value']
    block_index = repo_path['main_branch'][-1]['index']
    blocks_to_drop_reward = chain_length - (block_index % chain_length)
    block_index += blocks_to_drop_reward
    current_last_reward = current_last_reward * reward_ratio
    while round(current_last_reward, 2) > 0.09:
        current_last_reward = current_last_reward * reward_ratio
        block_index += chain_length
current_last_reward = round(current_last_reward, 2)
print("ex 10 - Block index with a reward equal to 0.09: %d" % block_index)

# ex 11
secret_blocks = []
for i in repo_path['main_branch']:
    if i.get('secret_info'):
        secret_block = {"index": i['index'], "secret_info": i['secret_info']}
        secret_blocks.append(secret_block)
list_secret_indexes = [d['index'] for d in secret_blocks]
print("ex 11 - Blocks indexes with information recorded in secret_info:", list_secret_indexes)

# ex 12
list_secret_data = [d['secret_info'] for d in secret_blocks]
print("ex 12 - Blocks secret data:", list_secret_data)

# ex 13
output_string = "".join(list_secret_data)
bytes_obj = bytes.fromhex(output_string)
output_string = bytes_obj.decode('utf-8')
print("ex 13 - Decoded string: %s" % output_string)
