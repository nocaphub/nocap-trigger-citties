# Código app.py com variáveis de ambiente via secrets.toml

app_safe_keys = """
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
import openai
from supabase import create_client

# CONFIGURAÇÃO INICIAL
st.set_page_config(page_title="Radar Nocap", layout="wide")
st.title("📍 Radar de Trigger Cities - Nocap")

# SEGREDOS DO STREAMLIT
openai.api_key = st.secrets["OPENAI_API_KEY"]
supabase_url = st.secrets["SUPABASE_URL"]
supabase_key = st.secrets["SUPABASE_KEY"]
supabase = create_client(supabase_url, supabase_key)

# CARREGAR DADOS DO SUPABASE
dados_resp = supabase.table("dados_plataformas").select("*").execute()
cidades_resp = supabase.table("cidades").select("*").execute()

df = pd.DataFrame(dados_resp.data)
cidades_df = pd.DataFrame(cidades_resp.data)

# Ajuste de tipos
df["cidade_id"] = df["cidade_id"].astype(str)
cidades_df["id"] = cidades_df["id"].astype(str)

# MERGE DOS DADOS
merged_df = pd.merge(df, cidades_df, left_on='cidade_id', right_on='id')

# MAPA
st.subheader("🌍 Mapa de Crescimento")
m = folium.Map(location=[-14.2350, -51.9253], zoom_start=4)
for _, row in merged_df.iterrows():
    if pd.notnull(row["Latitude"]) and pd.notnull(row["Longitude"]):
        folium.CircleMarker(
            location=[row["Latitude"], row["Longitude"]],
            radius=row["taxa_crescimento"] / 2,
            popup=f"{row['nome']} | {row['plataforma']} | Crescimento: {row['taxa_crescimento']}%",
            color="red" if row["taxa_crescimento"] > 20 else "blue",
            fill=True,
            fill_opacity=0.6
        ).add_to(m)
folium_static(m)

# INSIGHTS COM GPT
st.subheader("🔎 Geração de Insights por Cidade")
cidades_unicas = merged_df["nome"].unique()
cidade_escolhida = st.selectbox("Escolha uma cidade para analisar:", cidades_unicas)

# Dados da cidade selecionada
cidade_data = merged_df[merged_df["nome"] == cidade_escolhida].iloc[0]
cidade = cidade_data["nome"]
crescimento = cidade_data["taxa_crescimento"]
plataforma = cidade_data["plataforma"]
artistas = cidade_data["artistas_em_alta"]

if st.button("Gerar Insight com IA"):
    prompt = f\"\"\"
    Cidade: {cidade}
    Crescimento: {crescimento}%
    Plataforma destaque: {plataforma}
    Artistas em alta: {artistas}

    Gere uma análise no estilo Nocap, com linguagem direta, urbana e provocativa. A ideia é ajudar um artista independente a tomar uma ação estratégica nessa cidade, com base nesses dados. Dê 2 ou 3 sugestões práticas.
    \"\"\"
    resposta = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    insight = resposta["choices"][0]["message"]["content"]
    st.markdown("### 💡 Insight Gerado pela IA:")
    st.write(insight)
"""

# Salvar versão segura do app.py
safe_app_path = "/mnt/data/app.py"
with open(safe_app_path, "w") as f:
    f.write(app_safe_keys)

safe_app_path
