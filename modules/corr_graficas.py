import pickle as pkl 
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from scipy.stats import pearsonr, linregress

def cargar_datos(archivo_pkl, estacion):
    with open(archivo_pkl, 'rb') as f:
        data = pkl.load(f)
    pm_NL = data.query(f'Estación == "{estacion}"')
    try:    
        m_pm_NL = pm_NL.groupby(pm_NL['Fecha_Dia'].dt.to_period("M"))['Concentración por día'].mean().reset_index()
        m_pm_NL.rename(columns={'Fecha_Dia': 'Fecha', 'Concentración por día': 'Concentración Promedio Mensual'}, inplace=True)
    except:
        m_pm_NL = pm_NL.groupby(pm_NL['Fecha'].dt.to_period("M"))['Concentración por día'].mean().reset_index()
        m_pm_NL.rename(columns={'Fecha': 'Fecha', 'Concentración por día': 'Concentración Promedio Mensual'}, inplace=True)
    m_pm_NL['Concentración Promedio Mensual'] = m_pm_NL['Concentración Promedio Mensual'].round(3)
    return m_pm_NL

def graficar_datos(m_pm_NL, pemex_NL, iloc_inicio, iloc_fin, estacion):
    try:
        m_pm_NL = m_pm_NL.drop([24])
    except:
        pass
    barriles_all = pemex_NL['Miles de barriles mensuales']
    pm25_all = m_pm_NL['Concentración Promedio Mensual']
    
    
    barriles = pemex_NL['Miles de barriles mensuales'].iloc[iloc_inicio:iloc_fin]
    pm25 = m_pm_NL['Concentración Promedio Mensual'].iloc[iloc_inicio:iloc_fin]
    
    correlation = pearsonr(barriles, pm25)
    slope, intercept, _, p_value, _ = linregress(barriles, pm25)
    
    df = pd.DataFrame({'Mes': m_pm_NL['Fecha'].astype(str), 'Barriles': barriles, 'PM2.5': pm25})
    
    fig = px.scatter(df, x='Barriles', y='PM2.5', text='Mes',
                     title=f'Relación entre Producción de Barriles y Contaminante en {estacion}<br>Correlación: {correlation[0]:.2f}',
                     labels={'Barriles': 'Millones de Barriles', 'PM2.5': 'Concentración'})
    
    fig.add_scatter(x=df['Barriles'], y=slope * df['Barriles'] + intercept, mode='lines', name='Recta de Regresión', line=dict(color='blue'))
    fig.update_traces(textposition='top center', marker=dict(size=10, color='red'), textfont=dict(size=8))
    fig.show()
    
    print(f'Coeficiente de correlación de Pearson: {correlation[0]:.2f}')
    print(f'R² (coeficiente de determinación): {correlation[0]**2:.2f}')
    print(f'p-valor: {p_value:.4f}')
    
    meses = ['Ene 2023', 'Feb 2023', 'Mar 2023', 'Abr 2023', 'May 2023', 'Jun 2023', 'Jul 2023', 'Ago 2023', 'Sep 2023', 'Oct 2023', 'Nov 2023',
        'Dic 2023', 'Ene 2024', 'Feb 2024', 'Mar 2024', 'Abr 2024', 'May 2024', 'Jun 2024', 'Jul 2024', 'Ago 2024', 'Sep 2024', 'Oct 2024',
        'Nov 2024', 'Dic 2024']

    fig, ax1 = plt.subplots()
    ax1.plot(meses, pm25_all, label='Contaminante', color='black', marker='o')
    ax1.set_xlabel('Fecha')
    ax1.set_ylabel(r'Concentración Mensual', color='black')
    ax1.tick_params(axis='y', labelcolor='black')
    plt.legend()
    
    ax2 = ax1.twinx()
    ax2.plot(meses, barriles_all, label='Barriles', color='r', marker='o', linestyle='--')
    ax2.set_ylabel('Promedio mdb mensual', color='black')
    ax2.tick_params(axis='y', labelcolor='black')
    
    ax1.set_xticks(meses)  
    ax1.set_xticklabels(meses, rotation=45, ha='right')
    
    fig.tight_layout()
    plt.title(f'Evolución de PM2.5 y Producción de Barriles en {estacion}')
    plt.legend()
    plt.show()

def main(archivo_pkl='data/IndicedeCalidad/data_PM2.5.pkl', estacion='NL, Juarez', iloc_inicio=6, iloc_fin=16):
    m_pm_NL = cargar_datos(archivo_pkl, estacion)
    
    pemex_NL = pd.DataFrame({'Fecha': pd.date_range(start='2023-01', end='2025-01', freq='M').strftime('%Y-%m'),
                             'Miles de barriles mensuales': [101, 132, 135, 142, 82, 148, 84, 87, 94, 121, 147, 156,
                                                             169, 165, 160, 150, 89, 123, 162, 170, 131, 166, 96, 134]})
    graficar_datos(m_pm_NL, pemex_NL, iloc_inicio, iloc_fin, estacion)
    
if __name__ == "__main__":
    main()
