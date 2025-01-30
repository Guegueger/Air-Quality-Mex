import plotly.express as px

def generar_grafico(data, metrica, estacion, numero_mes):
    """
    Función para generar un gráfico de un contaminante para un mes específico y estacion
    
    :param data: Diccionario con los datos
    :param metrica: Nombre de la métrica a graficar (por ejemplo, 'PM25').
    :param estacion: Nombre de la estación a seleccionar (por ejemplo, 'CDMX_UAMI2023').
    :param numero_mes: Número del mes (1-12) para filtrar los datos.
    """
    
    estaciones = {
    'CDMX_CCA2023': 'CDMX, Centro de Ciencias de la Atmosfera',
    'CDMX_UAMI2023': 'CDMX, UAMI 2023',
    'NL_Cadereyta2024': 'Nuevo León, Cadereyta 2024',
    'NL_Juarez2024': 'Nuevo León, Juárez 2024',
    'NL_universidad2024': 'Nuevo León, Universidad 2024'
}
    metrica = metrica.upper()
    metricas = {'PM10': 'PM10', 'PM25': 'PM25', 'Ozono': 'O3', 'Dioxido_azufre': 'SO2', 'Dioxido_nitrógeno': 'NO2', 'Monoxido_carbono': 'CO'}
    metricas_invert = {v: k for k, v in metricas.items()}
    meses = {
        1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril', 5: 'Mayo', 6: 'Junio',
        7: 'Julio', 8: 'Agosto', 9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
    }
    if numero_mes not in meses:
        print(f"Error: El mes debe ser un número entre 1 y 12.")
        return
    # Verificar si la métrica y la estación están presentes en los datos
    
    
    metrica = metricas_invert[metrica]
    if metrica not in data:
        print(f"Error: La métrica '{metrica}' no se encuentra en los datos.")
        return
    data_metrica = data[metrica]

    if estacion not in data_metrica:
        print(f"Error: La estación '{estacion}' no se encuentra en los datos de la métrica '{metrica}'.")
        return

    # Filtrar los datos para la estación seleccionada y el mes especificado
    data_estacion = data_metrica[estacion]
    data_por_mes = data_estacion[data_estacion['Fecha'].dt.month == numero_mes]
    if data_por_mes.empty:
        print(f"Error: No hay datos para la estación '{estacion}' en el mes de {meses[numero_mes]}.")
        return
    # Verificar si 'Concentraciones horarias' está en las columnas
    if 'Concentraciones horarias' not in data_por_mes.columns:
        print("Error: La columna 'Concentraciones horarias' no se encuentra en los datos.")
        return
    if metrica == 'PM10' or metrica == 'PM25':
        unidades = '(µg/m³)'
    else:
        unidades = '(ppm)'
    # Generar el gráfico
    
    metrica = metricas[metrica]
    fig = px.line(
        data_por_mes, 
        x='Fecha', 
        y='Concentraciones horarias', 
        title=f' Estación {estaciones[estacion]} - {metrica} - Mes {meses[numero_mes]}',
        labels={'Fecha': 'Fecha y Hora', 'Concentraciones horarias': f'{metrica} {unidades}'},
        line_shape='vh',  # Considera cambiar a 'linear' o 'spline' para una línea más suave
        markers=True,  # Puntos en la línea
        color_discrete_sequence=['black'],  # Color de la línea
    )

    # Actualización de la línea
    fig.update_traces(
        marker=dict(size=5),  # Tamaño de los marcadores
        line=dict(dash='solid', width=2)  # Línea sólida, ancho de 2
    )
 
        
    # Personalización adicional
    fig.update_layout(
        xaxis_title="Fecha y Hora",
        yaxis_title=f"Concentración de {metrica} {unidades}",
        xaxis_tickangle=-45,  # Rotar etiquetas del eje X
        template='seaborn',  # Estilo de la plantilla
    )

    # Mostrar el gráfico
    fig.show()
