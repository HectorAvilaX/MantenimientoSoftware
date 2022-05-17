import MySQLdb
import mysql.connector
from cProfile import label
from cgitb import text
from collections import namedtuple
from sqlite3.dbapi2 import Row
from tkinter import ttk
from tkinter import *
import sys
import sqlite3

conexion = mysql.connector.connect(user='root', password='Kehljjexj456', host='localhost', database='bdmantenimiento', port='3307')
cursor =conexion.cursor()

class Product:

    #db_name = 'database.db'
    
    def producto_laptop(self):
        return "Laptop"

    def __init__(self, window):
        self.wind = window
        self.wind.title('Products Aplication')

        ########################################## MENU ###################################################
        menu = Menu(self.wind)
        self.wind.config(menu=menu)
        fileMenu = Menu(menu)
        fileMenu.add_command(label="Agregar Producto", command=self.Agregar_producto)
        fileMenu.add_command(label="Exit", command=self.salida)
        menu.add_cascade(label="File", menu=fileMenu)

        

        ##########################################################################################################33

        ttk.Button(text='Agregar Producto', command= self.Agregar_producto).grid(row=1, column=0,columnspan=2, sticky= W + E)
        ttk.Button(text='Agregar Accesorios', command= self.Agregar_Accesorios).grid(row=1, column=2,columnspan=3, sticky= W + E)
        #ttk.Button(text='Agregar PC-Escritorio', command= self.Agregar_PC_Escritorio).grid(row=1, column=2, sticky= W + E)

        #Output Messages
        self.message = Label(text= '', fg='red')
        self.message.grid(row= 3 , column= 0, columnspan=2, sticky= W + E)

        #Table - dos grillas
        self.tree = ttk.Treeview(height=10, columns=("1","2","3"))
        self.tree.grid(row = 4, column = 0, columnspan = 4)

        #encabezados/text para las grillas
        self.tree.heading('#0', text='ID', anchor = CENTER)
        self.tree.heading('1', text='Name', anchor = CENTER) #Centramos el texto.
        self.tree.heading('2', text='Price', anchor = CENTER)
        self.tree.heading('3', text='Descp', anchor = CENTER)

        #Buttons / Botones
        ttk.Button(text= 'DELETE', command= self.delete_product).grid(row=5, column= 0, sticky= W + E)
        ttk.Button(text='EDIT', command= self.edit_product).grid(row=5, column=1, sticky=W + E)
        ttk.Button(text='EXIT', command= self.salida).grid(row=5, column=2, sticky=W + E)
        # filling the row / llenando las filas
        self.get_products() #llamo los productos de la bbdd

    

    def salida(self):
        sys.exit()
    


    ############################################### AÑADIR PC ESCRITORIO ###############################################

    def Agregar_producto(self):

        self.edit_wind = Toplevel()
        self.edit_wind.title = 'PC Escritorio'

        Label(self.edit_wind, text='PC Escritorio').grid(row=1,column=1,columnspan=2)
        Label(self.edit_wind, text= 'Name: ').grid(row=2, column=1)
        new_name = Entry(self.edit_wind)
        new_name.grid(row=2, column=2)

        Label(self.edit_wind, text= 'Price: ').grid(row=3, column=1)
        price = Entry(self.edit_wind)
        price.grid(row=3, column=2)

        Label(self.edit_wind, text= 'Descp: ').grid(row=4, column=1)
        descp = Entry(self.edit_wind)
        descp.grid(row=4, column=2)

        Button(self.edit_wind, text='Agregar producto', command=lambda:self.add_product("producto", new_name.get(),price.get(),descp.get())).grid(row=5, column=1,columnspan=2)


    ############################################### AÑADIR ACCESORIO ###############################################

    def Agregar_Accesorios(self):
        self.edit_wind = Toplevel()
        self.edit_wind.title = 'Accesorio'

        Label(self.edit_wind, text='Agregar Accesorio').grid(row=1,column=1,columnspan=2)
        Label(self.edit_wind, text= 'Name: ').grid(row=2, column=1)
        new_name = Entry(self.edit_wind)
        new_name.grid(row=2, column=2)

        Label(self.edit_wind, text= 'Price: ').grid(row=3, column=1)
        price = Entry(self.edit_wind)
        price.grid(row=3, column=2)

        Label(self.edit_wind, text= 'Descp: ').grid(row=4, column=1)
        descp = Entry(self.edit_wind)
        descp.grid(row=4, column=2)

        Button(self.edit_wind, text='Agregar Accesorio', command=lambda:self.add_product("accesorios",new_name.get(),price.get(),descp.get())).grid(row=5, column=1,columnspan=2)


    ############################################### AÑADIR LAPTOP ###############################################

    # def Agregar_Laptop(self):
    
    #     self.edit_wind = Toplevel()
    #     self.edit_wind.title = 'Laptops'

    #     Label(self.edit_wind, text='Agregar Laptop').grid(row=1,column=1,columnspan=2)
    #     Label(self.edit_wind, text= 'Name: ').grid(row=2, column=1)
    #     new_name = Entry(self.edit_wind)
    #     new_name.grid(row=2, column=2)

    #     Label(self.edit_wind, text= 'Price: ').grid(row=3, column=1)
    #     price = Entry(self.edit_wind)
    #     price.grid(row=3, column=2)

    #     Label(self.edit_wind, text= 'Descp: ').grid(row=4, column=1)
    #     descp = Entry(self.edit_wind)
    #     descp.grid(row=4, column=2)

    #     Button(self.edit_wind, text='Agregar Producto', command=lambda:self.add_product("laptop",new_name.get(),price.get(),descp.get())).grid(row=5, column=1,columnspan=2)

    ################################################################################################################    

    def run_query(self, query):
        
        #print(parameters)
        cursor = conexion.cursor()
        cursor.execute(query) #
        result = cursor.fetchall()
        conexion.commit()  # run - Ejecutamos la consulta sql
            
        return result
    
    def insertar(self, query, parmeter=()):
        cursor = conexion.cursor()
        cursor.execute(query,parmeter)
        conexion.commit()

    ################################################# MOSTRAR PRODUCTO #############################################
    def get_products(self):
        #cleaning table
        records = self.tree.get_children() #children: trae todos los datos
        for element in records:
            self.tree.delete(element)

        #quering data
        query ='SELECT * FROM producto ORDER BY idproducto DESC' # Ordenalos de forma descendente
        query3 ='SELECT * FROM accesorios ORDER BY idaccesorios DESC'
        db_rows = self.run_query(query) #filas de la base de datos
        db_rows3 = self.run_query(query3)
        #aux = self.run_query(query)
        #print(db_rows)

        #filling data
        #print("entro")
        aux=0
        for row in db_rows:
            #print(row)
            self.tree.insert('', 0, text= row[0], values= row[1:])
            aux +=1

        for row3 in db_rows3:
            #print(row2)
            self.tree.insert('', 0, text= row3[0], values= row3[1:])

    def validation(self,name,price,descp):
        return len(str(name))> 0 and len(str(price)) > 0 and len(str(descp)) > 0 #lectura del input

    ################################################## INSERTAR PRODUCTO #######################################
    
    def add_product(self,tipo,nombre,precio,descp):
        if self.validation(nombre,precio,descp):
            query = 'INSERT INTO ' + tipo + '(nombre, precio, descp) VALUES (%s, %s,%s)'
            #parameters = (self.name.get(), self.price.get(), self.descp.get())
            parameters = (nombre,precio,descp)
            self.insertar(query,parameters)
            #self.message['text'] = 'Product {} added Successfully'.format(self.name.get()) #imprimos mensaje de guardado con nombre de producto
            #self.name.delete(0, END)
            #self.price.delete(0, END)
            #self.descp.delete(0, END)
        else:
            self.message['text'] = "Name, price and Description required"
        self.get_products()

    def delete_product(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text']
        except Exception as ex:
            self.message['text'] = 'Please Select a Record'
            return
        self.message['text'] = ''
        id = self.tree.item(self.tree.selection())['text']
        name = self.tree.item(self.tree.selection())['values'][0]
        datos = (id,name,)
        print(name)
        query = 'DELETE FROM producto WHERE idProducto = %s AND nombre = %s'
        query2 = 'DELETE FROM accesorios WHERE idaccesorios = %s AND nombre = %s'
        self.insertar(query, datos)
        self.insertar(query2, datos)
        self.message['text'] = 'Record {} deleted Successfully'.format(id)
        self.get_products()

    def edit_product(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text']
        except Exception as ex:
            self.message['text'] = 'Please Select a Record'
            return
        id = self.tree.item(self.tree.selection())['text']
        name = self.tree.item(self.tree.selection())['values'][0]
        old_price = self.tree.item(self.tree.selection())['values'][1]
        old_descp = self.tree.item(self.tree.selection())['values'][2]
        self.edit_wind = Toplevel()
        self.edit_wind.title = 'Edit Product'

        #Old name
        Label(self.edit_wind, text= 'Old name').grid(row=0, column=1)
        Entry(self.edit_wind, textvariable= StringVar(self.edit_wind, value= name), state='readonly').grid(row=0, column=2)

        #New name
        Label(self.edit_wind, text= 'New name').grid(row=1, column=1)
        new_name = Entry(self.edit_wind)
        new_name.grid(row=1, column=2)

        #Old price
        Label(self.edit_wind, text= 'Old price').grid(row=2, column=1)
        Entry(self.edit_wind, textvariable=StringVar(self.edit_wind, value=old_price), state= 'readonly').grid(row=2, column=2) # traemos el valor de la variable (StrinVar) PRICE
        

        #New price
        Label(self.edit_wind, text= 'New price').grid(row=3, column=1)
        new_price = Entry(self.edit_wind)
        new_price.grid(row=3, column=2)


        #Old descp
        Label(self.edit_wind, text= 'Old descp').grid(row=4, column=1)
        Entry(self.edit_wind, textvariable=StringVar(self.edit_wind, value=old_descp), state= 'readonly').grid(row=4, column=2) 
        
        
        #New descp
      
        Label(self.edit_wind, text= 'New descp').grid(row=5, column=1)
        new_descp = Entry(self.edit_wind)
        new_descp.grid(row=5, column=2)


        Button(self.edit_wind, text='Update', command= lambda:self.edit_records(id , new_name.get(), name, new_price.get(), old_price, new_descp.get(), old_descp)).grid(row=6, column=2, sticky= W)

    def edit_records(self,id, new_name, name, new_price, old_price, new_descp, old_descp):
        #query = 'UPDATE product SET name = ?, price = ?, descp = ? WHERE name = ? AND price = ? AND descp = ?'
        query = "UPDATE FROM producto SET  nombre = '{}' , precio = '{}' , descp = '{}' WHERE idProducto = '{}' AND nombre = '{}'"
        query2 = "UPDATE FROM accesorios SET nombre = '{}' , precio = '{}' , descp = '{}' WHERE idaccesorios = '{}' AND nombre = '{}'s"
        parameters = (new_name, new_price, new_descp, id, name,)
        #cursor = conexion.cursor()
        #cursor.execute(query,parameters)
        #cursor.execute(query2,parameters)
        self.insertar(query, parameters)
        self.insertar(query2, parameters)
        self.edit_wind.destroy()
        self.message['text'] = 'Record {} updated Successfully'.format(name)
        self.get_products()

if __name__ == '__main__':
    window = Tk()
    application = Product(window)
    window.mainloop()