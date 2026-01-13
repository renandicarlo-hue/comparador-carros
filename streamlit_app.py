import streamlit as st
from PIL import Image, ImageChops

def trim_image(img):
    bg = Image.new(img.mode, img.size, img.getpixel((0,0)))
    diff = ImageChops.difference(img, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return img.crop(bbox)
    return img

st.set_page_config(page_title="Comparador Técnico de Carros", layout="wide")

st.title("🚗 Comparador com Escala Real (mm)")

col1, col2 = st.columns(2)
with col1:
    file1 = st.file_uploader("Carro A (Base)", type=["png", "jpg", "jpeg"])
    comp_a = st.number_input("Comprimento Carro A (mm)", value=4000)

with col2:
    file2 = st.file_uploader("Carro B (Sobreposição)", type=["png", "jpg", "jpeg"])
    comp_b = st.number_input("Comprimento Carro B (mm)", value=4000)

if file1 and file2:
    # 1. Carrega e limpa as bordas
    img1 = trim_image(Image.open(file1).convert("RGBA"))
    img2 = trim_image(Image.open(file2).convert("RGBA"))

    # 2. Lógica de Redimensionamento Automático
    # Calculamos quantos pixels o Carro A tem por milímetro real
    pixels_por_mm_a = img1.size[0] / comp_a
    
    # Calculamos qual deveria ser a largura do Carro B em pixels para manter a escala
    new_width_b = int(comp_b * pixels_por_mm_a)
    # Mantemos a proporção da altura (ratio)
    ratio_b = img2.size[1] / img2.size[0]
    new_height_b = int(new_width_b * ratio_b)
    
    img2_scaled = img2.resize((new_width_b, new_height_b), Image.LANCZOS)

    # 3. Controles Laterais
    st.sidebar.header("Ajustes de Alinhamento")
    off_x = st.sidebar.slider("Mover Horizontal (Eixo)", -1000, 1000, 0)
    off_y = st.sidebar.slider("Mover Vertical (Chão)", -500, 500, 0)
    alpha = st.sidebar.slider("Opacidade", 0.0, 1.0, 0.5)

    # 4. Criação do Canvas Final
    # Criamos um fundo grande o suficiente para ambos
    max_w = max(img1.size[0], img2_scaled.size[0] + abs(off_x)) + 100
    max_h = max(img1.size[1], img2_scaled.size[1] + abs(off_y)) + 100
    
    canvas = Image.new("RGBA", (int(max_w), int(max_h)), (255, 255, 255, 0))
    overlay = Image.new("RGBA", (int(max_w), int(max_h)), (255, 255, 255, 0))
    
    # Colamos o Carro A no "chão" (base do canvas)
    canvas.paste(img1, (0, int(max_h - img1.size[1])))
    # Colamos o Carro B com o deslocamento
    overlay.paste(img2_scaled, (off_x, int(max_h - img2_scaled.size[1] + off_y)))

    result = Image.blend(canvas, overlay, alpha)
    
    st.image(result, use_container_width=True)
    st.caption(f"Escala baseada em {pixels_por_mm_a:.2f} pixels/mm")
else:
    st.info("💡 Dica: Tente usar imagens em .PNG com fundo transparente para resultados perfeitos.")
