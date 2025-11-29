from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional


class ClienteCreate(BaseModel):
    """
    Schema para criar um novo cliente na fila
    """
    nome: str = Field(..., max_length=20, description="Nome do cliente (máximo 20 caracteres)")
    tipo_atendimento: str = Field(..., max_length=1, description="Tipo de atendimento: N (Normal) ou P (Prioritário)")

    @field_validator('nome')
    @classmethod
    def validar_nome(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Nome não pode ser vazio')
        if len(v) > 20:
            raise ValueError('Nome deve ter no máximo 20 caracteres')
        return v.strip()

    @field_validator('tipo_atendimento')
    @classmethod
    def validar_tipo(cls, v):
        if v.upper() not in ['N', 'P']:
            raise ValueError('Tipo de atendimento deve ser N (Normal) ou P (Prioritário)')
        return v.upper()


class ClienteResponse(BaseModel):
    """
    Schema para resposta de dados do cliente
    """
    posicao: int
    nome: str
    data_chegada: datetime
    tipo_atendimento: str

    class Config:
        from_attributes = True


class MensagemResponse(BaseModel):
    """
    Schema para mensagens de resposta
    """
    mensagem: str

