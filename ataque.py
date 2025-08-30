import requests
import time
import random
import urllib.parse
from datetime import datetime

url = "https://script.google.com/macros/s/AKfycbyx6hsWgd8fkhw3cGCCtVGH9GTN7BCTdlGnx9uiAkBG1cHPIDFvE-RmUB8S-2zjxgI2Aw/callback"

TOKEN_PREFIX = "AJuLMu0DuqqeqSFlMzAPQNVmARHZs6LnxQ"

headers = {
    "content-type": "application/x-www-form-urlencoded;charset=UTF-8",
    "origin": "https://script.google.com",
    "referer": "https://script.google.com/macros/s/AKfycbyx6hsWgd8fkhw3cGCCtVGH9GTN7BCTdlGnx9uiAkBG1cHPIDFvE-RmUB8S-2zjxgI2Aw/exec",
    "sec-ch-ua": '"Not;A=Brand";v="99", "Brave";v="139", "Chromium";v="139"',
    "sec-ch-ua-platform": '"Windows"',
    "x-same-domain": "1"
}

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/118.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/139.0.0.0"
]

def criar_payload(user_agent):
    return f'["submitVote","[{{\\"id\\":\\"12\\",\\"userAgent\\":\\"{user_agent}\\"}}]",null,[0],null,null,1,0]'

lotes = [
    {"quantidade": 3000, "delay_min": 1.5, "delay_max": 3.5, "pausa_apos": 180},
    {"quantidade": 4000, "delay_min": 1.6, "delay_max": 4.0, "pausa_apos": 300},
    {"quantidade": 4000, "delay_min": 1.8, "delay_max": 5.0, "pausa_apos": 420},
    {"quantidade": 4000, "delay_min": 2.0, "delay_max": 6.0, "pausa_apos": 0}
]

total_votos = 0
inicio_total = time.time()

print("🌙 VOTAÇÃO NOTURNA TURBO - 15K VOTOS")
print("=" * 50)
print("🎯 Total planejado: 15.000 votos")
print("⏰ Previsão: 10-12 horas")
print("🚀 Velocidade: ~1500 votos/hora")
print("=" * 50)

for lote_num, lote in enumerate(lotes, 1):
    quantidade = lote["quantidade"]
    delay_min = lote["delay_min"]
    delay_max = lote["delay_max"]
    pausa_apos = lote["pausa_apos"]
    
    print(f"\n🎯 LOTE {lote_num}: {quantidade} votos")
    print(f"   ⏰ Delay: {delay_min}-{delay_max}s | Pausa após: {pausa_apos//60}min")
    print(f"   🕒 Início: {datetime.now().strftime('%H:%M:%S')}")
    
    inicio_lote = time.time()
    votos_lote = 0
    ultimo_log = 0
    
    for i in range(quantidade):
        try:
            user_agent_escolhido = random.choice(user_agents)
            headers["user-agent"] = user_agent_escolhido
            
            payload_bruto = criar_payload(user_agent_escolhido)
            payload_encoded = "request=" + urllib.parse.quote(payload_bruto, safe='')

            ts = str(int(time.time() * 1000))
            token = f"{TOKEN_PREFIX}:{ts}"
            token_encoded = urllib.parse.quote(token, safe='')
            nocache_aleatorio = str(random.randint(1, 50))

            params = {"nocache_id": nocache_aleatorio, "token": token_encoded}

            response = requests.post(url, params=params, headers=headers, data=payload_encoded, timeout=10)
            total_votos += 1
            votos_lote += 1
            
            if response.status_code == 200:
                if time.time() - ultimo_log > 30:
                    tempo_decorrido = (time.time() - inicio_total) / 3600
                    votos_por_hora = total_votos / tempo_decorrido
                    tempo_restante = ((15000 - total_votos) / votos_por_hora) if votos_por_hora > 0 else 0
                    print(f"✅ {total_votos}/15000 votos (~{votos_por_hora:.0f}/hora) - ⏳{tempo_restante:.1f}h restantes")
                    ultimo_log = time.time()
            else:
                print(f"❌ Erro {response.status_code} no voto {total_votos}")
                time.sleep(10)
                continue
                
        except Exception as e:
            print(f"⚠️  Exception: {e}")
            time.sleep(15)
            continue
        
        delay_base = random.uniform(delay_min, delay_max)
        
        if random.random() < 0.08:
            pausa_extra = random.uniform(10, 30)
            time.sleep(pausa_extra)
        else:
            time.sleep(delay_base)
    
    tempo_lote = time.time() - inicio_lote
    votos_por_hora = quantidade / (tempo_lote / 3600)
    print(f"✅ Lote {lote_num} concluído!")
    print(f"   📊 {quantidade} votos em {tempo_lote//3600:.0f}h {(tempo_lote%3600)//60:.0f}min")
    print(f"   🚀 Velocidade: {votos_por_hora:.0f} votos/hora")
    print(f"   🎯 Total acumulado: {total_votos} votos")
    
    if lote_num < len(lotes) and pausa_apos > 0:
        print(f"⏸️  Pausa de {pausa_apos//60} minutos...")
        time.sleep(pausa_apos)

tempo_total = time.time() - inicio_total
votos_por_hora_final = total_votos / (tempo_total / 3600)
print("\n" + "=" * 50)
print("🎉 VOTAÇÃO CONCLUÍDA!")
print(f"📊 Total de votos: {total_votos}")
print(f"⏰ Tempo total: {tempo_total//3600:.0f}h {(tempo_total%3600)//60:.0f}min")
print(f"🚀 Velocidade média: {votos_por_hora_final:.0f} votos/hora")
print(f"🏁 Término: {datetime.now().strftime('%H:%M:%S')}")
print("=" * 50)