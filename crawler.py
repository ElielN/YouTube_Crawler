import re
import requests
import json
from bs4 import BeautifulSoup

#-------------  Define se temos uma URLs ou um query de pesquisa do YouTube  -------------
def url_or_query(url):
    if 'http' in url:
        return "url"
    else:
        return "query"

#-------------  Faz a busca no youtube e retorna a URL do primeiro video  -------------
def change_query_to_url(query):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0'}    #Um agente só pra garantir que não vai barrar a request
    query = 'https://www.youtube.com/results?search_query=' + query                                     #Query de busca no youtube
    content = requests.get(query, headers=headers)
    soup = BeautifulSoup(content.text, 'html.parser')
    initial_data = soup.find('script',string=re.compile('ytInitialData'))                               #Puxamos o enorme JSON onde contém as informações que queremos (videoId e title)

    str_initial_data = str(initial_data)                                                                #Transforma o objeto em uma string para poder manipular
    extracted_josn_text = str_initial_data.split(';')[0].strip()                                        #Remove caracteres indesejados em um json
    new_extracted_josn_text = re.sub('<script nonce=.*>var ytInitialData = ','',extracted_josn_text)    #Remove caracteres indesejados em um json

    video_results = json.loads(new_extracted_josn_text)
    video_json = video_results['contents']['twoColumnSearchResultsRenderer']['primaryContents']["sectionListRenderer"]["contents"][0]["itemSectionRenderer"]["contents"][0]['videoRenderer'] #Busca o id do vídeo
    video_id = video_json['videoId']
    video_name = video_json['title']['runs'][0]['text']
    print(video_id)
    #print(video_name)

    true_url = 'https://www.youtube.com/watch?v=' + video_id

    return true_url


search = input("URL or YouTube query: ")
if url_or_query(search) == 'query':
    search = change_query_to_url(search)  #Transforma uma query do youtube no link do primeiro video indicado por essa query
    print("New search: ", search)

#-------------  Faz um request com a URL e pega os dados  -------------
content = requests.get(search)
soup = BeautifulSoup(content.text, 'html.parser')
video_name = soup.find(itemprop='name')
video_id = soup.find(itemprop='videoId')

print('Video name: ', video_name['content'])
print('Video id: ', video_id['content'])
