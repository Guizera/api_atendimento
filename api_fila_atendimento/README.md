# API de Fila de Atendimento

API REST desenvolvida com FastAPI para gerenciamento de fila de atendimento presencial. Esta API pode ser integrada em totems de autoatendimento ou sistemas de gerenciamento de filas.

## 📋 Características

- Gerenciamento completo de fila de atendimento
- Suporte a atendimento prioritário e normal
- Sistema de posicionamento automático
- Validações robustas de dados
- Documentação interativa automática (Swagger UI)
- Banco de dados SQLite (fácil implementação)

## 🚀 Instalação

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Passo a passo

1. **Clone ou navegue até o diretório do projeto:**

```bash
cd api_fila_atendimento
```

2. **Crie um ambiente virtual (recomendado):**

```bash
python3 -m venv venv
```

3. **Ative o ambiente virtual:**

- No macOS/Linux:
```bash
source venv/bin/activate
```

- No Windows:
```bash
venv\Scripts\activate
```

4. **Instale as dependências:**

```bash
pip install -r requirements.txt
```

5. **Inicialize o banco de dados (opcional - será criado automaticamente):**

```bash
python init_db.py
```

## ▶️ Como Executar

Execute a API com o comando:

```bash
uvicorn main:app --reload
```

Ou diretamente com Python:

```bash
python main.py
```

A API estará disponível em: **http://localhost:8000**

## 📚 Documentação Interativa

Após iniciar a API, acesse a documentação interativa:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## 🔌 Endpoints da API

### 1. GET `/fila`

**Descrição:** Lista todos os clientes não atendidos na fila.

**Resposta de Sucesso (200):**
```json
[
  {
    "posicao": 1,
    "nome": "João Silva",
    "data_chegada": "2024-11-29T10:30:00",
    "tipo_atendimento": "P"
  },
  {
    "posicao": 2,
    "nome": "Maria Santos",
    "data_chegada": "2024-11-29T10:35:00",
    "tipo_atendimento": "N"
  }
]
```

**Resposta quando fila vazia (200):**
```json
[]
```

### 2. GET `/fila/{id}`

**Descrição:** Retorna os dados do cliente na posição especificada.

**Parâmetros:**
- `id` (path): Posição na fila (inteiro)

**Resposta de Sucesso (200):**
```json
{
  "posicao": 1,
  "nome": "João Silva",
  "data_chegada": "2024-11-29T10:30:00",
  "tipo_atendimento": "P"
}
```

**Resposta de Erro (404):**
```json
{
  "detail": {
    "mensagem": "Nenhum cliente encontrado na posição 5 da fila"
  }
}
```

### 3. POST `/fila`

**Descrição:** Adiciona um novo cliente na fila.

**Body (JSON):**
```json
{
  "nome": "João Silva",
  "tipo_atendimento": "P"
}
```

**Campos:**
- `nome` (obrigatório): String com máximo de 20 caracteres
- `tipo_atendimento` (obrigatório): "N" (Normal) ou "P" (Prioritário)

**Resposta de Sucesso (201):**
```json
{
  "posicao": 1,
  "nome": "João Silva",
  "data_chegada": "2024-11-29T10:30:00",
  "tipo_atendimento": "P"
}
```

**Resposta de Erro (422) - Validação:**
```json
{
  "detail": [
    {
      "msg": "Nome deve ter no máximo 20 caracteres"
    }
  ]
}
```

### 4. PUT `/fila`

**Descrição:** Chama o próximo cliente da fila para atendimento.

**Comportamento:**
- Cliente na posição 1 é marcado como atendido (posição 0)
- Todos os outros clientes sobem uma posição na fila

**Resposta de Sucesso (200):**
```json
{
  "mensagem": "Cliente João Silva chamado para atendimento. Fila atualizada."
}
```

**Resposta de Erro (404):**
```json
{
  "detail": {
    "mensagem": "Não há clientes na fila para serem chamados"
  }
}
```

### 5. DELETE `/fila/{id}`

**Descrição:** Remove um cliente específico da fila.

**Parâmetros:**
- `id` (path): Posição na fila (inteiro)

**Resposta de Sucesso (200):**
```json
{
  "mensagem": "Cliente João Silva removido da posição 1. Fila atualizada."
}
```

