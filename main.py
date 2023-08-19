#---------------------[DELTA NOVA]---------------------
# Kenet Francisco Orellana Meza       	20141011708
# Marvin Dionicio Martínez Aguilera     20161004203
# Luis Enrique Verde Sánchez	  	    20171031756

# Librerías
import tkinter as tk
from tkinter import messagebox
import ply.lex as lex
import ply.yacc as yacc

# Ventana principal de la Calculadora de Operaciones
ventana = tk.Tk()
ventana.title("Calculadora de Operaciones | Diseño de Compiladores (IS-913) | Delta Nova")
ventana.resizable(0,0)
ventana.geometry("775x440+100+100")
ventana.iconbitmap('G:\\Mi unidad\\Diseño de Compiladores (IS-913)\\Trabajo Final (Proyecto)\\Calculadora de Operaciones\\Logo-Ingenieria-en-Sistemas.ico')

# Se define la entrada de texto y se ubica en la primera fila (row)
input_text = tk.StringVar()
entrada = tk.Entry(ventana, width=50, font=("Helvetica", 20), relief="flat", textvariable=input_text, bg="#FFFFFF")
entrada.grid(ipadx=10, ipady=10, row=0, column=0, columnspan=5, sticky="snew")

botones = ["1","2","3","+","(","4","5","6","-",")","7","8","9","*","$",
           "0",".","/","DEL"]

#-----------------[Analizador léxico]---------------------
def traductor():
    mensaje = input_text.get()
    salida = " "
    salida2 = "Tokens:\n\n"
    salida3 = ""

    # Definiendo los diccionarios que va a utilizar el analizador léxico
    # Lista de tokens necesarios para el analizador léxico
    tokens = [
        'ENTERO',
        'DECIMAL',
        'MAS',
        'MENOS',
        'POR',
        'ENTRE',
        'PARENT_A',
        'PARENT_C',
        'IGNORAR'
    ]

    # Definición de las reglas que tendrá de cada token
    t_MAS = r'[\+]'
    t_MENOS = r'[\-]'
    t_POR = r'[\*]'
    t_ENTRE = r'[\/]'
    t_PARENT_A= r'[\(]'
    t_PARENT_C= r'[\)]'
    t_IGNORAR = r'[ ]'

    # Creación de expresiones regulares para los tokens
    def t_DECIMAL(t):
        r'[0-9]+[.]+[0-9]+'
        t.value = float(t.value)
        return t

    def t_ENTERO(t):
        r'[0-9]+'
        t.value = int(t.value)
        return t
    
    # Manejo de errores
    # Función en caso de que se ingrese un caracter no permitido
    def t_error(t):
        messagebox.showerror("ADVERTENCIA","¡Usted ha ingresado un caracter no permitido!")
        t.lexer.skip(1)


    lexer = lex.lex()
    lexer.input(mensaje)

    while True:
        tok = lexer.token()
        if not tok:
            break
        salida3 = salida3+str(tok) +"\n"
        
    salida2 = salida2 + salida3

#-----------------[Analizador sintáctico]---------------------
    precedence = (
        ('left', 'MAS', 'MENOS'),
        ('left', 'POR', 'ENTRE')
    )

    #Función para calcular la respuesta
    def p_calculo(p):
        '''
        calculo : expresion
                | vacio
        '''
        salida = salida2 + "\n\nOperaciones: " + str(p[1]) + "\n\nResultado: " + str(correr(p[1])) 
        ventana_nueva(salida)
        
    def p_error(p):
        messagebox.showwarning("ADVERTENCIA","Error de sintaxis")
        salida ="\n\nError de sintaxis" 
     

    def p_expresion_ENTERO_DECIMAL(p):
        '''
        expresion : ENTERO
                | DECIMAL
        '''
        p[0] = p[1]    

    def p_expresion(p):
        '''
        expresion : expresion POR expresion
                | expresion ENTRE expresion
                | expresion MAS expresion
                | expresion MENOS expresion
        '''
        p[0] = (p[2],p[1],p[3])


    def p_expresion_par(p):
        '''
        expresion : PARENT_A expresion PARENT_C
        '''
        p[0] = p[2]
        
    def p_vacio(p):
        '''
        vacio : 
        '''
        p[0] = None

    parser = yacc.yacc()

    def correr(p):
        if type(p) == tuple:
            if p[0] == "+":
                return correr(p[1]) + correr(p[2])
            elif p[0] == "-":
                return correr(p[1]) - correr(p[2])
            if p[0] == "*":
                return correr(p[1]) * correr(p[2])
            if p[0] == "/":
                return correr(p[1]) / correr(p[2])
        else:
            return p


    while True:
        try:
            s = mensaje
        except EOFError:
            break
        parser.parse(s)
        break

    # Función para agregar el valor de un boton a la entrada de texto
def agregar_valor(valor):
    entrada_actual = input_text.get()
    entrada_actual += valor
    input_text.set(entrada_actual)

def limpiar_entrada():
     input_text.set("")

    # Nueva ventana donde se muestra en pantalla Tokens, Funciones y Resultado de la Calculadora de Operaciones
def ventana_nueva(tokens):
    ventana_nueva = tk.Toplevel()
    ventana_nueva.resizable(0,0)
    ventana_nueva.geometry("775x440+100+100")
    ventana_nueva.iconbitmap('G:\\Mi unidad\\Diseño de Compiladores (IS-913)\\Trabajo Final (Proyecto)\\Calculadora de Operaciones\\Logo-Ingenieria-en-Sistemas.ico')
    etiqueta = tk.Label(ventana_nueva, font=("Helvetica", 12), text=tokens, justify='left')
    derechos_de_autor = tk.Label(ventana_nueva, text="\n\n© Derechos Reservados 2023 | Prohibida su copia, distribución parcial o total sin la autorización de Delta Nova.", font=("Helvetica", 10))
    etiqueta.pack()
    derechos_de_autor.pack()

    # Se ejecuta el método mainloop() que permite mostrar todo en pantalla
    ventana_nueva.mainloop()

def go():
    traductor()

    # Se define el grid (cuadrícula) de 4 filas y 5 columnas (matriz de 4x5)
for i in range(4):
    ventana.rowconfigure(i+1, weight=1)
for j in range(5):
    ventana.columnconfigure(j, weight=1)

    # Se crean botones y se ubican en el grid (cuadrícula)
for i in range(4):
    for j in range(5):
        if i == 3 and j == 0:
            boton = tk.Button(ventana, text="GO", font=("Date Stamp", 14, "bold"), command=go, bg="#E74C3C", fg="#000000")
            boton.grid(row=i+1, column=j, columnspan=1, sticky="nsew")
        elif i != 3 or j != 0:
            boton_nombre = botones.pop(0)
            if boton_nombre == "DEL":
                boton = tk.Button(ventana, text=boton_nombre, font=("Date Stamp", 14, "bold"), command=limpiar_entrada, bg="#E74C3C", fg="#000000")
            else:
                boton = tk.Button(ventana, text=boton_nombre, font=("Date Stamp", 14, "bold"), command=lambda val=boton_nombre: input_text.set(input_text.get() + val))
            boton.grid(row=i+1, column=j, sticky="nsew")

    # Se ejecuta el método mainloop() que permite mostrar todo en pantalla
ventana.mainloop()