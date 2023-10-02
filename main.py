import streamlit as st 
import plotly.express as px
import plotly.subplots as sp
import pandas as pd


st.set_page_config('Busiess Analytics Dashboard',page_icon='',layout='wide' )

st.markdown("<h1 style='text-align: center;'>Busiess Analytics Dashboard</h1>", unsafe_allow_html=True)
theme_plotly=None
df =pd.read_csv('customers.csv')

df['HireDate'] =pd.to_datetime(df['HireDate'])


st.markdown(
    """
    <style>
    /* Cambiar el tipo de cursor en el área del sidebar */
    .sidebar-content {
        cursor: pointer; /* Cambiar a cualquier tipo de cursor deseado */
    }
    </style>
    """,
    unsafe_allow_html=True
)

df.set_index('id',inplace=True)
st.sidebar.header('Filtar Los Datos')
Department=st.sidebar.multiselect(
    label='filtre por departamento',
    options=df['Department'].unique(),
    default=df['Department'].unique()[:2]
)
Country=st.sidebar.multiselect(
    label='filtre por Pasí',
    options=df['Country'].unique(),
    default=df['Country'].unique()[:2]
)
BusinessUnit=st.sidebar.multiselect(
    label='filtre por unidad de negocios',
    options=df['BusinessUnit'].unique(),
    default=df['BusinessUnit'].unique()[:2]
)

df_selecionado= df.query('Department==@Department & Country==@Country & BusinessUnit==@BusinessUnit')

def metricas():
    from streamlit_extras.metric_cards import style_metric_cards
    col1,col2,col3=st.columns(3)

    col1.metric(label='Total de Empleados ',value=f'N° {df_selecionado.EEID.count()}',delta='Total de Empleados')
    col2.metric(label='Salario Anual',value=f'$ {df_selecionado.AnnualSalary.sum():,.0f}',delta='Suma Total de los Salarios')
    col3.metric(label='Salario Anual',value=f'$ {df_selecionado.AnnualSalary.max():,.0f}',delta='Salario Mas Alto')
    style_metric_cards(background_color='black',border_left_color='white')


metricas()

div1,div2=st.columns (2)
def pie():
    with div1:
        fig=px.pie(df_selecionado, values="AnnualSalary", names= "Department", title='Salarios por Departamento')
        fig. update_layout (legend_title="Department", legend_y=0.9)
        fig.update_traces (textinfo="percent+label", textposition="inside")
        st.plotly_chart(fig,use_container_width=True, theme=theme_plotly)
pie()

def bar():
    with div2:
        
        fig=px.bar (df_selecionado,y="AnnualSalary", x= "Department", text_auto=' .2s', title="Salarios por Departamento")
        fig.update_traces(textfont_size=18, textangle=0, textposition="outside" ,cliponaxis=False)
        st.plotly_chart(fig,use_container_width=True, theme=theme_plotly)
bar ()


df_selecionado.sort_values(by='HireDate',inplace=True)
def line_chart():
        fig=px.line(df_selecionado,x='HireDate',y='AnnualSalary',height=500,color='Department',title='Linea Temporal De Los Salarios Por Departamentos')
        st.plotly_chart(fig,use_container_width=True, theme=theme_plotly)

line_chart()


def bar_gender():
     fig=px.bar(df_selecionado,x='Age',y='AnnualSalary',height=600,barmode='group',color='Gender',title='Salarios por Genero')
     fig.update_traces(textfont_size=18, textangle=0, textposition="outside" ,cliponaxis=False)
     st.plotly_chart(fig,use_container_width=True, theme=theme_plotly)   

bar_gender()

def promedio_salario_dep():
    # Calcular el promedio de salarios por departamento
    promedio_salarios = df_selecionado.groupby('Department')['AnnualSalary'].mean().reset_index()

    # Crear el gráfico de barras para el promedio de salarios por departamento
    fig = px.bar(promedio_salarios, x='Department', y='AnnualSalary',color='Department',
                labels={'Departamento': 'Departamento', 'Salario': 'Promedio de Salario'},
                title='Promedio de Salarios por Departamento')

    # Mostrar el gráfico
    st.plotly_chart(fig, use_container_width=True,theme=theme_plotly)
promedio_salario_dep()

def promedio_salario_gender():
    # Calcular el promedio de salarios por departamento
    promedio_salarios = df_selecionado.groupby('Gender')['AnnualSalary'].mean().reset_index()

    # Crear el gráfico de barras para el promedio de salarios por departamento
    fig = px.bar(promedio_salarios, x='Gender', y='AnnualSalary',color='Gender',
                labels={'Gender': 'Genero', 'Salario': 'Promedio de Salario'},
                title='Promedio de Salarios por Genero')

    # Mostrar el gráfico
    st.plotly_chart(fig, use_container_width=True,theme=theme_plotly)
promedio_salario_gender()

def promedio_salario_age():
    # Calcular el promedio de salarios por departamento
    promedio_salarios = df_selecionado.groupby('Age')['AnnualSalary'].mean().reset_index()

    # Crear el gráfico de barras para el promedio de salarios por departamento
    fig = px.bar(promedio_salarios, x='Age', y='AnnualSalary',color='Age',
                labels={'Gender': 'Genero', 'Salario': 'Promedio de Salario'},
                title='Promedio de Salarios por Eda')

    # Mostrar el gráfico
    st.plotly_chart(fig, use_container_width=True,theme=theme_plotly)
promedio_salario_age()
def Bonus_pais():
    # Calcular el promedio de salarios por departamento
    promedio_salarios = df_selecionado.groupby('Country')['Bonus'].mean().reset_index()

    # Crear el gráfico de barras para el promedio de salarios por departamento
    fig = px.bar(promedio_salarios, x='Country', y='Bonus',color='Country',
                labels={'Gender': 'Genero', 'Salario': 'Promedio de Salario'},
                title='Promedio de Salarios por País')

    # Mostrar el gráfico
    st.plotly_chart(fig, use_container_width=True,theme=theme_plotly)
Bonus_pais()

def top_10_maax_salario():
    df_top_10=df_selecionado.sort_values(by='AnnualSalary',ascending=False).head(10)
    st.markdown("<h1 style='text-align: center;'>Top 10 De Los Empleados Con Mayor Salarios</h1>", unsafe_allow_html=True)
    st.dataframe(df_top_10,)

top_10_maax_salario()

