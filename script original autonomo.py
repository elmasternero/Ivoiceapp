import mysql.connector
from mysql.connector import Error
from datetime import datetime

# Funciones de Conexión y Utilidades

def  connect_to_mysql():
    try:
        connection = mysql.connector.connect(
            host='localhost',  # por lo general "localhost" si es en tu máquina local
            database='facturacion',  # el nombre de tu base de datos
            user='root',  # tu usuario de MySQL
            password='Adela.159!'  # tu contraseña de MySQL
        )
        return connection
    except Error as e:
        print(f"Error connecting toMySQL: {e}")
        return None

def ask_for_date(message):
    while True:
        date_str = input(message)
        try:
            # Convertir la cadena de texto a un objeto datetime
            date = datetime.strptime(date_str, "%Y-%m")
            return date.replace(day=1)  # Establecer día como 1
        except ValueError:
            print("Invalid format. Please, insert date in format YYYY-MM.")

def calculate_yield_date(base_date, choice):
    if choice == '0':
        return base_date
    elif choice == '1':
        return base_date.replace(month=base_date.month-1) if base_date.month > 1 else base_date.replace(month=12, year=base_date.year-1)
    elif choice == '2':
        return base_date.replace(month=base_date.month-2) if base_date.month > 2 else base_date.replace(month=12-(2-base_date.month), year=base_date.year-1)
    elif choice == '3':
        return base_date.replace(month=base_date.month-3) if base_date.month > 3 else base_date.replace(month=12-(3-base_date.month), year=base_date.year-1)

# Función para Insertar Facturas:

def insert_invoice(connection, date_invoice):
    try:
        provider = input("Enter provider name: ")

        # Validar que amount sea un número entero
        while True:
            amount_str = input("Enter the invoice amount: ")
            if amount_str.isdigit():  # Verifica si la entrada es un número entero
                amount = int(amount_str)
                break
            else:
                print("Invalid input. Please enter an integer.")

        # Validar la elección del yield date
        while True:
            yield_choice = input("Is the yield date this month (0), last month (1), two months ago (2), three months ago (3)? ")
            if yield_choice in ['0', '1', '2', '3']:
                yield_date = calculate_yield_date(date_invoice, yield_choice)
                break
            else:
                print("Invalid input. Please enter 0, 1, 2, or 3.")

        cursor = connection.cursor()
        query = """INSERT INTO facturas (provider, amount, date, yield) VALUES (%s, %s, %s, %s)"""
        cursor.execute(query, (provider, amount, date_invoice.strftime("%Y-%m-%d"), yield_date.strftime("%Y-%m-%d")))
        connection.commit()
        print("Invoice inserted successfully")

    except Error as e:
        print(f"Error inserting invoice: {e}")

# Función para Visualizar la Base de Datos: 

def see_database(connection):
    option = input("Do you wish to see all the database (1), by provider (2), by invoice date (3) or by yield date (4)? ")
    
    if option == '1':
        # Mostrar toda la base de datos
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM facturas")
        for register in cursor.fetchall():
            print(register)

    elif option in ['2', '3', '4']:
        # Mostrar opciones disponibles o pedir criterio de búsqueda
        see_options = input("Do you wish to see the options available? (y/n): ")
        if see_options.lower() == 'y':
            # Mostrar opciones disponibles (ejemplo para proveedor)
            if option == '2':
                cursor = connection.cursor()
                cursor.execute("SELECT DISTINCT provider FROM facturas")
                for provider in cursor.fetchall():
                    print(provider[0])
        criteria = input("Select your search criteria: ")

        # Filtrar datos en base al criterio
        cursor = connection.cursor()
        if option == '2':
            query = "SELECT * FROM facturas WHERE provider = %s"
        elif option == '3':
            query = "SELECT * FROM facturas WHERE date = %s"
        elif option == '4':
            query = "SELECT * FROM facturas WHERE yield = %s"
        cursor.execute(query, (criteria,))
        for register in cursor.fetchall():
            print(register)

    else:
        print("Enter a valid option.")

# Función para Modificar Datos Existentes: 
def show_invoice_info(connection, id_invoice):
    try:
        cursor = connection.cursor()
        query = "SELECT * FROM facturas WHERE id = %s"
        cursor.execute(query, (id_invoice,))
        invoice = cursor.fetchone()
        if invoice:
            print("Invoice information:")
            print(f"ID: {invoice[0]}")
            print(f"Provider: {invoice[1]}")
            print(f"Amount: {invoice[2]}")
            print(f"Date: {invoice[3]}")
            print(f"Yield: {invoice[4]}")
        else:
            print(f"No invoice was found with the ID {id_invoice}")
    except Error as e:
        print(f"Error obtaining information of the invoice: {e}")

def modify_data(connection):
    id_invoice = input("Enter the Id of the invoice you wish to modify: ")

    show_invoice_info(connection, id_invoice)

    # Mostrar los campos que se pueden modificar
    print("1. Provider")
    print("2. Amount")
    print("3. Date")
    print("4. Yield")
    option = input("Which field do you wish to modify? (Insert number): ")

    new_value = input("Insert the new value for the selected field: ")
    field = ""

    if option == '1':
        field = "provider"
    elif option == '2':
        field = "amount"
    elif option == '3':
        field = "date"
    elif option == '4':
        field = "yield"
    else:
        print("Invalid option.")
        return

    try:
        cursor = connection.cursor()
        query = f"UPDATE facturas SET {field} = %s WHERE id = %s"
        cursor.execute(query, (new_value, id_invoice))
        connection.commit()
        print(f"Invoice with ID {id_invoice} modified succesfully.")
    except Error as e:
        print(f"Error modifying the invoice: {e}")

# MAIN
def main():
    connection =  connect_to_mysql()

    if connection is not None and connection.is_connected():
        while True:
            action = input("Do you wish to see the database (1), insert an invoice (2), modify an existing invoice/entry (3) or leave the programme (4)? ")
            
            if action == '1':
                see_database(connection)
            elif action == '2':
                fecha_factura = ask_for_date("Enter the month and year for the invoices (YYYY-MM): ")
                while True:
                    insert_invoice(connection, fecha_factura)
                    while True:
                        continuar = input("Do you want to insert another invoice? (y/n): ")
                        if continuar.lower() in ['y', 'n']:
                            break
                        print("Answer not valid. Please, insert 'y' for yes or 'n' for no.")
                    if continuar.lower() != 'y':
                        break
                    continuar_mes = input("Is the next invoice in the same month? (y/n): ")
                    if continuar_mes.lower() != 'y':
                        fecha_factura = ask_for_date("Enter the month and year for the next invoice (YYYY-MM): ")
            elif action == '3':
                modify_data(connection)
            elif action == '4':
                print("Leaving the programme...")
                break
            else:
                answer_leaving = input("Invalid option. Do you wish to leave the programme? (y/n): ")
                if answer_leaving.lower() == 'y':
                    print("Leaving the programme...")
                    break

        connection.close()

if __name__ == "__main__":
    main()

