# TreeBank

## Descrição

A Treebank é um banco com sistema de login e permite que os usuários façam transferências monetárias, vizualização do histórido de transações, criação de carteiras. Ele oferece recursos avançados, como análises feitas em gráficos sobre suas transações, filtro de pesquisa por data e tipo de transação, exportação de PDF e muito mais.


## Instalação

1. Clone o repositório para sua máquina local:
``` 
git clone https://github.com/DjalmaFelipe02/Bank.git
```
2. Navegue até o diretório do projeto:
``` 
cd controller
```
3. Inicialize um ambiente virtual:
``` 
py -m venv venv
```
4. Ative o ambiente virtual (comando para Windows):
``` 
venv\Scripts\activate
```
5. Instale as dependências do projeto:
``` 
pip install -r requirements.txt
```
6. Execute as migrações do Django para criar o esquema do banco de dados:
``` 
python manage.py makemigrations
python manage.py migrate
```
## Uso

Para executar o servidor de desenvolvimento, execute o seguinte comando:
``` 
python manage.py runserver
```
Isso iniciará o servidor de desenvolvimento em 'http://localhost:8000/'.

Depois coloque essa URL 'http://localhost:8000/home' para acessar a página.
