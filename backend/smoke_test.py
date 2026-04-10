"""
LAMD 60445 — Lab 07: Smoke Test da API REST
============================================
Professor: Cristiano de Macedo Neto — PUC Minas

Execute este script ANTES de abrir o projeto Flutter para confirmar que
o backend Flask está respondendo corretamente em localhost:5000.

O script reproduz exatamente o que o cliente Flutter fará:
  1. Verifica o endpoint /health
  2. Lista todos os itens (GET /itens)
  3. Cria um item de teste (POST /itens)
  4. Busca o item criado (GET /itens/<id>)
  5. Testa tratamento de erro: busca id inexistente (deve retornar 404)
  6. Testa validação: envia payload incompleto (deve retornar 400)

Cada etapa imprime o resultado no terminal com detalhes suficientes para
responder às questões de reflexão do roteiro.

Execução:
    python smoke_test.py

Dependências: apenas a biblioteca padrão Python (urllib).
"""

import json
import sys
import time
import urllib.request
import urllib.error

BASE_URL = "http://localhost:5000"

# ── Cores ANSI para terminal ───────────────────────────────────────────────
VERDE   = "\033[92m"
VERMELHO = "\033[91m"
AMARELO = "\033[93m"
CIANO   = "\033[96m"
RESET   = "\033[0m"
BOLD    = "\033[1m"

def ok(msg):    print(f"  {VERDE}✓{RESET}  {msg}")
def erro(msg):  print(f"  {VERMELHO}✗{RESET}  {msg}")
def info(msg):  print(f"  {CIANO}→{RESET}  {msg}")
def titulo(msg): print(f"\n{BOLD}{AMARELO}{'─'*55}{RESET}\n{BOLD}  {msg}{RESET}")

# ── Utilitário HTTP ────────────────────────────────────────────────────────

def _req(metodo: str, path: str, body: dict = None) -> tuple[int, dict | list | None]:
    """
    Realiza uma requisição HTTP e retorna (status_code, json_body).
    Usa apenas urllib da stdlib para não exigir instalação de pacotes extras.
    """
    url = BASE_URL + path
    headers = {"Content-Type": "application/json", "Accept": "application/json"}

    data_bytes = json.dumps(body).encode("utf-8") if body else None
    req = urllib.request.Request(url, data=data_bytes, headers=headers, method=metodo)

    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            latencia = (time.time() - t0) * 1000
            conteudo = json.loads(resp.read().decode("utf-8"))
            return resp.status, conteudo, latencia
    except urllib.error.HTTPError as e:
        latencia = (time.time() - t0) * 1000
        try:
            conteudo = json.loads(e.read().decode("utf-8"))
        except Exception:
            conteudo = {"erro": str(e)}
        return e.code, conteudo, latencia
    except urllib.error.URLError as e:
        print(f"\n{VERMELHO}ERRO DE CONEXÃO:{RESET} Não foi possível conectar em {BASE_URL}")
        print(f"  Certifique-se de que o servidor Flask está rodando: python app.py")
        print(f"  Detalhe: {e.reason}\n")
        sys.exit(1)


def _imprimir_resposta(status: int, corpo, latencia: float):
    cor = VERDE if 200 <= status < 300 else VERMELHO
    print(f"  {cor}HTTP {status}{RESET}  ({latencia:.0f} ms)")
    corpo_str = json.dumps(corpo, ensure_ascii=False, indent=4)
    # Recua cada linha para alinhamento visual
    for linha in corpo_str.splitlines():
        print(f"    {linha}")


# ══════════════════════════════════════════════════════════════════════════
# TESTES
# ══════════════════════════════════════════════════════════════════════════

print(f"\n{BOLD}{'═'*55}")
print(f"  LAMD 60445 — Lab 07 — Smoke Test da API REST")
print(f"  Backend: {BASE_URL}")
print(f"{'═'*55}{RESET}")

resultados = {"passou": 0, "falhou": 0}

# ── Teste 1: /health ───────────────────────────────────────────────────────
titulo("TESTE 1 — Verificação de saúde do servidor")
info(f"GET {BASE_URL}/health")
status, corpo, lat = _req("GET", "/health")
_imprimir_resposta(status, corpo, lat)

if status == 200 and corpo.get("status") == "ok":
    ok("Servidor respondendo corretamente.")
    ok(f"Total de itens no servidor: {corpo.get('total_itens', '?')}")
    resultados["passou"] += 1
else:
    erro("Resposta inesperada do /health.")
    resultados["falhou"] += 1

# ── Teste 2: GET /itens ───────────────────────────────────────────────────
titulo("TESTE 2 — Listagem de itens (GET /itens)")
info(f"GET {BASE_URL}/itens")
status, corpo, lat = _req("GET", "/itens")
_imprimir_resposta(status, corpo, lat)

if status == 200 and isinstance(corpo, list):
    ok(f"Lista recebida com {len(corpo)} item(ns).")
    ok("Campos presentes no primeiro item: " +
       ", ".join(corpo[0].keys()) if corpo else "(lista vazia)")
    resultados["passou"] += 1