**Resposta de Erro (404):**
```json
{
  "detail": {
    "mensagem": "Nenhum cliente encontrado na posição 5 da fila"
  }
}
```

## 🎯 Sistema de Prioridades

A API implementa um sistema inteligente de prioridades:

- **Clientes Prioritários (P):** Idosos, gestantes, pessoas com deficiência, etc.
- **Clientes Normais (N):** Atendimento padrão

### Regras de Posicionamento:

1. Clientes prioritários sempre ficam à frente dos normais
2. Dentro de cada categoria, a ordem é por chegada (FIFO)
3. Ao adicionar um novo cliente prioritário, ele é inserido após os prioritários existentes, mas antes de todos os normais

**Exemplo:**

Fila atual: `[P1, P2, N1, N2]`

Ao adicionar `P3`, a fila fica: `[P1, P2, P3, N1, N2]`

Ao adicionar `N3`, a fila fica: `[P1, P2, P3, N1, N2, N3]`

## 🧪 Testando a API

### Usando cURL

**Adicionar cliente:**
```bash
curl -X POST "http://localhost:8000/fila" \
  -H "Content-Type: application/json" \
  -d '{"nome": "João Silva", "tipo_atendimento": "P"}'
```

**Listar fila:**
```bash
curl -X GET "http://localhost:8000/fila"
```

**Buscar por posição:**
```bash
curl -X GET "http://localhost:8000/fila/1"
```

**Chamar próximo:**
```bash
curl -X PUT "http://localhost:8000/fila"
```

**Remover da fila:**
```bash
curl -X DELETE "http://localhost:8000/fila/2"
```

### Usando Python (requests)

```python
import requests

BASE_URL = "http://localhost:8000"

# Adicionar cliente
response = requests.post(
    f"{BASE_URL}/fila",
    json={"nome": "João Silva", "tipo_atendimento": "P"}
)
print(response.json())

# Listar fila
response = requests.get(f"{BASE_URL}/fila")
print(response.json())

# Chamar próximo
response = requests.put(f"{BASE_URL}/fila")
print(response.json())
```

## 📊 Estrutura do Banco de Dados

### Tabela: `clientes`

| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | Integer | Chave primária (auto-incremento) |
| nome | String(20) | Nome do cliente |
| tipo_atendimento | String(1) | N = Normal, P = Prioritário |
| posicao | Integer | Posição atual na fila |
| data_chegada | DateTime | Data e hora de entrada na fila |
| atendido | Boolean | Status de atendimento (True/False) |

## 🛠️ Tecnologias Utilizadas

- **FastAPI:** Framework web moderno e rápido
- **SQLAlchemy:** ORM para manipulação do banco de dados
- **Pydantic:** Validação de dados e serialização
- **Uvicorn:** Servidor ASGI de alta performance
- **SQLite:** Banco de dados leve e embutido

## 📁 Estrutura do Projeto

```
api_fila_atendimento/
├── main.py              # Aplicação principal com endpoints
├── models.py            # Modelos do banco de dados
├── schemas.py           # Schemas de validação (Pydantic)
├── database.py          # Configuração do banco de dados
├── init_db.py           # Script de inicialização do banco
├── requirements.txt     # Dependências do projeto
├── README.md           # Documentação
└── fila_atendimento.db # Banco de dados SQLite (criado automaticamente)
```

## ⚠️ Validações Implementadas

1. **Nome:**
   - Campo obrigatório
   - Não pode ser vazio
   - Máximo de 20 caracteres

2. **Tipo de Atendimento:**
   - Campo obrigatório
   - Apenas "N" ou "P" (case-insensitive)

3. **Posição:**
   - Deve existir na fila
   - Cliente não pode estar atendido

## 🔒 Status HTTP

- `200 OK`: Operação bem-sucedida
- `201 Created`: Recurso criado com sucesso
- `404 Not Found`: Recurso não encontrado
- `422 Unprocessable Entity`: Erro de validação

## 🎓 Autor

Desenvolvido como avaliação final da disciplina de Desenvolvimento de APIs e Microsserviços.

## 📄 Licença

Este projeto foi desenvolvido para fins educacionais.

