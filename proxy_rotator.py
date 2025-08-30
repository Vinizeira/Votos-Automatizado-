import requests
import time
import random
import urllib.parse
import threading
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import os

class GerenciadorProxies:
    def __init__(self):
        # Lista de proxies (adicionar aqui)
        self.proxies = [
            # Exemplo de formato:
            # {"http": "http://proxy1:port", "https": "https://proxy1:port"},
            # {"http": "http://proxy2:port", "https": "https://proxy2:port"},
        ]
        
        # Verificar se há proxies configurados
        self.usar_proxies = len(self.proxies) > 0
        self.indice_proxy_atual = 0
        
    def proximo_proxy(self):
        """Retorna o próximo proxy da lista"""
        if not self.usar_proxies:
            return None
            
        proxy = self.proxies[self.indice_proxy_atual]
        self.indice_proxy_atual = (self.indice_proxy_atual + 1) % len(self.proxies)
        return proxy
    
    def testar_proxy(self, proxy):
        """Testa se um proxy está funcionando"""
        try:
            response = requests.get(
                "https://httpbin.org/ip", 
                proxies=proxy, 
                timeout=10
            )
            return response.status_code == 200
        except:
            return False

class SistemaVotacaoAvancado:
    def __init__(self):
        self.gerenciador_proxies = GerenciadorProxies()
        self.url = "https://script.google.com/macros/s/AKfycbyx6hsWgd8fkhw3cGCCtVGH9GTN7BCTdlGnx9uiAkBG1cHPIDFvE-RmUB8S-2zjxgI2Aw/callback"
        self.TOKEN_PREFIX = "AJuLMu0DuqqeqSFlMzAPQNVmARHZs6LnxQ"
        
        # Navegadores disponíveis
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/119.0.0.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1.2 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (iPad; CPU OS 17_1_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1.2 Mobile/15E148 Safari/604.1"
        ]
        
        # Headers base
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
        
        # Configurações de velocidade
        self.configuracoes_velocidade = {
            "ultra_rapido": {"min_delay": 0.3, "max_delay": 0.8, "threads": 5},
            "rapido": {"min_delay": 0.5, "max_delay": 1.2, "threads": 4},
            "normal": {"min_delay": 0.8, "max_delay": 2.0, "threads": 3},
            "lento": {"min_delay": 1.5, "max_delay": 3.5, "threads": 2},
            "muito_lento": {"min_delay": 2.5, "max_delay": 5.0, "threads": 1}
        }
        
        # Estatísticas
        self.total_votos = 0
        self.votos_sucesso = 0
        self.votos_erro = 0
        self.inicio_total = time.time()
        self.lock = threading.Lock()
        
    def gerar_headers(self):
        """Gera headers únicos com variações"""
        headers = self.base_headers.copy()
        headers["user-agent"] = random.choice(self.user_agents)
        
        # Variações nos headers
        variacoes = [
            ("accept-encoding", ["gzip, deflate, br", "gzip, deflate"]),
            ("accept-language", ["pt-BR,pt;q=0.9,en;q=0.8", "en-US,en;q=0.9", "pt-BR,pt;q=0.8,en;q=0.7"]),
            ("sec-ch-ua", [
                '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
                '"Not_A Brand";v="99", "Chromium";v="119", "Google Chrome";v="119"',
                '"Not_A Brand";v="8", "Chromium";v="121", "Google Chrome";v="121"'
            ])
        ]
        
        for header, valores in variacoes:
            if random.random() < 0.3:
                headers[header] = random.choice(valores)
        
        return headers
    
    def criar_payload(self, user_agent):
        """Cria payload com variações"""
        candidate_id = "12"
        
        # Variações no payload
        if random.random() < 0.05:
            candidate_id = str(random.randint(10, 15))
        
        # Variações na estrutura
        payload_variacoes = [
            f'["submitVote","[{{\\"id\\":\\"{candidate_id}\\",\\"userAgent\\":\\"{user_agent}\\"}}]",null,[0],null,null,1,0]',
            f'["submitVote","[{{\\"id\\":\\"{candidate_id}\\",\\"userAgent\\":\\"{user_agent}\\"}}]",null,[0],null,null,1,0]',
            f'["submitVote","[{{\\"id\\":\\"{candidate_id}\\",\\"userAgent\\":\\"{user_agent}\\"}}]",null,[0],null,null,1,0]'
        ]
        
        return random.choice(payload_variacoes)
    
    def enviar_voto_avancado(self, vote_id, config_velocidade):
        """Envia voto com técnicas avançadas"""
        try:
            # Headers únicos
            headers = self.gerar_headers()
            user_agent = headers["user-agent"]
            
            # Payload
            payload_bruto = self.criar_payload(user_agent)
            payload_encoded = "request=" + urllib.parse.quote(payload_bruto, safe='')
            
            # Token
            ts = str(int(time.time() * 1000))
            token = f"{self.TOKEN_PREFIX}:{ts}"
            token_encoded = urllib.parse.quote(token, safe='')
            
            # Parâmetros
            nocache_aleatorio = str(random.randint(1, 999))
            params = {"nocache_id": nocache_aleatorio, "token": token_encoded}
            
            # Proxy
            proxy = self.gerenciador_proxies.proximo_proxy()
            
            # Timeout
            timeout = random.uniform(5, 20)
            
            # Sessão única
            session = requests.Session()
            session.headers.update(headers)
            
            # Enviar requisição
            response = session.post(
                self.url, 
                params=params, 
                headers=headers, 
                data=payload_encoded, 
                timeout=timeout,
                proxies=proxy
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
    
    def processar_lote_avancado(self, quantidade, nome_velocidade, lote_num):
        """Processa um lote com configuração específica"""
        config_velocidade = self.configuracoes_velocidade[nome_velocidade]
        min_delay = config_velocidade["min_delay"]
        max_delay = config_velocidade["max_delay"]
        max_threads = config_velocidade["threads"]
        
        print(f"\n🚀 LOTE {lote_num}: {quantidade} votos - {nome_velocidade.upper()}")
        print(f"   ⚡ Velocidade: {min_delay}-{max_delay}s | Threads: {max_threads}")
        print(f"   🕐 Início: {datetime.now().strftime('%H:%M:%S')}")
        
        inicio_lote = time.time()
        votos_enviados = 0
        ultimo_log = time.time()
        
        # Processamento paralelo
        with ThreadPoolExecutor(max_workers=max_threads) as executor:
            futures = []
            
            for i in range(quantidade):
                future = executor.submit(self.enviar_voto_avancado, i, config_velocidade)
                futures.append(future)
                
                delay = random.uniform(min_delay, max_delay)
                time.sleep(delay)
                
                # Log periódico
                if time.time() - ultimo_log > 15:
                    tempo_decorrido = (time.time() - self.inicio_total) / 3600
                    votos_por_hora = self.total_votos / tempo_decorrido if tempo_decorrido > 0 else 0
                    tempo_restante = ((10000 - self.total_votos) / votos_por_hora) if votos_por_hora > 0 else 0
                    print(f"✅ {self.total_votos}/10000 votos (~{votos_por_hora:.0f}/hora) - ⏳{tempo_restante:.1f}h restantes")
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
        
        return votos_enviados
    
    def executar_avancado(self):
        """Executa o sistema avançado"""
        print("🚀 SISTEMA DE VOTAÇÃO AVANÇADO")
        print("=" * 50)
        print("🎯 Objetivo: 10.000 votos")
        print("⏰ Previsão: 4-6 horas")
        print("🚀 Velocidade: ~2500 votos/hora")
        print("🛡️  Proteções: MÁXIMAS")
        print("=" * 50)
        
        # Configuração dos lotes
        lotes_config = [
            {"quantidade": 1500, "speed": "ultra_rapido", "pausa": 60},
            {"quantidade": 2000, "speed": "rapido", "pausa": 90},
            {"quantidade": 2000, "speed": "normal", "pausa": 120},
            {"quantidade": 2000, "speed": "normal", "pausa": 150},
            {"quantidade": 1500, "speed": "lento", "pausa": 180},
            {"quantidade": 1000, "speed": "muito_lento", "pausa": 0}
        ]
        
        for lote_num, config in enumerate(lotes_config, 1):
            votos_enviados = self.processar_lote_avancado(
                config["quantidade"], 
                config["speed"], 
                lote_num
            )
            
            # Pausa entre lotes
            if config["pausa"] > 0 and lote_num < len(lotes_config):
                print(f"⏸️  Pausa de {config['pausa']//60} minutos...")
                time.sleep(config["pausa"])
        
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
    sistema = SistemaVotacaoAvancado()
    sistema.executar_avancado()
