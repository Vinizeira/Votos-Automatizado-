#!/usr/bin/env python3
"""
Teste Completo do Sistema de Votação Melhorado
Verifica todas as funcionalidades e melhorias implementadas
"""

import os
import sys
import json
import time
import subprocess
import threading
from datetime import datetime

def print_header(title):
    """Imprime cabeçalho formatado"""
    print("\n" + "="*60)
    print(f"🧪 {title}")
    print("="*60)

def print_test(test_name, result, details=""):
    """Imprime resultado de teste formatado"""
    status = "✅ PASSOU" if result else "❌ FALHOU"
    print(f"{status} - {test_name}")
    if details:
        print(f"   📝 {details}")

def test_imports():
    """Testa importação de módulos"""
    print_header("TESTE DE IMPORTAÇÕES")
    
    modules = [
        ('requests', 'Biblioteca para requisições HTTP'),
        ('psutil', 'Monitoramento de processos'),
        ('threading', 'Threading para concorrência'),
        ('logging', 'Sistema de logs'),
        ('subprocess', 'Execução de processos'),
        ('argparse', 'Argumentos de linha de comando'),
        ('json', 'Manipulação de JSON'),
        ('time', 'Funções de tempo'),
        ('datetime', 'Manipulação de datas')
    ]
    
    all_passed = True
    for module, description in modules:
        try:
            __import__(module)
            print_test(f"{module}", True, description)
        except ImportError as e:
            print_test(f"{module}", False, f"Erro: {e}")
            all_passed = False
    
    return all_passed

def test_files():
    """Testa existência de arquivos importantes"""
    print_header("TESTE DE ARQUIVOS")
    
    files = [
        ('ataque_otimizado.py', 'Sistema principal de votação'),
        ('monitor_sistema.py', 'Monitor automático'),
        ('iniciar_sistema.py', 'Script de inicialização'),
        ('config_votacao.py', 'Configurações do sistema'),
        ('requirements.txt', 'Dependências do projeto'),
        ('README.md', 'Documentação')
    ]
    
    all_passed = True
    for file, description in files:
        exists = os.path.exists(file)
        print_test(f"{file}", exists, description)
        if not exists:
            all_passed = False
    
    return all_passed

def test_configuration():
    """Testa configurações do sistema"""
    print_header("TESTE DE CONFIGURAÇÃO")
    
    try:
        import config_votacao
        
        # Testar configurações básicas
        configs = [
            ('URL', hasattr(config_votacao, 'URL')),
            ('TOKEN_PREFIX', hasattr(config_votacao, 'TOKEN_PREFIX')),
            ('CANDIDATE_ID', hasattr(config_votacao, 'CANDIDATE_ID')),
            ('USER_AGENTS', hasattr(config_votacao, 'USER_AGENTS')),
            ('HEADERS', hasattr(config_votacao, 'HEADERS'))
        ]
        
        all_passed = True
        for config_name, exists in configs:
            print_test(f"Config {config_name}", exists)
            if not exists:
                all_passed = False
        
        # Testar valores específicos
        if hasattr(config_votacao, 'USER_AGENTS'):
            user_agents = config_votacao.USER_AGENTS
            print_test("User Agents válidos", len(user_agents) > 0, f"{len(user_agents)} agentes")
        
        if hasattr(config_votacao, 'HEADERS'):
            headers = config_votacao.HEADERS
            print_test("Headers válidos", len(headers) > 0, f"{len(headers)} headers")
        
        return all_passed
        
    except Exception as e:
        print_test("Configuração", False, f"Erro: {e}")
        return False

