# Construção — Pipeline ETL de Análise de Notícias com IA
> Última atualização: 2026-09-23 · Etapa atual: E2 — Enrich hello world · Nível de ajuda: N1
> Arquitetura de referência: (nenhum ARQUITETURA-*.md ainda — decisões tomadas em conversa)

## Plano de construção
- [x] E1 — Hello world ponta a ponta (NewsAPI → SQLite raw)
- [ ] E2 — Enrich hello world (Gemini → SQLite enriched)
- [ ] E3 — Extract robusto (N notícias, sem duplicar)
- [ ] E4 — Enrich robusto (lote, idempotência, erros)
- [ ] E5 — Transform (agregações → SQLite mart)

---

## E1 — Hello world ponta a ponta
**Objetivo:** provar o cano inteiro NewsAPI → SQLite `raw` funcionando com 1 notícia só, antes de investir em robustez.
**Critério de pronto:** `python extract.py` roda sem erro e `raw.db` fica com 1 linha em `articles`.
**Como eu resolvi:** "A E1 foi uma construção inicial do funcionamento do projeto, de forma vertical. Foi feita a extração dos dados de notícias via API por um script Python (`extract.py`), que faz a chamada e coloca o resultado num banco SQLite, importando as funções de criação de conexão, criação de tabela e inserção de outro script Python, o `raw.py`. No final, ficou a tabela com o JSON transformado, com id, fonte, autor, título, descrição, url, data de publicação e data de extração. Um ETL completo, de ponta a ponta."
**Conceito novo:** camada `raw` (guardar o dado cru, sem transformar, como rede de segurança) · `.env`/`python-dotenv` pra manter segredo fora do código · `INSERT OR IGNORE` + `UNIQUE` como dedupe básico no SQLite.
**Comandos usados:**
```bash
python -m venv venv               # cria ambiente virtual isolado
pip install requests python-dotenv  # instala libs do projeto
git init                          # inicia repositório git local
python extract.py                 # roda o pipeline (extract -> raw.db)
```
**Erros que apareceram:**
- `IndexError: list index out of range` → filtro `country=br` + `category=technology` no `/top-headlines` não tinha cobertura (totalResults=0) → resolvido tirando `country` e mantendo só `category`.
- Parâmetro `country` usado por engano em `/v2/everything` (é parâmetro de `/top-headlines`, não daquele endpoint) → corrigido trocando de endpoint.
**Nível de ajuda usado:** N1 (extract.py) e N2 (esqueleto pra ligar extract.py com raw.py). A parte de `criar_tabela`/`inserir_artigo` em `scripts/raw.py` foi escrita por IA (N4, a pedido explícito) — ver dívida de entendimento.

---

## Dívida de entendimento
- [ ] `criar_tabela` e `inserir_artigo` em `scripts/raw.py` — escritas pela IA a pedido do usuário, não construídas por ele. Revisitar: no checkpoint da fatia (antes de fechar E3, quando extract.py escala pra N notícias e essa lógica de dedupe passa a importar de verdade).

## Dúvidas em aberto

## Próxima etapa
E2 — Enrich hello world (pegar a notícia do raw, mandar pro Gemini, salvar em enriched)
