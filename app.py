import csv
import re
import os
import numpy as np
from colorama import Fore, Style

def app():
    # Mostramos el menú en pantalla
    print("Selecciona símbolo: ")
    print("1. XAUUSD")
    print("2. S&P500")
    print("3. EURUSD")
    print("4. Salir")
    print("-----------------------------------------------------------------------")

    # Pedimos al usuario que seleccione una opción
    selection = input()
    print("-----------------------------------------------------------------------")
    # Diccionario para el nombre de los archivos dependiendo de la opción
    menu = {
        "1": {
            "dataPath": "C:/Users/PcCom/Desktop/Scripts/MonthlyBIAS/XAUUSD.csv",
            "mulPips": 10
        },
        "2": {
            "dataPath": "C:/Users/PcCom/Desktop/Scripts/MonthlyBIAS/S&P.csv",
            "mulPips": 10
        },
        "3": {
            "dataPath": "C:/Users/PcCom/Desktop/Scripts/MonthlyBIAS/EURUSD.csv",
            "mulPips": 10000
        },
    }

    # Si la opción seleccionada es válida, obtenemos el archivo correspondiente
    # del diccionario y lo cargamos
    if selection in menu:
        archivo = menu[selection]["dataPath"]
        mulPips = menu[selection]["mulPips"]

    # Si la opción seleccionada es "4", terminamos la ejecución del programa
    if selection == "4":
        exit(0)

    # Comprobamos si el archivo existe
    file_exists = os.path.exists(archivo)

    # Si el archivo no existe, lanzamos una excepción
    if not file_exists:
        raise Exception("El archivo no existe.")

    # Abrimos el archivo de input en modo lectura
    with open(archivo, 'r', newline='\n', encoding='utf-8-sig') as input_file:
        
        # Creamos un lector de archivos CSV a partir del archivo de input
        csv_reader = csv.DictReader(input_file, delimiter=';') # Asocia la columna como clave al valor

        # Inicializamos una lista vacía para almacenar los datos del archivo
        data = []

        # Iteramos sobre las filas del archivo
        for row in csv_reader:
            # Agregamos cada fila a la lista como un diccionario
            data.append(row)

    # Pedimos al usuario que ingrese el mes que desea consultar
    month = input('Por favor ingresa el mes que deseas consultar (en formato MM): ')

    # Pedimois al usuario desde que año quiere procesar los datos
    year = input('Desde que año quieres realizar el estudio [1993-2021]: ')

    # Comprobar que el input es correcto
    match = re.search(r'^(0[1-9]|1[0-2])$', month) and (int(year) >= 1993 and int(year) <= 2021)
    if not match:
        raise Exception("Comprueba que has introducido un mes y año dentro del rango")

    # Creamos una lista para almacenar las filas que correspondan al mes proporcionado
    month_data = []

    # Iteramos sobre las filas de la lista de datos
    for row in data:
        # Separamos la fecha en día, mes y año
        day_str, month_str, year_str = row['Fecha'].split('.')

        # Si el mes de la fila coincide con el mes proporcionado por el usuario,
        # agregamos la fila a la lista de datos del mes
        if month_str == month and year_str >= year:
            month_data.append(row)

    # Calculamos la probabilidad de que el valor de la columna "% var." sea negativo
    # o positivo, primero convertimos el valor a número flotante
    var_values = [float(row['% var.'].replace(',', '.').replace('%','')) for row in month_data] # Modificar la data para luego hacer cálculos
    num_negatives = len([v for v in var_values if v < 0]) # Deja en la lista los valores negativos
    num_positives = len([v for v in var_values if v >= 0]) # Deja en la lista los valores positivos

    # Calcular la distancia en pips dependiendo si es mes positivo o negatio, después sumar todos los resultado para después hacer la media
    sumPips_positives = np.sum([(float(row['Máximo'].replace(',', '.')) - float(row['Apertura'].replace(',', '.')))*mulPips for row in month_data if float(row['% var.'].replace(',', '.').replace('%','')) > 0])
    sumPips_negatives = np.sum([(float(row['Apertura'].replace(',', '.')) - float(row['Mínimo'].replace(',', '.')))*mulPips for row in month_data if float(row['% var.'].replace(',', '.').replace('%','')) < 0])
    
    # Comprobar que haya datos para realizar los cálculos
    total = len(var_values)
    if total == 0:
        print('No hay datos disponibles para el mes proporcionado.')
        exit(1)
    
    # Calcular estadísticas
    prob_negatives = num_negatives / total
    prob_positives = num_positives / total
    meanPipsPositives = sumPips_positives / num_positives
    meanPipsNegatives = sumPips_negatives / num_negatives
    # Mostramos el resultado en pantalla
    print("-----------------------------------------------------------------------")
    print(Fore.RED + f'Bearish: ' + f'{prob_negatives:.2%}' + Style.RESET_ALL)
    print(f'Media de pips a favor del BIAS (Apertura - Mínimo): ' + Fore.LIGHTBLUE_EX + f'{meanPipsNegatives:.0f}\n' + Style.RESET_ALL)
    print(Fore.GREEN + f'Bullish: ' +  f'{prob_positives:.2%}' + Style.RESET_ALL)
    print(f'Media de pips a favor del BIAS (Máximo - Apertura): ' + Fore.LIGHTBLUE_EX + f'{meanPipsPositives:.0f}' + Style.RESET_ALL)
    print("-----------------------------------------------------------------------")


if __name__ == "__main__":
    app()