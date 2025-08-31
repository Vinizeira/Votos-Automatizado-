#!/usr/bin/env python3
"""
Script de Inicialização do Sistema de Votação
Versão Melhorada - Mais Robusta e Profissional
"""

import os
import sys
import subprocess
import time
import threading
import argparse
import logging
from datetime import datetime
from typing import Optional, Dict, Any

# Configurar logging centralizado
def setup_logging():
    """Configura o sistema de logging centralizado"""
    log_format = '%(asctime)s - %(levelname)s - %(message)s'
    
    # Criar diretório de logs se não existir
    os.makedirs('logs', exist_ok=True)
    
    # Configurar logging com rotação de arquivos
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=[
            logging.FileHandler('logs/sistema.log', encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    return logging.getLogger(__name__)

logger = setup_logging()

def limpar_tela():
    """Limpa a tela do terminal de forma mais robusta"""
    try:
        # Tentar usar ANSI escape codes primeiro
        print("\033c", end="")
    except:
        try:
            # Fallback para comandos do sistema
            os.system('cls' if os.name == 'nt' else 'clear')
        except:
            # Último recurso: imprimir várias linhas em branco
            print("\n" * 50)

def mostrar_banner():
    """Mostra o banner do sistema"""
    print("=" * 70)
    print("🚀 SISTEMA DE VOTAÇÃO OTIMIZADO")
    print("=" * 70)
    print("Versão Melhorada - Com Proteções Avançadas")
    print("=" * 70)

def verificar_dependencias():
    """Verifica se todas as dependências estão instaladas com instruções"""
    logger.info("🔧 Verificando dependências...")
    
    dependencias = {
        'requests': 'pip install requests',
        'psutil': 'pip install psutil',
        'threading': 'built-in',
        'logging': 'built-in'
    }
    
    todas_ok = True
    
    for modulo, comando in dependencias.items():
        try:
            __import__(modulo)
            logger.info(f"✅ {modulo} - OK")
        except ImportError:
            logger.error(f"❌ {modulo} - FALTANDO")
            if comando != 'built-in':
                logger.error(f"   Instale com: {comando}")
            todas_ok = False
    
    if todas_ok:
        logger.info("✅ Todas as dependências estão instaladas!")
    else:
        logger.error("❌ Algumas dependências estão faltando!")
        logger.info("💡 Execute: pip install -r requirements.txt")
    
    return todas_ok

def mostrar_menu():
    """Mostra o menu principal"""
    print("\n📋 MODOS DE EXECUÇÃO:")
    print("1. 🚀 Sistema Principal (Recomendado)")
    print("2. 🔍 Sistema + Monitor Automático")
    print("3. 🔧 Apenas Monitor")
    print("4. 📊 Verificar Status")
    print("5. 🛑 Parar Todos os Processos")
    print("6. 📁 Ver Logs")
    print("7. 🔄 Reiniciar Sistema")
    print("8. ⚙️  Configurações")
    print("0. ❌ Sair")
    print("-" * 40)

class ProcessoManager:
    """Gerencia processos do sistema de forma robusta"""
    
    def __init__(self):
        self.processos = {}
        self.lock = threading.Lock()
    
    def iniciar_processo(self, nome: str, comando: list, descricao: str = "") -> bool:
        """Inicia um processo com monitoramento"""
        try:
            logger.info(f"🚀 Iniciando {nome}: {descricao}")
            
            processo = subprocess.Popen(
                comando,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            with self.lock:
                self.processos[nome] = {
                    'processo': processo,
                    'comando': comando,
                    'descricao': descricao,
                    'inicio': datetime.now(),
                    'status': 'rodando'
                }
            
            logger.info(f"✅ {nome} iniciado com PID: {processo.pid}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro ao iniciar {nome}: {e}")
            return False
    
    def parar_processo(self, nome: str, timeout: int = 30) -> bool:
        """Para um processo graciosamente"""
        with self.lock:
            if nome not in self.processos:
                logger.warning(f"⚠️ Processo {nome} não encontrado")
                return False
            
            processo_info = self.processos[nome]
            processo = processo_info['processo']
        
        try:
            logger.info(f"🛑 Parando {nome} (PID: {processo.pid})...")
            
            # Tentar terminar graciosamente
            processo.terminate()
            
            try:
                processo.wait(timeout=timeout)
                logger.info(f"✅ {nome} parado graciosamente")
            except subprocess.TimeoutExpired:
                logger.warning(f"⚠️ {nome} não parou graciosamente, forçando...")
                processo.kill()
                processo.wait()
                logger.info(f"✅ {nome} forçado a parar")
            
            with self.lock:
                processo_info['status'] = 'parado'
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro ao parar {nome}: {e}")
            return False
    
    def verificar_processos(self) -> Dict[str, Dict]:
        """Verifica status de todos os processos"""
        with self.lock:
            processos_status = {}
            
            for nome, info in self.processos.items():
                processo = info['processo']
                
                # Verificar se processo ainda está rodando
                if processo.poll() is None:
                    info['status'] = 'rodando'
                    info['uptime'] = datetime.now() - info['inicio']
                else:
                    info['status'] = 'parado'
                    info['exit_code'] = processo.returncode
                
                processos_status[nome] = info.copy()
            
            return processos_status
    
    def parar_todos(self):
        """Para todos os processos"""
        logger.info("🛑 Parando todos os processos...")
        
        with self.lock:
            nomes = list(self.processos.keys())
        
        for nome in nomes:
            self.parar_processo(nome)

# Instância global do gerenciador de processos
processo_manager = ProcessoManager()

def executar_sistema_principal():
    """Executa apenas o sistema principal com monitoramento robusto"""
    logger.info("🚀 Iniciando Sistema Principal...")
    print("Pressione Ctrl+C para parar graciosamente")
    print("-" * 40)
    
    try:
        sucesso = processo_manager.iniciar_processo(
            "sistema_principal",
            [sys.executable, "ataque_otimizado.py"],
            "Sistema de votação principal"
        )
        
        if sucesso:
            # Monitorar o processo
            while True:
                status = processo_manager.verificar_processos()
                if status.get("sistema_principal", {}).get("status") != "rodando":
                    logger.warning("⚠️ Sistema principal parou inesperadamente")
                    break
                time.sleep(5)
        
    except KeyboardInterrupt:
        logger.info("🛑 Interrupção solicitada pelo usuário")
    except Exception as e:
        logger.error(f"❌ Erro ao executar sistema: {e}")
    finally:
        processo_manager.parar_processo("sistema_principal")

def executar_com_monitor():
    """Executa o sistema com monitor automático robusto"""
    logger.info("🔍 Iniciando Sistema + Monitor...")
    print("O monitor reiniciará automaticamente se necessário")
    print("-" * 40)
    
    try:
        # Iniciar monitor
        sucesso_monitor = processo_manager.iniciar_processo(
            "monitor",
            [sys.executable, "monitor_sistema.py"],
            "Monitor automático"
        )
        
        if sucesso_monitor:
            time.sleep(2)  # Aguardar inicialização do monitor
            
            # Iniciar sistema principal
            sucesso_sistema = processo_manager.iniciar_processo(
                "sistema_principal",
                [sys.executable, "ataque_otimizado.py"],
                "Sistema de votação principal"
            )
            
            if sucesso_sistema:
                # Monitorar ambos os processos
                while True:
                    status = processo_manager.verificar_processos()
                    
                    sistema_status = status.get("sistema_principal", {}).get("status")
                    monitor_status = status.get("monitor", {}).get("status")
                    
                    if sistema_status != "rodando" and monitor_status != "rodando":
                        logger.warning("⚠️ Ambos os processos pararam")
                        break
                    
                    time.sleep(10)
        
    except KeyboardInterrupt:
        logger.info("🛑 Interrupção solicitada pelo usuário")
    except Exception as e:
        logger.error(f"❌ Erro ao executar sistema: {e}")
    finally:
        processo_manager.parar_todos()

def executar_apenas_monitor():
    """Executa apenas o monitor com monitoramento robusto"""
    logger.info("🔍 Iniciando Monitor...")
    print("O monitor verificará e reiniciará o sistema automaticamente")
    print("-" * 40)
    
    try:
        sucesso = processo_manager.iniciar_processo(
            "monitor",
            [sys.executable, "monitor_sistema.py"],
            "Monitor automático"
        )
        
        if sucesso:
            # Monitorar o processo
            while True:
                status = processo_manager.verificar_processos()
                if status.get("monitor", {}).get("status") != "rodando":
                    logger.warning("⚠️ Monitor parou inesperadamente")
                    break
                time.sleep(10)
        
    except KeyboardInterrupt:
        logger.info("🛑 Interrupção solicitada pelo usuário")
    except Exception as e:
        logger.error(f"❌ Erro ao executar monitor: {e}")
    finally:
        processo_manager.parar_processo("monitor")

def verificar_status():
    """Verifica o status dos processos de forma otimizada"""
    logger.info("📊 Verificando status...")
    print("-" * 40)
    
    try:
        import psutil
        
        # Verificar processos gerenciados
        processos_gerenciados = processo_manager.verificar_processos()
        
        if processos_gerenciados:
            print("🔄 Processos Gerenciados:")
            for nome, info in processos_gerenciados.items():
                status = info['status']
                if status == 'rodando':
                    uptime = info.get('uptime', datetime.now() - info['inicio'])
                    print(f"   ✅ {nome}: RODANDO (Uptime: {uptime})")
                else:
                    print(f"   ❌ {nome}: PARADO")
        else:
            print("ℹ️ Nenhum processo gerenciado encontrado")
        
        # Verificar todos os processos relacionados
        processos_encontrados = []
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            if proc.info['cmdline']:
                cmdline = ' '.join(proc.info['cmdline'])
                if any(script in cmdline for script in ['ataque_otimizado.py', 'monitor_sistema.py']):
                    processos_encontrados.append(proc)
        
        if processos_encontrados:
            print("\n🔍 Processos Encontrados no Sistema:")
            for proc in processos_encontrados:
                print(f"   ✅ PID {proc.pid}: {' '.join(proc.info['cmdline'])}")
        else:
            print("\nℹ️ Nenhum processo relacionado encontrado no sistema")
        
        # Verificar arquivo de progresso
        if os.path.exists("progresso_votacao.json"):
            import json
            with open("progresso_votacao.json", "r") as f:
                progress = json.load(f)
            
            total_votos = progress.get('total_votos', 0)
            votos_sucesso = progress.get('votos_sucesso', 0)
            votos_erro = progress.get('votos_erro', 0)
            
            print(f"\n📈 Progresso: {total_votos} votos")
            print(f"✅ Sucessos: {votos_sucesso}")
            print(f"❌ Erros: {votos_erro}")
            
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
            
            if 'timestamp' in progress:
                print(f"🕐 Última atualização: {progress['timestamp']}")
        else:
            print("\n📈 Progresso: Nenhum arquivo encontrado")
        
        # Verificar logs
        if os.path.exists("logs/sistema.log"):
            size = os.path.getsize("logs/sistema.log")
            print(f"\n📝 Log do sistema: {size} bytes")
        
        if os.path.exists("votacao.log"):
            size = os.path.getsize("votacao.log")
            print(f"📝 Log de votação: {size} bytes")
            
    except Exception as e:
        logger.error(f"❌ Erro ao verificar status: {e}")

def parar_processos():
    """Para todos os processos relacionados"""
    logger.info("🛑 Parando processos...")
    print("-" * 40)
    
    try:
        # Parar processos gerenciados
        processo_manager.parar_todos()
        
        # Parar processos não gerenciados
        import psutil
        processos_parados = 0
        
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            if proc.info['cmdline']:
                cmdline = ' '.join(proc.info['cmdline'])
                if any(script in cmdline for script in ['ataque_otimizado.py', 'monitor_sistema.py']):
                    try:
                        logger.info(f"🛑 Parando processo {proc.pid}...")
                        proc.terminate()
                        proc.wait(timeout=10)
                        processos_parados += 1
                        logger.info(f"✅ Processo {proc.pid} parado")
                    except psutil.TimeoutExpired:
                        logger.warning(f"⚠️ Forçando parada do processo {proc.pid}...")
                        proc.kill()
                        processos_parados += 1
                    except Exception as e:
                        logger.error(f"❌ Erro ao parar processo {proc.pid}: {e}")
        
        if processos_parados == 0:
            logger.info("ℹ️ Nenhum processo encontrado para parar")
        else:
            logger.info(f"✅ {processos_parados} processo(s) parado(s)")
            
    except Exception as e:
        logger.error(f"❌ Erro ao parar processos: {e}")

def ver_logs():
    """Mostra os logs recentes de forma organizada"""
    logger.info("📁 Exibindo logs recentes...")
    print("-" * 40)
    
    def mostrar_log(arquivo, titulo, max_linhas=20):
        if os.path.exists(arquivo):
            print(f"\n📝 {titulo}:")
            print("-" * 30)
            try:
                with open(arquivo, 'r', encoding='utf-8') as f:
                    linhas = f.readlines()
                    # Mostrar últimas linhas
                    for linha in linhas[-max_linhas:]:
                        print(linha.strip())
            except Exception as e:
                logger.error(f"❌ Erro ao ler {arquivo}: {e}")
        else:
            print(f"📝 {titulo}: Arquivo não encontrado")
    
    mostrar_log("logs/sistema.log", "Log do Sistema")
    mostrar_log("votacao.log", "Log de Votação")
    mostrar_log("monitor.log", "Log do Monitor")

def reiniciar_sistema():
    """Reinicia o sistema sem precisar parar e rodar de novo"""
    logger.info("🔄 Reiniciando sistema...")
    print("-" * 40)
    
    try:
        # Parar processos atuais
        processo_manager.parar_todos()
        
        # Aguardar um pouco
        time.sleep(3)
        
        # Reiniciar sistema principal
        sucesso = processo_manager.iniciar_processo(
            "sistema_principal",
            [sys.executable, "ataque_otimizado.py"],
            "Sistema de votação principal (reiniciado)"
        )
        
        if sucesso:
            logger.info("✅ Sistema reiniciado com sucesso!")
            print("🔄 Sistema reiniciado! Monitorando...")
            
            # Monitorar o processo reiniciado
            while True:
                status = processo_manager.verificar_processos()
                if status.get("sistema_principal", {}).get("status") != "rodando":
                    logger.warning("⚠️ Sistema parou após reinicialização")
                    break
                time.sleep(5)
        else:
            logger.error("❌ Falha ao reiniciar sistema")
        
    except KeyboardInterrupt:
        logger.info("🛑 Reinicialização interrompida")
    except Exception as e:
        logger.error(f"❌ Erro ao reiniciar sistema: {e}")
    finally:
        processo_manager.parar_processo("sistema_principal")

def mostrar_configuracoes():
    """Mostra e permite alterar configurações"""
    logger.info("⚙️ Exibindo configurações...")
    print("-" * 40)
    
    print("🔧 CONFIGURAÇÕES ATUAIS:")
    print("   • Logs: logs/sistema.log")
    print("   • Progresso: progresso_votacao.json")
    print("   • Monitoramento: Ativo")
    print("   • Timeout: 30 segundos")
    print("   • Verificação: A cada 10 segundos")
    print()
    print("📁 ARQUIVOS IMPORTANTES:")
    print("   • ataque_otimizado.py - Sistema principal")
    print("   • monitor_sistema.py - Monitor automático")
    print("   • config_votacao.py - Configurações")
    print("   • requirements.txt - Dependências")
    print()
    print("💡 DICAS:")
    print("   • Use Ctrl+C para parar graciosamente")
    print("   • Monitore a taxa de sucesso")
    print("   • Verifique os logs regularmente")

def main():
    """Função principal com suporte a argumentos de linha de comando"""
    parser = argparse.ArgumentParser(description='Sistema de Votação Otimizado')
    parser.add_argument('--modo', choices=['principal', 'monitor', 'status', 'parar'], 
                       help='Modo de execução')
    parser.add_argument('--log-level', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
                       default='INFO', help='Nível de log')
    
    args = parser.parse_args()
    
    # Configurar nível de log
    logging.getLogger().setLevel(getattr(logging, args.log_level))
    
    # Se modo especificado, executar diretamente
    if args.modo:
        logger.info(f"🚀 Executando em modo: {args.modo}")
        
        if args.modo == 'principal':
            executar_sistema_principal()
        elif args.modo == 'monitor':
            executar_apenas_monitor()
        elif args.modo == 'status':
            verificar_status()
        elif args.modo == 'parar':
            parar_processos()
        return
    
    # Modo interativo
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
            elif opcao == "7":
                reiniciar_sistema()
            elif opcao == "8":
                mostrar_configuracoes()
                input("\nPressione Enter para continuar...")
            elif opcao == "0":
                logger.info("👋 Saindo...")
                processo_manager.parar_todos()
                break
            else:
                logger.warning("❌ Opção inválida!")
                time.sleep(1)
                
        except KeyboardInterrupt:
            logger.info("\n🛑 Interrupção solicitada pelo usuário")
            processo_manager.parar_todos()
            break
        except Exception as e:
            logger.error(f"\n❌ Erro: {e}")
            time.sleep(2)

if __name__ == "__main__":
    main()
