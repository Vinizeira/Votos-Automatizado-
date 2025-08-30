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
        
        # Intervalos de espera
        self.delays = {
            "rapido": {"min": 0.8, "max": 1.5},
            "normal": {"min": 1.2, "max": 2.5},
            "lento": {"min": 2.0, "max": 4.0}
        }
        
        # Configuração dos lotes
        self.lotes = [
            {"quantidade": 2000, "delay": "rapido", "pausa_apos": 120, "threads": 3},
            {"quantidade": 3000, "delay": "normal", "pausa_apos": 180, "threads": 2},
            {"quantidade": 3000, "delay": "normal", "pausa_apos": 240, "threads": 2},
            {"quantidade": 2000, "delay": "lento", "pausa_apos": 300, "threads": 1},
            {"quantidade": 2000, "delay": "lento", "pausa_apos": 360, "threads": 1},
            {"quantidade": 3000, "delay": "normal", "pausa_apos": 0, "threads": 2}
        ]

class SistemaVotacao:
    def __init__(self):
        self.config = ConfiguracaoSistema()
        self.session = requests.Session()
        self.total_votos = 0
        self.votos_sucesso = 0
        self.votos_erro = 0
        self.inicio_total = time.time()
        self.lock = threading.Lock()
        
        # Configurar sessão
        self.session.headers.update(self.config.base_headers)
        
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
        """Retorna delay com variações"""
        delay_config = self.config.delays[tipo_delay]
        delay_base = random.uniform(delay_config["min"], delay_config["max"])
        
        # Variação pequena
        variacao = random.uniform(-0.1, 0.1)
        return max(0.1, delay_base + variacao)
    
    def enviar_voto(self, vote_id):
        """Envia um voto individual"""
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
            
            # Timeout
            timeout = random.uniform(8, 15)
            
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
        except Exception as e:
            with self.lock:
                self.votos_erro += 1
            return False, str(e)
    
    def processar_lote(self, lote_config, lote_num):
        """Processa um lote de votos"""
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
        
        # Processamento paralelo
        with ThreadPoolExecutor(max_workers=max_threads) as executor:
            futures = []
            
            for i in range(quantidade):
                future = executor.submit(self.enviar_voto, i)
                futures.append(future)
                
                delay = self.obter_delay(delay_type)
                time.sleep(delay)
                
                # Log periódico
                if time.time() - ultimo_log > 20:
                    tempo_decorrido = (time.time() - self.inicio_total) / 3600
                    votos_por_hora = self.total_votos / tempo_decorrido if tempo_decorrido > 0 else 0
                    tempo_restante = ((12000 - self.total_votos) / votos_por_hora) if votos_por_hora > 0 else 0
                    print(f"✅ {self.total_votos}/12000 votos (~{votos_por_hora:.0f}/hora) - ⏳{tempo_restante:.1f}h restantes")
                    ultimo_log = time.time()
            
            # Aguardar conclusão
            for future in as_completed(futures):
                try:
                    success, result = future.result()
                    if success:
                        votos_enviados += 1
                except Exception as e:
                    print(f"⚠️ Erro no thread: {e}")
        
        # Estatísticas do lote
        tempo_lote = time.time() - inicio_lote
        votos_por_hora = votos_enviados / (tempo_lote / 3600) if tempo_lote > 0 else 0
        
        print(f"✅ Lote {lote_num} finalizado!")
        print(f"   📊 {votos_enviados} votos em {tempo_lote//3600:.0f}h {(tempo_lote%3600)//60:.0f}min")
        print(f"   🚀 Velocidade: {votos_por_hora:.0f} votos/hora")
        print(f"   🎯 Total acumulado: {self.total_votos} votos")
        
        # Pausa entre lotes
        if pausa_apos > 0:
            print(f"⏸️  Pausa de {pausa_apos//60} minutos...")
            time.sleep(pausa_apos)
    
    def executar(self):
        """Executa o sistema completo"""
        print("🚀 SISTEMA DE VOTAÇÃO OTIMIZADO")
        print("=" * 50)
        print("🎯 Objetivo: 12.000 votos")
        print("⏰ Previsão: 6-8 horas")
        print("🚀 Velocidade: ~2000 votos/hora")
        print("🛡️  Proteções: ATIVADAS")
        print("=" * 50)
        
        for lote_num, lote_config in enumerate(self.config.lotes, 1):
            self.processar_lote(lote_config, lote_num)
        
        # Estatísticas finais
        tempo_total = time.time() - self.inicio_total
        votos_por_hora_final = self.total_votos / (tempo_total / 3600) if tempo_total > 0 else 0
        
        print("\n" + "=" * 50)
        print("🎉 PROCESSO FINALIZADO!")
        print(f"📊 Total de votos: {self.total_votos}")
        print(f"✅ Sucessos: {self.votos_sucesso}")
        print(f"❌ Erros: {self.votos_erro}")
        print(f"⏰ Tempo total: {tempo_total//3600:.0f}h {(tempo_total%3600)//60:.0f}min")
        print(f"🚀 Velocidade média: {votos_por_hora_final:.0f} votos/hora")
        print(f"🏁 Término: {datetime.now().strftime('%H:%M:%S')}")
        print("=" * 50)

if __name__ == "__main__":
    sistema = SistemaVotacao()
    sistema.executar()