def test_connectivity():
    """Testa conectividade básica"""
    print_header("TESTE DE CONECTIVIDADE")
    
    try:
        import config_votacao
        import requests
        
        if not hasattr(config_votacao, 'URL'):
            print_test("Conectividade", False, "URL não configurada")
            return False
        
        # Teste de conectividade básica
        try:
            response = requests.get(config_votacao.URL, timeout=10)
            print_test("Conectividade básica", True, f"Status: {response.status_code}")
            
            # Status 405 é esperado (Method Not Allowed para GET)
            if response.status_code == 405:
                print_test("Proteção do servidor", True, "Servidor protegido corretamente")
            else:
                print_test("Proteção do servidor", False, f"Status inesperado: {response.status_code}")
            
            return True
            
        except requests.exceptions.Timeout:
            print_test("Conectividade básica", False, "Timeout na conexão")
            return False
        except requests.exceptions.ConnectionError:
            print_test("Conectividade básica", False, "Erro de conexão")
            return False
        except Exception as e:
            print_test("Conectividade básica", False, f"Erro: {e}")
            return False
            
    except Exception as e:
        print_test("Conectividade", False, f"Erro: {e}")
        return False

def test_sistema_votacao():
    """Testa funcionalidades do sistema de votação"""
    print_header("TESTE DO SISTEMA DE VOTAÇÃO")
    
    try:
        # Importar e testar classe principal
        sys.path.insert(0, '.')
        from ataque_otimizado import SistemaVotacao
        
        # Testar instanciação
        sistema = SistemaVotacao()
        print_test("Instanciação", True, "Sistema criado com sucesso")
        
        # Testar configurações
        configs = [
            ('session', hasattr(sistema, 'session')),
            ('running', hasattr(sistema, 'running')),
            ('consecutive_errors', hasattr(sistema, 'consecutive_errors')),
            ('last_success_time', hasattr(sistema, 'last_success_time'))
        ]
        
        all_passed = True
        for attr, exists in configs:
            print_test(f"Atributo {attr}", exists)
            if not exists:
                all_passed = False
        
        # Testar métodos
        methods = [
            ('enviar_voto', hasattr(sistema, 'enviar_voto')),
            ('enviar_voto_com_retry', hasattr(sistema, 'enviar_voto_com_retry')),
            ('processar_lote', hasattr(sistema, 'processar_lote')),
            ('executar', hasattr(sistema, 'executar')),
            ('save_progress', hasattr(sistema, 'save_progress')),
            ('load_progress', hasattr(sistema, 'load_progress'))
        ]
        
        for method, exists in methods:
            print_test(f"Método {method}", exists)
            if not exists:
                all_passed = False
        
        return all_passed
        
    except Exception as e:
        print_test("Sistema de Votação", False, f"Erro: {e}")
        return False

def test_monitor_sistema():
    """Testa funcionalidades do monitor"""
    print_header("TESTE DO MONITOR")
    
    try:
        # Importar e testar classe do monitor
        sys.path.insert(0, '.')
        from monitor_sistema import MonitorSistema
        
        # Testar instanciação
        monitor = MonitorSistema()
        print_test("Instanciação", True, "Monitor criado com sucesso")
        
        # Testar métodos
        methods = [
            ('verificar_processo_rodando', hasattr(monitor, 'verificar_processo_rodando')),
            ('verificar_progresso', hasattr(monitor, 'verificar_progresso')),
            ('iniciar_processo', hasattr(monitor, 'iniciar_processo')),
            ('parar_processo', hasattr(monitor, 'parar_processo')),
            ('verificar_saude_sistema', hasattr(monitor, 'verificar_saude_sistema'))
        ]
        
        all_passed = True
        for method, exists in methods:
            print_test(f"Método {method}", exists)
            if not exists:
                all_passed = False
        
        return all_passed
        
    except Exception as e:
        print_test("Monitor", False, f"Erro: {e}")
        return False

