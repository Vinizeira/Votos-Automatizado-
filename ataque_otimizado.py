import requests
import time
import random
import urllib.parse
import threading
from datetime import datetime
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
import socket
import ssl
import signal
import sys
import os
from typing import Optional, Dict, Any
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('votacao.log'),
        logging.StreamHandler()
    ]
)

# Configurações do sistema
class ConfiguracaoSistema:
    def __init__(self):
        self.url = "https://script.google.com/macros/s/AKfycbyx6hsWgd8fkhw3cGCCtVGH9GTN7BCTdlGnx9uiAkBG1cHPIDFvE-RmUB8S-2zjxgI2Aw/callback"
        self.TOKEN_PREFIX = "AJuLMu0DuqqeqSFlMzAPQNVmARHZs6LnxQ"
        
        # Lista de navegadores
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/119.0.0.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0"
        ]
        
        # Headers padrão
        self.base_headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "pt-BR,pt;q=0.9,en;q=0.8",
            "cache-control": "no-cache",
            "content-type": "application/x-www-form-urlencoded;charset=UTF-8",
            "origin": "https://script.google.com",
            "pragma": "no-cache",
            "referer": "https://script.google.com/macros/s/AKfycbyx6hsWgd8fkhw3cGCCtVGH9GTN7BCTdlGnx9uiAkBG1cHPIDFvE-RmUB8S-2zjxgI2Aw/exec",
            "sec-ch-ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "upgrade-insecure-requests": "1",
            "x-same-domain": "1"
        }
        
        # Intervalos de espera AJUSTADOS para estabilidade
        self.delays = {
            "estavel": {"min": 1.5, "max": 2.5},      # Muito estável
            "normal": {"min": 1.0, "max": 1.8},       # Normal
            "rapido": {"min": 0.8, "max": 1.5},       # Rápido mas seguro
            "ultra_rapido": {"min": 0.5, "max": 1.0}  # Ultra rápido (cuidado)
        }
        
        # Configuração dos lotes AJUSTADA para estabilidade
        self.lotes = [
            {"quantidade": 2000, "delay": "estavel", "pausa_apos": 120, "threads": 2},
            {"quantidade": 2000, "delay": "estavel", "pausa_apos": 120, "threads": 2},
            {"quantidade": 2000, "delay": "normal", "pausa_apos": 90, "threads": 3},
            {"quantidade": 2000, "delay": "normal", "pausa_apos": 90, "threads": 3},
            {"quantidade": 2000, "delay": "rapido", "pausa_apos": 60, "threads": 4},
            {"quantidade": 2000, "delay": "rapido", "pausa_apos": 60, "threads": 4}
        ]
        
        # Configurações de retry e recuperação AJUSTADAS
        self.retry_config = {
            "max_retries": 3,        # Mais tentativas para sucesso
            "retry_delay": 3,        # Delay maior entre tentativas
            "backoff_factor": 2,     # Backoff mais agressivo
            "max_backoff": 30        # Backoff máximo maior
        }
        
        # Configurações de saúde do sistema AJUSTADAS
        self.health_config = {
            "max_consecutive_errors": 15,     # Mais tolerante
            "error_threshold_percent": 40,    # Mais tolerante
            "health_check_interval": 180,     # Verificar menos frequentemente
            "auto_restart_threshold": 60      # Mais tolerante
        }

