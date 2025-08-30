import requests
import time
import urllib.parse

def teste_saude():
    url = "https://script.google.com/macros/s/AKfycbyx6hsWgd8fkhw3cGCCtVGH9GTN7BCTdlGnx9uiAkBG1cHPIDFvE-RmUB8S-2zjxgI2Aw/callback"
    
    # Configuração MÍNIMA para o teste
    headers = {
        "content-type": "application/x-www-form-urlencoded;charset=UTF-8",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"
    }
    
    # Payload simples
    payload_encoded = "request=%5B%22submitVote%22%2C%22%5B%7B%5C%22id%5C%22%3A%5C%2212%5C%22%2C%5C%22userAgent%5C%22%3A%5C%22Mozilla%2F5.0%20(Windows%20NT%2010.0%3B%20Win64%3B%20x64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F139.0.0.0%20Safari%2F537.36%5C%22%7D%5D%22%2Cnull%2C%5B0%5D%2Cnull%2Cnull%2C1%2C0%5D"
    
    # Teste APENAS 1 vez com delay grande
    try:
        params = {
            "nocache_id": "7",
            "token": "AJuLMu0DuqqeqSFlMzAPQNVmARHZs6LnxQ:1756520320147"
        }
        
        print("🧪 Testando conexão...")
        response = requests.post(url, params=params, headers=headers, data=payload_encoded, timeout=10)
        
        if response.status_code == 200:
            print("✅ SERVIDOR RESPONDENDO - Não está bloqueado!")
            return True
        else:
            print(f"❌ ERRO {response.status_code} - Possível bloqueio")
            return False
            
    except Exception as e:
        print(f"⚠️ ERRO: {e}")
        return False

# Executa o teste APENAS 1 vez com intervalo grande
teste_saude()
print("\n⏰ Aguardando 5 minutos para próximo teste...")
time.sleep(300)  # 5 minutos de esperaced