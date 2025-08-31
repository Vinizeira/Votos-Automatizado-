#!/usr/bin/env python3
"""
Script de Inicialização do Sistema de Votação
Permite escolher entre diferentes modos de execução
"""

import os
import sys
import subprocess
import time
import threading
from datetime import datetime

def limpar_tela():
    """Limpa a tela do terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_banner():
    """Mostra o banner do sistema"""
    print("=" * 60)
    print("🚀 SISTEMA DE VOTAÇÃO OTIMIZADO")
    print("=" * 60)
    print("Versão Melhorada - Com Proteções Avançadas")
    print("=" * 60)

def verificar_dependencias():
    """Verifica se todas as dependências estão instaladas"""
    print("🔧 Verificando dependências...")
    
    try:
        import requests
        print("✅ requests - OK")
    except ImportError:
        print("❌ requests - FALTANDO")
        return False
    
    try:
        import psutil
        print("✅ psutil - OK")
    except ImportError:
        print("❌ psutil - FALTANDO")
        return False
    
    print("✅ Todas as dependências estão instaladas!")
    return True

def mostrar_menu():
    """Mostra o menu principal"""
    print("\n📋 MODOS DE EXECUÇÃO:")
    print("1. 🚀 Sistema Principal (Recomendado)")
    print("2. 🔍 Sistema + Monitor Automático")
    print("3. 🔧 Apenas Monitor")
    print("4. 📊 Verificar Status")
    print("5. 🛑 Parar Todos os Processos")
    print("6. 📁 Ver Logs")
    print("0. ❌ Sair")
    print("-" * 40)

def executar_sistema_principal():
    """Executa apenas o sistema principal"""
    print("\n🚀 Iniciando Sistema Principal...")
    print("Pressione Ctrl+C para parar graciosamente")
    print("-" * 40)
    
    try:
        subprocess.run([sys.executable, "ataque_otimizado.py"])
    except KeyboardInterrupt:
        print("\n🛑 Sistema interrompido pelo usuário")
    except Exception as e:
        print(f"❌ Erro ao executar sistema: {e}")

def executar_com_monitor():
    """Executa o sistema com monitor automático"""
    print("\n🔍 Iniciando Sistema + Monitor...")
    print("O monitor reiniciará automaticamente se necessário")
    print("-" * 40)
    
    try:
        # Iniciar monitor em thread separada
        monitor_thread = threading.Thread(
            target=lambda: subprocess.run([sys.executable, "monitor_sistema.py"]),
            daemon=True
        )
        monitor_thread.start()
        
        # Aguardar um pouco para o monitor inicializar
        time.sleep(2)
        
        # Executar sistema principal
        subprocess.run([sys.executable, "ataque_otimizado.py"])
        
    except KeyboardInterrupt:
        print("\n🛑 Sistema interrompido pelo usuário")
    except Exception as e:
        print(f"❌ Erro ao executar sistema: {e}")

def executar_apenas_monitor():
    """Executa apenas o monitor"""
    print("\n🔍 Iniciando Monitor...")
    print("O monitor verificará e reiniciará o sistema automaticamente")
    print("-" * 40)
    
    try:
        subprocess.run([sys.executable, "monitor_sistema.py"])
    except KeyboardInterrupt:
        print("\n🛑 Monitor interrompido pelo usuário")
    except Exception as e:
        print(f"❌ Erro ao executar monitor: {e}")

def verificar_status():
    """Verifica o status dos processos"""
    print("\n📊 VERIFICANDO STATUS...")
    print("-" * 40)
    
    try:
        import psutil
        
        # Verificar processo principal
        principal_rodando = False
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            if proc.info['cmdline'] and 'ataque_otimizado.py' in ' '.join(proc.info['cmdline']):
                print(f"✅ Sistema Principal: RODANDO (PID: {proc.pid})")
                principal_rodando = True
                break
        
        if not principal_rodando:
            print("❌ Sistema Principal: PARADO")
        
        # Verificar monitor
        monitor_rodando = False
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            if proc.info['cmdline'] and 'monitor_sistema.py' in ' '.join(proc.info['cmdline']):
                print(f"✅ Monitor: RODANDO (PID: {proc.pid})")
                monitor_rodando = True
                break
        
        if not monitor_rodando:
            print("❌ Monitor: PARADO")
        
        # Verificar arquivo de progresso
        if os.path.exists("progresso_votacao.json"):
            import json
            with open("progresso_votacao.json", "r") as f:
                progress = json.load(f)
            
            print(f"📈 Progresso: {progress.get('total_votos', 0)} votos")
            print(f"✅ Sucessos: {progress.get('votos_sucesso', 0)}")
            print(f"❌ Erros: {progress.get('votos_erro', 0)}")
            
            if 'timestamp' in progress:
                print(f"🕐 Última atualização: {progress['timestamp']}")
        else:
            print("📈 Progresso: Nenhum arquivo encontrado")
        
        # Verificar logs
        if os.path.exists("votacao.log"):
            size = os.path.getsize("votacao.log")
            print(f"📝 Log principal: {size} bytes")
        
        if os.path.exists("monitor.log"):
            size = os.path.getsize("monitor.log")
            print(f"📝 Log monitor: {size} bytes")
            
    except Exception as e:
        print(f"❌ Erro ao verificar status: {e}")

def parar_processos():
    """Para todos os processos relacionados"""
    print("\n🛑 PARANDO PROCESSOS...")
    print("-" * 40)
    
    try:
        import psutil
        
        processos_parados = 0
        
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            if proc.info['cmdline']:
                cmdline = ' '.join(proc.info['cmdline'])
                if 'ataque_otimizado.py' in cmdline or 'monitor_sistema.py' in cmdline:
                    try:
                        print(f"🛑 Parando processo {proc.pid}...")
                        proc.terminate()
                        proc.wait(timeout=10)
                        processos_parados += 1
                        print(f"✅ Processo {proc.pid} parado")
                    except psutil.TimeoutExpired:
                        print(f"⚠️ Forçando parada do processo {proc.pid}...")
                        proc.kill()
                        processos_parados += 1
                    except Exception as e:
                        print(f"❌ Erro ao parar processo {proc.pid}: {e}")
        
        if processos_parados == 0:
            print("ℹ️ Nenhum processo encontrado para parar")
        else:
            print(f"✅ {processos_parados} processo(s) parado(s)")
            
    except Exception as e:
        print(f"❌ Erro ao parar processos: {e}")

def ver_logs():
    """Mostra os logs recentes"""
    print("\n📁 LOGS RECENTES:")
    print("-" * 40)
    
    def mostrar_log(arquivo, titulo):
        if os.path.exists(arquivo):
            print(f"\n📝 {titulo}:")
            print("-" * 30)
            try:
                with open(arquivo, 'r', encoding='utf-8') as f:
                    linhas = f.readlines()
                    # Mostrar últimas 20 linhas
                    for linha in linhas[-20:]:
                        print(linha.strip())
            except Exception as e:
                print(f"❌ Erro ao ler {arquivo}: {e}")
        else:
            print(f"📝 {titulo}: Arquivo não encontrado")
    
    mostrar_log("votacao.log", "Log Principal")
    mostrar_log("monitor.log", "Log do Monitor")

def main():
    """Função principal"""
    while True:
        limpar_tela()
        mostrar_banner()
        
        if not verificar_dependencias():
            print("\n❌ Instale as dependências com: pip install -r requirements.txt")
            input("Pressione Enter para sair...")
            break
        
        mostrar_menu()
        
        try:
            opcao = input("\nEscolha uma opção: ").strip()
            
            if opcao == "1":
                executar_sistema_principal()
            elif opcao == "2":
                executar_com_monitor()
            elif opcao == "3":
                executar_apenas_monitor()
            elif opcao == "4":
                verificar_status()
                input("\nPressione Enter para continuar...")
            elif opcao == "5":
                parar_processos()
                input("\nPressione Enter para continuar...")
            elif opcao == "6":
                ver_logs()
                input("\nPressione Enter para continuar...")
            elif opcao == "0":
                print("\n👋 Saindo...")
                break
            else:
                print("❌ Opção inválida!")
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\n\n👋 Saindo...")
            break
        except Exception as e:
            print(f"\n❌ Erro: {e}")
            time.sleep(2)

if __name__ == "__main__":
    main()
