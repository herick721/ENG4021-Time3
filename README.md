# 🐾 PetConnect

> Plataforma web de adoção e estadia temporária de animais de rua vulneráveis.

---

## Sobre o projeto

O **PetConnect** é um hub completo para donos de pets, adotantes, resgatadores e clínicas. Conecta animais de rua vulneráveis a famílias amorosas, centralizando adoção, guia de vacinas, mapa de clínicas, guia de compras com afiliados e dicas para donos de pet.

---

## Funcionalidades

- 🐾 **Adoção de pets** — busca com filtros, perfil completo do animal e solicitação online
- 🏠 **Lar temporário** — fluxo dedicado para famílias que oferecem guarda temporária
- ✅ **Aprovação / rejeição** — dashboard para ONGs e resgatadores gerenciarem candidatos
- 💉 **Guia de vacinas** — calendário completo com lembretes por espécie e idade
- 📍 **Mapa de clínicas** — integração com Google Maps para clínicas e abrigos próximos
- 🛟 **Grupos de resgate** — diretório de ONGs e voluntários por cidade
- 🛒 **Guia de compras** — produtos de afiliados verificados com condições exclusivas
- 💝 **Doação** — redirecionamento para canais oficiais de ONGs parceiras
- 👤 **Perfil do usuário** — histórico de adoções, favoritos e linha do tempo do processo

---

## Status dos animais

| Status | Descrição |
|---|---|
| 🟢 Disponível | Animal aguardando solicitação |
| 🟡 Em análise | Solicitação recebida, candidato em avaliação |
| 🟠 Lar temporário | Animal em guarda temporária |
| 🔵 Adotado | Processo finalizado com sucesso |

---

## Como executar o projeto

### Pré-requisitos
- Python 3.10+
- Git

### Passo a passo

**1. Clone o repositório**
Abra o seu terminal e rode o comando abaixo para clonar o repositório:
```bash
git clone https://github.com/herick721/ENG4021-Time3
cd /ENG4021-Time3/petconnect
```

**2. Crie e ative um ambiente virtual**
É recomendado usar um ambiente virtual para instalar as dependências.
```bash
# Criar o ambiente virtual (chamado 'venv')
python -m venv venv

# Ativar no Windows:
venv\Scripts\activate

# Ativar no Linux/Mac:
source venv/bin/activate
```

**3. Instale as dependências**
Com o ambiente ativado, instale as bibliotecas necessárias:
```bash
pip install -r requirements.txt
```

**4. Aplique as migrações do banco de dados**
Configure o banco de dados inicial do Django:
```bash
python manage.py makemigrations core
python manage.py migrate
```

**5. (Opcional) Popule o banco com dados de teste**
Para ter alguns dados iniciais já cadastrados para testar o sistema, você pode usar o script de população:
```bash
python populate.py
```

**6. Inicie o servidor**
Por fim, rode o servidor de desenvolvimento:
```bash
python manage.py runserver
```

**7. Acesse o site**
Abra o seu navegador e acesse a seguinte URL:
[http://127.0.0.1:8000/](http://127.0.0.1:8000/)

Abrir no navegador: **http://127.0.0.1:8000**

---

## Stack

- **Frontend:** HTML · CSS puro
- **Backend:** Django (Python)
- **Banco de dados:** SQLite (desenvolvimento)
- **Autenticação:** django.contrib.auth
- **Armazenamento de imagens:** Cloudinary (previsto)

---

## Documentação de produto

| Documento | Descrição |
|---|---|
| `Sprint2/fluxogramaDoApp.pdf` | Fluxograma completo do sistema (6 fluxos) |
| `Sprint2/petconect_personasf.docx` | Definição de público-alvo e personas |
| `Sprint5/petconect_monetizacao.docx` | Pesquisa de monetização |
| `Sprint5/petconect_apis.docx` | Pesquisa de APIs de apoio |
| `petconnect/` | Aplicação Django completa |

---

## Licença

MIT © 2026 PetConect