class SistemaVotacao:
    def __init__(self):
        self.config = ConfiguracaoSistema()
        self.session = requests.Session()
        self.total_votos = 0
        self.votos_sucesso = 0
        self.votos_erro = 0
        self.inicio_total = time.time()
        self.lock = threading.Lock()
        self.running = True
        self.consecutive_errors = 0
        self.last_success_time = time.time()
        self.health_monitor_thread = None
        self.lote_atual = 0
        self.votos_este_lote = 0
        self.ultimo_sucesso = time.time()
        
        # Configurar sessão
        self.session.headers.update(self.config.base_headers)
        
        # Configurar timeout da sessão AJUSTADO
        self.session.timeout = (10, 25)  # Timeouts mais conservadores
        
        # Configurar retry adapter AJUSTADO
        retry_adapter = requests.adapters.HTTPAdapter(
            max_retries=2,           # Menos retries automáticos
            pool_connections=10,     # Menos conexões simultâneas
            pool_maxsize=20          # Pool menor
        )
        self.session.mount('http://', retry_adapter)
        self.session.mount('https://', retry_adapter)
        
        # Configurar handlers de sinal para graceful shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        # Iniciar monitor de saúde
        self.start_health_monitor()
        
    def signal_handler(self, signum, frame):
        """Handler para sinais de interrupção"""
        print(f"\n🛑 Recebido sinal {signum}. Finalizando graciosamente...")
        self.running = False
        self.save_progress()
        sys.exit(0)
        
    def save_progress(self):
        """Salva o progresso atual"""
        progress = {
            "total_votos": self.total_votos,
            "votos_sucesso": self.votos_sucesso,
            "votos_erro": self.votos_erro,
            "timestamp": datetime.now().isoformat(),
            "tempo_execucao": time.time() - self.inicio_total,
            "lote_atual": self.lote_atual,
            "votos_este_lote": self.votos_este_lote
        }
        
        try:
            with open("progresso_votacao.json", "w") as f:
                json.dump(progress, f, indent=2)
            print("💾 Progresso salvo!")
        except Exception as e:
            logging.error(f"Erro ao salvar progresso: {e}")
    
    def load_progress(self):
        """Carrega progresso salvo anteriormente"""
        try:
            if os.path.exists("progresso_votacao.json"):
                with open("progresso_votacao.json", "r") as f:
                    progress = json.load(f)
                
                self.total_votos = progress.get("total_votos", 0)
                self.votos_sucesso = progress.get("votos_sucesso", 0)
                self.votos_erro = progress.get("votos_erro", 0)
                self.lote_atual = progress.get("lote_atual", 0)
                self.votos_este_lote = progress.get("votos_este_lote", 0)
                print(f"📂 Progresso carregado: {self.total_votos} votos (Lote {self.lote_atual})")
                return True
        except Exception as e:
            logging.error(f"Erro ao carregar progresso: {e}")
        return False
    
    def start_health_monitor(self):
        """Inicia o monitor de saúde do sistema"""
        def health_monitor():
            while self.running:
                try:
                    time.sleep(self.config.health_config["health_check_interval"])
                    self.check_system_health()
                except Exception as e:
                    logging.error(f"Erro no monitor de saúde: {e}")
        
        self.health_monitor_thread = threading.Thread(target=health_monitor, daemon=True)
        self.health_monitor_thread.start()
    
    def check_system_health(self):
        """Verifica a saúde do sistema"""
        try:
            # Verificar taxa de erro
            if self.total_votos > 0:
                error_rate = (self.votos_erro / self.total_votos) * 100
                if error_rate > self.config.health_config["error_threshold_percent"]:
                    logging.warning(f"Taxa de erro alta: {error_rate:.1f}%")
                    
                    # Reduzir velocidade se necessário
                    if error_rate > self.config.health_config["auto_restart_threshold"]:
                        logging.warning("Taxa de erro muito alta. Pausa de 60s...")
                        time.sleep(60)  # Pausa maior para estabilizar
            
            # Verificar se houve sucessos recentes
            time_since_last_success = time.time() - self.last_success_time
            if time_since_last_success > 300:  # 5 minutos sem sucesso
                logging.warning("Muito tempo sem sucessos. Verificando conexão...")
                self.test_connection()
                
        except Exception as e:
            logging.error(f"Erro na verificação de saúde: {e}")
    
    def test_connection(self):
        """Testa a conexão com o servidor"""
        try:
            response = self.session.get(self.config.url, timeout=10)
            if response.status_code == 200:
                logging.info("✅ Conexão OK")
                return True
            else:
                logging.warning(f"⚠️ Servidor retornou status {response.status_code}")
                return False
        except Exception as e:
            logging.error(f"❌ Erro de conexão: {e}")
            return False
    
    def gerar_headers(self):
        """Gera headers únicos para cada requisição"""
        headers = self.config.base_headers.copy()
        headers["user-agent"] = random.choice(self.config.user_agents)
        
        # Variações nos headers
        if random.random() < 0.3:
            headers["accept-encoding"] = "gzip, deflate"
        if random.random() < 0.2:
            headers["accept-language"] = "en-US,en;q=0.9"
        
        return headers
    
    def criar_payload(self, user_agent):
        """Cria payload com variações"""
        candidate_id = "12"
        if random.random() < 0.05:
            candidate_id = str(random.randint(10, 15))
            
        return f'["submitVote","[{{\\"id\\":\\"{candidate_id}\\",\\"userAgent\\":\\"{user_agent}\\"}}]",null,[0],null,null,1,0]'
    
    def obter_delay(self, tipo_delay):
        """Retorna delay com variações AJUSTADO"""
        delay_config = self.config.delays[tipo_delay]
        delay_base = random.uniform(delay_config["min"], delay_config["max"])
        
        # Variação pequena
        variacao = random.uniform(-0.1, 0.1)
        return max(0.5, delay_base + variacao)  # Mínimo aumentado
    
    def enviar_voto_com_retry(self, vote_id):
        """Envia um voto com sistema de retry AJUSTADO"""
        for attempt in range(self.config.retry_config["max_retries"]):
            try:
                success, result = self.enviar_voto(vote_id)
                
                if success:
                    self.consecutive_errors = 0
                    self.last_success_time = time.time()
                    self.ultimo_sucesso = time.time()
                    return True, result
                else:
                    self.consecutive_errors += 1
                    
                    # Se muitos erros consecutivos, pausa mais longa
                    if self.consecutive_errors > self.config.health_config["max_consecutive_errors"]:
                        logging.warning(f"Muitos erros consecutivos ({self.consecutive_errors}). Pausa de 60s...")
                        time.sleep(60)  # Pausa maior para estabilizar
                        self.consecutive_errors = 0
                    
                    # Retry com backoff exponencial AJUSTADO
                    if attempt < self.config.retry_config["max_retries"] - 1:
                        delay = min(
                            self.config.retry_config["retry_delay"] * (self.config.retry_config["backoff_factor"] ** attempt),
                            self.config.retry_config["max_backoff"]
                        )
                        time.sleep(delay)
                        
            except Exception as e:
                logging.error(f"Erro na tentativa {attempt + 1}: {e}")
                self.consecutive_errors += 1
                
                if attempt < self.config.retry_config["max_retries"] - 1:
                    time.sleep(self.config.retry_config["retry_delay"])
        
        return False, "max_retries_exceeded"
    
    def enviar_voto(self, vote_id):
        """Envia um voto individual AJUSTADO"""
        try:
            # Headers únicos
            headers = self.gerar_headers()
            user_agent = headers["user-agent"]
            
            # Payload
            payload_bruto = self.criar_payload(user_agent)
            payload_encoded = "request=" + urllib.parse.quote(payload_bruto, safe='')
            
            # Token
            ts = str(int(time.time() * 1000))
            token = f"{self.config.TOKEN_PREFIX}:{ts}"
            token_encoded = urllib.parse.quote(token, safe='')
            
            # Parâmetros
            nocache_aleatorio = str(random.randint(1, 100))
            params = {"nocache_id": nocache_aleatorio, "token": token_encoded}
            
            # Timeout dinâmico AJUSTADO
            timeout = random.uniform(8, 20)  # Timeouts mais conservadores
            
            # Enviar requisição
            response = self.session.post(
                self.config.url, 
                params=params, 
                headers=headers, 
                data=payload_encoded, 
                timeout=timeout
            )
            
            with self.lock:
                self.total_votos += 1
                self.votos_este_lote += 1
                
            if response.status_code == 200:
                with self.lock:
                    self.votos_sucesso += 1
                return True, "sucesso"
            else:
                with self.lock:
                    self.votos_erro += 1
                return False, f"erro_{response.status_code}"
                
        except requests.exceptions.Timeout:
            with self.lock:
                self.votos_erro += 1
            return False, "timeout"
        except requests.exceptions.ConnectionError:
            with self.lock:
                self.votos_erro += 1
            return False, "connection_error"
        except requests.exceptions.RequestException as e:
            with self.lock:
                self.votos_erro += 1
            return False, f"request_error: {str(e)}"
        except Exception as e:
            with self.lock:
                self.votos_erro += 1
            return False, str(e)
    
    def processar_lote(self, lote_config, lote_num):
        """Processa um lote de votos AJUSTADO"""
        quantidade = lote_config["quantidade"]
        delay_type = lote_config["delay"]
        pausa_apos = lote_config["pausa_apos"]
        max_threads = lote_config["threads"]
        
        print(f"\n📦 LOTE {lote_num}: {quantidade} votos (Threads: {max_threads})")
        print(f"   ⏱️  Delay: {self.config.delays[delay_type]['min']}-{self.config.delays[delay_type]['max']}s")
        print(f"   🕐 Início: {datetime.now().strftime('%H:%M:%S')}")
        
        inicio_lote = time.time()
        votos_enviados = 0
        ultimo_log = time.time()
        
        try:
            # Processamento paralelo com melhor controle
            with ThreadPoolExecutor(max_workers=max_threads) as executor:
                futures = []
                
                for i in range(quantidade):
                    if not self.running:
                        print("🛑 Sistema interrompido pelo usuário")
                        break
                        
                    future = executor.submit(self.enviar_voto_com_retry, i)
                    futures.append(future)
                    
                    delay = self.obter_delay(delay_type)
                    time.sleep(delay)
                    
                    # Log periódico AJUSTADO
                    if time.time() - ultimo_log > 15:  # Log a cada 15 segundos
                        self.log_progress()
                        ultimo_log = time.time()
                
                # Aguardar conclusão com timeout AJUSTADO
                for future in as_completed(futures, timeout=3600):  # 1 hora de timeout
                    try:
                        success, result = future.result(timeout=60)  # 1 minuto por resultado
                        if success:
                            votos_enviados += 1
                    except Exception as e:
                        logging.error(f"Erro no thread: {e}")
                        
        except Exception as e:
            logging.error(f"Erro no processamento do lote {lote_num}: {e}")
            print(f"⚠️ Erro no lote {lote_num}: {e}")
        
        # Estatísticas do lote
        tempo_lote = time.time() - inicio_lote
        votos_por_hora = votos_enviados / (tempo_lote / 3600) if tempo_lote > 0 else 0
        
        print(f"✅ Lote {lote_num} finalizado!")
        print(f"   📊 {votos_enviados} votos em {tempo_lote//3600:.0f}h {(tempo_lote%3600)//60:.0f}min")
        print(f"   🚀 Velocidade: {votos_por_hora:.0f} votos/hora")
        print(f"   🎯 Total acumulado: {self.total_votos} votos")
        
        # Salvar progresso após cada lote
        self.save_progress()
        
        # Pausa entre lotes AJUSTADA
        if pausa_apos > 0:
            print(f"⏸️  Pausa de {pausa_apos} segundos...")
            time.sleep(pausa_apos)
    
    def log_progress(self):
        """Log do progresso atual AJUSTADO"""
        tempo_decorrido = (time.time() - self.inicio_total) / 3600
        votos_por_hora = self.total_votos / tempo_decorrido if tempo_decorrido > 0 else 0
        
        # Calcular taxa de sucesso
        taxa_sucesso = (self.votos_sucesso / self.total_votos * 100) if self.total_votos > 0 else 0
        
        print(f"✅ {self.total_votos} votos (~{votos_por_hora:.0f}/hora) - Lote {self.lote_atual}")
        print(f"   📈 Sucessos: {self.votos_sucesso} | ❌ Erros: {self.votos_erro} | 🎯 Taxa: {taxa_sucesso:.1f}%")
    
    def executar(self):
        """Executa o sistema completo AJUSTADO para estabilidade"""
        print("🚀 SISTEMA DE VOTAÇÃO ESTÁVEL - VERSÃO INFINITA")
        print("=" * 70)
        print("🎯 Objetivo: VOTAR INFINITAMENTE COM ESTABILIDADE")
        print("⏰ Velocidade: OTIMIZADA PARA SUCESSOS")
        print("🚀 Threads: 2-4 SIMULTÂNEOS")
        print("🛡️  Proteções: ATIVADAS")
        print("🔄 Sistema de retry: OTIMIZADO")
        print("💾 Salvamento automático: ATIVADO")
        print("🏥 Monitor de saúde: ATIVADO")
        print("=" * 70)
        
        # Carregar progresso anterior
        if self.load_progress():
            print("📂 Continuando de onde parou...")
        
        try:
            while self.running:  # LOOP INFINITO
                for lote_config in self.config.lotes:
                    if not self.running:
                        break
                        
                    self.lote_atual += 1
                    self.votos_este_lote = 0
                    
                    try:
                        self.processar_lote(lote_config, self.lote_atual)
                    except KeyboardInterrupt:
                        print("\n🛑 Interrupção solicitada pelo usuário")
                        break
                    except Exception as e:
                        logging.error(f"Erro crítico no lote {self.lote_atual}: {e}")
                        print(f"⚠️ Erro crítico no lote {self.lote_atual}: {e}")
                        print("🔄 Tentando continuar com próximo lote...")
                        time.sleep(30)  # Pausa maior
                        continue
                
                # Após completar todos os lotes, recomeça infinitamente
                if self.running:
                    print("\n🔄 RECOMEÇANDO CICLO INFINITO...")
                    print(f"📊 Total acumulado: {self.total_votos} votos")
                    print("=" * 50)
                    time.sleep(10)  # Pausa maior antes de recomeçar
            
        except KeyboardInterrupt:
            print("\n🛑 Interrupção solicitada pelo usuário")
        except Exception as e:
            logging.error(f"Erro crítico no sistema: {e}")
            print(f"❌ Erro crítico: {e}")
        finally:
            # Estatísticas finais
            self.finalizar_execucao()
    
    def finalizar_execucao(self):
        """Finaliza a execução com estatísticas"""
        tempo_total = time.time() - self.inicio_total
        votos_por_hora_final = self.total_votos / (tempo_total / 3600) if tempo_total > 0 else 0
        taxa_sucesso_final = (self.votos_sucesso / self.total_votos * 100) if self.total_votos > 0 else 0
        
        print("\n" + "=" * 70)
        print("🎉 PROCESSO FINALIZADO!")
        print(f"📊 Total de votos: {self.total_votos}")
        print(f"✅ Sucessos: {self.votos_sucesso}")
        print(f"❌ Erros: {self.votos_erro}")
        print(f"🎯 Taxa de sucesso: {taxa_sucesso_final:.1f}%")
        print(f"⏰ Tempo total: {tempo_total//3600:.0f}h {(tempo_total%3600)//60:.0f}min")
        print(f"🚀 Velocidade média: {votos_por_hora_final:.0f} votos/hora")
        print(f"🔄 Lotes completados: {self.lote_atual}")
        print(f"🏁 Término: {datetime.now().strftime('%H:%M:%S')}")
        print("=" * 70)
        
        # Salvar progresso final
        self.save_progress()

if __name__ == "__main__":
    try:
        sistema = SistemaVotacao()
        sistema.executar()
    except KeyboardInterrupt:
        print("\n🛑 Programa interrompido pelo usuário")
    except Exception as e:
        logging.error(f"Erro fatal: {e}")
        print(f"❌ Erro fatal: {e}")
    finally:
        print("👋 Programa finalizado")
