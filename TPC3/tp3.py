import re

def markdown_to_html(markdown_text):
    # Cabeçalhos
    markdown_text = re.sub(r'# (.+)', r'<h1>\1</h1>', markdown_text)

    # Negrito
    markdown_text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', markdown_text)

    # Itálico
    markdown_text = re.sub(r'\*(.+?)\*', r'<i>\1</i>', markdown_text)

    # Lista numerada
    markdown_text = re.sub(r'^(\d+\..+)$', r'<li>\1</li>', markdown_text, flags=re.MULTILINE)
    markdown_text = re.sub(r'<ol>\n', r'<ol>\n', markdown_text)

    # Link e Imagem
    markdown_text = re.sub(r'!\[([^]]+)\]\(([^)]+)\)', r'<img alt="\1" src="\2"/>', markdown_text)
    markdown_text = re.sub(r'\[([^]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', markdown_text)

    return markdown_text

# Função para ler o conteúdo de um arquivo e converter para HTML
def convert_file_to_html(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        markdown_content = file.read()

    html_content = markdown_to_html(markdown_content)

    # Adiciona tags HTML básicas para criar um documento HTML completo
    html_content = f'<!DOCTYPE html>\n<html>\n<head>\n<title>Markdown para HTML</title>\n</head>\n<body>\n{html_content}\n</body>\n</html>'

    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(html_content)

input_file_path = 'exemplo.md'
output_file_path = 'exemplo.html'

convert_file_to_html(input_file_path, output_file_path)
