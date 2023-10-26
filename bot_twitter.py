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
from datetime import datetime, timedelta


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
    con = conecta_db()
    cursor = con.cursor()

    sql3 = """UPDATE pesquisa_avulsa_twitter
            SET status=true
            WHERE id ="""+ str(id) +""";"""
    
    cursor.execute(sql3)
    con.commit()

    cursor.close()
    con.close()

def set_status_rotina(id):
    con = conecta_db()
    cursor = con.cursor()

    sql3 = """UPDATE bot_rotina_twitter_agendado
            SET status=true
            WHERE id ="""+ str(id) +""";"""
    
    
    cursor.execute(sql3)
    con.commit()

    cursor.close()
    con.close()

def retorna_credencial(credencial_id):
    con = conecta_db()
    cursor = con.cursor()

    sql3 = """SELECT id, descricao, usuario, senha, arroba
    FROM bot_credencial_twitter WHERE id ="""+ str(credencial_id) +""";"""

    cursor.execute(sql3)
    row3 = cursor.fetchall()

    cursor = cursor.close()
    con = con.close()

    return row3

def retorna_rotina(id):
    con = conecta_db()
    cursor = con.cursor()

    sql2 = """SELECT id, credencial_id, search_keyword
            FROM bot_rotina_twitter WHERE id ="""+ str(id) +""";"""
    
    
    cursor.execute(sql2)
    row2 = cursor.fetchall()

    cursor.close()
    con.close()

    return row2

def rotinas_agendadas():
    con = conecta_db()
    cursor = con.cursor()

    sql = """ SELECT id, id_rotina_twitter, dt_agendamento, dt_executado, dt_cancelado, status, id_usuario_agendamento, id_usuario_executado, id_usuario_cancelamento, forcar_execucao
              FROM bot_rotina_twitter_agendado 
              WHERE status IS NULL OR status = False;;"""

    cursor.execute(sql)
    rows = cursor.fetchall()

    cursor.close()
    con.close()

    return rows

def verificando_rotina():
    print('verificando rotina')
    
    rows = rotinas_agendadas()


    for row in rows:
        
        id_agendado, id_rotina_twitter, dt_agendamento, dt_executado, dt_cancelado, status, id_usuario_agendamento, id_usuario_executado, id_usuario_cancelamento, forcar_execucao = row

        dt_agendamento = datetime.strptime(str(dt_agendamento), '%Y-%m-%d %H:%M:%S')

        # Obtenha a hora atual
        hora_atual = datetime.now()

        # Calcule a diferença de tempo entre a hora atual e a hora de agendamento
        diferenca_tempo = hora_atual - dt_agendamento

        # Verifique se a diferença de tempo está dentro de 10 minutos
        if timedelta(minutes=-10) <= diferenca_tempo <= timedelta(minutes=0):
            print('Executando rotina')
            pass
        else:
            break

        row2 = retorna_rotina(id_rotina_twitter)

        id, credencial_id, search_keyword = row2[0]

        row3 = retorna_credencial(credencial_id)

        _, _, cred_usuario, cred_senha, arroba = row3[0]

        
        try:
            main(cred_usuario, cred_senha, 14, search_keyword, arroba)
        except Exception as e:
            print('erro na execução: ', e)
            main(cred_usuario, cred_senha, 14, search_keyword, arroba)

        set_status_rotina(id_agendado)

def verificando_busca_avulsa():
    print('verificando busca avulsa')
    rows = retorna_pesquisa_avulsa()

    for row in rows:
        print('executando busca avulsa')
        id, id_usuario, id_credencial, date_search, status, search_keyword, filtro = row

        row2 = retorna_credencial(id_credencial)

        _, _, cred_usuario, cred_senha, arroba = row2[0]

        try:
            main(cred_usuario, cred_senha, 5, search_keyword, arroba, id)
        except:
            main(cred_usuario, cred_senha, 5, search_keyword, arroba, id)

        set_status_pesquisa_avulsa(id)

