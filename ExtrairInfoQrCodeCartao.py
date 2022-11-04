from cgi import print_form
from dataclasses import replace
from email.policy import default
import os
import shutil
from unittest import result
import cv2
from pyzbar.pyzbar import decode
import numpy as np
import sys
import qrcode
import pyqrcode
import qrtools
from pdf2image import *
sys.stdout.reconfigure(encoding='utf-8')
def clear(): return os.system('cls')

import mysql.connector

def PegarNomeTemplate(id_template):
    mydb = mysql.connector.connect(
    host="localhost",
    user="wallace",
    password="522345",
    database="semed_manaus"
)
    mycursor = mydb.cursor()
    mycursor.execute("SELECT FOLDER_TEMPLATE_REZ FROM template WHERE ID_TEMPLATE = {ID};".format(ID = id_template))
    myresult = mycursor.fetchall()
    mydb.close()
    return  myresult[0]

def PegarNomeAluno(matricula, id_turma):
    mydb = mysql.connector.connect(
    host="localhost",
    user="wallace",
    password="522345",
    database="semed_manaus"
)
    mycursor = mydb.cursor()
    mycursor.execute("SELECT NOME_ALUNO FROM aluno WHERE MATRICULA = {ID} AND ID_TURMA = {id_turma} ;".format(ID = matricula, id_turma = id_turma))
    myresult = mycursor.fetchall()
    mydb.close()
    #print(myresult);
    if(len(myresult) < 1):
        return ""
    return myresult[0][0];

def MoverArquivo(f, pastaOrigem, pastaDestino):
    shutil.move(pastaOrigem + os.path.basename(f),
                pastaDestino + os.path.basename(f))


def LerQrCode(barcode, pastaOrigem, n, f):

    data = barcode.data.decode('utf-8')
    if (data != "" and data is not None):
        n = n+1
        dadosEmVetor = data.split(";")
        id_template = dadosEmVetor[1]
        print("\n")
       ## print(dadosEmVetor)
        print("\n")
        matricula = dadosEmVetor[5]
        #print(matricula)
        id_turma = dadosEmVetor[3]
        #print(id_template)
        caminhoArquivoResposta = PegarNomeTemplate(id_template)
        nomeAluno = PegarNomeAluno(matricula, id_turma)
        #print("\n"+ nomeAluno +"\n")
        
        fi = open("QrCodesRead.txt", "a")
        fi.write("QrCode: {data1}; Nome do Aluno: {nomeAluno}; Caminho Arquivo de Resposta Remark: \"{caminho}\"\n".format(data1=data, caminho = caminhoArquivoResposta[0], nomeAluno = nomeAluno))
        fi.close()
        try:
            MoverArquivo(f, pastaOrigem, "CartoesProcessados\\")
        except:
            print("Arquivo não encontrado : " +
                  str(os.path.basename(f)) + "\n")
    # print(data)
    return n


def DecodificarQrCode(f, image):
    pastaOrigem = f.replace(os.path.basename(f), "")
    decoded = ""
    decoded = decode(image)
    if (decoded == None or len(decoded) < 1):
        decoded = "Não lido... arquivo: " + str(os.path.basename(f))
        try:
            MoverArquivo(f, pastaOrigem, "QrCodeNaoLido\\")
        except Exception as e:
            print("Arquivo não encontrado : " +
                  str(os.path.basename(f)) + "\n")

    return decoded, pastaOrigem


def ConverterImagem(directory, filename, m):
    f = os.path.join(directory, filename)
    if os.path.isfile(f) and f.find(".pdf") > 0:
        try:
            m = m + 1
            filename = f.replace(".\\", "")
            images = convert_from_path(f, dpi=100, fmt="ppm", thread_count=4)
            images[0].save("CartaoConvertidoParaLeitura.tiff", "tiff")
            image = cv2.imread("CartaoConvertidoParaLeitura.tiff")
        except:
            MoverArquivo(f,f.replace(os.path.basename(f), ""), "PDFInvalido\\")
            print("Erro na conversão do arquivo: {file}".format(file = filename))
            return "", f, m
        return image, f, m


def LerArquivosPDF(directory):
    n = 0
    m = 0
    for filename in os.listdir(directory):
        image, f, m = ConverterImagem(directory, filename, m)
        try:
            if(image != "") :
                decoded, pastaOrigem = DecodificarQrCode(f, image)
                for barcode in decoded:
                    n = LerQrCode(barcode, pastaOrigem, n, f)
                    print("Nro QrCode lidos: " + str(n) + " / " + str(m))
                    # clear()
        except Exception as e:
            print("Erro no processamento do QR Code: " + str(e))
            try:
                MoverArquivo(f, pastaOrigem, "QrCodeNaoLido\\")
            except:
                print("Arquivo não encontrado : " +
                      str(os.path.basename(f)) + "\n")
            continue

    return "Nro QrCode lidos: " + str(n) + " / " + str(m)


def exec():
    directory = 'cartoesPDF'
    LerArquivosPDF(directory)
    return


def main():
    fi = open("QrCodesRead.txt", "w")
    fi.write("")
    fi.close()
    loop = True
    while loop:
        """
        try:
            opcao = input(
                "O que deseja fazer?\r\n[1] => Executar\r\n[2] => Executar sem apagar o log\r\n[3] => Encerrar\r\n")

            match opcao:
                case "1":
                    fi = open("QrCodesRead.txt", "w")
                    fi.write("")
                    fi.close()
                    exec()
                case "2":
                    exec()
                case "3":
                    loop = False
                case _:
                    raise Exception

        except:
            print("Opção Inválida!\r\n")
            continue
    """
       # fi = open("QrCodesRead.txt", "w")
       # fi.write("")
       # fi.close()
        exec()


main()
