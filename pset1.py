# IDENTIFICAÇÃO DO ESTUDANTE:
# Preencha seus dados e leia a declaração de honestidade abaixo. NÃO APAGUE
# nenhuma linha deste comentário de seu código!
#
#    Nome completo: vinicius teixeira melo
#    Matrícula: 202200059
#    Turma: cc3M
#    Email: viniciust.melo@hotmail.com
#
# DECLARAÇÃO DE HONESTIDADE ACADÊMICA:
# Eu afirmo que o código abaixo foi de minha autoria. Também afirmo que não
# pratiquei nenhuma forma de "cola" ou "plágio" na elaboração do programa,
# e que não violei nenhuma das normas de integridade acadêmica da disciplina.
# Estou ciente de que todo código enviado será verificado automaticamente
# contra plágio e que caso eu tenha praticado qualquer atividade proibida
# conforme as normas da disciplina, estou sujeito à penalidades conforme
# definidas pelo professor da disciplina e/ou instituição.
#


# Imports permitidos (não utilize nenhum outro import!):
import sys
import math
import base64
import tkinter
from io import BytesIO
from PIL import Image as PILImage


# Classe Imagem:
class Imagem:
    def __init__(self, largura, altura, pixels):
        self.largura = largura
        self.altura = altura
        self.pixels = pixels

    def get_pixel(self, x, y):
        # Retorna o valor do pixel nas coordenadas (x, y)
        ## return self.pixels[x, y] este codgio esta errado pois ele tentando usar uma tupla como indice,
        #no lugar de dois indexes 
        #print(f"{x}")
        #print(f"{y}")
        #return self.pixels(x, y) 
        x = min(max(0, x), self.largura - 1)
        #define o valor minimo entre (max, e largura-1)
        #deine max(0,x) o maior valor entre 0 e x 
        y = min(max(0, y), self.altura - 1) 
        return self.pixels[x + y * self.largura]
 

    def set_pixel(self, x, y, c):
        # Define o valor do pixel nas coordenadas (x, y) como c
        self.pixels[(x + y * self.largura)] = c # aqui eu tive que corrigir com o kernel para chegar correto

    def aplicar_por_pixel(self, func):
        # Aplica uma função a cada pixel da imagem e retorna uma nova imagem com os resultados
        resultado = Imagem.nova( self.largura, self.altura) #aqui largura e altura estavam trocados tambem, corrigi e agora a imagem nao vem mais borrada em baixo
        for x in range(resultado.largura):
            for y in range(resultado.altura):      
                cor = self.get_pixel(x, y)
                nova_cor = func(cor)
                resultado.set_pixel( x, y, nova_cor) #aqui y e x estavam trocados, mudei para x e y, e agora a imagem parece em pe
        return resultado


    
    def invertida(self):
        return self.aplicar_por_pixel(lambda c: 255 - c)

    def borrada(self, n):
         # Retorna uma nova imagem borrada aplicando um filtro de borramento com um tamanho n
        kernel = gerador_kernel_blur(n)
        resultado = self.correlacao(kernel)
        resultado.corrigir()
        return resultado

    def focada(self, n):
         # Retorna uma nova imagem com o efeito de foco, utilizando a imagem original e uma imagem borrada
        resultado = Imagem.nova(self.largura,self.altura)
        borrada = self.borrada(n)
        for x in range(resultado.largura):
            for y in range(resultado.altura):
                imagem_original = self.get_pixel(x, y)
                imagem_borrada = borrada.get_pixel(x, y)
                nova_cor = round(2 * imagem_original - imagem_borrada)    # S(x,y) = round(2I(x,y) − B(x,y))
                resultado.set_pixel(x, y, nova_cor)
        resultado.corrigir() 
        return resultado 

    def bordas(self):
         # Retorna uma nova imagem com o efeito de detecção de bordas
         # Os kernels usados para gerar a imagem com filtro de detecção de bordas
        kernel_lateral =  [[-1, 0, 1],
                           [-2, 0, 2],
                           [-1, 0, 1]]
        kernel_vertical = [[-1, -2, -1],
                           [ 0,  0,  0],
                           [ 1,  2,  1]]
        imgborda_lateral = self.correlacao(kernel_lateral) # salva a imagem com as bordas horizontais(Kx)
        imgborda_vertical = self.correlacao(kernel_vertical) # salva a imagem com as bordas verticais(Ky)
        resultado = Imagem.nova(self.largura, self.altura) # cria nova imagem com dimensões iguais as da original
        for x in range(self.largura):
            for y in range(self.altura):
                valor_quadrado_lateral = imgborda_lateral.get_pixel(x, y)**2
                valor_quadrado_vertical = imgborda_vertical.get_pixel(x, y)**2
                nova_cor = round(math.sqrt(valor_quadrado_lateral + valor_quadrado_vertical)) # Calcula nova cor dos pixels com base na formula dada no pset
                resultado.set_pixel(x, y, nova_cor)
        resultado.corrigir() 
        return resultado

    def correlacao(self, kernel):
        tamanho_kernel = len(kernel)
        raio = tamanho_kernel//2
        resultado = Imagem.nova(self.largura, self. altura)
        for x in range(self.largura):
            for y in range(self.altura):
                nova_cor = 0
                for i in range(tamanho_kernel):
                    for j in range(tamanho_kernel):
                        cor_mutavel = self.get_pixel((x-raio+i),(y-raio+j))
                        nova_cor += cor_mutavel * (kernel[i][j]) 
                        # a get_pixel((x-raio+i)(y-raio+j)) solicita dois parametros x e y, 
                        # para identificar o local, pixel, que o kernel se refere 
                        # ele entao pega 
                resultado.set_pixel(x,y, nova_cor)
        return resultado

    def corrigir(self):
        for x in range(self.largura):
            for y in range(self.altura):
                cor_corrigida = self.get_pixel(x,y)
                cor_corrigida = max(min(255, cor_corrigida), 0)
                cor_corrigida = int(round(cor_corrigida))
                self.set_pixel(x, y, cor_corrigida)

    # Abaixo deste ponto estão utilitários para carregar, salvar e mostrar
    # as imagens, bem como para a realização de testes.

    def __eq__(self, other):
        return all(getattr(self, i) == getattr(other, i)
                   for i in ('altura', 'largura', 'pixels'))

    def __repr__(self):
        return "Imagem(%s, %s, %s)" % (self.largura, self.altura, self.pixels)

    @classmethod
    def carregar(cls, nome_arquivo):
        """
        Carrega uma imagem do arquivo fornecido e retorna uma instância dessa
        classe representando essa imagem. Também realiza a conversão para tons
        de cinza.

        Invocado como, por exemplo:
           i = Imagem.carregar('test_images/cat.png')
        """
        with open(nome_arquivo, 'rb') as guia_para_imagem:
            img = PILImage.open(guia_para_imagem)
            img_data = img.getdata()
            if img.mode.startswith('RGB'):
                pixels = [round(.299 * p[0] + .587 * p[1] + .114 * p[2]) for p in img_data]
            elif img.mode == 'LA':
                pixels = [p[0] for p in img_data]
            elif img.mode == 'L':
                pixels = list(img_data)
            else:
                raise ValueError('Modo de imagem não suportado: %r' % img.mode)
            l, a = img.size
            return cls(l, a, pixels)

    @classmethod
    def nova(cls, largura, altura):
        """
        Cria imagens em branco (tudo 0) com a altura e largura fornecidas.

        Invocado como, por exemplo:
            i = Imagem.nova(640, 480)
        """
        return cls(largura, altura, [0 for i in range(largura * altura)])

    def salvar(self, nome_arquivo, modo='PNG'):
        """
        Salva a imagem fornecida no disco ou em um objeto semelhante a um arquivo.
        Se o nome_arquivo for fornecido como uma string, o tipo de arquivo será
        inferido a partir do nome fornecido. Se nome_arquivo for fornecido como
        um objeto semelhante a um arquivo, o tipo de arquivo será determinado
        pelo parâmetro 'modo'.
        """
        saida = PILImage.new(mode='L', size=(self.largura, self.altura))
        saida.putdata(self.pixels)
        if isinstance(nome_arquivo, str):
            saida.save(nome_arquivo)
        else:
            saida.save(nome_arquivo, modo)
        saida.close()

    def gif_data(self):
        """
        Retorna uma string codificada em base 64, contendo a imagem
        fornecida, como uma imagem GIF.

        Função utilitária para tornar show_image um pouco mais limpo.
        """
        buffer = BytesIO()
        self.salvar(buffer, modo='GIF')
        return base64.b64encode(buffer.getvalue())

    def mostrar(self):
        """
        Mostra uma imagem em uma nova janela Tk.
        """
        global WINDOWS_OPENED
        if tk_root is None:
            # Se Tk não foi inicializado corretamente, não faz mais nada.
            return
        WINDOWS_OPENED = True
        toplevel = tkinter.Toplevel()
        # O highlightthickness=0 é um hack para evitar que o redimensionamento da janela
        # dispare outro evento de redimensionamento (causando um loop infinito de
        # redimensionamento). Para maiores informações, ver:
        # https://stackoverflow.com/questions/22838255/tkinter-canvas-resizing-automatically
        tela = tkinter.Canvas(toplevel, height=self.altura,
                              width=self.largura, highlightthickness=0)
        tela.pack()
        tela.img = tkinter.PhotoImage(data=self.gif_data())
        tela.create_image(0, 0, image=tela.img, anchor=tkinter.NW)

        def ao_redimensionar(event):
            # Lida com o redimensionamento da imagem quando a tela é redimensionada.
            # O procedimento é:
            #  * converter para uma imagem PIL
            #  * redimensionar aquela imagem
            #  * obter os dados GIF codificados em base 64 (base64-encoded GIF data)
            #    a partir da imagem redimensionada
            #  * colocar isso em um label tkinter
            #  * mostrar a imagem na tela
            nova_imagem = PILImage.new(mode='L', size=(self.largura, self.altura))
            nova_imagem.putdata(self.pixels)
            nova_imagem = nova_imagem.resize((event.largura, event.altura), PILImage.NEAREST)
            buffer = BytesIO()
            nova_imagem.save(buffer, 'GIF')
            tela.img = tkinter.PhotoImage(data=base64.b64encode(buffer.getvalue()))
            tela.configure(height=event.altura, width=event.largura)
            tela.create_image(0, 0, image=tela.img, anchor=tkinter.NW)

        # Por fim, faz o bind da função para que ela seja chamada quando a tela
        # for redimensionada:
        tela.bind('<Configure>', ao_redimensionar)
        toplevel.bind('<Configure>', lambda e: tela.configure(height=e.altura, width=e.largura))

        # Quando a tela é fechada, o programa deve parar
        toplevel.protocol('WM_DELETE_WINDOW', tk_root.destroy)