def inserir_db(sql, publication_id,i):
    con = conecta_db()
    cursor = con.cursor()

    cursor.execute("""SELECT publication_id FROM pesquisa_bot_twitter WHERE publication_id = '"""+ str(publication_id) +"""';""")
    linhas = cursor.fetchall()

    cursor.close()
    con.close()
    
    # Conte o número de linhas retornadas
    numero_de_linhas = len(linhas)
    print(numero_de_linhas)

    if numero_de_linhas == 0:
        try:
            con = conecta_db()
            cursor = con.cursor()

            cursor.execute(sql)
            con.commit()

            cursor.close()
            con.close()

            print('i', i)
            with open('imgs/'+str(i)+'.png', 'rb') as file:
                print('caminho: ', 'imgs/'+str(i)+'.png')
                
                imagem_bytes = file.read()

            # data_bin = (psycopg2.Binary(imagem_bytes),)

            data = (publication_id, psycopg2.Binary(imagem_bytes))


            # inserir tabela pesquisa_screenshot_twitter
            # sql2 = """
            # INSERT into pesquisa_screenshot_twitter (publication_id, bytea) 
            # values('%s', '%s');
            # """ % (publication_id, data_bin)

            sql2 = """
                    INSERT INTO pesquisa_screenshot_twitter (publication_id, bytea) 
                    VALUES (%s, %s);
                    """
            print('data_bin: ',data)

            con = conecta_db()
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

def conecta_db():
  con = psycopg2.connect(host='dev.danillodars.com.br', 
                         database='infoverse',
                         user='infoverse', 
                         password=')IU+#8Jf{TM8ec5L{94a[6Z@}rk0R7P$')
  return con

def checking_clickable(i, browser):

    try:
        WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/section/div/div/div["+ str(i) +"]/div/div/article/div/div/div[1]/div/div")))
        print(f'O objeto com i: {i} é clicável!!')
        return i
    except:
        if i == 1:
            print('People identificado!!')
            while True:
                i += 1
                try:
                    WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/section/div/div/div["+ str(i) +"]/div/div/article/div/div/div[1]/div/div")))
                    print('Valor de i no primeiro post: ', i)
                    return i
                except:
                    pass
        
        else:
            print('scroll no i: ',i)
            # i = 1
            sleep(2)
            browser.execute_script("window.scrollBy(0,1000)")
            print('verificando se o people foi carregado')
            i = checking_clickable(i, browser)
            print('valor de i após verificação: ', i)

            return i
            
def get_information(data, browser, first = False):
    print('entrou no get_information')
    text_xpath = '/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/section/div/div/div[1]/div/div/article/div/div/div[3]/div[1]/div/div[1]/span'
    usuario_xpath = '/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/section/div/div/div[1]/div/div/article/div/div/div[2]/div[2]/div/div/div[1]/div/div/div[2]/div/div/a/div/span'
    sleep(4)
    data_temp = list()
    
    data_temp.append(browser.find_element(by=By.XPATH, value=usuario_xpath).text)
    try:
        data_temp.append(browser.find_element(by=By.XPATH, value=text_xpath).text)
    except:
        data_temp.append('')
    data_temp.append("https://twitter.com/" + data_temp[0][1:])
    data_temp.append(browser.current_url)

    
    if first:
        print(f'novo conteudo do usuario {data_temp[1]} adicionado!')
        browser.get_screenshot_as_file("imgs/"+str(len(data))+".png")
        image = browser.get_screenshot_as_png()
        data_temp.append(image)
        data.append(data_temp)
        print('tamanho do vetor: ', len(data))

        return data


    else:
        aux = [x[0] for x in data]
        print(data_temp[0])
        print(aux)

        
        print(f'novo conteudo do usuario {data_temp[1]} adicionado!')
        browser.get_screenshot_as_file("imgs/"+str(len(data))+".png")
        image = browser.get_screenshot_as_png()
        data_temp.append(image)
        data.append(data_temp)
        print('tamanho do vetor: ', len(data))

        return data
            
