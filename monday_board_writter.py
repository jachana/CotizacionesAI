import requests
import os

def find_item_id_by_sku(sku_value, products_list):
  counter = 0
  for product in products_list:
    # if counter < 5:
    #   counter += 1
    #   print("compare: ", product[6], " with: ", sku_value)
    if product[6] == sku_value:
      return product[0]


def update_row(api_key, board_id,  sku, value_column_id, value, products_list):
    item_id = find_item_id_by_sku( sku, products_list)
    if item_id:
        mutation = f'''
        mutation {{
          change_simple_column_value(board_id: {board_id}, item_id: {item_id}, column_id: "{value_column_id}", value: "{value}") {{
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
        #check if the request was successful
        if response.status_code == 200:
            #print(f"Item with SKU: {sku} updated successfully")
            pass
        else:
            print(f"Error updating item with SKU: {sku}")
    else:
        print(f"No item found with SKU: {sku}")

# Example usage
