import streamlit as st 
import plotly.express as px
import plotly.subplots as sp
import pandas as pd


st.set_page_config('Panel De Análisis Empresarial',page_icon='📊',layout='wide' )

st.subheader('Hecho Por Jhon Kerly Mosquera 🕵️‍♂️ Este panel se estara atualizando')
st.markdown("<h1 style='text-align: center;'>Panel De Análisis Empresarial 📊</h1>", unsafe_allow_html=True)
theme_plotly=None
df =pd.read_csv('customers.csv')

df['HireDate'] =pd.to_datetime(df['HireDate'])

df['Bonus'] = df['AnnualSalary'] * (df['Bonus'] / 100)

# Sumar el bonus al salario
df['TotalSalary'] = df['AnnualSalary'] + df['Bonus']


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
st.sidebar.header('Filtar Los Datos 🔎')
Department=st.sidebar.multiselect(
    label='Filtre Por Departamento',
    options=df['Department'].unique(),
    default=df['Department'].unique()[:2]
)
Country=st.sidebar.multiselect(
    label='Filtre Por Pasí 🔎',
    options=df['Country'].unique(),
    default=df['Country'].unique()[:1]
)
BusinessUnit=st.sidebar.multiselect(
    label='Filtre Por Unidad De Negocios 🔎',
    options=df['BusinessUnit'].unique(),
    default=df['BusinessUnit'].unique()[:2]
)
Gender=st.sidebar.multiselect(
    label='Filtre Por Genero 🔎',
    options=df['Gender'].unique(),
    default=df['Gender'].unique()[:2]
)
Ethnicity=st.sidebar.multiselect(
    label='Filtre Por Etnicidad 🔎',
    options=df['Ethnicity'].unique(),
    default=df['Ethnicity'].unique()[:]
)

df_selecionado= df.query('Department==@Department & Country==@Country & BusinessUnit==@BusinessUnit & Gender==@Gender & Ethnicity==@Ethnicity')

def metricas():
    max_salary_index = df_selecionado['AnnualSalary'].idxmax()
    employee_id_max_salary = df_selecionado.loc[max_salary_index, 'FullName']
    min_salary_index = df_selecionado['AnnualSalary'].idxmin()
    employee_id_min_salary = df_selecionado.loc[min_salary_index, 'FullName']

    from streamlit_extras.metric_cards import style_metric_cards
    col1,col2,col3,col4,col5=st.columns(5)

    col1.metric(label='Total De Empleados ',value=f'N° {df_selecionado.EEID.count()}',delta='Total De Empleados')
    col2.metric(label='Salario Anual',value=f'$ {df_selecionado.AnnualSalary.sum():,.0f}',delta='Suma Total De Los Salarios')
    col3.metric(label='Salario Anual',value=f'$ {df_selecionado.AnnualSalary.max():,.0f}',delta='Salario Mas Alto')
    col4.metric(label='Empleado con el salario mas alto',value=employee_id_max_salary,delta=f'Salario Mas Alto $ {df_selecionado.AnnualSalary.max():,.0f}')
    col5.metric(label='Empleado con el salario mas Bajo',value=employee_id_min_salary,delta=f'Salario Mas Bajo $ {df_selecionado.AnnualSalary.min():,.0f}')
    style_metric_cards(background_color='black',border_left_color='white')


metricas()

div1,div2=st.columns (2)
def pie():
    with div1:
        fig=px.pie(df_selecionado, values="AnnualSalary",hole=0.3, names= "Department", title='Salarios Por Departamento')
        fig. update_layout (legend_title="Department", legend_y=0.9)
        fig.update_traces (textinfo="percent+label", textposition="inside")
        st.plotly_chart(fig,use_container_width=True, theme=theme_plotly)
pie()

def bar():
    with div2:
        
        fig=px.bar (df_selecionado,y="AnnualSalary", x= "Department", text_auto=' .2s', title="Salarios Por Departamento")
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

div_pie,div_bar=st.columns(2)

def promedio_salario_gender():
    with div_bar:
        # Calcular el promedio de salarios por departamento
        promedio_salarios = df_selecionado.groupby('Gender')['AnnualSalary'].mean().reset_index()

        # Crear el gráfico de barras para el promedio de salarios por departamento
        fig = px.bar(promedio_salarios, x='Gender', y='AnnualSalary',color='Gender',
                    labels={'Gender': 'Genero', 'Salario': 'Promedio de Salario'},
                    title='Promedio de Salarios por Genero')

        # Mostrar el gráfico
        st.plotly_chart(fig, use_container_width=True,theme=theme_plotly)
promedio_salario_gender()



def gender_porcentaje():
    with div_pie:
        conteo_genero = df_selecionado['Gender'].value_counts()
        fig=px.pie(df_selecionado, values=conteo_genero.values,hole=0.3, names=conteo_genero.index, title='Distribucion de Genero')
        fig. update_layout (legend_title="Genero", legend_y=0.9)
        fig.update_traces (textinfo="percent+label", textposition="inside")
        st.plotly_chart(fig,use_container_width=True, theme=theme_plotly)

gender_porcentaje()

def promedio_salario_age():
    # Calcular el promedio de salarios por departamento
    promedio_salarios = df_selecionado.groupby('Age')['AnnualSalary'].mean().reset_index()

    # Crear el gráfico de barras para el promedio de salarios por departamento
    fig = px.bar(promedio_salarios, x='Age', y='AnnualSalary',color='Age', text_auto=' .2s',
                labels={'Gender': 'Genero', 'Salario': 'Promedio de Salario'},
                title='Promedio de Salarios por Eda')

    # Mostrar el gráfico
    st.plotly_chart(fig, use_container_width=True,theme=theme_plotly)