def create_webdriver(url):
    browser = webdriver.Firefox()
    browser.get(url)

    return browser

def acessando_twitter(browser, cred_usuario, cred_senha, arroba):
    browser.maximize_window()
    sleep(3)
    browser.find_element(by=By.XPATH, value='/html/body/div/div/div/div[2]/main/div/div/div[1]/div[1]/div/div[3]/div[5]/a/div/span/span').click()
    WebDriverWait(browser, 15).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div[2]/div/input"))).click()
    browser.find_element(by=By.XPATH, value='/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div[2]/div/input').send_keys(cred_usuario)
    browser.find_element(by=By.XPATH, value='/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]/div/span/span').click()
    sleep(3)
    try:
        browser.find_element(by=By.XPATH, value='/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/label/div/div[2]/div/input').send_keys(arroba)
        sleep(3)
        browser.find_element(by=By.XPATH, value='/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/div/div/span/span').click()
        sleep(3)
        browser.find_element(by=By.XPATH, value='/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input').send_keys(cred_senha)
        sleep(3)
        browser.find_element(by=By.XPATH, value='/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div/div/span/span').click()
    except:
        sleep(3)
        browser.find_element(by=By.XPATH, value='/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input').send_keys(cred_senha)
        sleep(3)
        browser.find_element(by=By.XPATH, value='/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div/div/span/span').click()

def pesquisando(browser, key_word):
    sleep(6)
    browser.find_element(by=By.XPATH, value='/html/body/div[1]/div/div/div[2]/main/div/div/div/div[2]/div/div[2]/div/div/div/div[1]/div/div/div/form/div[1]/div/div/div/label/div[2]/div/input').click()
    browser.find_element(by=By.XPATH, value='/html/body/div[1]/div/div/div[2]/main/div/div/div/div[2]/div/div[2]/div/div/div/div[1]/div/div/div/form/div[1]/div/div/div/label/div[2]/div/input').send_keys(key_word)
    browser.find_element(by=By.XPATH, value='/html/body/div[1]/div/div/div[2]/main/div/div/div/div[2]/div/div[2]/div/div/div/div[1]/div/div/div/form/div[1]/div/div/div/label/div[2]/div/input').send_keys(Keys.ENTER)

def extraindo_dados(browser, n = 10):
    sleep(5)
    data = list()
    back_button_xpath = "/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[1]/div[1]/div/div/div/div/div/div[1]/div/div"
    i = 1
    first = True
    aux = 0
    
    while True:
        sair = True
        xpath ="/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/section/div/div/div["+ str(i) +"]/div/div/article/div/div/div[1]/div/div"

        try:
            sleep(1)
            
            WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, xpath))).click()
            print('clicou')

            if first:
                    data = get_information(data, browser, True)
                    first = False

            else:
                try:
                    data_temp = get_information(data, browser)
                    if data_temp == None:
                        if 'status' in browser.current_url:
                            WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.XPATH, back_button_xpath))).click()
                        sleep(2)
                        browser.execute_script("window.scrollBy(0,950)")
                        print('voltou para a tela de pesquisa')
                        sair = False
                    else:
                        data = data_temp
                
                except:
                    pass
            
            if sair:
                sleep(2)
                if 'status' in browser.current_url:
                    WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.XPATH, back_button_xpath))).click()
                print('voltou para a tela de pesquisa')

        except Exception as e:
            if i == 1:
                print('people identificado!')
                while True:
                    print(i)
                    i += 1
                    xpath = "/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/section/div/div/div["+ str(i) +"]/div/div/article/div/div/div[1]/div/div"
                    try:
                        if i == 12: 
                            print('i igual a 12')
                            i = 1
                            xpath = "/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/section/div/div/div["+ str(i) +"]/div/div/article/div/div/div[1]/div/div"
                            try:
                                if 'status' in browser.current_url:
                                    WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.XPATH, back_button_xpath))).click()
                            except:
                                pass
                            browser.execute_script("window.scrollBy(0,950)")
                        print('xpath clicavel')
                        WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.XPATH, xpath)))
                        print('Valor de i no primeiro post: ', i)
                        WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH, xpath))).click()
                        print('clicou')

                        if first: 
                            data = get_information(data, browser, True)
                            first = False

                        else:
                            print('entrou no else')
                            try:
                                data_temp = get_information(data, browser)
                            except Exception as e:
                                print(e)

                            if data_temp == None:
                                if 'status' in browser.current_url:
                                    WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.XPATH, back_button_xpath))).click()
                                sleep(2)
                                browser.execute_script("window.scrollBy(0,950)")
                                print('voltou para a tela de pesquisa')
                                sair = False
                                aux = 0
                            else:
                                data = data_temp
                            print('saiu do else')

                        if 'status' in browser.current_url:
                            WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH, back_button_xpath))).click()
                        print('voltou para a tela de pesquisa')
                        print('i que deu certo: ', i, end='\n\n')
                        break

                    except:
                        pass
            else:
                try:
                    browser.execute_script("window.scrollBy(0,950)")
                    aux += 1
                    if aux > 11:
                        if 'status' in browser.current_url:
                            WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH, back_button_xpath))).click()
                        aux = 0

                except:
                    browser.execute_script("window.scrollBy(0,950)")

                print('i que deu errado:', i, end='\n\n')

        if i == 11:
            i = 1
            browser.execute_script("window.scrollBy(0,950)")
        
        else:
            i += 1

        if len(data) >= n:
            print('acabou')
            break

    return data

