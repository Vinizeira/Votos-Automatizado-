# 🚀 Sistema de Votação Otimizado - Versão Melhorada

Sistema desenvolvido para otimizar processos de votação online com foco em performance, segurança e **estabilidade contínua**.
Fiz com o intuito de ajudar um amigo, mas como está automatizado, é só trocar o url que funciona.

## 🆕 NOVIDADES DA VERSÃO MELHORADA

### ✨ Melhorias Implementadas
- **🔄 Sistema de Retry Automático** - Tentativas automáticas em caso de falha
- **💾 Salvamento Automático de Progresso** - Nunca perca o progresso
- **🏥 Monitor de Saúde** - Verifica continuamente se o sistema está funcionando
- **🛡️ Tratamento Robusto de Erros** - Não para mais inesperadamente
- **📊 Logs Detalhados** - Monitoramento completo de todas as operações
- **🔍 Monitor Automático** - Reinicia automaticamente se necessário
- **⚡ Graceful Shutdown** - Para graciosamente quando solicitado

## 📁 Estrutura do Projeto

### Arquivos Principais
- **`ataque_otimizado.py`** - Sistema principal otimizado com todas as melhorias
- **`iniciar_sistema.py`** - Script de inicialização com menu interativo
- **`monitor_sistema.py`** - Monitor automático que reinicia o sistema se necessário
- **`proxy_rotator.py`** - Sistema avançado com rotação de proxies
- **`config_votacao.py`** - Configurações e perfis do sistema
- **`ataque.py`** - Código base original

### Arquivos de Suporte
- **`bloqueio2.py`** - Verificação de status de IP
- **`testedebloqueio.py`** - Teste de conectividade
- **`requirements.txt`** - Dependências do projeto

## 🎯 Como Usar

### Instalação
```bash
pip install -r requirements.txt
```

### Execução Recomendada (Fácil)
```bash
python iniciar_sistema.py
```

### Execução Direta
```bash
# Sistema principal apenas
python ataque_otimizado.py

# Sistema com monitor automático
python monitor_sistema.py
```

## 🚀 Modos de Execução

### 1. Sistema Principal (Recomendado)
- Executa apenas o sistema de votação
- Salvamento automático de progresso
- Tratamento robusto de erros
- Para graciosamente com Ctrl+C

### 2. Sistema + Monitor Automático
- Sistema principal + monitor em background
- Reinicia automaticamente se parar
- Máximo de 5 reinicializações
- Ideal para execução contínua

### 3. Apenas Monitor
- Monitora e reinicia o sistema automaticamente
- Verifica progresso a cada minuto
- Reinicia se não houver progresso por 10 minutos

## ⚡ Funcionalidades

### Proteções Implementadas
- Headers dinâmicos com variação automática
- Delays naturais entre requisições
- Processamento paralelo controlado
- Payload com variações sutis
- Timeouts adaptativos
- **Sistema de retry com backoff exponencial**
- **Monitor de saúde contínuo**
- **Salvamento automático de progresso**

### Performance
- Threading com até 5 threads simultâneos
- Sessões otimizadas para reutilização
- Sistema de lotes inteligente
- Monitoramento em tempo real
- **Recuperação automática de falhas**
- **Continuidade de execução**

## 🛡️ Sistema de Recuperação

### Retry Automático
- Máximo de 3 tentativas por voto
- Backoff exponencial (5s, 10s, 20s)
- Reset automático após sucessos

### Monitor de Saúde
- Verifica taxa de erro a cada minuto
- Pausa automática se taxa > 30%
- Teste de conectividade periódico
- Ajuste automático de velocidade

### Salvamento de Progresso
- Salva progresso a cada lote
- Carrega automaticamente ao reiniciar
- Arquivo: `progresso_votacao.json`
- Nunca perca votos já enviados

## 📊 Configurações de Velocidade

| Perfil | Votos/Hora | Tempo Total | Nível de Risco |
|--------|------------|-------------|----------------|
| Conservador | ~1.500 | 8-10h | Baixo |
| Padrão | ~2.000 | 6-8h | Médio |
| Agressivo | ~2.500 | 4-6h | Alto |

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

## 📈 Monitoramento Avançado

### Logs Detalhados
- **`votacao.log`** - Log principal do sistema
- **`monitor.log`** - Log do monitor automático
- Timestamp de cada operação
- Status de resposta detalhado
- Erros com stack trace completo

### Verificação de Status
```bash
python iniciar_sistema.py
# Opção 4: Verificar Status
```

Mostra:
- Processos em execução
- Progresso atual
- Última atualização
- Tamanho dos logs

## 🚨 Tratamento de Problemas

### Se o Sistema Parar
1. **Verifique os logs**: `votacao.log` e `monitor.log`
2. **Use o monitor**: `python monitor_sistema.py`
3. **Reinicie com progresso**: O sistema carrega automaticamente

### Verificação de Bloqueio
```bash
python bloqueio2.py
```

### Teste de Conectividade
```bash
python testedebloqueio.py
```

### Parar Todos os Processos
```bash
python iniciar_sistema.py
# Opção 5: Parar Todos os Processos
```

## 🔄 Recursos Avançados

### Auto-Retry Melhorado
- Tentativas automáticas em caso de erro
- Backoff exponencial inteligente
- Limite máximo de tentativas configurável
- Reset automático após sucessos

### Rate Limiting Inteligente
- Controle automático de velocidade
- Adaptação baseada em respostas
- Pausas inteligentes
- **Detecção automática de bloqueios**

### Health Check Avançado
- Verificação periódica do servidor
- Detecção de bloqueios
- Ajuste automático de parâmetros
- **Monitoramento de recursos do sistema**

### Graceful Shutdown
- Para graciosamente com Ctrl+C
- Salva progresso automaticamente
- Finaliza threads adequadamente
- **Nunca perde dados**

## 📝 Arquivos de Log

### `votacao.log`
- Todas as operações do sistema principal
- Erros detalhados com stack trace
- Estatísticas de performance
- Timestamps precisos

### `monitor.log`
- Operações do monitor automático
- Reinicializações automáticas
- Verificações de saúde
- Status do sistema

### `progresso_votacao.json`
- Progresso salvo automaticamente
- Total de votos, sucessos e erros
- Timestamp da última atualização
- Carregado automaticamente ao reiniciar

## ⚠️ Recomendações

### Para Execução Contínua
- Use o **Sistema + Monitor Automático**
- Configure pausas adequadas
- Monitore os logs periodicamente
- Use proxies se disponível

### Para Execução Manual
- Use o **Sistema Principal**
- Para com Ctrl+C quando necessário
- O progresso é salvo automaticamente
- Reinicie quando quiser continuar

### Para Máxima Estabilidade
- Use perfil conservador
- Execute em horários de baixo tráfego
- Monitore logs para erros
- Use o monitor automático

## 📞 Suporte

Para problemas:
1. **Verifique os logs**: `votacao.log` e `monitor.log`
2. **Use o menu de inicialização**: `python iniciar_sistema.py`
3. **Teste com configurações mais conservadoras**
4. **Verifique se o servidor está respondendo**

## 🎉 Benefícios da Versão Melhorada

- **✅ Nunca para inesperadamente**
- **✅ Recupera automaticamente de falhas**
- **✅ Salva progresso automaticamente**
- **✅ Reinicia automaticamente se necessário**
- **✅ Logs detalhados para diagnóstico**
- **✅ Interface amigável para controle**
- **✅ Tratamento robusto de erros**
- **✅ Monitoramento contínuo de saúde**
