"""
🌟 DEMONSTRAÇÃO DO SISTEMA DE PRIORIDADE
Este script demonstra visualmente como o sistema de prioridade funciona
"""
import requests
import json
from time import sleep

BASE_URL = "http://localhost:8000"

def limpar_fila():
    """Limpa toda a fila para começar do zero"""
    fila = requests.get(f"{BASE_URL}/fila").json()
    for cliente in fila:
        requests.delete(f"{BASE_URL}/fila/{cliente['posicao']}")

def exibir_fila(titulo="FILA ATUAL"):
    """Exibe a fila de forma visual"""
    print("\n" + "="*70)
    print(f"📊 {titulo}")
    print("="*70)
    
    response = requests.get(f"{BASE_URL}/fila")
    fila = response.json()
    
    if not fila:
        print("   [FILA VAZIA]")
    else:
        print(f"\n{'Pos':<5} {'Tipo':<8} {'Nome':<25} {'Chegada':<20}")
        print("-"*70)
        for cliente in fila:
            tipo_texto = "⭐ P" if cliente['tipo_atendimento'] == 'P' else "👤 N"
            hora = cliente['data_chegada'].split('T')[1][:8]
            print(f"{cliente['posicao']:<5} {tipo_texto:<8} {cliente['nome']:<25} {hora:<20}")
    
    print("="*70)

def adicionar(nome, tipo, mostrar=True):
    """Adiciona cliente e mostra resultado"""
    tipo_texto = "Prioritário ⭐" if tipo == "P" else "Normal 👤"
    if mostrar:
        print(f"\n➕ Adicionando: {nome} ({tipo_texto})")
    
    response = requests.post(
        f"{BASE_URL}/fila",
        json={"nome": nome, "tipo_atendimento": tipo}
    )
    
    if response.status_code == 201:
        resultado = response.json()
        if mostrar:
            print(f"   ✅ Inserido na posição {resultado['posicao']}")
        return resultado
    else:
        print(f"   ❌ Erro: {response.json()}")
        return None

def demonstracao_completa():
    """Demonstração completa do sistema de prioridade"""
    
    print("\n" + "🌟"*35)
    print("   DEMONSTRAÇÃO DO SISTEMA DE PRIORIDADE")
    print("🌟"*35)
    
    print("\n📝 Limando fila para começar demonstração...")
    limpar_fila()
    sleep(0.5)
    
    exibir_fila("FILA INICIAL (VAZIA)")
    input("\n⏸️  Pressione ENTER para continuar...")
    
    # Cenário 1: Adicionar clientes normais
    print("\n\n" + "━"*70)
    print("📌 CENÁRIO 1: Adicionando apenas clientes NORMAIS")
    print("━"*70)
    
    adicionar("Ana Costa", "N")
    sleep(0.3)
    adicionar("Carlos Souza", "N")
    sleep(0.3)
    adicionar("Maria Santos", "N")
    
    exibir_fila("FILA COM CLIENTES NORMAIS")
    print("\n💡 Observe: Ordem de chegada respeitada (FIFO)")
    input("\n⏸️  Pressione ENTER para continuar...")
    
    # Cenário 2: Adicionar cliente prioritário
    print("\n\n" + "━"*70)
    print("📌 CENÁRIO 2: Adicionando cliente PRIORITÁRIO")
    print("━"*70)
    print("\n❓ O que acontece quando um prioritário chega?")
    
    sleep(1)
    adicionar("João Silva", "P")
    
    exibir_fila("FILA REORGANIZADA")
    print("\n💡 Observe: João (P) passou na frente de TODOS os normais!")
    input("\n⏸️  Pressione ENTER para continuar...")
    
    # Cenário 3: Adicionar mais prioritários
    print("\n\n" + "━"*70)
    print("📌 CENÁRIO 3: Adicionando MAIS prioritários")
    print("━"*70)
    
    adicionar("Pedro Oliveira", "P")
    sleep(0.3)
    adicionar("Luiza Ferreira", "P")
    
    exibir_fila("FILA COM MÚLTIPLOS PRIORITÁRIOS")
    print("\n💡 Observe:")
    print("   1. Prioritários ficam JUNTOS no início")
    print("   2. Entre prioritários: ordem de chegada")
    print("   3. Normais ficam DEPOIS de todos os prioritários")
    input("\n⏸️  Pressione ENTER para continuar...")
    
    # Cenário 4: Intercalando tipos
    print("\n\n" + "━"*70)
    print("📌 CENÁRIO 4: Intercalando Normal → Prioritário → Normal")
    print("━"*70)
    
    adicionar("Roberto Lima", "N")
    sleep(0.3)
    adicionar("Sandra Costa", "P")
    sleep(0.3)
    adicionar("Paulo Dias", "N")
    
    exibir_fila("FILA FINAL ORGANIZADA")
    print("\n💡 Observe:")
    print("   ⭐ Todos os PRIORITÁRIOS nas primeiras posições")
    print("   👤 Todos os NORMAIS depois")
    print("   📅 Ordem de chegada respeitada DENTRO de cada categoria")
    input("\n⏸️  Pressione ENTER para continuar...")
    
    # Cenário 5: Chamando clientes
    print("\n\n" + "━"*70)
    print("📌 CENÁRIO 5: Chamando clientes para atendimento")
    print("━"*70)
    
    for i in range(3):
        print(f"\n🔔 Chamando próximo cliente (chamada {i+1}/3)...")
        response = requests.put(f"{BASE_URL}/fila")
        resultado = response.json()
        print(f"   {resultado['mensagem']}")
        sleep(0.5)
        exibir_fila(f"FILA APÓS CHAMADA {i+1}")
    
    print("\n💡 Observe: Prioritários são chamados primeiro!")
    input("\n⏸️  Pressione ENTER para continuar...")
    
    # Cenário 6: Removendo da fila
    print("\n\n" + "━"*70)
    print("📌 CENÁRIO 6: Removendo cliente da posição 2")
    print("━"*70)
    
    fila_antes = requests.get(f"{BASE_URL}/fila").json()
    if len(fila_antes) >= 2:
        cliente_pos2 = fila_antes[1]
        print(f"\n🗑️  Removendo: {cliente_pos2['nome']} (posição 2)")
        
        response = requests.delete(f"{BASE_URL}/fila/2")
        print(f"   {response.json()['mensagem']}")
        
        exibir_fila("FILA APÓS REMOÇÃO")
        print("\n💡 Observe: Posições reorganizadas automaticamente!")
    
    # Resumo Final
    print("\n\n" + "🎯"*35)
    print("   RESUMO DO SISTEMA DE PRIORIDADE")
    print("🎯"*35)
    print("\n✅ CARACTERÍSTICAS:")
    print("   1. Prioritários (P) SEMPRE à frente dos Normais (N)")
    print("   2. Ordem de chegada respeitada DENTRO de cada tipo")
    print("   3. Reorganização AUTOMÁTICA em todas as operações:")
    print("      • Ao adicionar cliente (POST)")
    print("      • Ao chamar próximo (PUT)")
    print("      • Ao remover da fila (DELETE)")
    print("\n📊 ALGORITMO:")
    print("   1. Busca todos os clientes P (ordem de chegada)")
    print("   2. Busca todos os clientes N (ordem de chegada)")
    print("   3. Atribui posições: [P1, P2, ..., Pn, N1, N2, ..., Nn]")
    print("\n⚖️  LEGISLAÇÃO:")
    print("   Baseado na Lei 10.048/2000 (Atendimento Prioritário)")
    print("   • Idosos (60+ anos)")
    print("   • Gestantes")
    print("   • Lactantes")
    print("   • Pessoas com deficiência")
    print("   • Pessoas com crianças de colo")
    print("\n" + "🎯"*35 + "\n")

