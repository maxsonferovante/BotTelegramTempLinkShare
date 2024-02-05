---

# TempLinkShareBot

O TempLinkShareBot é um bot do Telegram que permite o compartilhamento seguro e temporário de arquivos através de links. Faça upload de arquivos e obtenha links de download com tempo de expiração. Ideal para compartilhar arquivos sensíveis, garantindo acesso restrito e temporário.

## Tecnologias Utilizadas 

[![My Skills](https://skillicons.dev/icons?i=python,postgres,peewee,docker,aws,git,github,telegram)](https://skillicons.dev)

## Como Usar

Para executar o bot localmente, siga estas etapas:

1. Clone o repositório:

   ```bash
   git clone https://github.com/maxsonferovante/BotTelegramTempLinkShare.git
   ```

2. Configure o ambiente virtual (venv):

   ```bash
   cd BotTelegramTempLinkShare
   python3 -m venv venv
   ```

3. Ative o ambiente virtual:

   ```bash
   source venv/bin/activate   # Para Linux/Mac
   # ou
   venv\Scripts\activate      # Para Windows
   ```

4. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

5. Adquira um token de bot do Telegram e substitua-o em `config.py`.

6. Execute o bot:

   ```bash
   python main.py
   ```


## TempLinkShare - API AWS S3

O TempLinkShare também inclui uma API em Node.js que lida com o acesso ao bucket S3 na AWS. Os arquivos são armazenados temporariamente e ficam disponíveis por 30 minutos.

Para mais detalhes sobre a API, consulte o [repositório no GitHub](https://github.com/maxsonferovante/TempLinkShare).

---