else:
    erro("Resposta inesperada para GET /itens.")
    resultados["falhou"] += 1

# ── Teste 3: POST /itens ──────────────────────────────────────────────────
titulo("TESTE 3 — Criação de item (POST /itens)")
payload = {"nome": "Item de Teste — Lab 07", "preco": 42.00, "categoria": "teste"}
info(f"POST {BASE_URL}/itens")
info(f"Payload: {json.dumps(payload, ensure_ascii=False)}")
status, corpo, lat = _req("POST", "/itens", body=payload)
_imprimir_resposta(status, corpo, lat)

if status == 201 and "id" in corpo:
    id_criado = corpo["id"]
    ok(f"Item criado com sucesso. id={id_criado}")
    ok(f"Nome retornado: '{corpo.get('nome')}'")
    ok(f"Preço retornado: {corpo.get('preco')}")
    resultados["passou"] += 1
else:
    erro(f"Esperado HTTP 201, recebido {status}.")
    id_criado = None
    resultados["falhou"] += 1

# ── Teste 4: GET /itens/<id> ──────────────────────────────────────────────
titulo("TESTE 4 — Busca por ID (GET /itens/<id>)")
if id_criado:
    info(f"GET {BASE_URL}/itens/{id_criado}")
    status, corpo, lat = _req("GET", f"/itens/{id_criado}")
    _imprimir_resposta(status, corpo, lat)

    if status == 200 and corpo.get("id") == id_criado:
        ok(f"Item id={id_criado} recuperado corretamente.")
        resultados["passou"] += 1
    else:
        erro("Item não encontrado após criação.")
        resultados["falhou"] += 1
else:
    info("Teste ignorado (item não foi criado no Teste 3).")

# ── Teste 5: Erro 404 ─────────────────────────────────────────────────────
titulo("TESTE 5 — Tratamento de erro 404 (id inexistente)")
id_inexistente = 99999
info(f"GET {BASE_URL}/itens/{id_inexistente}")
status, corpo, lat = _req("GET", f"/itens/{id_inexistente}")
_imprimir_resposta(status, corpo, lat)

if status == 404:
    ok("Servidor retornou 404 corretamente para id inexistente.")
    ok("O cliente Flutter deve exibir mensagem de erro ao receber este status.")
    resultados["passou"] += 1
else:
    erro(f"Esperado HTTP 404, recebido {status}.")
    resultados["falhou"] += 1

# ── Teste 6: Validação 400 ────────────────────────────────────────────────
titulo("TESTE 6 — Validação de payload inválido (POST sem 'preco')")
payload_invalido = {"nome": "Item sem preço"}  # falta o campo 'preco'
info(f"POST {BASE_URL}/itens")
info(f"Payload incompleto: {json.dumps(payload_invalido)}")
status, corpo, lat = _req("POST", "/itens", body=payload_invalido)
_imprimir_resposta(status, corpo, lat)

if status == 400:
    ok("Servidor rejeitou payload inválido com 400 Bad Request.")
    ok("O cliente Flutter deve tratar este erro e exibir feedback ao usuário.")
    resultados["passou"] += 1
else:
    erro(f"Esperado HTTP 400, recebido {status}.")
    resultados["falhou"] += 1

# ── Teste 7: Filtro por categoria ─────────────────────────────────────────
titulo("TESTE 7 — Filtro por categoria (GET /itens?categoria=eletronicos)")
info(f"GET {BASE_URL}/itens?categoria=eletronicos")
status, corpo, lat = _req("GET", "/itens?categoria=eletronicos")
_imprimir_resposta(status, corpo, lat)

if status == 200 and isinstance(corpo, list):
    todos_eletronicos = all(i.get("categoria") == "eletronicos" for i in corpo)
    if todos_eletronicos:
        ok(f"Filtro funcionou: {len(corpo)} item(ns) da categoria 'eletronicos'.")
        resultados["passou"] += 1
    else:
        erro("Filtro retornou itens de outras categorias.")
        resultados["falhou"] += 1
else:
    erro("Falha na requisição de filtro.")
    resultados["falhou"] += 1

# ── Resumo ────────────────────────────────────────────────────────────────
total = resultados["passou"] + resultados["falhou"]
print(f"\n{BOLD}{'═'*55}{RESET}")
print(f"{BOLD}  RESULTADO: {resultados['passou']}/{total} testes passaram{RESET}")

if resultados["falhou"] == 0:
    print(f"{VERDE}{BOLD}  ✓ Backend pronto! Abra o projeto Flutter.{RESET}")
else:
    print(f"{VERMELHO}{BOLD}  ✗ Corrija os erros acima antes de iniciar o Flutter.{RESET}")

print(f"{BOLD}{'═'*55}{RESET}\n")

print(f"{AMARELO}OBSERVAÇÃO PARA REFLEXÃO:{RESET}")
print("  Anote as latências acima (coluna entre parênteses).")
print("  A Q4 do reflexao.md pergunta o que aconteceria se a UI")
print("  bloqueasse esperando estas respostas sem async/await.")
print()
