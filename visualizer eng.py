import tkinter as tk
from tkinter import Toplevel, Entry, Button, Label, messagebox, PhotoImage, ttk
from funciones import connect_to_mysql, insert_invoice, calculate_yield_date, ask_for_date, modify_data, on_modify, consultar_datos 

campos = ["provider", "amount", "date", "yield"]

class InterfazApp:
    def __init__(self, ventana):
        self.ventana = ventana
        self.connection = connection
        self.ventana.title("Invoice App")

        # Obtener el ancho y alto de la pantalla
        screen_width = self.ventana.winfo_screenwidth()
        screen_height = self.ventana.winfo_screenheight()

        # Calcular las coordenadas x e y para centrar la ventana
        x = (screen_width - 400) // 2  # Ancho de la ventana (ajústalo según tus necesidades)
        y = (screen_height - 300) // 2  # Alto de la ventana (ajústalo según tus necesidades)

        # Configurar la geometría de la ventana para que esté centrada
        self.ventana.geometry(f"320x160+{x}+{y}")

        # Botones con el mismo ancho
        button_width = 20  # Define el ancho deseado para los botones

        # Botones
        self.boton_ver_bd = tk.Button(ventana, text="See Database", command=self.ver_bd,width=button_width)
        self.boton_insertar_factura = tk.Button(ventana, text="Insert Invoice", command=self.insertar_factura,width=button_width)
        self.boton_modificar_factura = tk.Button(ventana, text="Modify Invoice", command=self.modificar_factura,width=button_width)
        self.boton_salir = tk.Button(ventana, text="Exit Programme", command=self.ventana.quit,width=button_width)
        
        # Cargar la imagen
        self.logo = PhotoImage(file=r"C:\Users\IoweLouisbeer4ever\Python-2023\Project\logo.png")  # Asegúrate de usar la ruta correcta al archivo de la imagen
        self.small_logo = self.logo.subsample(5, 5)  # Reducir la imagen en un factor de 5
        label_logo = tk.Label(self.ventana, image=self.small_logo)
        label_logo.grid(row=0, column=0, columnspan=2)  # Ajusta row y column según sea necesario
        # Colocar el logo y el texto


        # Texto adicional
        label_text = tk.Label(self.ventana, text="ReDi school final project: A simple web GUI. Julián Lilloy")
        label_text.grid(row=1, column=0, columnspan=2)  # Ajusta row y column según sea necesario
        # Colocar los botones en la ventana utilizando grid
        self.boton_ver_bd.grid(row=2, column=0, padx=5, pady=5)
        self.boton_insertar_factura.grid(row=2, column=1, padx=5, pady=5)
        self.boton_modificar_factura.grid(row=3, column=0, padx=5, pady=5)
        self.boton_salir.grid(row=3, column=1, padx=5, pady=5)
    #Método de cerrado de ventan
    #def on_closing_insertar_factura(self, ventana_insertar_factura):
    #    ventana_insertar_factura.destroy()
    #    self.ventana.deiconify()


    def ver_bd(self):
        ventana_ver_bd = tk.Toplevel(self.ventana)
        ventana_ver_bd.title("Visualize Database")
        ventana_ver_bd.geometry("1200x600")

    # Configurar las filas y columnas de la ventana
        ventana_ver_bd.grid_columnconfigure(0, minsize=200)
        ventana_ver_bd.grid_columnconfigure(1, weight=1)
        ventana_ver_bd.grid_rowconfigure(0, weight=0)
        ventana_ver_bd.grid_rowconfigure(1, weight=0)
        for i in range(3):  # Para las primeras tres filas donde se colocan los filtros
            ventana_ver_bd.grid_rowconfigure(i, weight=0)
        ventana_ver_bd.grid_rowconfigure(3, weight=1)
        ventana_ver_bd.grid_rowconfigure(4, weight=0)

    # Configurar los widgets de filtro en la parte superior de la columna 0
        opciones_filtro = ["See All", "ID", "provider", "amount", "date", "yield"]
        self.filtro = tk.StringVar(value=opciones_filtro[0])
        tk.Label(ventana_ver_bd, text="Filter by:").grid(row=0, column=0, sticky="ew")
        tk.OptionMenu(ventana_ver_bd, self.filtro, *opciones_filtro).grid(row=1, column=0, sticky="ew")
        self.valor_filtro = tk.StringVar()
        tk.Entry(ventana_ver_bd, textvariable=self.valor_filtro).grid(row=2, column=0, sticky="ew")
        tk.Button(ventana_ver_bd, text="Filter", command=self.aplicar_filtro).grid(row=3, column=0, sticky="ew")

    # Configurar el Treeview para llenar el espacio restante
        self.tree = ttk.Treeview(ventana_ver_bd, columns=("ID", "provider", "amount", "date", "yield"), show='headings')
        self.tree.grid(row=0, column=1, rowspan=4, sticky="nsew")

    # Configurar las cabeceras y columnas del Treeview
        for col in ("ID", "provider", "amount", "date", "yield"):
            self.tree.heading(col, text=col.capitalize())

    # Botón para volver al menú principal en la última fila
        tk.Button(ventana_ver_bd, text="Back to Menu", command=lambda: self.volver_al_menu_principal(ventana_ver_bd)).grid(row=4, column=0, sticky="ew")


    def aplicar_filtro(self):
        filtro = self.filtro.get()
        valor = self.valor_filtro.get() if self.filtro.get() != "See All" else None
        resultados = consultar_datos(self.connection, filtro, valor)
        
        # Limpiar el Treeview
        for i in self.tree.get_children():
            self.tree.delete(i)

        # Añadir los datos filtrados al Treeview
        for fila in resultados:
            self.tree.insert('', 'end', values=fila)

    def insertar_factura(self):
        # Ocultar la ventana principal
        self.ventana.withdraw()
        
        # Crear una nueva ventana emergente
        ventana_insertar_factura = Toplevel()
        ventana_insertar_factura.title("Insert Invoice")
        #Protocolo para volver al menu principal al cerrar la ventana
        ventana_insertar_factura.protocol("WM_DELETE_WINDOW", lambda: self.volver_al_menu_principal(ventana_insertar_factura))


        # Calcular las coordenadas x e y para centrar la ventana
        screen_width = ventana_insertar_factura.winfo_screenwidth()
        screen_height = ventana_insertar_factura.winfo_screenheight()
        x = (screen_width - 400) // 2
        y = (screen_height - 300) // 2
        ventana_insertar_factura.geometry(f"+{x}+{y}")

        # Etiquetas y campos de entrada
        label_proveedor = Label(ventana_insertar_factura, text="Name of the provider:")
        label_monto = Label(ventana_insertar_factura, text="Amount:")
        label_mes_pago = Label(ventana_insertar_factura, text="Month (YYYY-MM):")
        label_mes_correspondiente = Label(ventana_insertar_factura, text="Yield Month (0,1,2,3):")

        entry_proveedor = Entry(ventana_insertar_factura)
        entry_monto = Entry(ventana_insertar_factura)
        entry_mes_pago = Entry(ventana_insertar_factura)
        entry_mes_correspondiente = Entry(ventana_insertar_factura)
        
        def on_insert():
            # Llamar a insert_invoice y obtener la respuesta
            respuesta = insert_invoice(
                connection,
                entry_proveedor.get(),
                entry_monto.get(),
                entry_mes_pago.get(),
                entry_mes_correspondiente.get()
            )

            # Verificar la respuesta
            if respuesta == "Invoice inserted successfully":
                # Mostrar mensaje de éxito
                resultado = messagebox.askyesno("Success", "Invoice inserted successfully. Do you want to insert another invoice?")
                if resultado:
                    ventana_insertar_factura.destroy()
                    self.insertar_factura()
                else:
                    ventana_insertar_factura.destroy()
                    self.ventana.deiconify()
            else:
                # Mostrar mensaje de error
                messagebox.showerror("Error", respuesta)
        # Botón para confirmar la inserción y volver al menú principal
        button_width = 20  # Define el ancho deseado para los botones
        boton_insertar = Button(ventana_insertar_factura, text="Insert", command=on_insert, width=button_width)
        boton_menu_principal = Button(ventana_insertar_factura, text="Back to Menu", command=lambda: self.volver_al_menu_principal(ventana_insertar_factura), width=button_width)

        # Colocar etiquetas y campos de entrada en la ventana
        label_proveedor.grid(row=0, column=0)
        entry_proveedor.grid(row=0, column=1)
        label_monto.grid(row=1, column=0)
        entry_monto.grid(row=1, column=1)
        label_mes_pago.grid(row=2, column=0)
        entry_mes_pago.grid(row=2, column=1)
        label_mes_correspondiente.grid(row=3, column=0)
        entry_mes_correspondiente.grid(row=3, column=1)
        
    # Botones
        boton_insertar.grid(row=4, column=0,padx=10,pady=10)
        boton_menu_principal.grid(row=4, column=1, padx=10,pady=10)
    
    def volver_al_menu_principal(self, ventana_secundaria):
        ventana_secundaria.destroy()
        self.ventana.deiconify()

    def modificar_factura(self):
        self.ventana.withdraw()  # Ocultar ventana principal

        ventana_modificar_factura = Toplevel()
        ventana_modificar_factura.title("Modify Invoice")
        ventana_modificar_factura.protocol("WM_DELETE_WINDOW", lambda: self.volver_al_menu_principal(ventana_modificar_factura))


        # Calcular las coordenadas x e y para centrar la ventana
        screen_width = ventana_modificar_factura.winfo_screenwidth()
        screen_height = ventana_modificar_factura.winfo_screenheight()
        x = (screen_width - 400) // 2
        y = (screen_height - 300) // 2
        ventana_modificar_factura.geometry(f"+{x}+{y}")

        # Crear widgets para el ID de la factura, el campo a modificar y el nuevo valor
        Label(ventana_modificar_factura, text="ID from the Invoice:").grid(row=0, column=0)
        entry_id_invoice = Entry(ventana_modificar_factura)
        entry_id_invoice.grid(row=0, column=1)

        # Crear la lista desplegable para el campo a modificar
        Label(ventana_modificar_factura, text="Field to modify:").grid(row=1, column=0)
        #campos = ["provider", "amount", "date", "yield"]
        selected_field = tk.StringVar()
        selected_field.set(campos[0])  # default value
        drop_down_menu = tk.OptionMenu(ventana_modificar_factura, selected_field, *campos)
        drop_down_menu.grid(row=1, column=1)

        Label(ventana_modificar_factura, text="New value:").grid(row=2, column=0)
        entry_new_value = Entry(ventana_modificar_factura)
        entry_new_value.grid(row=2, column=1)
        
        def modify_action():
            id_invoice = entry_id_invoice.get()
            field = selected_field.get()
            new_value = entry_new_value.get()
            
            respuesta = on_modify(self.connection, entry_id_invoice.get(), selected_field.get(), entry_new_value.get())
            if "Error:" in respuesta:
                messagebox.showerror("Error", respuesta)
            else:
                messagebox.showinfo("Result", respuesta)
                if "successfully" in respuesta:
                    ventana_modificar_factura.destroy()
                    self.ventana.deiconify()

        Button(ventana_modificar_factura, text="Modify Invoice", command=modify_action).grid(row=3, column=0, padx=10, pady=10)
        # Botón para modificar la factura
#         Button(ventana_modificar_factura, text="Modificar Factura", command=lambda: self.on_modify(
#     entry_id_invoice.get(),
#     selected_field.get(),  # Usar selected_field.get() en lugar de entry_field.get()
#     entry_new_value.get(),
#     ventana_modificar_factura
# )).grid(row=3, column=0, padx=10, pady=10)

        # Botón para cancelar y volver al menú anterior
        Button(ventana_modificar_factura, text="Back to Menu", command=lambda: self.volver_al_menu_principal(ventana_modificar_factura)).grid(row=3, column=1,padx=10,pady=10)
    
    # # Llamar a modify_data y mostrar el resultado
    #     respuesta = modify_data(self.connection, id_invoice, field, new_value)
    #     messagebox.showinfo("Resultado", respuesta)
    #     if "successfully" in respuesta:
    #         ventana_modificar_factura.destroy()
    #         self.ventana.deiconify()


if __name__ == "__main__":
    connection =  connect_to_mysql()
    if connection is not None and connection.is_connected():
        ventana_principal = tk.Tk()
        app = InterfazApp(ventana_principal)
        ventana_principal.mainloop()
    connection.close()