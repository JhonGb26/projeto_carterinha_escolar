from PIL import Image, ImageDraw, ImageFont, ImageOps
import pandas as pd
import qrcode
import barcode
from barcode import Code39
from barcode.writer import ImageWriter

pd.read_csv("alunos.csv",sep = ";")

dados_alunos = pd.read_csv("alunos.csv",sep = ";")

for indice, aluno in dados_alunos.iterrows():
    matricula = dados_alunos['Matrícula'].values[0]
    nome = dados_alunos["Nome"].values[0]
    serie = ['1', '2','3']
    turno = ['Matutino', 'Vespertino']
    curso = ['RH', 'ADM', 'Medio']

codigo_de_barras = Code39(str(dados_alunos['Matrícula'].values[0]), writer=ImageWriter(), add_checksum=False)
codigo_de_barras_imagem = codigo_de_barras.render()
nova_largura = 135
nova_altura = int(float(nova_largura) / codigo_de_barras_imagem.width * codigo_de_barras_imagem.height)
codigo_de_barras_imagem = codigo_de_barras_imagem.resize((nova_largura, nova_altura))


qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr.add_data(f"Nome: {nome}\nMatrícula: {matricula}\nSerie: {serie[0]}")
qr.make(fit=True)
img_qr = qr.make_image(fill_color="black", back_color="white")
img_qr = img_qr.resize((150, 150))


carteirinha1 = Image.open("Group 4.png")
carteirinha2 = Image.open("Group 6.png")

carteirinha1 = ImageOps.expand(carteirinha1, border=5, fill="black")
carteirinha2 = ImageOps.expand(carteirinha2, border=5, fill="black")

carteirinhas_lado_a_lado = Image.new("RGB", (carteirinha1.width + carteirinha2.width, carteirinha1.height))
carteirinhas_lado_a_lado.paste(carteirinha1, (0, 0))
carteirinhas_lado_a_lado.paste(carteirinha2, (carteirinha1.width, 0))

img_foto = Image.open("foto.png")
tamanho_foto = (180, 240)
img_foto = img_foto.resize(tamanho_foto)
posicao_foto = (378, 15)
carteirinhas_lado_a_lado.paste(img_foto, posicao_foto)

posicao_qr = (10, 95)
carteirinhas_lado_a_lado.paste(img_qr, posicao_qr)
carteirinhas_lado_a_lado.paste(codigo_de_barras_imagem, (970, 30))

posicao_nome = (50, 280)
posicao_matricula = (412, 280)
posicao_serie = (222, 310)
posicao_turno = (425, 308)
posicao_curso = (510, 308)
font = ImageFont.truetype("arial.ttf", size=14)
font2 = ImageFont.truetype("arial.ttf", size=16)
draw = ImageDraw.Draw(carteirinhas_lado_a_lado)
draw.text(posicao_nome, f"Nome: {nome}", font=font, fill="black")
draw.text(posicao_matricula, f"RM: {matricula}", font=font, fill="black")
draw.text(posicao_serie, f"Serie: {serie[0]}", font=font2, fill="black")
draw.text(posicao_turno, f"{turno[1]}", font=font2, fill="black")
draw.text(posicao_curso, f"{curso[2]}", font=font2, fill="black")

nome_arquivo = f"{nome}.png"
carteirinhas_lado_a_lado.save(nome_arquivo)