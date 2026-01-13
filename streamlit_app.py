import streamlit as st
from PIL import Image

st.set_page_config(page_title="Comparador de Carros", layout="wide")

st.title("🚗 Protótipo: Comparação de Vista Lateral")
st.write("Suba duas fotos de perfil para comparar as silhuetas.")

# Colunas para upload
col1, col2 = st.columns(2)
with col1:
    file1 = st.file_uploader("Carro A (Base)", type=["png", "jpg", "jpeg"])
with col2:
    file2 = st.file_uploader("Carro B (Sobreposição)", type=["png", "jpg", "jpeg"])

if file1 and file2:
    img1 = Image.open(file1).convert("RGBA")
    img2 = Image.open(file2).convert("RGBA")

    # Redimensiona a segunda imagem para o tamanho da primeira para o teste
    img2 = img2.resize(img1.size)

    # Controle de transparência
    alpha = st.slider("Nível de Sobreposição (Transparência)", 0.0, 1.0, 0.5)

    # Cria a sobreposição
    blended = Image.blend(img1, img2, alpha)
    
    st.subheader("Resultado da Comparação")
    st.image(blended, use_container_width=True)
    
    st.info("Dica: Use fotos com fundo branco ou transparente para um resultado melhor.")
else:
    st.warning("Aguardando o upload das duas imagens...")
