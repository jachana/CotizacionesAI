import datetime
import requests
import os

# Monday.com API Key
monday_api_key = os.getenv("MONDAY_API_KEY")
#using monday.com API to get the board data

def find_board_id_from_name(name):
    boards_structure = get_boards_structure()
    boards = boards_structure['data']['boards']
    for board in boards:
        if board['name'] == name:
            return board['id']
    return None

def get_boards_structure():
    query =     query = 'query {  me {    name  }  boards(limit: 100) {    name   id  }}'

    url = 'https://api.monday.com/v2'
    headers = {'Authorization': monday_api_key}
    data = {'query': query}
    response = requests.post(url, json=data, headers=headers)
    return response.json()

#get the board structure,column names and types
def get_board_structure(board_id):
    query = 'query {  boards(ids: ' + str(board_id) + ') {    name    columns {      title   id       }  }}'
    url = 'https://api.monday.com/v2'
    headers = {'Authorization': monday_api_key}
    data = {'query': query}
    response = requests.post(url, json=data, headers=headers)
    return response.json()


def find_item_id_by_sku(sku_value, products_list):
  for product in products_list:
    if product[6] == sku_value:
      return product[0]

def add_subitem( item_id,  subitem_id, subitem_name):
    mutation = f'''
    mutation {{
          create_subitem (item_name: "{subitem_name}", parent_item_id: {item_id}, \\"conectar_tablros\\": [\\"{subitem_id}\\"]") {{
        id
      }}
    }}
    '''
    print (mutation)
    headers = {
        'Authorization': monday_api_key,
        'Content-Type': 'application/json'
    }
    data = {
        'query': mutation
    }
    response = requests.post('https://api.monday.com/v2', json=data, headers=headers)
    #check if the request was successful
    if response.status_code == 200:
        print(f"Subitem: {subitem_name} added successfully")
        print(response.json())
    else:
        print(f"Error adding subitem: {subitem_name}")
        print(response)

def add_quote_row(quote):
  

  quotes_id = find_board_id_from_name("Cotizaciones")
  print(get_board_structure(quotes_id))
  current_month = datetime.datetime.now().month
  #transform the current month to a string in spanish
  if current_month == 1:
    current_month = "Enero"
  elif current_month == 2:
    current_month = "Febrero"
  elif current_month == 3:
    current_month = "Marzo"
  elif current_month == 4:
      current_month = "Abril"
  elif current_month == 5:
      current_month = "Mayo"
  elif current_month == 6:
      current_month = "Junio"
  elif current_month == 7:
      current_month = "Julio"
  elif current_month == 8:
      current_month = "Agosto"
  elif current_month == 9:
      current_month = "Septiembre"
  elif current_month == 10:
      current_month = "Octubre"
  elif current_month == 11:
      current_month = "Noviembre"
  elif current_month == 12:
      current_month = "Diciembre"

  print(f"Current month: {current_month}")
  total_price = 0
  for product in quote:
    total_price += product[3]

 

  if quotes_id:
     #add a mutation to create a new item in the board
    # the new item will have the name of the quote
    #each element in the quote list is a tuple with the following structure (product_name, unit_price, quantity, total_price)
    #each element should be a subitem in the quote item
    
    mutation = "mutation { create_item (board_id: " + str(quotes_id) + ", group_id: \"topics\", item_name: \"Cotizacion test Julio \") { id } }"
    print (mutation)

    headers = {
        'Authorization': monday_api_key,
        'Content-Type': 'application/json'
    }
    data = {
        'query': mutation
    }
    response = requests.post('https://api.monday.com/v2', json=data, headers=headers)
    #check if the request was successful
    if response.status_code == 200:
        print(f"Quote: {quote} added successfully")
        print(response.json())
        #get the id of the new item
        item_id = response.json()['data']['create_item']['id']
    else:
        print(f"Error adding quote: {quote}")
        print(response)
  else:
    print(f"No board found with name: Cotizaciones")
  if item_id:
     for product in quote:
        #add a subitem for each product in the quote
        name = product[0]
        id = product[4]
        print( id)
        #add a subitem for each product in the quote
        print( product)
        add_subitem(item_id, id, name)
  
def update_row(api_key, board_id,  sku, value_column_id, value, item_id=None):
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
