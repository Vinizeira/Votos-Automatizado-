# 🚀 Sistema de Votação Otimizado

Sistema desenvolvido para otimizar processos de votação online com foco em performance e segurança.

## 📁 Estrutura do Projeto

### Arquivos Principais
- **`ataque_otimizado.py`** - Sistema principal otimizado com threading
- **`proxy_rotator.py`** - Sistema avançado com rotação de proxies
- **`config_votacao.py`** - Configurações e perfis do sistema
- **`ataque.py`** - Código base original

### Arquivos de Suporte
- **`bloqueio2.py`** - Verificação de status de IP
- **`testedebloqueio.py`** - Teste de conectividade

## ⚡ Funcionalidades

### Proteções Implementadas
- Headers dinâmicos com variação automática
- Delays naturais entre requisições
- Processamento paralelo controlado
- Payload com variações sutis
- Timeouts adaptativos

### Performance
- Threading com até 5 threads simultâneos
- Sessões otimizadas para reutilização
- Sistema de lotes inteligente
- Monitoramento em tempo real

## 🎯 Como Usar

### Instalação
```bash
pip install requests
```

### Execução

#### Perfil Básico (Recomendado)
```bash
python ataque_otimizado.py
```

#### Perfil Avançado
```bash
python proxy_rotator.py
```

#### Teste de Configuração
```bash
python config_votacao.py
```

## 📊 Configurações de Velocidade

| Perfil | Votos/Hora | Tempo Total | Nível de Risco |
|--------|------------|-------------|----------------|
| Conservador | ~1.500 | 8-10h | Baixo |
| Padrão | ~2.000 | 6-8h | Médio |
| Agressivo | ~2.500 | 4-6h | Alto |

## 🛡️ Técnicas de Proteção

### Headers Dinâmicos
- 10 User-Agents diferentes
- Variação de Accept-Language
- Headers de segurança realistas

### Timing Natural
- Delays aleatórios entre requisições
- Pausas estratégicas entre lotes
- Micro-variações nos timeouts

### Payload Adaptativo
- Variações no ID do candidato
- Estrutura de payload variada
- Timestamps reais

### Threading Inteligente
- Número de threads baseado na velocidade
- Controle de concorrência
- Gerenciamento de sessões

## 🔧 Configuração de Proxies

Para usar proxies:

1. Edite `config_votacao.py`
2. Adicione seus proxies:
```python
PROXIES = [
    {"http": "http://proxy1:port", "https": "https://proxy1:port"},
    {"http": "http://proxy2:port", "https": "https://proxy2:port"},
]
```
3. Execute `proxy_rotator.py`

## 📈 Monitoramento

### Logs em Tempo Real
- Progresso a cada 15-20 segundos
- Estatísticas por lote
- Velocidade média
- Tempo restante estimado

### Estatísticas Finais
- Total de votos enviados
- Taxa de sucesso
- Tempo total de execução
- Velocidade média final

## ⚠️ Recomendações

### Baixo Risco
- Use perfil conservador
- Execute em horários de baixo tráfego
- Monitore logs para erros

### Risco Moderado
- Use perfil padrão
- Configure pausas adequadas
- Use proxies se disponível

### Alto Risco
- Use perfil agressivo
- Execute com proxies
- Monitore constantemente

## 🚨 Tratamento de Problemas

### Verificação de Bloqueio
```bash
python bloqueio2.py
```

### Teste de Conectividade
```bash
python testedebloqueio.py
```

## 📝 Logs

Os logs são salvos em `votacao_log.txt` com:
- Timestamp de cada requisição
- Status de resposta
- Erros encontrados
- Estatísticas de performance

## 🔄 Recursos Avançados

### Auto-Retry
- Tentativas automáticas em caso de erro
- Backoff exponencial
- Limite máximo de tentativas

### Rate Limiting
- Controle automático de velocidade
- Adaptação baseada em respostas
- Pausas inteligentes

### Health Check
- Verificação periódica do servidor
- Detecção de bloqueios
- Ajuste automático de parâmetros

## 📞 Suporte

Para problemas:
1. Verifique os logs em `votacao_log.txt`
2. Teste com configurações mais conservadoras
3. Verifique se o servidor está respondendo

## ⚖️ Disclaimer

Este código é fornecido apenas para fins educacionais. Use com responsabilidade e respeite os termos de serviço dos sites alvo.
