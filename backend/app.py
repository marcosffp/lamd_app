"""
LAMD 60445 — Lab 07: Backend Flask de Referência
=================================================
Professores: Cleiton Silva e Cristiano Neto — PUC Minas

Este servidor simula o backend do Lab 05 que os alunos já desenvolveram.
Ele expõe uma API REST simples para que o cliente Flutter possa:
  - GET  /itens          → listar todos os itens
  - POST /itens          → criar um novo item
  - GET  /itens/<id>     → buscar item por ID
  - PUT  /itens/<id>     → atualizar item
  - DELETE /itens/<id>   → remover item
  - GET  /health         → verificar se o servidor está vivo

Execução:
    python app.py

O servidor escuta em http://0.0.0.0:5000
No emulador Android, acesse via http://10.0.2.2:5000
Em dispositivo físico, use o IP da máquina na rede local (ex.: 192.168.1.X:5000)

Dependências:
    pip install flask flask-cors
"""

import json
import time
import threading
from flask import Flask, request, jsonify, abort
from flask_cors import CORS  # habilita CORS para clientes web/mobile

# ── Inicialização ──────────────────────────────────────────────────────────
app = Flask(__name__)
CORS(app)  # permite requisições de qualquer origem (necessário para emuladores)

# ── "Banco de dados" em memória ────────────────────────────────────────────
# Em produção, substitua por SQLite ou PostgreSQL (Lab 05/06).
_lock = threading.Lock()  # protege acesso concorrente ao dicionário
_proximo_id = 1
_itens: dict[int, dict] = {}

# Dados iniciais para facilitar os testes
_dados_iniciais = [
    {"nome": "Notebook Dell XPS 15",  "preco": 7499.90, "categoria": "eletronicos"},
    {"nome": "Mouse sem fio Logitech", "preco":  189.90, "categoria": "perifericos"},
    {"nome": "Teclado mecânico Keychron", "preco": 399.00, "categoria": "perifericos"},
    {"nome": "Monitor 27\" LG 4K",    "preco": 2899.00, "categoria": "eletronicos"},
    {"nome": "Headset Sony WH-1000XM5", "preco": 1599.00, "categoria": "audio"},
]

def _seed():
    """Popula o banco com dados iniciais."""
    global _proximo_id
    for d in _dados_iniciais:
        _itens[_proximo_id] = {"id": _proximo_id, **d}
        _proximo_id += 1

_seed()


# ── Utilitários ────────────────────────────────────────────────────────────

def _item_ou_404(item_id: int) -> dict:
    """Retorna o item ou aborta com 404."""
    item = _itens.get(item_id)
    if item is None:
        abort(404, description=f"Item com id={item_id} não encontrado.")
    return item


def _validar_payload(data: dict, exigir_campos: bool = True) -> tuple[str, float]:
    """
    Valida os campos 'nome' e 'preco' do payload JSON.
    Levanta ValueError com mensagem descritiva se inválido.
    """
    if exigir_campos and "nome" not in data:
        raise ValueError("Campo 'nome' é obrigatório.")
    if exigir_campos and "preco" not in data:
        raise ValueError("Campo 'preco' é obrigatório.")

    nome = data.get("nome", "").strip()
    if "nome" in data and not nome:
        raise ValueError("Campo 'nome' não pode ser vazio.")

    preco_raw = data.get("preco")
    if preco_raw is not None:
        try:
            preco = float(preco_raw)
        except (TypeError, ValueError):
            raise ValueError("Campo 'preco' deve ser um número.")
        if preco < 0:
            raise ValueError("Campo 'preco' não pode ser negativo.")
    else:
        preco = None

    return nome, preco


# ── Middleware de log ──────────────────────────────────────────────────────

@app.before_request
def _log_request():
    ts = time.strftime("%H:%M:%S")
    print(f"[{ts}] {request.method:6s} {request.path}", flush=True)


