
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

st.set_page_config(page_title="Radar Nocap", layout="wide")

st.title("📍 Radar de Trigger Cities - Nocap")
st.write("Veja onde os artistas da cena urbana estão esquentando 👇")

# Carrega os dados das tabelas exportadas
df = pd.read_csv("tabela_dados_plataformas_trigger.csv")
cidades_df = pd.read_csv("tabela_cidades_trigger.csv")

# Faz o merge dos dados
merged_df = pd.merge(df, cidades_df, left_on='cidade_id', right_on='id')

# Cria o mapa
m = folium.Map(location=[-14.2350, -51.9253], zoom_start=4)

# Adiciona marcadores no mapa
for _, row in merged_df.iterrows():
    folium.CircleMarker(
        location=[row["Latitude"], row["Longitude"]],
        radius=row["taxa_crescimento"] / 2,
        popup=f"{row['nome']} | {row['plataforma']} | Crescimento: {row['taxa_crescimento']}%",
        color="red" if row["taxa_crescimento"] > 20 else "blue",
        fill=True,
        fill_opacity=0.6
    ).add_to(m)

# Mostra o mapa no app
folium_static(m)