def main(cred_usuario, cred_senha, n_posts, key_word, arroba, id_pesquisa_avulsa = 0):
    data_hora_atual = datetime.now()

    # options = webdriver.FirefoxOptions()
    # options.add_argument("-headless")

    browser = webdriver.Firefox()
    # browser = webdriver.Firefox(options=options)
    browser.get("https://twitter.com")

    
    acessando_twitter(browser, cred_usuario, cred_senha, arroba)
    pesquisando(browser, key_word)

    data_hora = data_hora_atual.strftime('%m/%d/%Y %H:%M:%S')

    data_list = extraindo_dados(browser, n = n_posts)

    data = pd.DataFrame(data_list, columns=['usuario', 'data_publication', 'usuario_link', 'publication_link', 'bytea'])
    data['publication_id'] = [item[-2].split('/')[-1] for item in data_list]
    data['search_keyword'] = [key_word]*n_posts
    data['date_search'] = [data_hora]*n_posts
    
    data.to_csv('data.csv')

    for i in data.index: #inserir tabela pesquisa_bot_twitter
        data['data_publication'][i] = data['data_publication'][i].replace("'", "''")
        sql = """
        INSERT into pesquisa_bot_twitter (usuario,data_publication,usuario_link,publication_link,publication_id,search_keyword,date_search,id_pesquisa_avulsa) 
        values('%s','%s','%s','%s','%s','%s','%s','%s');
        """ % (data['usuario'][i], data['data_publication'][i], data['usuario_link'][i], data['publication_link'][i], data['publication_id'][i], data['search_keyword'][i], data['date_search'][i], id_pesquisa_avulsa)

        inserir_db(sql, data['publication_id'][i], i)


if __name__ == "__main__":
    global precessando 
    processando = False
    

    while True:
        
        # Aguarde 60 segundos
        time.sleep(10)

        if not processando:
            try:
                processando = True
                verificando_busca_avulsa()
                verificando_rotina()
                processando = False
            except:
                processando = True
                verificando_busca_avulsa()
                verificando_rotina()
                processando = False


    


    #  python bot.py --keyword "Dilma" --n_posts 2

    # parser = argparse.ArgumentParser(description="bot twitter")

    # parser.add_argument('--keyword', type=str, help='palavra de busca')
    # parser.add_argument('--n_posts', type=int, help='Numero de posts')

    # args = parser.parse_args()

    # key_word = args.keyword
    # posts = args.n_posts


        

        



        



    