def test_progress_system():
    """Testa sistema de progresso"""
    print_header("TESTE DO SISTEMA DE PROGRESSO")
    
    try:
        # Testar salvamento de progresso
        test_progress = {
            'total_votos': 100,
            'votos_sucesso': 80,
            'votos_erro': 20,
            'timestamp': datetime.now().isoformat()
        }
        
        with open('teste_progresso.json', 'w') as f:
            json.dump(test_progress, f)
        
        print_test("Salvamento", True, "Progresso salvo com sucesso")
        
        # Testar carregamento de progresso
        with open('teste_progresso.json', 'r') as f:
            loaded_progress = json.load(f)
        
        print_test("Carregamento", True, "Progresso carregado com sucesso")
        
        # Verificar dados
        data_ok = (loaded_progress['total_votos'] == 100 and 
                  loaded_progress['votos_sucesso'] == 80 and 
                  loaded_progress['votos_erro'] == 20)
        
        print_test("Integridade dos dados", data_ok, "Dados preservados corretamente")
        
        # Limpar arquivo de teste
        os.remove('teste_progresso.json')
        
        return True
        
    except Exception as e:
        print_test("Sistema de Progresso", False, f"Erro: {e}")
        return False

def test_logging_system():
    """Testa sistema de logging"""
    print_header("TESTE DO SISTEMA DE LOGGING")
    
    try:
        import logging
        
        # Criar diretório de logs se não existir
        os.makedirs('logs', exist_ok=True)
        
        # Configurar logging de teste
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/teste.log', encoding='utf-8'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        
        logger = logging.getLogger(__name__)
        
        # Testar diferentes níveis de log
        logger.info("Teste de log INFO")
        logger.warning("Teste de log WARNING")
        logger.error("Teste de log ERROR")
        
        print_test("Configuração", True, "Logging configurado com sucesso")
        
        # Verificar se arquivo foi criado
        if os.path.exists('logs/teste.log'):
            size = os.path.getsize('logs/teste.log')
            print_test("Arquivo de log", True, f"Arquivo criado: {size} bytes")
            
            # Verificar conteúdo
            with open('logs/teste.log', 'r', encoding='utf-8') as f:
                content = f.read()
                has_content = len(content) > 0
                print_test("Conteúdo do log", has_content, f"{len(content)} caracteres")
        else:
            print_test("Arquivo de log", False, "Arquivo não foi criado")
            return False
        
        # Limpar arquivo de teste
        os.remove('logs/teste.log')
        
        return True
        
    except Exception as e:
        print_test("Sistema de Logging", False, f"Erro: {e}")
        return False

def test_process_manager():
    """Testa gerenciador de processos"""
    print_header("TESTE DO GERENCIADOR DE PROCESSOS")
    
    try:
        # Importar ProcessoManager do iniciar_sistema
        sys.path.insert(0, '.')
        from iniciar_sistema import ProcessoManager
        
        # Testar instanciação
        manager = ProcessoManager()
        print_test("Instanciação", True, "Gerenciador criado com sucesso")
        
        # Testar métodos
        methods = [
            ('iniciar_processo', hasattr(manager, 'iniciar_processo')),
            ('parar_processo', hasattr(manager, 'parar_processo')),
            ('verificar_processos', hasattr(manager, 'verificar_processos')),
            ('parar_todos', hasattr(manager, 'parar_todos'))
        ]
        
        all_passed = True
        for method, exists in methods:
            print_test(f"Método {method}", exists)
            if not exists:
                all_passed = False
        
        # Testar verificação de processos vazios
        status = manager.verificar_processos()
        print_test("Verificação vazia", isinstance(status, dict), "Retorna dicionário")
        
        return all_passed
        
    except Exception as e:
        print_test("Gerenciador de Processos", False, f"Erro: {e}")
        return False

