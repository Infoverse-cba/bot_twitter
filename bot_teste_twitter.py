import psycopg2
import pandas as pd
import argparse
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from PIL import Image
from datetime import datetime


class bot_twitter():
    def __init__(self):
        self.driver = webdriver.Firefox()
        self.actions = ActionChains(self.driver)


        sleep(3)

    def remover_letra(self, string, letra_retirar):
        nova_string = ""
        for letra in string:
            if letra != letra_retirar:
                nova_string += letra
        return nova_string

    def time_out(void=None, time_out: int = 20, raise_exception: bool = True):


        """Executes a function with a timeout limit.

        :param void: (optional) Default argument, unused.
        :type void: any
        :param time_out: The timeout limit in seconds.
        :type time_out: int
        :param raise_exception: (optional) If True, a TimeoutException will be raised when the timeout is reached.
        :type raise_exception: bool
        :return: Returns the result of the executed function.
        :rtype: any

        Example:
            This decorator can be used to set a timeout limit for a function that takes too long to execute.
            >>>@time_out(time_out=30, raise_exception=True)
            >>>def slow_function():
            >>>    time.sleep(35)
            >>>
            >>>slow_function()
            TimeoutException: Timeout!"""
    

        def wrapper(func):
            def inner_wrapper(*args, **kwargs):
                # print("Time out value: {}".format(time_out))
                contadortime_out = 0
                ret = False
                error = None
                while contadortime_out < time_out:
                    try:
                        ret = func(*args, **kwargs)
                        break
                    except Exception as e:
                        logging.exception(e) # serve para salvar o erro no log
                        error = e
                        time.sleep(1)
                    contadortime_out += 1
                if contadortime_out >= time_out and raise_exception:
                    raise error
                return ret

            return inner_wrapper

        return wrapper

    def login_twitter(self):
        self.cred_senha = 'Master@rbb@'
        self.cred_login = 'rogerio@rbbtrade.com'
        self.cred_usuario = 'RBB1975249'

        self.driver.get('https://twitter.com/i/flow/login')
        self.driver.maximize_window()

        WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div[2]/div/input"))).click()
        sleep(1)
        self.driver.find_element(by=By.XPATH, value='/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div[2]/div/input').send_keys(self.cred_login)
        sleep(2)
        self.driver.find_element(by=By.XPATH, value='/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]/div').click()

        try:
            WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/label/div/div[2]/div/input"))).click()
            sleep(1)
            self.driver.find_element(by=By.XPATH, value='/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/label/div/div[2]/div/input').send_keys(self.cred_usuario)
            sleep(2)
            self.driver.find_element(by=By.XPATH, value='/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/div/div').click()

        except:
            pass

        WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input"))).click()
        sleep(3)
        self.driver.find_element(by=By.XPATH, value='/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input').send_keys(self.cred_senha)
        sleep(2)
        self.driver.find_element(by=By.XPATH, value='/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div/div').click()

        self.driver.implicitly_wait(10)
        sleep(10)

    @time_out(time_out=10, raise_exception=True)
    def search_keyword(self, keyword):
        sleep(2)
        self.search_keyword = keyword
        self.driver.get('https://twitter.com/search?q='+ self.search_keyword +'&src=typed_query')

    def getting_information(self, n_posts=20):
        """
        Informações importantes para o desenvolvimento do código:
        class do usuario do post, tempo de publicação ou anuncio: x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x4zkp8e x676frb x1nxh6w3 x1sibtaa xo1l8bm xi81zsa x1yc453h
        """

        self.post_links = list()
        n_scroll = 0

        script = f""" 
                    var results = document.getElementsByClassName('css-4rbku5 css-18t94o4 css-901oao r-1bwzh9t r-1loqt21 r-xoduu5 r-1q142lx r-1w6e6rj r-37j5jr r-a023e6 r-16dba41 r-9aw3ui r-rjixqe r-bcqeeo r-3s2u2q r-qvutc0')
                    return results
                  """
        
        elements = self.driver.execute_script(script)
    
        while True:
            for element in elements:
                try:
                    href = element.get_attribute('href')
                    
                except:
                    self.driver.execute_script("window.scrollBy(0,1150)")
                    n_scroll += 1
                    sleep(2)
                    continue

                if href not in self.post_links:
                    self.post_links.append(href)
            
            self.driver.execute_script("window.scrollBy(0,1150)")

            if len(self.post_links) >= n_posts or n_scroll > 50:
                break

            else:
                elements = self.driver.execute_script(script)

        for link in self.post_links:
            print(link)
        
    @time_out(time_out=10, raise_exception=False)
    def take_screenshot(self, publication_links):
        for i,link in enumerate(publication_links):
            self.driver.get(link)
            sleep(2)
            self.driver.save_screenshot('imgs/'+str(i)+'.png')

    def conecta_db(self):
        con = psycopg2.connect(host='dev.danillodars.com.br', 
                                database='infoverse',
                                user='infoverse', 
                                password=')IU+#8Jf{TM8ec5L{94a[6Z@}rk0R7P$')
        return con
        
    def retorna_pesquisa_avulsa(self):
        con = self.conecta_db()
        cursor = con.cursor()

        sql = """SELECT id, id_usuario, id_credencial, data_pesquisa, rede_social, status, palavra_chave, filtro, filtro_avancado, ano_referencia, publicacoes_de, localizacao_marcada
                FROM pesquisa_avulsa
                WHERE status IS NULL OR status = False;"""
        
        cursor.execute(sql)
        rows = cursor.fetchall()

        cursor.close()
        con.close()

        return rows
    
    def set_status_pesquisa_avulsa(self, id):
        con = self.conecta_db()
        cursor = con.cursor()

        sql3 = """UPDATE pesquisa_avulsa
                SET status=true
                WHERE id ="""+ str(id) +""";"""
        
        cursor.execute(sql3)
        con.commit()

        cursor.close()
        con.close()

    def retorna_credencial(self, credencial_id):
        con = self.conecta_db()
        cursor = con.cursor()

        sql3 = """SELECT id, descricao, usuario, senha
        FROM bot_credencial_facebook WHERE id ="""+ str(credencial_id) +""";"""

        cursor.execute(sql3)
        row3 = cursor.fetchall()

        cursor = cursor.close()
        con = con.close()

        return row3
    
    def verificando_busca_avulsa(self):
        rows = self.retorna_pesquisa_avulsa()

        for row in rows:
            id, id_usuario, id_credencial, date_search, rede_social, status, keyword, filtro, filtro_avancado, ano_referencia, publicacoes_de, localizacao_marcada = row

            row2 = self.retorna_credencial(id_credencial)
            _, _, cred_usuario, cred_senha = row2[0]

            self.id = id
            self.id_usuario = id_usuario
            self.id_credencial = id_credencial
            self.date_search = date_search
            self.status = status
            self.keyword = keyword
            self.filtro = filtro
            self.cred_usuario = cred_usuario
            self.cred_senha = cred_senha

            if len(row) != 0:
                print('busca encontrada')
                try:
                    self.main()
                except:
                    self.main()

            else:
                print('nenhuma busca encontrada')
                break

            self.set_status_pesquisa_avulsa(id)

    def main(self, keyword):
        bot.login_twitter()
        sleep(5)
        bot.search_keyword(keyword)
        bot.getting_information()
        # bot.take_screenshot()
        # bot.inserir_db()
        
    def inserir_db(self):
        for i,link in enumerate(self.post_links):
            publication_id = self.remover_letra(self.link, '/')
            publication_id = self.remover_letra(self.link, ':')

            sql = """
            INSERT into contigencia (link_publication, publication_id, id_pesquisa_avulsa) 
            values('%s','%s', '%s');
            """ % (link, publication_id, self.id)

            con = self.conecta_db()
            cursor = con.cursor()

            cursor.execute("""SELECT publication_id FROM pesquisa_bot_twitter WHERE publication_id = '"""+ str(publication_id) +"""';""")
            linhas = cursor.fetchall()

            cursor.close()
            con.close()
            
            # Conte o número de linhas retornadas
            numero_de_linhas = len(linhas)

            if numero_de_linhas == 0:
                try:
                    con = self.conecta_db()
                    cursor = con.cursor()

                    cursor.execute(sql)
                    con.commit()

                    cursor.close()
                    con.close()


                    with open('imgs/'+str(i)+'.png', 'rb') as file:
                        print('caminho: ', 'imgs/'+str(i)+'.png')
                        
                        imagem_bytes = file.read()

                    # data_bin = (psycopg2.Binary(imagem_bytes),)

                    data = (publication_id, psycopg2.Binary(imagem_bytes))

                    sql2 = """
                            INSERT INTO pesquisa_screenshot (publication_id, bytea) 
                            VALUES (%s, %s);
                            """
                    print('data_bin: ',data)

                    con = self.conecta_db()
                    cursor = con.cursor()

                    cursor.execute(sql2, data)
                    con.commit()

                    cursor.close()
                    con.close()

                except (Exception, psycopg2.DatabaseError) as error:
                    print("Error: %s" % error)
                    con.rollback()
                    cursor.close()
                    con.close()

                    return 1


if __name__ == '__main__':
    bot = bot_twitter()
    
    bot.main('Hamas')

