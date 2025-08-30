import requests
import time

def teste_desbloqueio():
    try:
        # Teste simples de conexão (sem enviar voto)
        response = requests.get("https://script.google.com/macros/s/AKfycbyx6hsWgd8fkhw3cGCCtVGH9GTN7BCTdlGnx9uiAkBG1cHPIDFvE-RmUB8S-2zjxgI2Aw/exec", timeout=10)
        
        if response.status_code == 200:
            print("✅ IP DESBLOQUEADO - Pode tentar votar de novo")
            return True
        else:
            print(f"❌ Ainda bloqueado (Status: {response.status_code})")
            return False
            
    except Exception as e:
        print(f"⚠️ Erro de conexão: {e}")
        return False

# Testa a cada 30 minutos
while True:
    if teste_desbloqueio():
        break
    else:
        print("⏳ Aguardando 30 minutos para próximo teste...")
        time.sleep(1800)  # 30 minutos