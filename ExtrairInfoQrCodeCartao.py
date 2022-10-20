from cgi import print_form
from dataclasses import replace
from email.policy import default
import os
import shutil
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


def MoverArquivo(f, pastaOrigem, pastaDestino):
    shutil.move(pastaOrigem + os.path.basename(f),
                pastaDestino + os.path.basename(f))


def LerQrCode(barcode, pastaOrigem, n, f):

    data = barcode.data.decode('utf-8')
    if (data != "" and data is not None):
        n = n+1
        fi = open("QrCodesRead.txt", "a")
        fi.write("{data1}\n".format(data1=data))
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
  #  fi = open("QrCodesRead.txt", "w")
  # fi.write("")
 #   fi.close()
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
