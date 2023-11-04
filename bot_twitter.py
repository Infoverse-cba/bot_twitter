import psycopg2
import pandas as pd
import argparse
import time
import logging

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from datetime import datetime


class bot_twitter():
    def __init__(self, cred_usuario, cred_login, cred_senha):
        self.cred_usuario = cred_usuario
        self.cred_login = cred_login
        self.cred_senha = cred_senha

        options = webdriver.FirefoxOptions()
        options.add_argument("-headless")

        self.driver = webdriver.Firefox(options=options)
        # self.driver = webdriver.Firefox()
        self.actions = ActionChains(self.driver)

        sleep(3)

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

    def login(self):
        print('fazendo login no twitter')
        # self.cred_login = 'rogerio@rbbtrade.com'
        # self.cred_usuario = 'RBB1975249'

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
        print('pesquisando palavra chave')
        sleep(2)
        self.search_keyword = keyword
        self.driver.get('https://twitter.com/search?q='+ self.search_keyword +'&src=typed_query')

    def get_post_links(self, n_posts=20):
        """
        Informações importantes para o desenvolvimento do código:
        class do usuario do post, tempo de publicação ou anuncio: x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x4zkp8e x676frb x1nxh6w3 x1sibtaa xo1l8bm xi81zsa x1yc453h
        """
        print('Obtendo links dos posts...')
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

                else:
                    n_scroll += 1
                    
            self.driver.execute_script("window.scrollBy(0,1150)")

            if len(self.post_links) >= n_posts or n_scroll > 150:
                break

            else:
                elements = self.driver.execute_script(script)

    def get_information(self):
        print('Obtendo informações dos posts...')
        data_temp = list()
        data = list()

        text_xpath = '/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/section/div/div/div[1]/div/div/article/div/div/div[3]/div[1]/div/div[1]/span'
        usuario_xpath = '/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/section/div/div/div[1]/div/div/article/div/div/div[2]/div[2]/div/div/div[1]/div/div/div[2]/div/div/a/div/span'

        for i,link in enumerate(self.post_links):
            data_temp = list()
            try:
                self.driver.get(link)
                sleep(2)

                data_temp.append(self.driver.find_element(by=By.XPATH, value=usuario_xpath).text)

                try:
                    data_temp.append(self.driver.find_element(by=By.XPATH, value=text_xpath).text)

                except:
                    data_temp.append('')

                data_temp.append("https://twitter.com/" + data_temp[0][1:])
                data_temp.append(link)

                self.driver.get_screenshot_as_file("imgs/"+str(i)+".png")
                image = self.driver.get_screenshot_as_png()
                data_temp.append(image)

                data.append(data_temp)
                i += 1


            except Exception as e:
                print('erro na hora de extrair informações')
                print(e)

        try:
            data_hora_atual = datetime.now()
            data_hora = data_hora_atual.strftime('%m/%d/%Y %H:%M:%S')

            self.dataframe = pd.DataFrame(data, columns=['usuario', 'data_publication', 'usuario_link', 'publication_link', 'bytea'])
            self.dataframe['publication_id'] = [item[-2].split('/')[-1] for item in data]
            self.dataframe['search_keyword'] = [self.search_keyword] * len(data)
            self.dataframe['date_search'] = [data_hora] * len(data)

        except Exception as e:
            print('erro na hora de criar o dataframe')
            print(e)

        self.driver.quit()

    def get_data(self):
        return self.dataframe

def execute_sql(sql, data = None, fetch=False):
    try:
        con = conecta_db()
        cursor = con.cursor()

        if fetch:
            cursor.execute(sql)
            rows = cursor.fetchall()
            con.commit()
            cursor.close()
            con.close()

            return rows
        
        cursor.execute(sql, data)
        con.commit()

        cursor.close()
        con.close()

    except (Exception, psycopg2.DatabaseError) as error:
                    print("Error: %s" % error)
                    con.rollback()
                    cursor.close()
                    con.close()
                    raise(error)

def remover_letra(string, letra_retirar):
    nova_string = ""
    
    for letra in string:
        if letra != letra_retirar:
            nova_string += letra

    return nova_string

def conecta_db():
    con = psycopg2.connect(host='db.infoverse.com.br', 
                            database='infoverse',
                            user='infoverse', 
                            password='fMCTSepyEXpH')
    return con
    