def gerador_kernel_blur(tamanho_desejado):
        # Inicializa uma lista vazia para armazenar o kernel de desfoque
        kernel_blur = []
        # Itera sobre o tamanho desejado para criar as linhas do kernel
        for _ in range(tamanho_desejado):
            linha = []
            # Itera sobre o tamanho desejado para criar os elementos de cada linha
            for _ in range(tamanho_desejado):
                # Calcula o valor de cada elemento como 1 dividido pelo quadrado do tamanho desejado
                elemento = 1 / (tamanho_desejado ** 2)
                linha.append(elemento)            
            # Adiciona a linha completa ao kernel de desfoque
            kernel_blur.append(linha)        
        # Retorna o kernel de desfoque completo
        return kernel_blur
    #gerador_kernel_blur(3)
    #kernel_blur =  [[0.1111111111111111, 0.1111111111111111, 0.1111111111111111], 
    #               [0.1111111111111111, 0.1111111111111111, 0.1111111111111111],  
    #               [0.1111111111111111, 0.1111111111111111, 0.1111111111111111]]

# Não altere o comentário abaixo:
# noinspection PyBroadException
try:
    tk_root = tkinter.Tk()
    tk_root.withdraw()
    tcl = tkinter.Tcl()


    def refaz_apos():
        tcl.after(500, refaz_apos)


    tcl.after(500, refaz_apos)
