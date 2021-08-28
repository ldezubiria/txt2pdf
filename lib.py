from pathlib import Path
import re
import sqlite3
from os import path
import itertools
import os


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
        pdf.set_font('Courier', '', 7)
        pdf.set_xy(0.25, 0.25)
        for ii in i:
            pdf.write(font_height, ii)

    pdf.output(pdf_file_name, 'F')


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


def read_cedula(source_d, output='single'):
    """extract cedula from list of lines output is str"""
    import re
    xy = []
    for xx in source_d:
        p = re.findall('^([A0-9].+?) ', xx)
        if not p:
            continue
        else:
            if output == 'single':
                y = str(p[0].strip('A'))
                return y
            else:
                xy.append(p[0].strip('A'))
    return xy


def doLiquid(source_path, dest_path):
    archivo_txt = []
    for i in source_path:
        with open(i, 'r', encoding="latin-1") as original:
            archivo = original.readlines()
            archivo_txt.extend(archivo)
    last_line = ''
    pages = []
    temp_page = []
    cedula = ''
    out = []
    numero = 0
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
                    filename = cedula
                    pdf_file = unique_file("{dest_path}/{filename}".format(dest_path=dest_path, filename=filename))
                    print(pdf_file)
                    liquidaciones_pdf(pages, pdf_file)
                    numero += 1
                    pages = []
                    temp_page = []
                    out.append(filename)
                else:
                    cedula = ced
                    pages.append(temp_page)
                    temp_page = []
            else:
                last_line = each_line
    print('\n{0} documentos creados.'.format(numero))
    return out


def doVolantes(filepaths,save_file_path):
    # Read all input txt Files and merge the contents into a single list (result)
    result = []
    for i in filepaths:
        with open(i, 'r', encoding="latin-1") as fileh:
            contents = fileh.readlines()
            result.extend(contents)

        # add EOF marker  - Esto indica el final del archivo
        result.append("PAGEBREAK\n")
    print(result)
    # remove duplicate lines + create nuevo_plano.txt
    unique = []

    with open('../nuevo_plano.txt', 'w') as nuevo_plano:

        for x in range(len(result)):
            if result[x].startswith('==========') and x > 5:
                nuevo_plano.write("PAGEBREAK\n")

            unique.append(result[x])
            nuevo_plano.write(result[x])

    # write individual pdfs
    doc = []
    out = []
    numero = 0
    for line in open('../nuevo_plano.txt', 'r'):
        pp = re.findall('^(PAGEBREAK)', line)
        if not pp:
            doc.append(line)
        else:
            filename = read_cedula(doc)
            new_pdf = unique_file(f'{save_file_path}/{filename}')
            print(new_pdf)
            volantes_pdf(doc, new_pdf)
            numero += 1
            out.append(new_pdf)
            doc = []
    print('{0} documentos creados.'.format(numero))
    return out

def read_nombres(source_d):
    """extract nombres from list of lines. output is a list"""
    import re
    xy = []
    for t in range(len(source_d)):
        p = re.findall('^[A0-9].+?([A-Z][A-Z].+)\$', source_d[t])
        if not p:
            continue
        else:
            xy.append(p[0].strip())
    return xy


def read_fecha(source_d):
    """Extrae la fecha de la nomina de los volantes"""
    import re
    for x in range(len(source_d)):
        p = re.findall('(NOMINA.[0-9].+?20[0-9][0-9])', source_d[x])
        q = re.findall('(LIQ.PRIMAS.+20[0-9][0-9] )', source_d[x])
        r = re.findall('(PRIMA.EXTRALEGAL.LAUDO.+20[0-9][0-9] )', source_d[x])
        s = re.findall('(LIQ.INTERES.*CESANTIAS.+20[0-9][0-9] )', source_d[x])
        if not p and not q and not r and not s:
            continue
        else:
            if not p and not r and not s:
                return q[0]
            elif not p and not q and not s:
                return r[0]
            elif not p and not q and not r:
                return s[0]
            else:
                return p[0]


def read_empresa(source_d):
    """Selecciona la tabla donde se debe consultar o agregar los registros"""
    for z in source_d:
        if 'SERVICIOS INDUSTRIALES Y PORTUARIOS SAS' in z:
            emp = 'personal_sp'
            return emp
        elif 'SIPORT TECNICO SAS' in z:
            emp = 'personal_st'
            return emp
    return -1

def check_dir(dir):

    return path.isdir(dir)


def check_files(filepaths):
    for i in filepaths:
        if path.isfile(i) is False:
            return False
        else:
            print(i)
    return True

def unique_file(basename):
    #Check for existing filename and rename accordingly
    actualname = "{0}.pdf".format(basename)
    c = itertools.count(1)
    while os.path.exists(actualname):
        actualname = "{0} ({1}).pdf".format(basename, next(c))
    return str(actualname)
