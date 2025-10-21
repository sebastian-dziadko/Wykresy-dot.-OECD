import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import numpy as np

# Wczytanie danych z Excela
df = pd.read_excel("OECD.xlsx") 

# Obliczenie średniej długości życia
df['Średnia długość życia'] = (df['Długość życia kobiet'] + df['Długość życia mężczyzn']) / 2

# Inicjalizacja aplikacji Dash
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Analiza Wskaźników OECD", style={'textAlign': 'center'}),
    
    # Pierwszy wykres: PKB vs Długość życia
    html.Div([
        dcc.Graph(id='wykres-pkb-zycie'),
        dcc.RangeSlider(
            id='pkb-slider',
            min=df['Pkb per capita'].min(),
            max=df['Pkb per capita'].max(),
            step=5000,
            value=[df['Pkb per capita'].min(), df['Pkb per capita'].max()],
            marks={i: f'{i:,.0f}' for i in range(20000, 120001, 20000)}
        )
    ], style={'padding': '20px', 'border': '1px solid #ddd', 'margin': '10px'}),
    
    # Drugi wykres: Korelacje wskaźników
    html.Div([
        dcc.Graph(id='wykres-korelacji'),
        dcc.Dropdown(
            id='kolor-dropdown',
            options=[
                {'label': 'Stopa bezrobocia', 'value': 'Stopa bezrobocia'},
                {'label': 'Wskaźnik Giniego', 'value': 'Gini dochod'},
                {'label': 'Wydatki publiczne', 'value': 'Wydatki publiczne jako % PKB'}
            ],
            value='Stopa bezrobocia',
            clearable=False
        )
    ], style={'padding': '20px', 'border': '1px solid #ddd', 'margin': '10px'}),
    
    # Trzeci wykres: Wiek emerytalny
    html.Div([
        dcc.Graph(id='wykres-wiek-emerytalny'),
        dcc.Dropdown(
            id='kraj-dropdown',
            options=[{'label': kraj, 'value': kraj} for kraj in df['Kraj'].unique()],
            value=['Polska', 'Niemcy', 'Szwecja', 'Stany Zjednoczone', 'Japonia'],
            multi=True,
            placeholder="Wybierz kraje do porównania"
        )
    ], style={'padding': '20px', 'border': '1px solid #ddd', 'margin': '10px'}),
    

])

# Callback dla pierwszego wykresu
@app.callback(
    Output('wykres-pkb-zycie', 'figure'),
    Input('pkb-slider', 'value')
)
def update_wykres_pkb_zycie(pkb_range):
    filtered_df = df[(df['Pkb per capita'] >= pkb_range[0]) & 
                    (df['Pkb per capita'] <= pkb_range[1])]
    
    fig = px.scatter(
        filtered_df,
        x='Pkb per capita',
        y='Średnia długość życia',
        size='Liczba samobójstw na 100 tys. mieszkanców',
        color='Stopa bezrobocia',
        hover_name='Kraj',
        title='Zależność między PKB per capita a długością życia<br><sup>Rozmiar punktów odpowiada liczbie samobójstw na 100 tys. mieszkańców</sup>',
        labels={
            'Pkb per capita': 'PKB per capita (USD)',
            'Średnia długość życia': 'Średnia długość życia (lata)',
            'Liczba samobójstw na 100 tys. mieszkanców': 'Liczba samobójstw',
            'Stopa bezrobocia': 'Stopa bezrobocia (%)'
        },
        size_max=40
    )
    fig.update_layout(transition_duration=500)
    return fig

# Callback dla drugiego wykresu
@app.callback(
    Output('wykres-korelacji', 'figure'),
    Input('kolor-dropdown', 'value')
)
def update_wykres_korelacji(kolor):
    fig = px.scatter(
        df,
        x='Konsumpcja',
        y='Decyl 9/1 dochód',
        color=kolor,
        hover_name='Kraj',
        title='Korelacja wskaźników ekonomicznych',
        labels={
            'Konsumpcja': 'Konsumpcja per capita',
            'Decyl 9/1 dochód': 'Nierówności dochodowe (9/1)'
        },
        trendline='ols'
    )
    fig.update_layout(transition_duration=500)
    return fig

# Callback dla trzeciego wykresu (wiek emerytalny)
@app.callback(
    Output('wykres-wiek-emerytalny', 'figure'),
    Input('kraj-dropdown', 'value')
)
def update_wykres_wiek_emerytalny(wybrane_kraje):
    if not wybrane_kraje:
        wybrane_kraje = ['Polska']  # Domyślny kraj jeśli nic nie wybrano
    
    filtered_df = df[df['Kraj'].isin(wybrane_kraje)].melt(
        id_vars=['Kraj'], 
        value_vars=['Wiek emerytalny kobiet', 'Wiek emerytalny mężczyzn'],
        var_name='Płeć', 
        value_name='Wiek emerytalny'
    )
    
    # Zamiana nazw dla czytelności
    filtered_df['Płeć'] = filtered_df['Płeć'].replace({
        'Wiek emerytalny kobiet': 'Kobiety',
        'Wiek emerytalny mężczyzn': 'Mężczyźni'
    })
    
    fig = px.bar(
        filtered_df,
        x='Kraj',
        y='Wiek emerytalny',
        color='Płeć',
        barmode='group',
        title='Porównanie wieku emerytalnego kobiet i mężczyzn',
        labels={'Wiek emerytalny': 'Wiek emerytalny (lata)', 'Kraj': 'Kraj'},
        text='Wiek emerytalny',
        hover_data={'Kraj': True, 'Płeć': True, 'Wiek emerytalny': ':.1f'}
    )
    
    fig.update_traces(texttemplate='%{y:.1f}', textposition='outside')
    fig.update_layout(
        uniformtext_minsize=8,
        uniformtext_mode='hide',
        yaxis_range=[50,70],  # Stała skala dla lepszego porównania
        transition_duration=500
    )
    
    return fig

# Callback dla tabeli



if __name__ == "__main__":
    app.run(debug=True)
#http://127.0.0.1:8050/ lokalny link

