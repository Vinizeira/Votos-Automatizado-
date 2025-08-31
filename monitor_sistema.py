#!/usr/bin/env python3
"""
Monitor do Sistema de Votação
Verifica se o sistema principal está funcionando e pode reiniciá-lo automaticamente
"""

import os
import time
import subprocess
import json
import logging
from datetime import datetime, timedelta
import psutil
import signal
import sys

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('monitor.log'),
        logging.StreamHandler()
    ]
)

class MonitorSistema:
    def __init__(self):
        self.script_principal = "ataque_otimizado.py"
        self.progresso_file = "progresso_votacao.json"
        self.process = None
        self.max_restarts = 5
        self.restart_count = 0
        self.last_progress_check = time.time()
        self.last_progress_votos = 0
        
    def verificar_processo_rodando(self):
        """Verifica se o processo principal está rodando"""
        try:
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                if proc.info['cmdline'] and self.script_principal in ' '.join(proc.info['cmdline']):
                    return proc
            return None
        except Exception as e:
            logging.error(f"Erro ao verificar processo: {e}")
            return None
    
    def verificar_progresso(self):
        """Verifica se o progresso está sendo atualizado"""
        try:
            if not os.path.exists(self.progresso_file):
                return False
                
            # Verificar se o arquivo foi modificado recentemente
            mtime = os.path.getmtime(self.progresso_file)
            if time.time() - mtime > 300:  # 5 minutos
                logging.warning("Arquivo de progresso não atualizado há mais de 5 minutos")
                return False
            
            # Verificar se o número de votos aumentou
            with open(self.progresso_file, 'r') as f:
                progress = json.load(f)
                current_votos = progress.get('total_votos', 0)
                
            if current_votos > self.last_progress_votos:
                self.last_progress_votos = current_votos
                self.last_progress_check = time.time()
                return True
            elif time.time() - self.last_progress_check > 600:  # 10 minutos sem progresso
                logging.warning("Sem progresso há mais de 10 minutos")
                return False
                
            return True
            
        except Exception as e:
            logging.error(f"Erro ao verificar progresso: {e}")
            return False
    
    def iniciar_processo(self):
        """Inicia o processo principal"""
        try:
            logging.info(f"Iniciando {self.script_principal}...")
            self.process = subprocess.Popen(
                [sys.executable, self.script_principal],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            self.restart_count += 1
            logging.info(f"Processo iniciado com PID: {self.process.pid}")
            return True
        except Exception as e:
            logging.error(f"Erro ao iniciar processo: {e}")
            return False
    
    def parar_processo(self):
        """Para o processo principal graciosamente"""
        if self.process:
            try:
                logging.info("Parando processo graciosamente...")
                self.process.terminate()
                
                # Aguardar até 30 segundos para terminação graciosa
                try:
                    self.process.wait(timeout=30)
                except subprocess.TimeoutExpired:
                    logging.warning("Processo não terminou graciosamente, forçando...")
                    self.process.kill()
                    self.process.wait()
                    
                logging.info("Processo parado")
            except Exception as e:
                logging.error(f"Erro ao parar processo: {e}")
    
    def verificar_saude_sistema(self):
        """Verifica a saúde geral do sistema"""
        try:
            # Verificar uso de CPU
            cpu_percent = psutil.cpu_percent(interval=1)
            if cpu_percent > 90:
                logging.warning(f"CPU muito alta: {cpu_percent}%")
            
            # Verificar uso de memória
            memory = psutil.virtual_memory()
            if memory.percent > 90:
                logging.warning(f"Memória muito alta: {memory.percent}%")
            
            # Verificar espaço em disco
            disk = psutil.disk_usage('/')
            if disk.percent > 90:
                logging.warning(f"Disco quase cheio: {disk.percent}%")
                
        except Exception as e:
            logging.error(f"Erro ao verificar saúde do sistema: {e}")
    
    def executar(self):
        """Executa o monitor principal"""
        logging.info("🚀 MONITOR DO SISTEMA INICIADO")
        logging.info("=" * 50)
        
        # Verificar se o script principal existe
        if not os.path.exists(self.script_principal):
            logging.error(f"Script principal não encontrado: {self.script_principal}")
            return
        
        # Iniciar processo se não estiver rodando
        if not self.verificar_processo_rodando():
            if not self.iniciar_processo():
                logging.error("Falha ao iniciar processo principal")
                return
        
        try:
            while True:
                # Verificar se o processo ainda está rodando
                proc = self.verificar_processo_rodando()
                if not proc:
                    logging.warning("Processo principal não está rodando!")
                    
                    if self.restart_count < self.max_restarts:
                        logging.info(f"Tentativa de reinicialização {self.restart_count + 1}/{self.max_restarts}")
                        if self.iniciar_processo():
                            time.sleep(10)  # Aguardar inicialização
                        else:
                            logging.error("Falha ao reiniciar processo")
                            break
                    else:
                        logging.error("Número máximo de reinicializações atingido")
                        break
                
                # Verificar progresso
                if not self.verificar_progresso():
                    logging.warning("Progresso não está sendo atualizado!")
                    
                    if self.restart_count < self.max_restarts:
                        logging.info("Reiniciando devido à falta de progresso...")
                        self.parar_processo()
                        time.sleep(5)
                        if self.iniciar_processo():
                            time.sleep(10)
                        else:
                            logging.error("Falha ao reiniciar processo")
                            break
                    else:
                        logging.error("Número máximo de reinicializações atingido")
                        break
                
                # Verificar saúde do sistema
                self.verificar_saude_sistema()
                
                # Log de status
                if proc:
                    logging.info(f"✅ Sistema OK - PID: {proc.pid} - Restarts: {self.restart_count}")
                
                # Aguardar próximo check
                time.sleep(60)  # Verificar a cada minuto
                
        except KeyboardInterrupt:
            logging.info("🛑 Monitor interrompido pelo usuário")
        except Exception as e:
            logging.error(f"Erro no monitor: {e}")
        finally:
            self.parar_processo()
            logging.info("👋 Monitor finalizado")

def main():
    """Função principal"""
    monitor = MonitorSistema()
    
    print("🔍 MONITOR DO SISTEMA DE VOTAÇÃO")
    print("=" * 40)
    print("Este monitor verifica se o sistema principal está funcionando")
    print("e reinicia automaticamente se necessário.")
    print("=" * 40)
    
    try:
        monitor.executar()
    except Exception as e:
        logging.error(f"Erro fatal no monitor: {e}")
        print(f"❌ Erro fatal: {e}")

if __name__ == "__main__":
    main()