def teste_rapido():
    """Teste rápido para verificar se está funcionando"""
    print("\n⚡ TESTE RÁPIDO DO SISTEMA DE PRIORIDADE\n")
    
    print("1. Limpando fila...")
    limpar_fila()
    
    print("2. Adicionando: Normal → Normal → Prioritário")
    adicionar("Cliente N1", "N", False)
    adicionar("Cliente N2", "N", False)
    adicionar("Cliente P1", "P", False)
    
    print("\n3. Verificando ordem...")
    fila = requests.get(f"{BASE_URL}/fila").json()
    
    print("\nResultado:")
    for cliente in fila:
        tipo = "⭐ P" if cliente['tipo_atendimento'] == 'P' else "👤 N"
        print(f"   Pos {cliente['posicao']}: {cliente['nome']} ({tipo})")
    
    # Verificar se prioritário está na posição 1
    if fila[0]['tipo_atendimento'] == 'P':
        print("\n✅ SISTEMA DE PRIORIDADE FUNCIONANDO CORRETAMENTE!")
        print("   Prioritário está na posição 1, como esperado.")
        return True
    else:
        print("\n❌ ERRO: Prioritário deveria estar na posição 1!")
        return False

if __name__ == "__main__":
    import sys
    
    print("\n" + "🌟"*35)
    print("   DEMONSTRAÇÃO - SISTEMA DE PRIORIDADE")
    print("🌟"*35)
    
    try:
        # Verificar se API está rodando
        requests.get(f"{BASE_URL}/")
        
        print("\nEscolha uma opção:")
        print("  1. Demonstração completa (recomendado)")
        print("  2. Teste rápido")
        
        escolha = input("\nDigite 1 ou 2 [1]: ").strip() or "1"
        
        if escolha == "1":
            demonstracao_completa()
        else:
            teste_rapido()
        
        print("\n✅ Demonstração concluída!")
        print("\n💡 DICA: Acesse http://localhost:8000/docs")
        print("   para testar a API interativamente no Swagger UI\n")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERRO: API não está rodando!")
        print("\nPara iniciar a API:")
        print("  cd api_fila_atendimento")
        print("  uvicorn main:app --reload")
        print("\nDepois execute este script novamente.\n")
    except KeyboardInterrupt:
        print("\n\n⏹️  Demonstração interrompida pelo usuário.\n")
    except Exception as e:
        print(f"\n❌ Erro: {e}\n")

