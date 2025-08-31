#!/usr/bin/env python3
"""
Script de Inicialização ESTÁVEL
Sistema otimizado para estabilidade e menos erros
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
    print("=" * 70)
    print("🚀 SISTEMA DE VOTAÇÃO ESTÁVEL")
    print("=" * 70)
    print("Versão INFINITA - Otimizada para SUCESSOS")
    print("Threads: 2-4 SIMULTÂNEOS")
    print("Delays: 1.5-2.5 segundos")
    print("Foco: ESTABILIDADE E SUCESSOS")
    print("=" * 70)

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
    print("\n📋 MODOS DE EXECUÇÃO ESTÁVEL:")
    print("1. 🚀 Sistema ESTÁVEL (Recomendado)")
    print("2. 🔍 Sistema + Monitor Automático")
    print("3. 🔧 Apenas Monitor")
    print("4. 📊 Verificar Status")
    print("5. 🛑 Parar Todos os Processos")
    print("6. 📁 Ver Logs")
    print("7. ⚡ Modo RÁPIDO (Cuidado)")
    print("8. 📈 Ver Estatísticas de Estabilidade")
    print("0. ❌ Sair")
    print("-" * 50)

def executar_sistema_estavel():
    """Executa o sistema estável"""
    print("\n🚀 Iniciando Sistema ESTÁVEL...")
    print("🎯 Objetivo: VOTAR INFINITAMENTE COM ESTABILIDADE")
    print("⚡ Velocidade: OTIMIZADA PARA SUCESSOS")
    print("🔄 Loop: INFINITO")
    print("Pressione Ctrl+C para parar")
    print("-" * 50)
    
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
    print("Velocidade: OTIMIZADA PARA ESTABILIDADE")
    print("-" * 50)
    
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
    print("-" * 50)
    
    try:
        subprocess.run([sys.executable, "monitor_sistema.py"])
    except KeyboardInterrupt:
        print("\n🛑 Monitor interrompido pelo usuário")
    except Exception as e:
        print(f"❌ Erro ao executar monitor: {e}")

def modo_rapido():
    """Modo RÁPIDO - Cuidado com erros"""
    print("\n⚡ MODO RÁPIDO ATIVADO!")
    print("🚀 Velocidade: AUMENTADA")
    print("🎯 Threads: 4-6 SIMULTÂNEOS")
    print("⏱️  Delays: 0.8-1.5 segundos")
    print("🔄 Loop: INFINITO")
    print("⚠️  ATENÇÃO: Pode gerar mais erros!")
    print("-" * 50)
    
    confirmacao = input("Confirma execução em modo RÁPIDO? (s/n): ").lower()
    if confirmacao == 's':
        try:
            subprocess.run([sys.executable, "ataque_otimizado.py"])
        except KeyboardInterrupt:
            print("\n🛑 Modo RÁPIDO interrompido")
        except Exception as e:
            print(f"❌ Erro no modo RÁPIDO: {e}")
    else:
        print("❌ Modo RÁPIDO cancelado")

def verificar_status():
    """Verifica o status dos processos"""
    print("\n📊 VERIFICANDO STATUS...")
    print("-" * 50)
    
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
            
            total_votos = progress.get('total_votos', 0)
            votos_sucesso = progress.get('votos_sucesso', 0)
            votos_erro = progress.get('votos_erro', 0)
            
            print(f"📈 Progresso: {total_votos} votos")
            print(f"✅ Sucessos: {votos_sucesso}")
            print(f"❌ Erros: {votos_erro}")
            
            # Calcular taxa de sucesso
            if total_votos > 0:
                taxa_sucesso = (votos_sucesso / total_votos) * 100
                print(f"🎯 Taxa de sucesso: {taxa_sucesso:.1f}%")
                
                # Avaliar qualidade
                if taxa_sucesso >= 80:
                    print("🟢 EXCELENTE - Taxa de sucesso muito boa!")
                elif taxa_sucesso >= 60:
                    print("🟡 BOM - Taxa de sucesso aceitável")
                elif taxa_sucesso >= 40:
                    print("🟠 REGULAR - Taxa de sucesso baixa")
                else:
                    print("🔴 RUIM - Taxa de sucesso muito baixa")
            
            print(f"🔄 Lote atual: {progress.get('lote_atual', 0)}")
            
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
    print("-" * 50)
    
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
    print("-" * 50)
    
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

def mostrar_estatisticas_estabilidade():
    """Mostra estatísticas de estabilidade"""
    print("\n📈 ESTATÍSTICAS DE ESTABILIDADE:")
    print("-" * 50)
    print("🚀 Modo ESTÁVEL:")
    print("   • Delays: 1.5-2.5 segundos")
    print("   • Threads: 2-4 simultâneos")
    print("   • Velocidade esperada: ~3.000-5.000 votos/hora")
    print("   • Taxa de sucesso esperada: 70-90%")
    print("   • Lotes: 2.000 votos cada")
    print("   • Pausas: 60-120 segundos entre lotes")
    print()
    print("⚡ Modo RÁPIDO:")
    print("   • Delays: 0.8-1.5 segundos")
    print("   • Threads: 4-6 simultâneos")
    print("   • Velocidade esperada: ~6.000-10.000 votos/hora")
    print("   • Taxa de sucesso esperada: 50-70%")
    print("   • Risco de erro aumentado")
    print()
    print("🎯 RECOMENDAÇÕES:")
    print("   • Use modo ESTÁVEL para máxima confiabilidade")
    print("   • Monitore a taxa de sucesso")
    print("   • Se taxa < 50%, reduza velocidade")
    print("   • Se taxa > 80%, pode aumentar velocidade")

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
                executar_sistema_estavel()
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
            elif opcao == "7":
                modo_rapido()
            elif opcao == "8":
                mostrar_estatisticas_estabilidade()
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
