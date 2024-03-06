# Import necessary libraries
import openai
import requests

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
    query = 'query {  boards(ids: ' + str(board_id) + ') {    name    columns {      title   id       }  }}'
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
    columns_request = 'items{ name column_values(ids:["precio_venta" "formato" "marca" "tipo8"]){id value}}'
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
    #print( response_json)
    items_count = response_json['data']['boards'][0]['items_count']
    print("items_count == " + str(items_count))
    items_requested = page_size
    print("items_requested == " + str(items_requested))
    #add the first page to the list
    for item in response_json['data']['boards'][0]['items_page']['items']:
        name = item['name']
        price = item['column_values'][1]['value']
        brand = item['column_values'][0]['value']
        product_type = item['column_values'][3]['value']
        if(brand == None):
            brand = "N/A"
        format = item['column_values'][2]['value']
        if format == None:
            format = "0"

        productsList.append((name ,brand, price,format, product_type))
    #TODO
        #I NEEED TO MATCH THE NAME BRAND BVALUE AND FORMAT TO THE CORRECT COLUMN NAMES
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
                brand = item['column_values'][0]['value']

                value = item['column_values'][1]['value']
                if value == None:
                    value = "0"
                format = item['column_values'][2]['value']
                if format == None:
                    format = "0"
                product_type = item['column_values'][3]['value']
                productsList.append((name , brand, value,format,product_type))
            if(cursor == None):
                break
            print("cursor == " + cursor)

    print("list length == " + str(len(productsList)))
    return productsList

def create_data_files():

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
    #define the file naemes
    tambores_file_name = "tambores.json"
    baldes_file_name = "baldes.json"
    cajas_file_name = "cajas.json"
    otros_file_name = "otros.json"

    tambores_file = open(tambores_file_name, "w", encoding="utf-8")
    baldes_file = open(baldes_file_name, "w",encoding="utf-8")
    cajas_file = open(cajas_file_name, "w",encoding="utf-8")
    otros_file = open(otros_file_name, "w",encoding="utf-8")

    sum = 0
    # #write headers
    # tambores_file.write("Nombre ; Precio ; Marca ; Formato\n")
    # baldes_file.write("Nombre ; Precio ; Marca ; Formato\n")
    # cajas_file.write("Nombre ; Precio ; Marca ; Formato\n")
    # otros_file.write("Nombre ; Precio ; Marca ; Formato\n")

    tambores_file.write("[\n")
    baldes_file.write("[\n")
    cajas_file.write("[\n")
    otros_file.write("[\n")


    for product in board_data:
        product_string = "{\n"

        #write the first element to a file
        name = product[0]
        value =product[2]
        if value == None:
            value = "9999999999"
        else:
            value = eval(product[2])
        format = product[3]
        brand = product[1]
        if(brand == None):
            brand = "N/A"

        if format != "0":
            if format[9] == '0':
                format = "balde"
            elif format[9] == '1':
                format = "tambor"
            elif format[9] == '2':
                format = "caja"
        else:
            format = "otro"

        product_type = product[4]
        if product_type == None:
            product_type = "N/A"
        #replace all " in strings with '
        name = name.replace("\"", "")
        brand = brand.replace("\"", "")
        format = format.replace("\"", "")
        product_type = product_type.replace("\"", "")

        #print (value)
        product_string += "  \"Nombre\": \"" + name + "\",\n"
        product_string += "  \"Precio\": " + str(value) + ",\n"
        product_string += "  \"Marca\": \"" + brand + "\",\n"
        product_string += "  \"Formato\": \"" + format + "\",\n"
        product_string += "  \"Tipo\": \"" + product_type + "\"\n"
        product_string += "},\n"
        if format == "tambor":
            tambores_file.write(product_string)
        elif format == "balde":
            baldes_file.write(product_string)
        elif format == "caja":
            cajas_file.write(product_string)
        else:
            otros_file.write(product_string)

        sum += int(value)
    #remove the last comma
    tambores_file.seek(tambores_file.tell() - 3, 0)
    baldes_file.seek(baldes_file.tell() - 3, 0)
    cajas_file.seek(cajas_file.tell() - 3, 0)
    otros_file.seek(otros_file.tell() - 3, 0)
    # close the JSON array
    tambores_file.write("\n]")
    baldes_file.write("\n]")
    cajas_file.write("\n]")
    otros_file.write("\n]")

    #close the file
    tambores_file.close()
    cajas_file.close()
    baldes_file.close()
    otros_file.close()
    print("The sum of all the items is " + str(sum))

    return [tambores_file_name, cajas_file_name, baldes_file_name, otros_file_name]