def retorna_pesquisa_avulsa():
    con = conecta_db()
    cursor = con.cursor()

    sql = """SELECT id, id_usuario, id_credencial, date_search, status, search_keyword, filtro
            FROM pesquisa_avulsa_twitter
            WHERE status IS NULL OR status = False;"""
    
    cursor.execute(sql)
    rows = cursor.fetchall()

    cursor.close()
    con.close()

    return rows

def set_status_pesquisa_avulsa(id):
    sql = """UPDATE pesquisa_avulsa_twitter
            SET status=true
            WHERE id ="""+ str(id) +""";"""
    
    execute_sql(sql)

def retorna_credencial(credencial_id):
    sql = """SELECT id, descricao, usuario, senha, arroba
    FROM bot_credencial_twitter WHERE id ="""+ str(credencial_id) +""";"""

    row = execute_sql(sql, fetch=True)

    return row

def verificando_busca_avulsa():
    rows = retorna_pesquisa_avulsa()

    for row in rows:
        id, id_usuario, id_credencial, date_search, status, search_keyword, filtro = row

        row2 = retorna_credencial(id_credencial)
        _, _, cred_login, cred_senha, cred_usuario = row2[0]

        executando_busca(id, id_usuario, id_credencial, date_search, status, search_keyword, filtro, cred_usuario, cred_login, cred_senha)

        set_status_pesquisa_avulsa(id)

def executando_busca(id, id_usuario, id_credencial, date_search, status, keyword, filtro, cred_usuario, cred_login, cred_senha):
    print('executando busca...')
    bot = bot_twitter(cred_login, cred_usuario, cred_senha)
    bot.login()

    sleep(5)

    bot.search_keyword(keyword)
    bot.get_post_links()
    bot.get_information()

    inserir_db(bot.get_data(), id)
        
def inserir_db(data, id_pesquisa_avulsa):
    print('Inserindo no banco de dados')

    for i,link in enumerate(data['publication_link']):
        try:
            publication_id = link
            publication_id = remover_letra(publication_id, '/')
            publication_id = remover_letra(publication_id, ':')
            publication_id = remover_letra(publication_id, '?')
            publication_id = remover_letra(publication_id, ',')
            publication_id = remover_letra(publication_id, '.')
            publication_id = remover_letra(publication_id, '=')
            publication_id = remover_letra(publication_id, '[')
            publication_id = remover_letra(publication_id, ']')
            publication_id = remover_letra(publication_id, '_')
            publication_id = remover_letra(publication_id, '-')
            publication_id = remover_letra(publication_id, '%')
            publication_id = remover_letra(publication_id, '#')
            publication_id = remover_letra(publication_id, '&')
            publication_id = remover_letra(publication_id, '!')
            publication_id = remover_letra(publication_id, '(')
            publication_id = remover_letra(publication_id, ')')

            replace_str = lambda frase: frase.replace("'", "''")
            data['data_publication'][i] = replace_str(data['data_publication'][i])

            sql = """
            INSERT into pesquisa_bot_twitter (publication_id, usuario, usuario_link, data_publication, publication_link, search_keyword, date_search, id_pesquisa_avulsa) 
            values('%s','%s', '%s', '%s', '%s', '%s', '%s', '%s' );
            """ % (publication_id, data['usuario'][i], data['usuario_link'][i], data['data_publication'][i], data['publication_link'][i], data['search_keyword'][i], data['date_search'][i], id_pesquisa_avulsa)

            linhas = execute_sql("""SELECT publication_id FROM pesquisa_bot_twitter WHERE publication_id = '"""+ str(publication_id) +"""';""", fetch=True)

            # Conte o número de linhas retornadas
            numero_de_linhas = len(linhas)

            if numero_de_linhas == 0:
                
                execute_sql(sql)

                with open('imgs/'+str(i+1)+'.png', 'rb') as file:
                    imagem_bytes = file.read()

                data_img = (publication_id, psycopg2.Binary(imagem_bytes))

                sql2 = """
                        INSERT INTO pesquisa_screenshot_twitter (publication_id, bytea) 
                        VALUES (%s, %s);
                        """

                execute_sql(sql2, data = data_img)
                
        except Exception as e:
            print('Erro na insersão de dados')
            raise(e)
        
    print('Dados inseridos com sucesso!!')

   

if __name__ == '__main__':
    global precessando 
    processando = False
    print('Verificando busca avulsa')
    
    while True:
        time.sleep(10)
        verificando_busca_avulsa()



    

