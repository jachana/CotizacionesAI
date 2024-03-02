# Import necessary libraries
import openai
import requests

# OpenAI API Key
openai.api_key = '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'

# Monday.com API Key
monday_api_key = 'eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjI5OTI2MDc5NiwiYWFpIjoxMSwidWlkIjo1MTIxODQzNiwiaWFkIjoiMjAyMy0xMS0yOFQyMDoyMzoyMC4wMDBaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6MTk2NDA1NTYsInJnbiI6InVzZTEifQ.2TEc781SSNyHVkafhut5iYSARIoGpBTgqPJcrTDhlUg'


#using monday.com API to get the board data

def get_boards_structure():
    query =     query = 'query {  me {    name  }  boards(limit: 100) {    name   id  }}'

    url = 'https://api.monday.com/v2'
    headers = {'Authorization': monday_api_key}
    data = {'query': query}
    response = requests.post(url, json=data, headers=headers)
    return response.json()

#get the board structure,column names and types
def get_board_structure(board_id):
    query = 'query {  boards(ids: ' + str(board_id) + ') {    name    columns {      title         }  }}'
    print(query)
    url = 'https://api.monday.com/v2'
    headers = {'Authorization': monday_api_key}
    data = {'query': query}
    response = requests.post(url, json=data, headers=headers)
    return response.json()



def get_board_data(board_id):
  #here I might have to use pagination to get all the data
    #first I should get the biggest page size possible
    productsList = []
    columns_request = 'items{ name column_values(ids:["precio_venta","formato"]){id value}}'
    page_size = 500
    #get the first page
    query = 'query {  boards(ids: ' + str(board_id) + ') { id items_page(limit: '+str(page_size)+'){ '+columns_request+' cursor  } items_count  }}'
    print(query)
    url = 'https://api.monday.com/v2'
    headers = {'Authorization': monday_api_key}
    data = {'query': query}
    response = requests.post(url, json=data, headers=headers)
    # now I should get the next pages if there are any
    #first check if there are more pages
    response_json = response.json()
    #print(response_json)
    #print( response_json)
    items_count = response_json['data']['boards'][0]['items_count']
    print("items_count == " + str(items_count))
    items_requested = page_size
    print("items_requested == " + str(items_requested))
    #add the first page to the list
    for item in response_json['data']['boards'][0]['items_page']['items']:
        name = item['name']
        value = item['column_values'][0]['value']
        if value == None:
            value = "0"
        format = item['column_values'][1]['value']
        if format == None:
            format = "0"
        productsList.append((name , value,format))

    if items_count > items_requested:
        #get the next pages
        cursor = response_json['data']['boards'][0]['items_page']['cursor']

        print("cursor == " + cursor)
        while items_requested < items_count:
            query = 'query {  next_items_page (limit: ' + str(page_size) + ', cursor: "' + cursor + '") {'+columns_request+' cursor }  }'
            print(query)
            data = {'query': query}
            response = requests.post(url, json=data, headers=headers)
            response_json = response.json()
            items_requested += page_size
            cursor = response_json['data']['next_items_page']['cursor']
            #add the items to the list
            for item in response_json['data']['next_items_page']['items']:
                name = item['name']
                value = item['column_values'][0]['value']
                if value == None:
                    value = "0"
                format = item['column_values'][1]['value']
                if format == None:
                    format = "0"
                productsList.append((name , value,format))
            if(cursor == None):
                break
            print("cursor == " + cursor)

    print("list length == " + str(len(productsList)))
    return productsList



#get the board content
boards_structure = get_boards_structure()

#print(boards_structure)
#parse the boards
boards = boards_structure['data']['boards']
#print(boards)
print ("we have " + str(len(boards)) + " boards in the account.")


#find the products board ID called "Subelementos de Productos"
products_board_id = 0
products_board_name = "Productos"
for board in boards:
    if board['name'] == products_board_name:
        #print(board)
        products_board_id = board['id']
        break

print("Checking board with name " + products_board_name + " and ID " + str(products_board_id))

#Get All column names for the board
#board_data = get_board_structure(products_board_id)
#print(board_data)


#Get the board data
board_data = get_board_data(products_board_id)
#print(board_data)

tambores_file = open("tambores.txt", "w")
baldes_file = open("baldes.txt", "w")
cajas_file = open("cajas.txt", "w")
otros_file = open("otros.txt", "w")
sum = 0
for product in board_data:
    #write the first element to a file
    name = product[0]
    value = eval(product[1])
    format = product[2]
    if format != "0":
        print(format[9])
        if format[9] == '0':
            format = "balde"
            baldes_file.write(name + " ; " + str(value) + " ; " + format + "\n")
        elif format[9] == '1':
            format = "tambor"
            tambores_file.write(name + " ; " + str(value) + " ; " + format + "\n")
        elif format[9] == '2':
            format = "caja"
            cajas_file.write(name + " ; " + str(value) + " ; " + format + "\n")
    else:
        format = "otro"
        otros_file.write(name + " ; " + str(value) + " ; " + format + "\n")
    #print (value)
    sum += int(value)
#close the file
tambores_file.close()
cajas_file.close()
baldes_file.close()
otros_file.close()
print("The sum of all the items is " + str(sum))
