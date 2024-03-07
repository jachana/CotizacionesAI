import requests
import os

def find_item_id_by_sku(api_key, board_id, sku_column_id, sku_value):
    query = f'''
    query {{
      items_by_column_values(board_id: {board_id}, column_id: "{sku_column_id}", column_value: "{sku_value}") {{
        id
      }}
    }}
    '''
    headers = {
        'Authorization': api_key,
        'Content-Type': 'application/json'
    }
    data = {
        'query': query
    }
    response = requests.post('https://api.monday.com/v2', json=data, headers=headers)
    result = response.json()
    # Assuming the SKU is unique and only one item will match
    if result['data']['items_by_column_values']:
        return result['data']['items_by_column_values'][0]['id']
    else:
        return None

def update_row(api_key, board_id, sku_column_id, sku, value_column_id, value):
    item_id = find_item_id_by_sku(api_key, board_id, sku_column_id, sku)
    if item_id:
        mutation = f'''
        mutation {{
          change_column_value(board_id: {board_id}, item_id: {item_id}, column_id: "{value_column_id}", value: "{value}") {{
            id
          }}
        }}
        '''
        headers = {
            'Authorization': api_key,
            'Content-Type': 'application/json'
        }
        data = {
            'query': mutation
        }
        response = requests.post('https://api.monday.com/v2', json=data, headers=headers)
        print(response.json())
    else:
        print(f"No item found with SKU: {sku}")

# Example usage
