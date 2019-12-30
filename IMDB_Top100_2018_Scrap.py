import pandas as pd
from bs4 import BeautifulSoup
import requests


url = "https://www.imdb.com/list/ls041322734/?sort=list_order,asc&st_dt=&mode=detail&page="

page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')


page_content = soup.find(class_='lister-list')
items = page_content.find_all(class_ = 'lister-item')

movie_ = soup.find_all('h3', class_='lister-item-header')
movie_title = [movie.find('a').get_text() for movie in movie_]


movie_rank = [movie.find(class_='lister-item-index unbold text-primary').get_text()[:-1] for movie in soup.findAll('h3', class_='lister-item-header')]


movie_year = [movie.find(class_= 'lister-item-year text-muted unbold').get_text()[1:-1] for movie in soup.findAll('h3', class_='lister-item-header')]


#movie_certificate = [movie.text for movie in soup.find_all(class_='certificate')]
movie_certificate=[]
k='Nil'
cert_detail = soup.find_all(class_='lister-item-content')
cert = [movie.find(class_='certificate') for movie in cert_detail]
for mov in cert:
    if mov is not None:
        movie_certificate.append(mov.text)
    else:
        movie_certificate.append(k)


movie_runtime = [movie.text for movie in soup.find_all(class_='runtime')]


movie_genre = [movie.text[1:-8][:-4] for movie in soup.find_all(class_='genre')]


movie_rating = [movie.find('span',class_='ipl-rating-star__rating').text for movie in soup.find_all(class_='ipl-rating-star small')]


#movie_metascore = [movie.text[1:3] for movie in soup.find_all('div', class_='inline-block ratings-metascore')]
movie_metascore=[]
meta_score=[]
k='Nil'
meta_detail = soup.find_all(class_='lister-item-content')
meta_ = [movie.find(class_= 'inline-block ratings-metascore') for movie in meta_detail]

for met in meta_:
    if met is not None:
        meta_score.append(met.find('span'))
    else:
        meta_score.append(k)
for metascore in meta_score:
    if metascore is not 'Nil':
        movie_metascore.append(metascore.text[:-8])
    else:
        movie_metascore.append(k)


#movie_votes = [movie['data-value'] for movie in soup.find_all('span',{'name':'nv'})[0::2]]
mov = soup.find_all(class_='lister-item-content')
mov_vote = [movie.find_all('span',{'name':'nv'}) for movie in mov]
m_votes = [mv[0] for mv in mov_vote]
movie_votes = [m_v['data-value'] for m_v in m_votes]


#movie_gross = [movie['data-value'] for movie in soup.find_all('span',{'name':'nv'})[1::2]]
mov = soup.find_all(class_='lister-item-content')
mov_gross = [movie.find_all('span',{'name':'nv'}) for movie in mov]
m_gross = [mv[0] for mv in mov_gross]
movie_gross = [m_v['data-value'] for m_v in m_gross]


movie_director = [mov.text for mov in [movie.find('a') for movie in soup.find_all('p', class_='text-muted text-small')[1::3]]]


#movie_actors = [movie_actors = [mov.text for mov in [movie.find('a') for movie in soup.find_all('p', class_='text-muted text-small')[2:5:1]]]mov.text for mov in [movie.find('a') for movie in soup.find_all('p', class_='text-muted text-small')[2:5:1]]]


actors_data = soup.find_all('p', class_='text-muted text-small')[1::3]
movie_actors=[]
for i in range(0,100):
    m_actor = [act.text for act in [actors for actors in [data for data in [movie.find_all('a') for movie in actors_data]][i][1:]]]
    movie_actors.append(m_actor)


df_dict = {'Movie Rank': movie_rank, 'Title': movie_title, 'Relase': movie_year,
           'Movie Certificate': movie_certificate, 'Metascore': movie_metascore,'Runtime': movie_runtime,
           'Genre': movie_genre, 'IMDB Rating': movie_rating, 'Votes': movie_votes,
           'Box Office Earnings': movie_gross, 'Director': movie_director, 'Actors': movie_actors}


print(len(movie_rank))
print(len(movie_title))
print(len(movie_year))
print(len(movie_certificate))
print(len(movie_metascore))
print(len(movie_runtime))
print(len(movie_genre))
print(len(movie_rating))
print(len(movie_votes))
print(len(movie_gross))
print(len(movie_director))
print(len(movie_actors))


df = pd.DataFrame(df_dict)
df.head()


export_csv = df.to_csv('/home/muneeb/IMDB_top100.csv', index = None, header=True)