except:
    tk_root = None

WINDOWS_OPENED = False

if __name__ == '__main__':
    # O código neste bloco só será executado quando você executar
    # explicitamente seu script e não quando os testes estiverem
    # sendo executados. Este é um bom lugar para gerar imagens, etc.
    pass

    # O código a seguir fará com que as janelas de Imagem.mostrar
#-----------------------------------------------------------
        # Criando uma instância da classe Imagem
     ## imagem =Imagem.carregar(r'C:\Users\vinic\OneDrive\Área de Trabalho\pset1\pset1\test_images\birdpig.png')
       
        # Chamando o método mostrar() na instância da classe Imagem
     ##imagem.mostrar()
#---------------------------------------------------------

    # Definindo a imagem de 4x1 pixels
    #altura = 1
    #largura = 4
    #pixels = [29, 89, 136, 200]
    
    kernel_Q4 = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [1, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0]]

    # Criando uma instância da classe Imagem
    #imagem = Imagem(largura, altura, pixels)
    imagem = Imagem.carregar('test_images\construct.png')

    # Exibindo a imagem original
    #print("Imagem original:")
    imagem_correlacao = imagem.bordas()
    imagem_correlacao.mostrar()
    imagem_correlacao.salvar('test_images\constructQ6.png')
    #imagem.mostrar()


    #teste borrada
    #imagem_borrada = imagem.borrada(10)
    #imagem_borrada.mostrar()

    #teste invertida
        #imagem = Imagem.carregar('test_images/pigbird.png')
    #imagem_invertida = imagem.invertida()
    #imagem_invertida.mostrar()
    #imagem_invertida.salvar('test_images/bluegill_invertido.png')

    # Teste imprindo o kernel_blur 
    #print(Imagem.gerador_kernel_blur(5))

    # Chamando o método salvar() na instância da classe Imagem
    ##imagem.salvar()
    

    # sejam exibidas corretamente, quer estejamos executando
    # interativamente ou não:
    if WINDOWS_OPENED and not sys.flags.interactive:
        tk_root.mainloop()
