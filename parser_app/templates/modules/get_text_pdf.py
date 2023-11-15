import subprocess


def get_text_pdf_pars(input_pdf_path, output_html_path):
    try:
        subprocess.run(
            ["pdftohtml", "-enc", "UTF-8", "-noframes", "-c", input_pdf_path, output_html_path],
            check=True
        )
        print(f"Conversion successful. HTML saved to {output_html_path}")

        # Додаємо розриви між сторінками
        add_page_breaks(output_html_path)


    except subprocess.CalledProcessError as e:
        print(f"Error during conversion: {e}")


def add_page_breaks(html_path):
    with open(html_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Додаємо розриви між сторінками
    html_content = html_content.replace('</div>', '</div><div class="page-break" style="padding: 10px;"></div>')


    with open(html_path, 'w', encoding='utf-8') as file:
        file.write(html_content)
