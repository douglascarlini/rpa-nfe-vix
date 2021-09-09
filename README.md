# RPA NF-e Vix
Automatizador de Sistema para Prefeitura de Vitória-ES.

### :warning: ATENÇÃO!
> Este é um projeto pessoal de estudos, use livremente por sua conta e risco.

### Requerimentos

- [chromedriver](https://chromedriver.chromium.org/downloads)
- flask-jwt-extended
- Python 3.9
- selenium
- waitress
- flask

### Configuração

1) Instale o driver do `Google Chrome` conforme sua versão do navegador instalada;
2) Instale as bibliotecas necessárias com `pip3 install -r requirements.txt`;
3) Rode o RPA com `python main.py`.

### WebService

- `POST /baixar` baixa as NFs do mês escolhido (ex. mes: 8 para agosto)
  - `{ "login": "login-vix", "senha": "senha-vix", "ins": "inscricao-vix", "mes": "mes-numerico" }`