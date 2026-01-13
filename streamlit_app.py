import streamlit as st
from PIL import Image, ImageChops

def trim_image(img):
    """Remove as bordas vazias (transparentes ou brancas) ao redor do carro."""
    bg = Image.new(img.mode, img.size, img.getpixel((0,0)))
    diff = ImageChops.difference(img, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return img.crop(bbox)
    return img

st.set_page_config(page_title="Comparador Pro", layout="wide")

st.title("🚗 Comparador de Silhuetas Automotivas")
st.write("O app agora recorta as bordas automaticamente para focar no veículo.")

col1, col2 = st.columns(2)
with col1:
    file1 = st.file_uploader("Carro A (Base)", type=["png", "jpg", "jpeg"])
with col2:
    file2 = st.file_uploader("Carro B (Sobreposição)", type=["png", "jpg", "jpeg"])

if file1 and file2:
    # Processamento das imagens
    img1 = trim_image(Image.open(file1).convert("RGBA"))
    img2 = trim_image(Image.open(file2).convert("RGBA"))

    st.sidebar.header("Ajustes de Precisão")
    
    # Redimensionamento para escala (Simulação)
    width1 = st.sidebar.slider("Redimensionar Carro B (%)", 50, 150, 100)
    new_width = int(img1.size[0] * (width1 / 100))
    new_height = int(img1.size[1] * (width1 / 100))
    img2 = img2.resize((new_width, new_height))

    # Ajuste de Posição (Essencial para alinhar rodas)
    off_x = st.sidebar.slider("Mover Horizontalmente", -500, 500, 0)
    off_y = st.sidebar.slider("Mover Verticalmente", -200, 200, 0)

    # Transparência
    alpha = st.sidebar.slider("Opacidade do Carro B", 0.0, 1.0, 0.5)

    # Criar tela de fundo (Canvas)
    canvas = Image.new("RGBA", img1.size, (255, 255, 255, 0))
    canvas.paste(img1, (0, 0))
    
    # Criar camada de sobreposição
    overlay = Image.new("RGBA", img1.size, (255, 255, 255, 0))
    overlay.paste(img2, (off_x, off_y))

    # Combinar
    result = Image.blend(canvas, overlay, alpha)
    
    st.image(result, caption="Compare o entre-eixos e a altura do teto", use_container_width=True)
else:
    st.info("💡 Dica: Tente usar imagens em .PNG com fundo transparente para resultados perfeitos.")
