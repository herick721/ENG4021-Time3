# 🐾 PetConect

> Plataforma web de adoção e estadia temporária de animais de rua vulneráveis.

---

## Sobre o projeto

O **PetConect** é um hub completo para donos de pets, adotantes, resgatadores e clínicas. Conecta animais de rua vulneráveis a famílias amorosas, centralizando adoção, guia de vacinas, mapa de clínicas, guia de compras com afiliados e dicas para donos de pet.

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

```bash
# 1. Clonar apenas a pasta da aplicação
git clone --no-checkout https://github.com/herick721/ENG4021-Time3.git
cd ENG4021-Time3
git sparse-checkout init --cone
git sparse-checkout set petconnect
git checkout main

# 2. Entrar na pasta
cd petconnect

# 3. Criar e ativar o ambiente virtual
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux

# 4. Instalar dependências
pip install -r requirements.txt

# 5. Rodar as migrations
python manage.py migrate

# 6. Popular o banco com dados de exemplo
python populate.py

# 7. Iniciar o servidor
python manage.py runserver
```

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