promedio_salario_age()

div_bar_et,div_pi_sal= st.columns(2)

def Bonus_pais():
    with div_bar_et:
    # Calcular el promedio de salarios por departamento
        promedio_salarios = df_selecionado.groupby('Country')['Bonus'].mean().reset_index()

        # Crear el gráfico de barras para el promedio de salarios por departamento
        fig = px.bar(promedio_salarios, x='Country', y='Bonus',color='Country',
                    labels={'Gender': 'Genero', 'Salario': 'Promedio de Bonus'},
                    title='Promedio de Bonus por País')

        # Mostrar el gráfico
        st.plotly_chart(fig, use_container_width=True,theme=theme_plotly)
Bonus_pais()

def salary_bonus():
     with div_pi_sal:   
        salary_bonus = df_selecionado.groupby('Country')['TotalSalary'].sum().reset_index()
        fig=px.pie(salary_bonus,values='TotalSalary',names='Country',hole=0.3, title='Salarios Con Bonos Por País')
        fig.update_layout(legend_title="Country", legend_y=0.9)
        fig.update_traces(textinfo="percent+label", textposition="inside")
        st.plotly_chart(fig,use_container_width=True, theme=theme_plotly)

salary_bonus()

d_reg1, d_reg2=st.columns(2)
def salior_mean_region():
    with d_reg1:
        # Calcular el promedio de salarios por departamento
        promedio_salarios = df_selecionado.groupby('Ethnicity')['AnnualSalary'].mean().reset_index()
        # Crear el gráfico de barras para el promedio de salarios por departamento
        fig = px.bar(promedio_salarios, x='Ethnicity', y='AnnualSalary',color='Ethnicity',
                    labels={'Ethnicity': 'Etnicidad', 'Salario': 'Promedio de Salario'},
                    title='Promedio de Salario por Etnicidad')
        # Mostrar el gráfico
        st.plotly_chart(fig, use_container_width=True,theme=theme_plotly)
salior_mean_region()


def bonus_mean_region():
     with d_reg2:   
    # Calcular el promedio de salarios por departamento
        promedio_salarios = df_selecionado.groupby('Ethnicity')['Bonus'].mean().reset_index()
        # Crear el gráfico de barras para el promedio de salarios por departamento
        fig = px.bar(promedio_salarios, x='Ethnicity', y='Bonus',color='Ethnicity',
                    labels={'Ethnicity': 'Etnicidad', 'Bonus': 'Promedio de Bonus'},
                    title='Promedio de Bonus por Etnicidad')
        # Mostrar el gráfico
        st.plotly_chart(fig, use_container_width=True,theme=theme_plotly)
bonus_mean_region()

jot_pie,jot_table=st.columns(2)
def Gender_Jot_pie():
    with jot_pie:
        grouped = df_selecionado.groupby(['JobTitle', 'Gender']).size().reset_index(name='Count')
    # Graficar en un gráfico de pastel
        # Graficar en un gráfico de pastel
        fig = px.pie(grouped, names='JobTitle', values='Count', 
                title='Conteo General por género en cada tipo de empleo', 
                color='JobTitle', hole=0.3,
                labels={'Gender': 'Género'},
                custom_data=['JobTitle']
            )  # Agregar el tipo de empleo como custom_data
        st.plotly_chart(fig, use_container_width=True,theme=theme_plotly)
Gender_Jot_pie()


def Gender_Jot_table():
    with jot_table:
        grouped = df_selecionado.groupby(['JobTitle', 'Gender']).size().reset_index(name='Count')
        st.markdown("<h6 style='text-align: center;'>Tabla de Conteo por género en cada tipo de empleo </h6>", unsafe_allow_html=True)
        st.dataframe(grouped,use_container_width=True)
Gender_Jot_table()


def Gender_Jot_bar():
    grouped = df_selecionado.groupby(['JobTitle', 'Gender']).size().reset_index(name='Count')
# Graficar en un gráfico de pastel
    # Graficar en un gráfico de pastel
    fig = px.bar(grouped, x='JobTitle', y='Count', color='Gender', 
             title='Conteo por género en cada tipo de empleo',
             labels={'Gender': 'Género'},
             text='Count', 
             barmode='group',height=500)

    fig.update_traces(texttemplate='%{text}', textposition='outside') # Agregar el tipo de empleo como custom_data
    st.plotly_chart(fig, use_container_width=True,theme=theme_plotly)
Gender_Jot_bar()


def top_10_city_salario_max():
    df_top_10=df_selecionado.groupby('City')['AnnualSalary'].sum().sort_values().head(10)
    fig=px.bar(df_top_10,color=df_top_10.index)
    st.markdown("<h1 style='text-align: center;'>Top 10 De Las Ciudades Con Mayores Salarios</h1>", unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True,theme=theme_plotly)
    
    
top_10_city_salario_max()

def top_10_maax_salario():
    df_top_10=df_selecionado.groupby('FullName')['AnnualSalary'].sum().sort_values().head(10)
    fig=px.bar(df_top_10,color=df_top_10.index)
    st.markdown("<h1 style='text-align: center;'>Top 10 De Los Empleados Con Mayores Salarios</h1>", unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True,theme=theme_plotly)

top_10_maax_salario()


st.markdown("<h1 style='text-align: center;'>Datos Utilizados</h1>", unsafe_allow_html=True)
st.dataframe(df_selecionado)

