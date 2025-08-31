#!/usr/bin/env python3
"""
Teste Rápido do Sistema de Votação
Verifica se todas as funcionalidades estão funcionando
"""

import os
import sys
import json
import time
from datetime import datetime

def testar_imports():
    """Testa se todas as dependências estão disponíveis"""
    print("🔧 Testando imports...")
    
    try:
        import requests
        print("✅ requests - OK")
    except ImportError as e:
        print(f"❌ requests - ERRO: {e}")
        return False
    
    try:
        import psutil
        print("✅ psutil - OK")
    except ImportError as e:
        print(f"❌ psutil - ERRO: {e}")
        return False
    
    try:
        import threading
        print("✅ threading - OK")
    except ImportError as e:
        print(f"❌ threading - ERRO: {e}")
        return False
    
    try:
        import logging
        print("✅ logging - OK")
    except ImportError as e:
        print(f"❌ logging - ERRO: {e}")
        return False
    
    return True

def testar_arquivos():
    """Testa se todos os arquivos necessários existem"""
    print("\n📁 Testando arquivos...")
    
    arquivos_necessarios = [
        "ataque_otimizado.py",
        "monitor_sistema.py", 
        "iniciar_sistema.py",
        "config_votacao.py",
        "requirements.txt"
    ]
    
    todos_ok = True
    for arquivo in arquivos_necessarios:
        if os.path.exists(arquivo):
            print(f"✅ {arquivo} - OK")
        else:
            print(f"❌ {arquivo} - FALTANDO")
            todos_ok = False
    
    return todos_ok

def testar_configuracao():
    """Testa se a configuração está válida"""
    print("\n⚙️ Testando configuração...")
    
    try:
        from config_votacao import CONFIGURACAO_BASICA, USER_AGENTS, HEADERS_BASE
        
        if CONFIGURACAO_BASICA["url"]:
            print("✅ URL configurada - OK")
        else:
            print("❌ URL não configurada")
            return False
        
        if CONFIGURACAO_BASICA["token_prefix"]:
            print("✅ Token prefix configurado - OK")
        else:
            print("❌ Token prefix não configurado")
            return False
        
        if len(USER_AGENTS) > 0:
            print(f"✅ {len(USER_AGENTS)} User Agents configurados - OK")
        else:
            print("❌ Nenhum User Agent configurado")
            return False
        
        if len(HEADERS_BASE) > 0:
            print(f"✅ {len(HEADERS_BASE)} Headers configurados - OK")
        else:
            print("❌ Headers não configurados")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao testar configuração: {e}")
        return False

def testar_conectividade():
    """Testa conectividade básica"""
    print("\n🌐 Testando conectividade...")
    
    try:
        import requests
        from config_votacao import CONFIGURACAO_BASICA
        
        response = requests.get(CONFIGURACAO_BASICA["url"], timeout=10)
        if response.status_code == 200:
            print("✅ Servidor respondendo - OK")
            return True
        else:
            print(f"⚠️ Servidor retornou status {response.status_code}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Timeout ao conectar com servidor")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ Erro de conexão com servidor")
        return False
    except Exception as e:
        print(f"❌ Erro ao testar conectividade: {e}")
        return False

def testar_sistema_principal():
    """Testa se o sistema principal pode ser importado"""
    print("\n🚀 Testando sistema principal...")
    
    try:
        # Testar importação das classes
        sys.path.append('.')
        from ataque_otimizado import ConfiguracaoSistema, SistemaVotacao
        
        # Testar criação de instâncias
        config = ConfiguracaoSistema()
        print("✅ ConfiguraçãoSistema - OK")
        
        sistema = SistemaVotacao()
        print("✅ SistemaVotacao - OK")
        
        # Testar métodos básicos
        headers = sistema.gerar_headers()
        if headers and "user-agent" in headers:
            print("✅ Geração de headers - OK")
        else:
            print("❌ Geração de headers falhou")
            return False
        
        payload = sistema.criar_payload("test")
        if payload and "submitVote" in payload:
            print("✅ Criação de payload - OK")
        else:
            print("❌ Criação de payload falhou")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao testar sistema principal: {e}")
        return False

def testar_monitor():
    """Testa se o monitor pode ser importado"""
    print("\n🔍 Testando monitor...")
    
    try:
        sys.path.append('.')
        from monitor_sistema import MonitorSistema
        
        monitor = MonitorSistema()
        print("✅ MonitorSistema - OK")
        
        # Testar verificação de processo
        proc = monitor.verificar_processo_rodando()
        print("✅ Verificação de processo - OK")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao testar monitor: {e}")
        return False

def testar_salvamento_progresso():
    """Testa o sistema de salvamento de progresso"""
    print("\n💾 Testando salvamento de progresso...")
    
    try:
        # Criar dados de teste
        progresso_teste = {
            "total_votos": 100,
            "votos_sucesso": 95,
            "votos_erro": 5,
            "timestamp": datetime.now().isoformat(),
            "tempo_execucao": 3600
        }
        
        # Salvar
        with open("teste_progresso.json", "w") as f:
            json.dump(progresso_teste, f, indent=2)
        print("✅ Salvamento - OK")
        
        # Carregar
        with open("teste_progresso.json", "r") as f:
            progresso_carregado = json.load(f)
        
        if progresso_carregado["total_votos"] == 100:
            print("✅ Carregamento - OK")
        else:
            print("❌ Carregamento falhou")
            return False
        
        # Limpar arquivo de teste
        os.remove("teste_progresso.json")
        print("✅ Limpeza - OK")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao testar salvamento: {e}")
        return False

def main():
    """Função principal do teste"""
    print("🧪 TESTE RÁPIDO DO SISTEMA DE VOTAÇÃO")
    print("=" * 50)
    
    testes = [
        ("Imports", testar_imports),
        ("Arquivos", testar_arquivos),
        ("Configuração", testar_configuracao),
        ("Conectividade", testar_conectividade),
        ("Sistema Principal", testar_sistema_principal),
        ("Monitor", testar_monitor),
        ("Salvamento", testar_salvamento_progresso)
    ]
    
    resultados = []
    
    for nome, teste in testes:
        try:
            resultado = teste()
            resultados.append((nome, resultado))
        except Exception as e:
            print(f"❌ Erro no teste {nome}: {e}")
            resultados.append((nome, False))
    
    # Resumo
    print("\n" + "=" * 50)
    print("📊 RESUMO DOS TESTES")
    print("=" * 50)
    
    sucessos = 0
    for nome, resultado in resultados:
        status = "✅ PASSOU" if resultado else "❌ FALHOU"
        print(f"{nome}: {status}")
        if resultado:
            sucessos += 1
    
    print(f"\n🎯 Resultado: {sucessos}/{len(resultados)} testes passaram")
    
    if sucessos == len(resultados):
        print("🎉 SISTEMA PRONTO PARA USO!")
        print("\nPara iniciar:")
        print("  python iniciar_sistema.py")
    else:
        print("⚠️ Alguns testes falharam. Verifique os erros acima.")
        print("\nPara instalar dependências:")
        print("  pip install -r requirements.txt")

if __name__ == "__main__":
    main()
