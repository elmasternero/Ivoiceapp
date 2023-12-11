import mysql.connector
from mysql.connector import Error
from datetime import datetime

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
def calculate_yield_date(base_date, choice):
    if choice == '0':
        return base_date
    elif choice == '1':
        return base_date.replace(month=base_date.month-1) if base_date.month > 1 else base_date.replace(month=12, year=base_date.year-1)
    elif choice == '2':
        return base_date.replace(month=base_date.month-2) if base_date.month > 2 else base_date.replace(month=12-(2-base_date.month), year=base_date.year-1)
    elif choice == '3':
        return base_date.replace(month=base_date.month-3) if base_date.month > 3 else base_date.replace(month=12-(3-base_date.month), year=base_date.year-1)

def ask_for_date(message):
    while True:
        date_str = input(message)
        try:
            # Convertir la cadena de texto a un objeto datetime
            date = datetime.strptime(date_str, "%Y-%m")
            return date.replace(day=1)  # Establecer día como 1
        except ValueError:
            print("Invalid format. Please, insert date in format YYYY-MM.")

def insert_invoice(connection, provider, amount_str, date_invoice_str, yield_choice):
    try:
        # Asegurar que los valores sean correctos
        #print(f"Provider: {provider}, Amount: {amount_str}, Date: {date_invoice_str}, Yield Choice: {yield_choice}")

        # Convertir amount_str a entero
        amount = int(amount_str) if amount_str.isdigit() else None
        if amount is None:
            return "Invalid input for amount. Please enter an integer."

        # Asumir que el día siempre es el primero
        try:
            date_invoice_str_with_day = date_invoice_str + "-01"
            date_invoice = datetime.strptime(date_invoice_str_with_day, "%Y-%m-%d")
        except ValueError:
            return "Error: Date must be in format YYYY-MM."
        #date_invoice_str_with_day = date_invoice_str + "-01"
        #date_invoice = datetime.strptime(date_invoice_str_with_day, "%Y-%m-%d")
        #print(f"Converted date_invoice: {date_invoice}")  # Depuración
        if yield_choice not in ['0', '1', '2', '3']:
            return "Error: El yield date debe ser 0, 1, 2, o 3."
        
        # Aquí vendría la lógica para calcular la fecha de rendimiento (yield_date)
        # basándote en el yield_choice, algo como esto:
        yield_date = calculate_yield_date(date_invoice, yield_choice)
        # Simplificar la lógica de yield_date para depuración
        #yield_date = date_invoice  # Para simplificar la depuración
        #print(f"Yield Date: {yield_date}")  # Depuración

        # Ejecución simulada de consulta SQL para depuración
        #print(f"SQL Query: INSERT INTO facturas (provider, amount, date, yield) VALUES ({provider}, {amount}, {date_invoice.strftime('%Y-%m-%d')}, {yield_date.strftime('%Y-%m-%d')})")
        
        #Comentar esta parte para evitar la ejecución real hasta resolver el problema
        cursor = connection.cursor()
        query = """INSERT INTO facturas (provider, amount, date, yield) VALUES (%s, %s, %s, %s)"""
        cursor.execute(query, (provider, amount, date_invoice.strftime("%Y-%m-%d"), yield_date.strftime("%Y-%m-%d")))
        connection.commit()
        return "Invoice inserted successfully"

    except Error as e:
        return f"Error inserting invoice: {e}"
    
def modify_data(connection, id_invoice, field, new_value):
    try:
        cursor = connection.cursor()
        # Asegúrate de que 'field' es un campo válido antes de incluirlo en la consulta
        if field not in ["provider", "amount", "date", "yield"]:
            return "Invalid field selected."

        query = f"UPDATE facturas SET {field} = %s WHERE id = %s"
        cursor.execute(query, (new_value, id_invoice))
        connection.commit()
        return f"Invoice with ID {id_invoice} modified successfully."
    except Error as e:
        return f"Error modifying the invoice: {e}"

def on_modify(connection, id_invoice, field, new_value):
    # Validar datos antes de intentar modificarlos en la base de datos
    if field == 'amount':
        if not new_value.isdigit():
            return "Error: El monto debe ser un número entero."
        new_value = int(new_value)
    elif field == 'date':
        try:
            datetime.strptime(new_value, "%Y-%m")
            new_value += "-01"  # Agregar el primer día del mes
        except ValueError:
            return "Error: La fecha debe estar en formato YYYY-MM."
    elif field == 'yield':
        if new_value not in ['0', '1', '2', '3']:
            return "Error: El yield date debe ser 0, 1, 2, o 3."

    # Llamar a modify_data y devolver el resultado
    respuesta = modify_data(connection, id_invoice, field, new_value)
    return respuesta

def consultar_datos(connection, filtro=None, valor=None):
    try:
        cursor = connection.cursor()
        query = "SELECT * FROM facturas"
        params = ()

        if filtro and valor:
            if filtro == "Ver todo":
                # No se aplica ningún filtro adicional
                pass
            else:
                # Aplicar filtro según el campo y el valor
                query += f" WHERE {filtro} = %s"
                params = (valor,)

        cursor.execute(query, params)
        return cursor.fetchall()  # Devolver todos los resultados de la consulta
    except Error as e:
        print(f"Error al consultar datos: {e}")
        return []