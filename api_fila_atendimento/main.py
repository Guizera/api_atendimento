from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from database import engine, get_db, Base
from models import Cliente
from schemas import ClienteCreate, ClienteResponse, MensagemResponse

# Criar as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Fila de Atendimento",
    description="API para gerenciamento de fila de atendimento presencial",
    version="1.0.0"
)


def reorganizar_posicoes(db: Session):
    """
    Reorganiza as posições da fila considerando prioridade
    Clientes prioritários (P) ficam na frente dos normais (N)
    """
    # Buscar todos os clientes não atendidos
    clientes_prioritarios = db.query(Cliente).filter(
        Cliente.atendido == False,
        Cliente.tipo_atendimento == 'P'
    ).order_by(Cliente.data_chegada).all()
    
    clientes_normais = db.query(Cliente).filter(
        Cliente.atendido == False,
        Cliente.tipo_atendimento == 'N'
    ).order_by(Cliente.data_chegada).all()
    
    # Atribuir posições: prioritários primeiro, depois normais
    posicao = 1
    for cliente in clientes_prioritarios:
        cliente.posicao = posicao
        posicao += 1
    
    for cliente in clientes_normais:
        cliente.posicao = posicao
        posicao += 1
    
    db.commit()


@app.get("/fila", response_model=List[ClienteResponse], status_code=status.HTTP_200_OK)
def listar_fila(db: Session = Depends(get_db)):
    """
    GET /fila
    
    Retorna todos os clientes não atendidos na fila, ordenados por posição.
    Exibe a posição na fila, o nome e a data de chegada de cada cliente.
    
    Retorna lista vazia com status 200 se não houver ninguém na fila.
    """
    clientes = db.query(Cliente).filter(
        Cliente.atendido == False
    ).order_by(Cliente.posicao).all()
    
    return clientes


@app.get("/fila/{id}", response_model=ClienteResponse, status_code=status.HTTP_200_OK)
def buscar_cliente_por_posicao(id: int, db: Session = Depends(get_db)):
    """
    GET /fila/{id}
    
    Retorna os dados do cliente na posição especificada (id) da fila.
    Retorna posição na fila, nome e data de chegada.
    
    Se não houver cliente na posição especificada, retorna status 404 com mensagem informativa.
    """
    cliente = db.query(Cliente).filter(
        Cliente.posicao == id,
        Cliente.atendido == False
    ).first()
    
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"mensagem": f"Nenhum cliente encontrado na posição {id} da fila"}
        )
    
    return cliente


@app.post("/fila", response_model=ClienteResponse, status_code=status.HTTP_201_CREATED)
def adicionar_cliente(cliente_data: ClienteCreate, db: Session = Depends(get_db)):
    """
    POST /fila
    
    Adiciona um novo cliente na fila informando seu nome e tipo de atendimento.
    
    Parâmetros:
    - nome: String obrigatória com máximo de 20 caracteres
    - tipo_atendimento: Caractere único (N para Normal ou P para Prioritário)
    
    O sistema identifica automaticamente a posição na fila considerando prioridade,
    registra a data de entrada e seta o campo atendido como FALSE.
    
    Clientes prioritários (P) são posicionados na frente dos clientes normais (N),
    respeitando a ordem de chegada dentro de cada categoria.
    """
    # Criar novo cliente
    novo_cliente = Cliente(
        nome=cliente_data.nome,
        tipo_atendimento=cliente_data.tipo_atendimento,
        data_chegada=datetime.now(),
        atendido=False,
        posicao=0  # Será atualizado pela função reorganizar_posicoes
    )
    
    db.add(novo_cliente)
    db.commit()
    
    # Reorganizar todas as posições considerando prioridade
    reorganizar_posicoes(db)
    
    # Atualizar o objeto com a nova posição
    db.refresh(novo_cliente)
    
    return novo_cliente


@app.put("/fila", response_model=MensagemResponse, status_code=status.HTTP_200_OK)
def chamar_proximo_cliente(db: Session = Depends(get_db)):
    """
    PUT /fila
    
    Chama o próximo cliente da fila para atendimento.
    
    Atualiza a posição de cada pessoa que está na fila diminuindo em 1 (-1).
    O cliente que está na posição 1 é atualizado para posição 0 e o campo
    atendido é setado para TRUE, indicando que foi chamado para atendimento.
    
    Os demais clientes têm suas posições atualizadas automaticamente.
    """
    # Buscar o cliente na posição 1
    cliente_posicao_1 = db.query(Cliente).filter(
        Cliente.posicao == 1,
        Cliente.atendido == False
    ).first()
    
    if not cliente_posicao_1:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"mensagem": "Não há clientes na fila para serem chamados"}
        )
    
    # Marcar como atendido e mover para posição 0
    cliente_posicao_1.atendido = True
    cliente_posicao_1.posicao = 0
    
    # Buscar todos os outros clientes não atendidos e reorganizar
    db.commit()
    reorganizar_posicoes(db)
    
    return {"mensagem": f"Cliente {cliente_posicao_1.nome} chamado para atendimento. Fila atualizada."}


@app.delete("/fila/{id}", response_model=MensagemResponse, status_code=status.HTTP_200_OK)
def remover_cliente(id: int, db: Session = Depends(get_db)):
    """
    DELETE /fila/{id}
    
    Remove o cliente na posição especificada (id) da fila.
    
    Após a remoção, atualiza automaticamente a posição dos demais clientes na fila.
    
    Se o cliente não for encontrado na posição especificada, retorna status 404
    com mensagem informativa.
    """
    # Buscar cliente na posição especificada
    cliente = db.query(Cliente).filter(
        Cliente.posicao == id,
        Cliente.atendido == False
    ).first()
    
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"mensagem": f"Nenhum cliente encontrado na posição {id} da fila"}
        )
    
    nome_removido = cliente.nome
    
    # Remover o cliente
    db.delete(cliente)
    db.commit()
    
    # Reorganizar as posições
    reorganizar_posicoes(db)
    
    return {"mensagem": f"Cliente {nome_removido} removido da posição {id}. Fila atualizada."}


@app.get("/", response_model=dict)
def root():
    """
    Endpoint raiz com informações sobre a API
    """
    return {
        "mensagem": "API de Fila de Atendimento",
        "versao": "1.0.0",
        "endpoints": {
            "GET /fila": "Listar todos os clientes na fila",
            "GET /fila/{id}": "Buscar cliente por posição",
            "POST /fila": "Adicionar novo cliente na fila",
            "PUT /fila": "Chamar próximo cliente para atendimento",
            "DELETE /fila/{id}": "Remover cliente da posição especificada"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

