# Configurações do Sistema de Votação
# Ajuste estes valores conforme necessário

# Configurações básicas
CONFIGURACAO_BASICA = {
    "url": "https://script.google.com/macros/s/AKfycbyx6hsWgd8fkhw3cGCCtVGH9GTN7BCTdlGnx9uiAkBG1cHPIDFvE-RmUB8S-2zjxgI2Aw/callback",
    "token_prefix": "AJuLMu0DuqqeqSFlMzAPQNVmARHZs6LnxQ",
    "candidate_id": "12",  # ID do candidato
    "total_votos_objetivo": 10000
}

# Configurações de velocidade (em segundos)
VELOCIDADES = {
    "ultra_rapido": {
        "min_delay": 0.3,
        "max_delay": 0.8,
        "threads": 5,
        "descricao": "Ultra Rápido - Máximo risco"
    },
    "rapido": {
        "min_delay": 0.5,
        "max_delay": 1.2,
        "threads": 4,
        "descricao": "Rápido - Risco moderado"
    },
    "normal": {
        "min_delay": 0.8,
        "max_delay": 2.0,
        "threads": 3,
        "descricao": "Normal - Equilibrado"
    },
    "lento": {
        "min_delay": 1.5,
        "max_delay": 3.5,
        "threads": 2,
        "descricao": "Lento - Baixo risco"
    },
    "muito_lento": {
        "min_delay": 2.5,
        "max_delay": 5.0,
        "threads": 1,
        "descricao": "Muito Lento - Mínimo risco"
    }
}

# Configuração de lotes recomendada
LOTES_RECOMENDADOS = [
    {
        "quantidade": 1500,
        "velocidade": "ultra_rapido",
        "pausa_apos": 60,  # segundos
        "descricao": "Lote inicial - velocidade máxima"
    },
    {
        "quantidade": 2000,
        "velocidade": "rapido",
        "pausa_apos": 90,
        "descricao": "Lote intermediário - velocidade alta"
    },
    {
        "quantidade": 2000,
        "velocidade": "normal",
        "pausa_apos": 120,
        "descricao": "Lote principal - velocidade equilibrada"
    },
    {
        "quantidade": 2000,
        "velocidade": "normal",
        "pausa_apos": 150,
        "descricao": "Lote continuidade - velocidade equilibrada"
    },
    {
        "quantidade": 1500,
        "velocidade": "lento",
        "pausa_apos": 180,
        "descricao": "Lote final - velocidade reduzida"
    },
    {
        "quantidade": 1000,
        "velocidade": "muito_lento",
        "pausa_apos": 0,
        "descricao": "Lote final - velocidade mínima"
    }
]

# Configuração conservadora (menos votos, mais seguro)
LOTES_CONSERVADOR = [
    {
        "quantidade": 1000,
        "velocidade": "normal",
        "pausa_apos": 180,
        "descricao": "Lote 1 - velocidade normal"
    },
    {
        "quantidade": 1000,
        "velocidade": "lento",
        "pausa_apos": 300,
        "descricao": "Lote 2 - velocidade lenta"
    },
    {
        "quantidade": 1000,
        "velocidade": "muito_lento",
        "pausa_apos": 0,
        "descricao": "Lote 3 - velocidade muito lenta"
    }
]

# Configuração agressiva (mais votos, mais risco)
LOTES_AGRESSIVO = [
    {
        "quantidade": 2500,
        "velocidade": "ultra_rapido",
        "pausa_apos": 30,
        "descricao": "Lote 1 - velocidade máxima"
    },
    {
        "quantidade": 2500,
        "velocidade": "rapido",
        "pausa_apos": 60,
        "descricao": "Lote 2 - velocidade alta"
    },
    {
        "quantidade": 2500,
        "velocidade": "normal",
        "pausa_apos": 90,
        "descricao": "Lote 3 - velocidade normal"
    },
    {
        "quantidade": 2500,
        "velocidade": "rapido",
        "pausa_apos": 0,
        "descricao": "Lote 4 - velocidade alta"
    }
]

# Navegadores disponíveis
USER_AGENTS = [
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
HEADERS_BASE = {
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

# Configurações de proxy (adicione seus proxies aqui)
PROXIES = [
    # Exemplo de formato:
    # {"http": "http://proxy1:port", "https": "https://proxy1:port"},
    # {"http": "http://proxy2:port", "https": "https://proxy2:port"},
]

# Configurações de timeout
TIMEOUT_CONFIG = {
    "min_timeout": 5,  # segundos
    "max_timeout": 20,  # segundos
    "retry_attempts": 3,  # tentativas de retry
    "retry_delay": 5  # segundos entre tentativas
}

# Configurações de log
LOG_CONFIG = {
    "log_interval": 15,  # segundos entre logs
    "show_detailed_errors": False,  # mostrar erros detalhados
    "save_logs_to_file": True,  # salvar logs em arquivo
    "log_filename": "votacao_log.txt"
}

# Configurações de segurança
SECURITY_CONFIG = {
    "randomize_payload": True,  # randomizar payload
    "randomize_headers": True,  # randomizar headers
    "use_proxy_rotation": len(PROXIES) > 0,  # usar rotação de proxy
    "add_random_delays": True,  # adicionar delays aleatórios
    "max_concurrent_requests": 5  # máximo de requisições simultâneas
}

# Função para obter configuração baseada no perfil
def obter_config(perfil="recomendado"):
    """
    Retorna configuração baseada no perfil escolhido
    
    Perfis disponíveis:
    - "conservador": Menos votos, mais seguro
    - "recomendado": Equilibrado (padrão)
    - "agressivo": Mais votos, mais risco
    """
    if perfil == "conservador":
        return {
            "lotes": LOTES_CONSERVADOR,
            "total_votos": 3000,
            "descricao": "Perfil Conservador - Baixo risco"
        }
    elif perfil == "agressivo":
        return {
            "lotes": LOTES_AGRESSIVO,
            "total_votos": 10000,
            "descricao": "Perfil Agressivo - Alto risco"
        }
    else:  # recomendado
        return {
            "lotes": LOTES_RECOMENDADOS,
            "total_votos": 10000,
            "descricao": "Perfil Recomendado - Risco equilibrado"
        }

# Função para validar configurações
def validar_config():
    """Valida se as configurações estão corretas"""
    erros = []
    
    if not CONFIGURACAO_BASICA["url"]:
        erros.append("URL não configurada")
    
    if not CONFIGURACAO_BASICA["token_prefix"]:
        erros.append("Token prefix não configurado")
    
    if len(USER_AGENTS) == 0:
        erros.append("Nenhum User Agent configurado")
    
    if len(HEADERS_BASE) == 0:
        erros.append("Headers base não configurados")
    
    return erros

if __name__ == "__main__":
    # Teste das configurações
    print("🔧 Verificando configurações...")
    erros = validar_config()
    
    if erros:
        print("❌ Problemas encontrados:")
        for erro in erros:
            print(f"   - {erro}")
    else:
        print("✅ Configurações válidas!")
        
        # Mostrar perfis disponíveis
        print("\n📋 Perfis disponíveis:")
        for perfil in ["conservador", "recomendado", "agressivo"]:
            config = obter_config(perfil)
            print(f"   - {perfil.capitalize()}: {config['total_votos']} votos - {config['descricao']}")
