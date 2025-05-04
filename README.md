# Bot FURIOSO DA FURIA

## 📌 Visão Geral
Este projeto tem como objetivo integrar diversas informações sobre a equipe FURIA — incluindo dados de partidas, estatísticas dos jogadores e notícias — e disponibilizá-las de forma acessível por meio de comandos no Telegram.

## 🚀 Funcionalidades

`/stats` — Exibe estatísticas atualizadas dos jogadores da FURIA.

`/noticias` — Lista as últimas notícias relevantes da equipe.

`/partidas` — Mostra resultados de partidas recentes.

`/proximos_jogos` — Informa os próximos confrontos agendados.

## 🛠️ Tecnologias Utilizadas

- **Python**
- **[python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)** — Para integração com a API do Telegram.
- **BeautifulSoup** — Para Web Scraping de dados em tempo real.
- **Agente de IA** — Hospedado na [DigitalOcean](https://www.digitalocean.com/), usado para interpretar e analisar dados estatísticos.


## 📄 Projeto 

- **main.py** : Contém o código do funcionamento do Bot e a chamada de funções
- **api.py** : Camada que realiza requisições e trata os dados para o main.py

## ⚙️ Como Configurar

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/MateusMendes0/Furioso-Bot.git
   cd Furioso-Bot
   ```

2. **Crie um ambiente virtual:**

   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Configure as variáveis de ambiente:**

   Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:

   ```
   TOKEN=seu_token_do_telegram
   DIGITALOCEAN_API=chave_de_api
   ```

   ## 💡 Exemplo de Uso

No Telegram, envie os comandos diretamente para o bot:

```
/stats Qual as estatísticas do Molodoy?
/noticias
/partidas
/proximos_jogos
```