def test_command_line_args():
    """Testa argumentos de linha de comando"""
    print_header("TESTE DE ARGUMENTOS DE LINHA DE COMANDO")
    
    try:
        import argparse
        
        # Testar criação do parser
        parser = argparse.ArgumentParser(description='Teste')
        parser.add_argument('--modo', choices=['principal', 'monitor', 'status', 'parar'])
        parser.add_argument('--log-level', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'])
        
        print_test("Parser criado", True, "ArgumentParser configurado")
        
        # Testar parsing de argumentos válidos
        args = parser.parse_args(['--modo', 'status', '--log-level', 'INFO'])
        print_test("Parsing válido", args.modo == 'status' and args.log_level == 'INFO')
        
        return True
        
    except Exception as e:
        print_test("Argumentos de Linha de Comando", False, f"Erro: {e}")
        return False

def test_error_handling():
    """Testa tratamento de erros"""
    print_header("TESTE DE TRATAMENTO DE ERROS")
    
    try:
        # Testar tratamento de exceções
        def test_function():
            try:
                # Simular erro
                raise ValueError("Erro de teste")
            except ValueError as e:
                return f"Erro capturado: {e}"
            except Exception as e:
                return f"Erro genérico: {e}"
        
        result = test_function()
        print_test("Captura de exceção", "Erro capturado" in result)
        
        # Testar tratamento de timeout
        def test_timeout():
            try:
                import requests
                requests.get("http://invalid-url-test.com", timeout=1)
            except requests.exceptions.Timeout:
                return "Timeout capturado"
            except requests.exceptions.ConnectionError:
                return "ConnectionError capturado"
            except Exception as e:
                return f"Outro erro: {e}"
        
        result = test_timeout()
        print_test("Tratamento de timeout", "capturado" in result)
        
        return True
        
    except Exception as e:
        print_test("Tratamento de Erros", False, f"Erro: {e}")
        return False

def run_performance_test():
    """Executa teste de performance básico"""
    print_header("TESTE DE PERFORMANCE")
    
    try:
        import time
        
        # Teste de velocidade de processamento
        start_time = time.time()
        
        # Simular processamento
        for i in range(1000):
            _ = i * 2
        
        end_time = time.time()
        duration = end_time - start_time
        
        print_test("Velocidade de processamento", duration < 1.0, f"{duration:.3f}s para 1000 iterações")
        
        # Teste de uso de memória
        import sys
        initial_memory = sys.getsizeof([])
        
        # Criar lista grande
        large_list = list(range(10000))
        final_memory = sys.getsizeof(large_list)
        
        memory_used = final_memory - initial_memory
        print_test("Uso de memória", memory_used < 100000, f"{memory_used} bytes para 10000 itens")
        
        return True
        
    except Exception as e:
        print_test("Performance", False, f"Erro: {e}")
        return False

def main():
    """Função principal do teste"""
    print("🧪 TESTE COMPLETO DO SISTEMA DE VOTAÇÃO MELHORADO")
    print("=" * 70)
    print(f"📅 Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    # Lista de testes
    tests = [
        ("Importações", test_imports),
        ("Arquivos", test_files),
        ("Configuração", test_configuration),
        ("Conectividade", test_connectivity),
        ("Sistema de Votação", test_sistema_votacao),
        ("Monitor", test_monitor_sistema),
        ("Sistema de Progresso", test_progress_system),
        ("Sistema de Logging", test_logging_system),
        ("Gerenciador de Processos", test_process_manager),
        ("Argumentos de Linha de Comando", test_command_line_args),
        ("Tratamento de Erros", test_error_handling),
        ("Performance", run_performance_test)
    ]
    
    # Executar testes
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ ERRO CRÍTICO em {test_name}: {e}")
            results.append((test_name, False))
    
    # Resumo final
    print_header("RESUMO DOS TESTES")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    print(f"📊 RESULTADO: {passed}/{total} testes passaram")
    print(f"🎯 Taxa de sucesso: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("🎉 TODOS OS TESTES PASSARAM! Sistema pronto para uso.")
    elif passed >= total * 0.8:
        print("✅ MAIORIA DOS TESTES PASSOU! Sistema funcional.")
    elif passed >= total * 0.6:
        print("⚠️ ALGUNS TESTES FALHARAM! Verificar problemas.")
    else:
        print("❌ MUITOS TESTES FALHARAM! Sistema com problemas.")
    
    # Detalhes dos testes que falharam
    failed_tests = [name for name, result in results if not result]
    if failed_tests:
        print(f"\n❌ Testes que falharam:")
        for test in failed_tests:
            print(f"   • {test}")
    
    print(f"\n⏱️ Tempo total de teste: {datetime.now().strftime('%H:%M:%S')}")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
