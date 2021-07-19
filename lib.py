
import re



def liqu_read_cedula(source_d):
    """extract cedula from list of lines"""
    y = ''
    for x in source_d:
        p = re.findall('^Empleado.+?([A0-9].+?) ', x)
        if not p:
            continue
        else:
            y = str(p[0])
    return y


def liquidaciones_pdf(source, pdf_file_name):
    """escribe la lista source a un archivo outfile"""
    from fpdf import FPDF
    pdf = FPDF('P', 'in', 'Letter')
    font_height = 0.12
    for i in source:
        pdf.add_page()
        pdf.set_margins(0.25, 0.25)
        pdf.set_auto_page_break(False, margin=0.25)
        pdf.set_font('Courier', '', 9)
        pdf.set_xy(0.25, 0.25)
        for ii in i:
            pdf.write(font_height, ii)

    pdf.output(pdf_file_name, 'F')


def doPDF(source_path, dest_path):
    from pathlib import Path
    with open(source_path, 'r', encoding="latin-1") as original:
        archivo_txt = original.readlines()

    last_line = ''
    pages = []
    temp_page = []
    cedula = ''
    out = []
    for each_line in archivo_txt:  # start reading
        if each_line == last_line:  # skip repeated lines
            continue
        else:
            fin_pagina = re.findall('(Revisado Por)', each_line)  # find EOP in line
            temp_page.append(each_line)  # add line to current page
            if fin_pagina:
                ced = liqu_read_cedula(temp_page)  # End_Of_Page found, find cedula in current page
                if not ced:
                    pages.append(temp_page)
                    filename = cedula + ".pdf"
                    pdf_file = f"{dest_path}/{filename}"
                    print(pdf_file)
                    liquidaciones_pdf(pages, pdf_file)
                    pages = []
                    temp_page = []
                    out.append(filename)
                else:
                    cedula = ced
                    pages.append(temp_page)
                    temp_page = []
            else:
                last_line = each_line
    return out

def volantes_pdf(source_lines, pdf_file):
    """escribe la lista source a un archivo outfile"""
    from fpdf import FPDF
    pdf = FPDF('P', 'in', (8.5, 5))
    font_height = 0.12
    pdf.add_page()
    pdf.set_margins(0.25, 0.25)
    pdf.set_auto_page_break(True, margin=0.25)
    pdf.set_font('Courier', '', 7)
    pdf.set_xy(0.25, 0.25)
    for linea in source_lines:
        pdf.write(font_height, linea)
    pdf.output(pdf_file, 'F')


def read_cedula(source_d):
    """extract cedula from list of lines output is str"""
    import re
    y = ''
    for xx in source_d:
        p = re.findall('^([A0-9].+?) ', xx)
        if not p:
            continue
        else:
            y = str(p[0].strip('A'))
    return y

def doVolantes(open_file_path,save_file_path):
    # Read input txt File
    with open(open_file_path, 'r', encoding="latin-1") as fileh:
        contents = fileh.readlines()

    # add EOF marker  - Esto indica el final del archivo
    contents.append("PAGEBREAK\n")

    # remove duplicate lines + create nuevo_plano.txt
    unique = []
    cedula = []
    pb = []
    with open('../nuevo_plano.txt', 'w') as nuevo_plano:

        for x in range(len(contents)):
            if contents[x].startswith('==========') and x > 5:
                nuevo_plano.write("PAGEBREAK\n")

            unique.append(contents[x])
            nuevo_plano.write(contents[x])

    # write individual pdfs
    doc = []
    out = []
    for line in open('../nuevo_plano.txt', 'r'):
        pp = re.findall('^(PAGEBREAK)', line)
        if not pp:
            doc.append(line)
        else:
            filename = read_cedula(doc) + ".pdf"
            new_pdf = (f'{save_file_path}/{filename}')
            volantes_pdf(doc, new_pdf)
            doc = []
            out.append(filename)
            print(filename)
    return out
