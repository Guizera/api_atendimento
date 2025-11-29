"""
Script de exemplo para testar a API de Fila de Atendimento
Execute este script após iniciar a API com: uvicorn main:app --reload
"""
import requests
import json

BASE_URL = "http://localhost:8000"


def print_response(title, response):
    """Função auxiliar para exibir respostas"""
    print(f"\n{'='*60}")
    print(f"📋 {title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response:\n{json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except:
        print(f"Response: {response.text}")


def test_api():
    """Testa todos os endpoints da API"""
    
    print("\n🚀 Iniciando testes da API de Fila de Atendimento\n")
    
    # 1. Testar endpoint raiz
    print("\n1️⃣ Testando endpoint raiz (GET /)")
    response = requests.get(f"{BASE_URL}/")
    print_response("GET /", response)
    
    # 2. Listar fila vazia
    print("\n2️⃣ Listando fila (inicialmente vazia)")
    response = requests.get(f"{BASE_URL}/fila")
    print_response("GET /fila", response)
    
    # 3. Adicionar cliente normal
    print("\n3️⃣ Adicionando cliente normal")
    response = requests.post(
        f"{BASE_URL}/fila",
        json={"nome": "Maria Santos", "tipo_atendimento": "N"}
    )
    print_response("POST /fila - Cliente Normal", response)
    
    # 4. Adicionar cliente prioritário
    print("\n4️⃣ Adicionando cliente prioritário")
    response = requests.post(
        f"{BASE_URL}/fila",
        json={"nome": "João Silva", "tipo_atendimento": "P"}
    )
    print_response("POST /fila - Cliente Prioritário", response)
    
    # 5. Adicionar mais clientes
    print("\n5️⃣ Adicionando mais clientes")
    clientes = [
        {"nome": "Ana Costa", "tipo_atendimento": "N"},
        {"nome": "Pedro Oliveira", "tipo_atendimento": "P"},
        {"nome": "Carlos Souza", "tipo_atendimento": "N"}
    ]
    
    for cliente in clientes:
        response = requests.post(f"{BASE_URL}/fila", json=cliente)
        print(f"✅ {cliente['nome']} ({cliente['tipo_atendimento']}) adicionado - Posição: {response.json()['posicao']}")
    
    # 6. Listar fila completa
    print("\n6️⃣ Listando fila completa")
    response = requests.get(f"{BASE_URL}/fila")
    print_response("GET /fila - Fila Completa", response)
    
    # 7. Buscar cliente na posição 1
    print("\n7️⃣ Buscando cliente na posição 1")
    response = requests.get(f"{BASE_URL}/fila/1")
    print_response("GET /fila/1", response)
    
    # 8. Buscar posição inexistente
    print("\n8️⃣ Buscando posição inexistente (deve retornar 404)")
    response = requests.get(f"{BASE_URL}/fila/99")
    print_response("GET /fila/99 (Erro esperado)", response)
    
    # 9. Chamar próximo cliente
    print("\n9️⃣ Chamando próximo cliente para atendimento")
    response = requests.put(f"{BASE_URL}/fila")
    print_response("PUT /fila", response)
    
    # 10. Listar fila após chamada
    print("\n🔟 Listando fila após chamar cliente")
    response = requests.get(f"{BASE_URL}/fila")
    print_response("GET /fila - Após Chamada", response)
    
    # 11. Remover cliente da posição 2
    print("\n1️⃣1️⃣ Removendo cliente da posição 2")
    response = requests.delete(f"{BASE_URL}/fila/2")
    print_response("DELETE /fila/2", response)
    
    # 12. Listar fila final
    print("\n1️⃣2️⃣ Listando fila final")
    response = requests.get(f"{BASE_URL}/fila")
    print_response("GET /fila - Fila Final", response)
    
    # 13. Testar validações - Nome muito longo
    print("\n1️⃣3️⃣ Testando validação - Nome com mais de 20 caracteres")
    response = requests.post(
        f"{BASE_URL}/fila",
        json={"nome": "Nome Muito Longo Que Ultrapassa Vinte Caracteres", "tipo_atendimento": "N"}
    )
    print_response("POST /fila - Nome Inválido (Erro esperado)", response)
    
    # 14. Testar validações - Tipo inválido
    print("\n1️⃣4️⃣ Testando validação - Tipo de atendimento inválido")
    response = requests.post(
        f"{BASE_URL}/fila",
        json={"nome": "Teste", "tipo_atendimento": "X"}
    )
    print_response("POST /fila - Tipo Inválido (Erro esperado)", response)
    
    print("\n" + "="*60)
    print("✅ Testes concluídos!")
    print("="*60 + "\n")


if __name__ == "__main__":
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("\n❌ Erro: Não foi possível conectar à API!")
        print("Certifique-se de que a API está rodando em http://localhost:8000")
        print("\nPara iniciar a API, execute:")
        print("  uvicorn main:app --reload")
    except Exception as e:
        print(f"\n❌ Erro durante os testes: {str(e)}")

