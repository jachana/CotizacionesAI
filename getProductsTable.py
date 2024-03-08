# Import necessary libraries
import openai
import requests
import monday_board_writter
import os
# Monday.com API Key
monday_api_key = os.getenv("MONDAY_API_KEY")
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
    url = 'https://api.monday.com/v2'
    headers = {'Authorization': monday_api_key}
    data = {'query': query}
    response = requests.post(url, json=data, headers=headers)
    return response.json()

def get_board_data(board_id, columns_requested = ["precio_venta","formato","marca","tipo8"]):
  #here I might have to use pagination to get all the data
    #first I should get the biggest page size possible
    productsList = []

    columns_request = 'items{ id name column_values(ids:['
    for column in columns_requested:
        columns_request += "\"" + column + "\" "
    columns_request += ']) {id value}}'
    page_size = 500
    #get the first page
    query = 'query {  boards(ids: ' + str(board_id) + ') { id items_page(limit: '+str(page_size)+'){ '+columns_request+' cursor  } items_count  }}'
    url = 'https://api.monday.com/v2'
    headers = {'Authorization': monday_api_key}
    data = {'query': query}
    response = requests.post(url, json=data, headers=headers)
    # now I should get the next pages if there are any
    #first check if there are more pages
    response_json = response.json()
    items_count = response_json['data']['boards'][0]['items_count']
    items_requested = page_size
    #add the first page to the list
    for item in response_json['data']['boards'][0]['items_page']['items']:
        name = item['name']
        item_id = item['id']
        price = item['column_values'][1]['value']
        brand = item['column_values'][0]['value']
        product_type = item['column_values'][3]['value']
        if(brand == None):
            brand = "N/A"
        format = item['column_values'][2]['value']
        if format == None:
            format = "0"
        sku = item['column_values'][4]['value']
        annual_sales = item['column_values'][5]['value']
        productsList.append((item_id, name ,brand, price,format, product_type, sku,annual_sales))

    if items_count > items_requested:
        #get the next pages
        cursor = response_json['data']['boards'][0]['items_page']['cursor']

        while items_requested < items_count:
            query = 'query {  next_items_page (limit: ' + str(page_size) + ', cursor: "' + cursor + '") {'+columns_request+' cursor }  }'
            data = {'query': query}
            response = requests.post(url, json=data, headers=headers)
            response_json = response.json()
            items_requested += page_size
            cursor = response_json['data']['next_items_page']['cursor']
            #add the items to the list
            for item in response_json['data']['next_items_page']['items']:
                name = item['name']
                item_id = item['id']

                brand = item['column_values'][0]['value']

                value = item['column_values'][1]['value']
                if value == None:
                    value = "0"
                format = item['column_values'][2]['value']
                if format == None:
                    format = "0"
                product_type = item['column_values'][3]['value']
                sku = item['column_values'][4]['value']
                annual_sales = item['column_values'][5]['value']
                productsList.append((item_id, name , brand, value,format,product_type,sku,annual_sales))
            if(cursor == None):
                break

    return productsList

def find_board_id_from_name(name):
    boards_structure = get_boards_structure()
    boards = boards_structure['data']['boards']
    for board in boards:
        if board['name'] == name:
            return board['id']
    return None

def create_data_files():

    #find the products board ID called "Productos"
    products_board_id = find_board_id_from_name("Productos")

    desired_columns = ["precio_venta","formato","marca","tipo8", "sku", "n_meros1"]

    board_data = get_board_data(products_board_id,desired_columns)

    #print the data one row at a time
    # for row in board_data:
    #     print(row)


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

    tambores_file.write("[\n")
    baldes_file.write("[\n")
    cajas_file.write("[\n")
    otros_file.write("[\n")
    tambores_element_amount = 0
    cajas_element_amount = 0
    baldes_element_amount = 0
    otros_element_amount = 0

    for product in board_data:

        product_string = "{\n"

        #write the first element to a file
        name = product[1]
        value =product[3]
        if value == None:
            value = "9999999999"
        else:
            value = eval(product[3])
        format = product[4]
        brand = product[2]
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

        product_type = product[5]

        SKU = product[6]

        if product_type == None:
            product_type = "N/A"
        #replace all " in strings with '
        name = name.replace("\"", "")
        brand = brand.replace("\"", "")
        format = format.replace("\"", "")
        product_type = product_type.replace("\"", "")
        if(SKU == None):
            SKU = "MISSING SKU"
        SKU = SKU.replace("\"", "")

        annual_sales = product[7]
        if(annual_sales == None):
            annual_sales = "0"
        else:
            annual_sales = annual_sales.replace("\"", "")

        product_string += "  \"Nombre\": \"" + name + "\",\n"
        product_string += "  \"Precio\": " + str(value) + ",\n"
        product_string += "  \"Marca\": \"" + brand + "\",\n"
        product_string += "  \"Formato\": \"" + format + "\",\n"
        product_string += "  \"Tipo\": \"" + product_type + "\",\n"
        product_string += "  \"SKU\": \"" + str(SKU) + "\",\n"
        product_string += "  \"Anual Sales\": \"" + str(annual_sales) + "\"\n"
        product_string += "}"

        if format == "tambor":
            #if it is the first element on this file, do not add a comma
            if tambores_element_amount > 0:
                tambores_file.write(",\n")
            tambores_element_amount += 1
            tambores_file.write(product_string)
        elif format == "balde":
            if baldes_element_amount > 0:
                baldes_file.write(",\n")
            baldes_element_amount += 1
            baldes_file.write(product_string)
        elif format == "caja":
            if cajas_element_amount > 0:
                cajas_file.write(",\n")
            cajas_element_amount += 1
            cajas_file.write(product_string)
        else:
            if otros_element_amount > 0:
                otros_file.write(",\n")
            otros_element_amount += 1
            otros_file.write(product_string)

        sum += int(value)

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

    return [tambores_file_name, cajas_file_name, baldes_file_name, otros_file_name]

def insert_row(board_id):
    pass
def update_row(board_id ,sku, value_column_id, value,products_list):
    api_key = os.getenv('MONDAY_API_KEY')

    monday_board_writter.update_row(api_key, board_id, sku, value_column_id, value, products_list)

def update_anual_sales():
    value_column_id = 'n_meros1'  # The column ID where you want to update the value
    sku = '"4202865"'  # The SKU value to match
    value = 0  # The new value to set, make sure it's a JSON string
    board_id = find_board_id_from_name("Productos")
    product_list = get_board_data(board_id,["precio_venta","formato","marca","tipo8", "sku", "n_meros1"] )
    #print the list of products row by row
    # for product in product_list:
    #     print(product)

    #load anual sales data from a csv file called "ventas por producto 2024.csv"
    #first I need to open the file and read the data
    file = open("ventas por producto 2024.csv", "r", encoding="utf-8")
    data = file.readlines()
    file.close()
    # use the first column and the 10th column
    data = [row.split(",") for row in data]
    data = [(row[0], row[10]) for row in data]
    #data = [('"4202865"', 1000), ('"958639"', 2000), ('"966948"', 3000)]
    #cycle through the data and update the rows
    for row in data:
        sku ="\"" +  str(row[0]) + "\""
        value = str(row[1])
        update_row(board_id, sku, value_column_id, value,product_list)

# update_anual_sales()
