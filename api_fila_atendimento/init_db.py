"""
Script para inicializar o banco de dados
"""
from database import engine, Base
from models import Cliente

def init_database():
    """
    Cria todas as tabelas no banco de dados
    """
    print("Criando tabelas no banco de dados...")
    Base.metadata.create_all(bind=engine)
    print("Banco de dados inicializado com sucesso!")

if __name__ == "__main__":
    init_database()