# ── Rotas ──────────────────────────────────────────────────────────────────

@app.route("/health", methods=["GET"])
def health():
    """Verifica se o servidor está operacional."""
    return jsonify({
        "status": "ok",
        "total_itens": len(_itens),
        "timestamp": time.time()
    })


@app.route("/itens", methods=["GET"])
def listar_itens():
    """
    GET /itens
    Retorna todos os itens cadastrados.
    Aceita query param ?categoria=<valor> para filtrar.
    """
    categoria = request.args.get("categoria")
    with _lock:
        resultado = list(_itens.values())

    if categoria:
        resultado = [i for i in resultado if i.get("categoria") == categoria]

    # Ordena por id para resposta determinista
    resultado.sort(key=lambda x: x["id"])
    return jsonify(resultado), 200


@app.route("/itens/<int:item_id>", methods=["GET"])
def buscar_item(item_id: int):
    """
    GET /itens/<id>
    Retorna um item específico pelo ID.
    """
    with _lock:
        item = _item_ou_404(item_id)
    return jsonify(item), 200


@app.route("/itens", methods=["POST"])
def criar_item():
    """
    POST /itens
    Cria um novo item.
    Body JSON: {"nome": str, "preco": float, "categoria": str (opcional)}
    Retorna o item criado com status 201 Created.
    """
    global _proximo_id
    data = request.get_json(silent=True)
    if not data:
        abort(400, description="Body JSON inválido ou ausente.")

    try:
        nome, preco = _validar_payload(data, exigir_campos=True)
    except ValueError as e:
        abort(400, description=str(e))

    categoria = data.get("categoria", "geral").strip()

    with _lock:
        novo = {
            "id": _proximo_id,
            "nome": nome,
            "preco": preco,
            "categoria": categoria,
        }
        _itens[_proximo_id] = novo
        _proximo_id += 1

    print(f"  → Item criado: id={novo['id']} nome='{novo['nome']}'", flush=True)
    return jsonify(novo), 201


@app.route("/itens/<int:item_id>", methods=["PUT"])
def atualizar_item(item_id: int):
    """
    PUT /itens/<id>
    Atualiza completamente um item existente.
    Body JSON: {"nome": str, "preco": float, "categoria": str (opcional)}
    """
    data = request.get_json(silent=True)
    if not data:
        abort(400, description="Body JSON inválido ou ausente.")

    try:
        nome, preco = _validar_payload(data, exigir_campos=True)
    except ValueError as e:
        abort(400, description=str(e))

    categoria = data.get("categoria", "geral").strip()

    with _lock:
        item = _item_ou_404(item_id)
        item.update({"nome": nome, "preco": preco, "categoria": categoria})

    return jsonify(item), 200


@app.route("/itens/<int:item_id>", methods=["DELETE"])
def remover_item(item_id: int):
    """
    DELETE /itens/<id>
    Remove um item pelo ID.
    Retorna 204 No Content em caso de sucesso.
    """
    with _lock:
        _item_ou_404(item_id)
        del _itens[item_id]

    print(f"  → Item removido: id={item_id}", flush=True)
    return "", 204


# ── Tratamento de erros ────────────────────────────────────────────────────

@app.errorhandler(400)
def bad_request(e):
    return jsonify({"erro": str(e.description)}), 400

@app.errorhandler(404)
def not_found(e):
    return jsonify({"erro": str(e.description)}), 404

@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({"erro": "Método HTTP não permitido para esta rota."}), 405


# ── Entrada ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 60)
    print("  LAMD 60445 — Lab 07 — Backend Flask")
    print("  Servidor iniciado em http://0.0.0.0:5000")
    print("  Emulador Android: http://10.0.2.2:5000")
    print(f"  Itens iniciais carregados: {len(_itens)}")
    print("=" * 60)
    # debug=False em produção; use True apenas para desenvolvimento
    app.run(host="0.0.0.0", port=5000, debug=True)
