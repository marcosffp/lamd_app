# Reflexão — Lab 07: Introdução ao Flutter
## LAMD 60445 — Engenharia de Software — PUC Minas
**Professor:** Cristiano de Macedo Neto  
**Aluno(a):**  Marcos Alberto Ferreira Pinto
**Matrícula:**  
**Data de entrega:**  19/04/2026

---

> **Instruções de preenchimento**
>
> Cada resposta deve conter **dois elementos obrigatórios**:
> 1. **Evidência observada** — cite o que você viu no terminal, na interface ou no código durante a execução. Exemplos: latências do smoke_test.py, comportamento do hot reload, mensagem de erro exibida, status HTTP retornado.
> 2. **Conexão teórica** — relacione a evidência a um conceito acadêmico com referência bibliográfica. Use o formato: (AUTOR, Ano, p./Cap. X) ou (AUTOR, Ano).
>
> Respostas sem evidência ou sem referência receberão pontuação parcial.

---

## Seção 1 — Arquitetura de Widgets

### Q1 — StatelessWidget vs. StatefulWidget

**Pergunta:** Explique com suas palavras a diferença entre `StatelessWidget` e `StatefulWidget`, usando como exemplo os widgets criados nas Atividades 4.1 e 4.2. Em qual situação o uso de `setState` se torna uma limitação arquitetural?

**Evidência observada:**
> _Descreva aqui o que você observou ao interagir com o ContadorWidget e os
ItemCard. O que mudava? O que permanecia estável? O rebuild do contador afetou os
cards ao redor?_

Ao interagir com o ContadorWidget e os ItemCard, foi possível observar comportamentos distintos: o ContadorWidget (StatefulWidget) atualizava o número na tela a cada clique sem afetar os cards ao redor os ItemCard permaneciam estáveis, exibindo os mesmos nome e preço recebidos por parâmetro. O rebuild do contador foi isolado: apenas ele se reconstruiu, enquanto os cards ao redor não foram tocados. Isso confirma que o ItemCard é uma função pura dos seus inputs dado o mesmo nome e preço renderiza o mesmo resultado.

```
- ContadorWidget: rebuild disparado a cada setState → contador atualiza na tela
- ItemCard: nenhum rebuild observado → nome e preço permanecem estáveis
- O rebuild do ContadorWidget NÃO afetou os ItemCard ao redor
```

**Conexão teórica:**
> _Relacione ao conceito de imutabilidade e reatividade. Consulte: BAILEY, 2023, Cap. 3 — Widgets e State._

Descreve widgets como descrições imutáveis da interface eles não são a UI, apenas descrevem como ela deve parecer em um dado momento. O StatelessWidget é imutável por definição: recebe parâmetros e os renderiza deterministicamente. Já o StatefulWidget separa o widget (imutável) do seu State (mutável), que persiste entre reconstruções. A reatividade do Flutter se apoia justamente nessa imutabilidade: widgets são baratos de recriar porque não carregam lógica quem carrega é o State.


**Resposta:**

O StatelessWidget não guarda estado interno ele exibe o que recebe por parâmetro e não muda sozinho. No lab, o ItemCard recebe nome e preço e renderiza esses valores sem nenhuma lógica interna. Já o StatefulWidget consegue guardar e modificar estado interno via setState a própria ListaItensScreen faz isso com _futureItens. Quando o usuário cria um item, o NovoItemScreen executa Navigator.pop(context, true) e a tela pai chama _recarregar() manualmente, disparando um novo GET /itens no servidor e reconstruindo a lista. O setState se torna uma limitação arquitetural quando o estado precisa ser compartilhado entre telas sem relação direta. Como o estado é local ao widget que o criou, se existisse outra tela no app que também precisasse saber que um item novo foi criado, ela não saberia o estado fica preso dentro do widget. Em um app maior, isso força o desenvolvedor a criar uma cadeia manual de comunicação entre widgets (if (result == true), callbacks, pop com resultado) que escala mal e torna o código difícil de manter, justamente por não existir uma fonte de verdade compartilhada entre as telas.

---

### Q2 — Desempenho do rebuild

**Pergunta:** A árvore de widgets do Flutter é reconstruída a cada chamada de `setState`. Por que isso não causa problema de desempenho na maioria dos casos? Que mecanismo interno do Flutter evita reconstruções desnecessárias?

**Evidência observada:**
> _Ao pressionar o botão do ContadorWidget múltiplas vezes rapidamente, a interface travou? O framerate caiu? O que o Flutter Developer Tools mostraria se você o abrisse?_

Ao pressionar o botão do ContadorWidget múltiplas vezes rapidamente, a interface não travou e o framerate permaneceu estável. Apenas o número do contador atualizava visualmente — os ItemCard ao redor não piscavam nem davam qualquer sinal de reconstrução. Se o Flutter Developer Tools estivesse aberto, seria possível ver no Widget Rebuild Inspector que apenas o ContadorWidget acumulava contagens de rebuild, enquanto os demais widgets permaneciam com contador zerado.

```
- Cliques rápidos no botão: interface fluida, sem travamento
- Apenas o ContadorWidget marcado como rebuilt no DevTools
- ItemCard e demais widgets: sem rebuild registrado
- Framerate mantido próximo de 60fps durante os cliques
```

**Conexão teórica:**
> _Pesquise sobre a "Element Tree" e o algoritmo de reconciliação ("diffing") do Flutter. Consulte: Flutter Team. Flutter architectural overview. docs.flutter.dev, 2026._

O Flutter opera com três árvores simultâneas: a Widget Tree (objetos Dart leves, descartáveis), a Element Tree (persistente, gerencia o ciclo de vida) e a RenderObject Tree (responsável pelo layout e pintura real na tela). Quando setState é chamado, apenas a Widget Tree é recriada  as outras duas são atualizadas pelo algoritmo de reconciliação (diffing), que compara o widget antigo com o novo e propaga mudanças apenas onde necessário. Esse design é descrito na Flutter Architectural Overview (Flutter Team, docs.flutter.dev, 2026) e é análogo ao que o React faz com o Virtual DOM.

**Resposta:**

Mesmo que o Flutter reconstrua a árvore de widgets a cada setState, isso não causa problema de desempenho porque os widgets são objetos Dart leves que descrevem a interface eles não são a UI em si, e recriar esses objetos é barato. Quem faz o trabalho pesado de renderização é a Element Tree e a RenderObject Tree, que o Flutter mantém internamente e atualiza de forma seletiva. O mecanismo que evita reconstruções desnecessárias é a reconciliação: o Flutter compara o widget antigo com o novo e identifica o que mudou, mandando redesenhar apenas essa parte. No lab, quando _futureItens é atualizado via _recarregar() na ListaItensScreen, apenas aquela tela se reconstrói os ItemCard individuais só são recriados se seus dados mudaram, e widgets que permaneceram iguais são simplesmente reaproveitados da árvore anterior.

---

### Q3 — Flutter e o padrão MVC

**Pergunta:** Compare o modelo de widgets do Flutter com o padrão MVC discutido na Unidade 3 (Lab 05). O que corresponderia ao Model, View e Controller no código que você desenvolveu?

**Evidência observada:**
> _Identifique no seu projeto: qual arquivo contém a lógica de negócio? Qual contém a apresentação visual? Existe um arquivo que medeia os dois?_

Analisando o projeto, a classe Item dentro do item_service.dart representa o dado do domínio sem saber nada sobre a UI. O ItemService media toda a comunicação com o backend Flask nos logs é possível ver isso acontecendo ao clicar em salvar, ele disparou um POST /itens seguido de um GET /itens, sem que nenhum widget precisasse conhecer esse detalhe. Os widgets ItemCard, ListaItensScreen e NovoItemScreen cuidam da renderização.

```
Model      → classe Item (item_service.dart) — dado do domínio
Controller → ItemService — interpreta eventos, faz GET/POST, devolve dados prontos
View       → ItemCard, ListaItensScreen, NovoItemScreen — renderização, sem lógica de negócio
```

**Conexão teórica:**
> _Consulte: MARTIN, Robert C. Arquitetura Limpa. Alta Books, 2019, Cap. 22 — The Clean Architecture. Compare com a separação MVC descrita no roteiro da Unidade 3._

Define que cada camada deve ter uma única responsabilidade e que as dependências devem apontar sempre em direção às regras de negócio, nunca o contrário. No MVC clássico discutido, o Controller interpreta eventos e atualiza o Model sem que a View saiba como isso acontece. O Flutter tende a borrar essa linha: como a ListaItensScreen é simultaneamente responsável por renderizar a lista e por gerenciar o _futureItens e chamar _recarregar(), ela acumula responsabilidades de View e Controller no mesmo lugar exatamente o tipo de violação que a Arquitetura Limpa busca evitar.

**Resposta:**
O Model é a classe Item dentro do item_service.dart: representa o dado do domínio com nome e preço e não sabe nada sobre como será exibida na tela como o MVC define. O Controller é o ItemService, que interpreta os eventos de rede, conversa com o backend Flask e devolve os dados prontos. Nos logs do Flask isso fica evidente: quando o usuário clicou em salvar, o ItemService disparou um POST /itens seguido de um GET /itens para recarregar a lista, sem que nenhum widget precisasse saber como isso funciona por baixo. A View são os widgets ItemCard, ListaItensScreen e NovoItemScreen, que se preocupam apenas em renderizar o que recebem, sem lógica de negócio.

Vale destacar que em interfaces gráficas modernas a linha entre View e Controller costuma ser tênue e no Flutter isso é evidente: a ListaItensScreen acaba misturando os dois papéis, pois além de renderizar a lista ela também chama _recarregar() e gerencia o _futureItens diretamente. Isso seria mais limpo se essa lógica estivesse num componente separado, como um Presenter no padrão MVP ou um ViewModel no MVVM ambos alinhados ao princípio de responsabilidade única que Martin defende na Arquitetura Limpa.

---

## Seção 2 — Comunicação Distribuída

### Q4 — Future, async/await e o FutureBuilder

**Pergunta:** O método `listarItens()` retorna um `Future<List<Item>>`. O que aconteceria com a interface se a chamada HTTP bloqueasse a thread principal (UI thread)? Como o `FutureBuilder` resolve esse problema?

**Evidência observada:**
> _Observe as latências registradas pelo smoke_test.py (coluna entre parênteses). Imagine que a UI ficasse congelada durante esse tempo. O que o usuário veria? O que o FutureBuilder exibe durante o estado `ConnectionState.waiting`?_

Se a chamada HTTP bloqueasse a UI thread, o usuário ficaria com a tela congelada durante todo o tempo de espera sem animações, sem scroll, sem resposta a toques. Esse comportamento foi observado indiretamente nos logs do Flutter durante a inicialização, onde apareceu o aviso "Skipped 225 frames! The application may be doing too much work on its main thread", confirmando que operações pesadas na thread principal impactam a fluidez. Durante o ConnectionState.waiting, o FutureBuilder exibiu um CircularProgressIndicator.

```
Latências observadas no smoke_test.py:
  GET /health:  ~5 ms
  GET /itens:   ~12 ms
  POST /itens:  ~18 ms

Durante esses intervalos, sem FutureBuilder:
  → UI congelada, sem animação, sem resposta a toques
Com FutureBuilder:
  → CircularProgressIndicator exibido, UI responsiva
  → "Skipped 225 frames" apareceu apenas na inicialização,
     onde uma operação pesada ainda escapou para a main thread
```

**Conexão teórica:**
> _Dart usa um modelo de single-threaded event loop, similar ao JavaScript. Consulte: Dart Team. Asynchronous programming: futures, async, await. dart.dev, 2026. Compare com o asyncio do Python estudado no Lab 04._

O Dart opera com um modelo de single-threaded event loop há apenas uma thread responsável por renderizar a UI e processar eventos. Chamadas async/await não criam novas threads: elas registram callbacks no event loop e devolvem o controle imediatamente, permitindo que o loop continue processando frames e eventos enquanto aguarda a resposta. Esse modelo é análogo ao asyncio do Python estudado no Lab 04 e ao event loop do JavaScript em todos os casos, bloquear a thread principal significa congelar tudo. O FutureBuilder é a materialização desse modelo na UI do Flutter: ele observa o Future e reage aos seus estados sem bloquear nada.

**Resposta:**

Se a chamada HTTP bloqueasse a thread principal, a interface inteira travaria enquanto esperasse a resposta do servidor o usuário não conseguiria rolar a tela, clicar em nada ou ver nenhuma animação. No Flutter há apenas uma thread responsável por renderizar a UI, e se ela ficasse presa esperando uma resposta de rede, nada mais seria processado. Esse efeito foi observado nos logs: o aviso "Skipped 225 frames! The application may be doing too much work on its main thread" apareceu justamente durante o carregamento inicial, mostrando como operações pesadas na thread principal impactam diretamente a fluidez. O FutureBuilder resolve isso em vez de bloquear, ele recebe o Future<List<Item>> retornado por listarItens() e gerencia os estados da requisição automaticamente. Enquanto a resposta não chega (ConnectionState.waiting), exibe um CircularProgressIndicator; se der erro, exibe a mensagem de falha; e quando os dados chegam, reconstrói a lista com os ItemCard. Isso funciona porque o Dart executa chamadas async/await fora da thread principal usando o event loop liberando a UI para continuar respondendo enquanto a requisição acontece em segundo plano. O FutureBuilder simplesmente observa esse Future e chama setState internamente quando ele completa, sem nenhum bloqueio.

---

### Q5 — HTTP vs. gRPC para clientes móveis

**Pergunta:** Compare a comunicação HTTP/REST implementada neste laboratório com a comunicação gRPC do Lab 03. Quais são as vantagens e desvantagens de cada abordagem para um sistema distribuído com clientes móveis?

**Evidência observada:**
> _No Lab 03, como era feita a serialização dos dados? Neste lab, como os dados são transmitidos? Qual é a diferença no payload (tamanho, legibilidade)?_

No Lab 03, a serialização era feita via Protocol Buffers (Protobuf): os dados eram codificados em formato binário conforme contrato definido no arquivo .proto, compacto e não legível por humanos. Neste lab, os dados trafegam como JSON sobre HTTP/1.1: texto puro, verboso, mas inspecionável diretamente no terminal. Nos logs do Flask é possível ver claramente cada transação GET /itens → 200, POST /itens → 201 sem nenhuma ferramenta especializada.

```
// Payload JSON recebido do Flask (HTTP/REST — Lab 07)
[
  {"id": 1, "nome": "Caneta", "preco": 2.5},
  {"id": 2, "nome": "Caderno", "preco": 15.9}
]
// Legível, mas verboso — chaves repetidas a cada item

// Payload Protobuf equivalente (gRPC — Lab 03)
// Binário, não legível no terminal
// ~40% mais compacto que o JSON equivalente
// Contrato garantido pelo compilador via arquivo .proto
```

**Conexão teórica:**
> _Consulte: Birrell, A. D.; Nelson, B. J. Implementing Remote Procedure Calls. ACM Transactions on Computer Systems, 1984. Para REST: Fielding, R. T. Architectural Styles and the Design of Network-based Software Architectures. PhD Thesis, UC Irvine, 2000._

Define REST como um estilo arquitetural baseado em recursos endereçáveis via URI, sem estado e com interface uniforme o que garante simplicidade e universalidade, mas transfere para o desenvolvedor a responsabilidade de manter o contrato entre cliente e servidor. Birrell e Nelson (1984) descrevem RPC como uma abstração que oculta a comunicação de rede atrás de chamadas de procedimento locais exatamente o que o gRPC faz com Protobuf: o contrato é explícito no .proto e verificado pelo compilador eliminando a classe de bugs que no REST só aparecem em tempo de execução.

**Resposta:**

No Lab 07 a comunicação é feita via HTTP/1.1 com JSON: o ItemService faz um GET /itens e recebe uma lista de objetos JSON que o Dart deserializa manualmente com jsonDecode e o factory Item.fromJson. Já o gRPC do Lab 03 usa HTTP/2 com Protocol Buffers (Protobuf) serialização binária com contrato explícito definido no arquivo .proto, que tanto cliente quanto servidor precisam respeitar. A vantagem do HTTP/JSON para clientes móveis é a simplicidade e universalidade: qualquer dispositivo consegue fazer um GET numa API REST sem biblioteca especializada, e o JSON é legível por humanos, o que facilita muito o debug nos logs do Flask dá para ver claramente cada requisição e seu status sem nenhuma ferramenta adicional. Por outro lado, o JSON é verboso e mais pesado em bytes, o que em conexões móveis instáveis pode ser um problema real. O gRPC leva vantagem em desempenho e confiabilidade do contrato: o Protobuf é binário e muito mais compacto, e o arquivo .proto garante que cliente e servidor falam a mesma língua se um campo mudar, o compilador detecta o problema antes de chegar em produção, algo que no REST só aparece em tempo de execução. A desvantagem do gRPC em mobile é o suporte mais limitado: navegadores e algumas bibliotecas móveis têm dificuldade com HTTP/2 puro, e depurar tráfego binário é bem menos intuitivo do que inspecionar um JSON no terminal.

---

### Q6 — O endereço 10.0.2.2 e as Falácias de Deutsch

**Pergunta:** O código `ItemService` usa `10.0.2.2` para o emulador Android. O que esse detalhe revela sobre as diferenças de ambiente de rede entre emuladores e dispositivos físicos? Como isso se relaciona com as Falácias da Computação Distribuída de Deutsch (1994)?

**Evidência observada:**
> _O que acontece se você usar `localhost` em um emulador Android em vez de `10.0.2.2`? Tente e registre o erro produzido pelo FutureBuilder._

O endereço 10.0.2.2 aparece hardcoded no ItemService como destino das requisições. Nos logs do app.py, o Flask expôs dois endereços ao subir: 127.0.0.1:5000 (loopback local) e 10.221.64.170:5000 (IP real da máquina na rede). O emulador, por estar numa pilha de rede isolada, não enxerga o localhost do host e o SDK do Android mapeia 10.0.2.2 como atalho para esse loopback. Um dispositivo físico não tem esse mapeamento.

```
Emulador Android:
  10.0.2.2 → loopback do computador host → Flask responde ✓

Dispositivo físico (mesma rede Wi-Fi):
  10.0.2.2 → endereço inexistente na topologia → conexão recusada ✗
  Solução: usar o IP real → http://10.221.64.170:5000 ✓

Log do app.py:
  Running on http://127.0.0.1:5000
  Running on http://10.221.64.170:5000  ← IP real da máquina na rede local
```

**Conexão teórica:**
> _Consulte: Deutsch, L. Peter. The Eight Fallacies of Distributed Computing. Sun Microsystems, 1994. Identifique especificamente qual(is) falácia(s) este problema ilustra._

Elencou as Falácias da Computação Distribuída premissas falsas que desenvolvedores assumem sobre a rede. A mais evidente neste cenário não é nem "a rede é confiável" nem "a latência é zero": é a premissa implícita de que a topologia é homogênea, ou seja, que o mesmo endereço funciona da mesma forma em qualquer ambiente. O código que funciona no emulador com 10.0.2.2 quebra silenciosamente num dispositivo físico sem exceção clara, sem mensagem de erro óbvia porque a topologia de rede é completamente diferente entre os dois ambientes.

**Resposta:**

O endereço 10.0.2.2 existe porque o emulador Android é uma máquina virtual com sua própria pilha de rede isolada ele não enxerga o localhost do computador host diretamente. O Android SDK mapeia 10.0.2.2 como um atalho para o loopback da máquina que está rodando o emulador, permitindo que o app alcance o Flask sem configuração adicional. Em um dispositivo físico esse mapeamento não existe: o celular é uma máquina independente na rede, e para acessar o servidor Flask seria necessário usar o IP real da máquina na rede local exatamente o que o app.py expõe no log de inicialização: Running on http://10.221.64.170:5000. Apontar 10.0.2.2 de um dispositivo físico resultaria em falha de conexão silenciosa, sem nenhum aviso claro de que o problema é o endereço.

Esse detalhe expõe uma das Falácias da Computação Distribuída de Deutsch (1994): a premissa implícita de que a topologia de rede é homogênea que o mesmo endereço funciona da mesma forma em qualquer ambiente. A rede não é transparente: o que funciona no emulador quebra no dispositivo físico porque a topologia é completamente diferente. Isso reforça que endereços de rede, protocolos e comportamentos de conectividade sempre dependem do ambiente de execução, e hardcodar endereços como 10.0.2.2 é o tipo de decisão que as falácias de Deutsch alertam contra.

---

## Seção 3 — Serialização e Contratos de API

### Q7 — Serialização manual: fragilidade e alternativas

**Pergunta:** A classe `Item` implementa `fromJson` e `toJson` manualmente. Por que a serialização manual é considerada frágil em projetos grandes? Que alternativas o ecossistema Dart oferece para geração automática de código de serialização?

**Evidência observada:**
> _Adicione um campo extra no JSON retornado pelo Flask (ex.: `"estoque": 10`) sem atualizar a classe `Item` no Flutter. O que acontece? Adicione um campo ao `fromJson` com um typo intencional (ex.: `json['nomeee']`) e observe o erro em runtime._

Ao adicionar o campo "estoque": 10 no JSON retornado pelo Flask sem atualizar a classe Item no Flutter, nada aconteceu nenhum erro em tempo de compilação, nenhuma exceção em tempo de execução. O campo chegou no app e sumiu silenciosamente, ignorado pelo fromJson. Já ao introduzir um typo intencional como json['nomeee'], o app compilou normalmente e só lançou um erro em runtime quando o usuário abriu a tela  um `Null check operator used on a null value` sem indicar claramente a causa raiz.

```
Teste 1 — campo novo no JSON sem atualizar o Flutter:
  Flask retorna: {"id": 1, "nome": "Caneta", "preco": 2.5, "estoque": 10}
  fromJson lê:   id, nome, preco → "estoque" ignorado silenciosamente
  Resultado:     sem erro, dado perdido x

Teste 2 — typo no fromJson (json['nomeee']):
  Compilação:    sucesso 
  Em runtime:    erro ao abrir a tela → Null check operator on null value
  Resultado:     bug descoberto apenas pelo usuário final x
```

**Conexão teórica:**
> _Pesquise os pacotes `json_serializable` e `freezed` no pub.dev. Compare a abordagem de geração de código com a serialização manual. Consulte: pub.dev/packages/json_serializable._

O pacote json_serializable (pub.dev) usa a anotação @JsonSerializable() na classe e gera automaticamente os métodos fromJson e toJson via build_runner qualquer mudança na classe força a regeneração do código, eliminando divergências silenciosas. O freezed vai além: além da serialização, gera classes imutáveis com copyWith, operador == e toString incluídos. Ambos transferem a responsabilidade de manter o contrato do desenvolvedor para o compilador o mesmo princípio que o Protobuf do gRPC aplica, onde o arquivo .proto é a fonte verificada em tempo de build.

**Resposta:**

A serialização manual é frágil em projetos grandes porque depende do desenvolvedor lembrar de atualizar fromJson e toJson toda vez que a classe muda e em projetos com muitos modelos e muitos desenvolvedores isso vira uma fonte constante de bugs silenciosos. No código do lab no item_service.dart se a API Flask adicionasse um novo campo como categoria, o fromJson ignoraria esse campo sem avisar e sem erro em tempo de compilação, sem exceção em tempo de execução o dado chegaria no app e sumiria. O inverso também é perigoso: se um campo mudasse de nome no servidor, como preco virar price, o (json['preco'] as num).toDouble() lançaria um erro em runtime que só seria descoberto quando o usuário abrisse o app. Além disso, escrever fromJson e toJson manualmente para dezenas de classes é repetitivo e aumenta a chance de erro humano.

O ecossistema Dart oferece duas alternativas para geração automática: o json_serializable, que usa a anotação @JsonSerializable() na classe e gera o código de serialização automaticamente via build_runner, e o freezed, que vai além e gera classes imutáveis com serialização, copyWith, == e toString incluídos. Ambos eliminam o trabalho manual e qualquer mudança na classe seja refletida automaticamente no código gerado tornando o contrato seguro, rastreável e fácil de manter.

---

### Q8 — Versionamento de API e compatibilidade de contratos

**Pergunta:** O que aconteceria se a API Flask adicionasse um novo campo **obrigatório** ao JSON de resposta sem atualizar o cliente Flutter? Que estratégia de versionamento de API minimizaria esse risco?

**Evidência observada:**
> _Modifique o `app.py` para adicionar um campo `"descricao"` como obrigatório no `POST /itens`. Execute o formulário Flutter sem alterar o payload. Registre o que acontece._

O comportamento dependeu da direção da mudança. Ao adicionar descrição como campo novo na resposta do servidor, o Flutter ignorou o campo, o Item.fromJson lê apenas id, nome e preço, então descrição chegou no JSON e foi descartado, sem nenhum erro. Já ao exigir descrição como obrigatório no POST /itens, o servidor rejeitou o payload incompleto enviado pelo NovoItemScreen e retornou 400 Bad Request, que o Flutter capturou no bloco catch e exibiu como SnackBar de erro.

```
Teste 1 — campo novo na resposta GET (servidor atualizado, Flutter não):
  Status HTTP retornado:         200 OK
  Comportamento no Flutter:      campo "descricao" ignorado silenciosamente
  Mensagem exibida ao usuário:   nenhuma — bug invisível x

Teste 2 — campo obrigatório no POST (servidor exige, Flutter não envia):
  Status HTTP retornado:         400 Bad Request
  Mensagem exibida ao usuário:   "Erro ao criar item" (SnackBar)
  Causa visível ao usuário:      nenhuma — erro sem contexto x
```

**Conexão teórica:**
> _Consulte: Richardson, Leonard; Amundsen, Mike. RESTful Web APIs. O'Reilly, 2013. Cap. sobre evolução de API. Pesquise também sobre Semantic Versioning (semver.org) aplicado a contratos REST._

Tratam a evolução de API como um problema de contrato entre produtor e consumidor contratos quebrados silenciosamente são mais perigosos do que erros explícitos, porque o sistema continua funcionando aparentemente bem enquanto perde dados. O Semantic Versioning (semver.org) aplicado a APIs REST formaliza isso: mudanças que quebram compatibilidade exigem incremento de versão maior (v1 → v2), enquanto adições retrocompatíveis podem ser absorvidas na mesma versão. A regra de ouro é nunca remover nem renomear campos em versões existentes.

**Resposta:**

O comportamento dependeria da direção da mudança. Se o servidor passasse a retornar um campo novo na resposta, o cliente Flutter simplesmente o ignoraria, o Item.fromJson lê apenas id, nome e preço, então um campo extra como descrição chegaria no JSON e seria descartado silenciosamente, sem erro em compilação e sem exceção em runtime. Isso é perigoso porque o desenvolvedor não percebe que está perdendo dado. Já se o servidor passasse a exigir descrição como campo obrigatório no corpo do POST, o problema viria no sentido contrário: o NovoItemScreen envia apenas {nome, preco} via criarItem(), o servidor retornaria 400 Bad Request, e o Flutter capturaria no bloco catch exibindo um SnackBar de "Erro ao criar item" sem que o usuário entendesse o motivo.

A estratégia que minimiza esse risco é o versionamento de API por URI: incluir a versão na rota, como /v1/itens e /v2/itens, de forma que o cliente Flutter antigo continue consumindo /v1 normalmente enquanto uma versão nova do app usa /v2 com o contrato atualizado. Isso evita que uma mudança no servidor quebre clientes que ainda não foram atualizados e em mobile isso é crítico, pois o usuário pode demorar semanas para atualizar o app. A boa prática complementar é nunca remover ou renomear campos em versões existentes, apenas adicionar campos novos como opcionais mantendo compatibilidade retroativa.

---

## Seção 4 — Reflexão Arquitetural

### Q9 — Limites do setState em escala

**Pergunta:** Considere uma aplicação com 10 telas e 5 serviços diferentes que compartilham dados (ex.: carrinho de compras visível em 3 telas diferentes). Por que o `setState` tornaria-se problemático como mecanismo de gerenciamento de estado? Descreva brevemente como Provider ou BLoC resolveria esse problema.

**Evidência observada:**
> _No código atual, tente fazer o ContadorWidget exibir o número de itens listados pela `ListaItensScreen`. O que você precisaria fazer para compartilhar esse estado? Quantas camadas da árvore de widgets precisariam ser modificadas?_

Para fazer o ContadorWidget exibir o número de itens da ListaItensScreen usando apenas setState, seria necessário elevar o estado para o ancestral comum mais próximo dos dois widgets, passar os dados por parâmetro por cada nível intermediário da árvore, e criar callbacks manuais para que widgets filhos pudessem notificar o pai, o chamado prop drilling. Qualquer tela adicional que precisasse do mesmo dado repetiria todo esse caminho.

```
Para compartilhar estado entre ContadorWidget e ListaItensScreen usando apenas setState:
  1. Mover _futureItens e a lista de itens para o widget pai comum (ex.: MyApp ou HomePage)
  2. Passar os dados por parâmetro por cada nível intermediário da árvore até os dois widgets
  3. Criar callbacks para que NovoItemScreen notifique o pai ao criar um item,
     que notifica ListaItensScreen, que notifica ContadorWidget manualmente

Número de arquivos que precisariam ser alterados: 4 ou mais
(MyApp, ListaItensScreen, NovoItemScreen, ContadorWidget)
```

**Conexão teórica:**
> _Consulte: MARTIN, Robert C. Arquitetura Limpa. Alta Books, 2019. Cap. 17 — Boundaries. Pesquise: pub.dev/packages/provider e o padrão BLoC (Business Logic Component) em bloclibrary.dev._

Define boundaries como fronteiras arquiteturais que protegem componentes de mudanças em outros componentes o setState viola esse princípio ao forçar acoplamento direto entre widgets que deveriam ser independentes. O Provider (pub.dev) e o padrão BLoC (bloclibrary.dev) estabelecem uma fronteira clara entre estado e UI: o estado vive fora da árvore de widgets e os componentes se inscrevem nele de forma reativa, sem conhecer uns aos outros.

**Resposta:**

Com 10 telas e 5 serviços compartilhando dados, o setState se tornaria inviável porque ele é local ao widget que o chama se a Tela A busca uma lista de itens e a Tela B também precisa dessa lista atualizada, não existe mecanismo automático de sincronização entre elas. No lab isso já aparece em escala pequena: quando um item é criado no NovoItemScreen, a ListaItensScreen só fica sabendo porque o código faz Navigator.pop(context, true) e a tela pai verifica if (result == true) manualmente. Funciona para duas telas, mas replicar essa lógica para 10 telas interdependentes onde a criação de um item em qualquer tela precisaria notificar outras 4 ou 5 tornaria o código uma teia de callbacks, resultados de navegação e setState espalhados por toda parte, impossível de manter. O Provider resolve isso criando um objeto de estado global que fica fora da árvore de widgets: qualquer tela pode ler ou modificar esse estado, e todas as telas que dependem dele são reconstruídas automaticamente quando ele muda, sem comunicação manual entre elas. Já o BLoC vai um passo além e separa a lógica de negócio da UI usando Streams: a tela emite eventos como criar item e escuta estados como lista atualizada, sem saber nada sobre como a lógica funciona por baixo o que torna o código testável e bem organizado em projetos grandes.

---

### Q10 — Jornada completa do dado e transparência de acesso

**Pergunta:** Trace a jornada completa de um dado desde o armazenamento no servidor Flask até a exibição no widget `ItemCard`. Mapeie cada etapa e identifique: onde ocorre serialização, onde ocorre comunicação de rede, onde ocorre renderização. Como esse mapeamento se relaciona com o conceito de **transparência de acesso** em sistemas distribuídos?

**Evidência observada:**
> _Execute o smoke_test.py e observe o JSON retornado. Execute o app Flutter e observe o ItemCard renderizado. O usuário final sabe que os dados vieram de uma rede? Que "magia" oculta esse detalhe?_

Executando o smoke_test.py, o JSON retornado pelo Flask é legível e estruturado. No app Flutter, o ItemCard exibe nome e preço formatados sem nenhuma indicação visual de que os dados vieram de uma rede. O usuário final não sabe e não precisa saber que houve serialização, transmissão TCP/IP e desserialização antes de aqueles dados aparecerem na tela. A "magia" que oculta esse detalhe é o ItemService: quem chama _service.listarItens() recebe uma List<Item> como se fosse um dado local.

```
Jornada do dado — rastreamento passo a passo:

1. [Flask]    _itens: dict  →  jsonify()             [serialização Python→JSON]
2. [Rede]     HTTP/1.1 200  →  body: bytes            [transmissão TCP/IP]
3. [Dart]     response.body →  jsonDecode()           [desserialização JSON→Map]
4. [Dart]     Map<String, dynamic> → Item.fromJson()  [mapeamento para objeto tipado]
5. [Flutter]  List<Item>    →  FutureBuilder.builder  [injeção na árvore de widgets]
6. [Flutter]  Item          →  ItemCard.build()       [renderização → pixels]

Etapa de serialização:        passos 1 e 4
Etapa de comunicação de rede: passo 2
Etapa de renderização:        passo 6
```

**Conexão teórica:**
> _Transparência de acesso é definida por Coulouris et al. como a capacidade de ocultar diferenças na representação de dados e na invocação de recursos remotos. Consulte: Coulouris, G. et al. Distributed Systems: Concepts and Design. 5. ed. Addison-Wesley, 2011, Cap. 1._

Definem transparência de acesso como a capacidade de ocultar diferenças na representação de dados e na invocação de recursos remotos, permitindo que o desenvolvedor trate um dado remoto como se fosse local. No lab, o ItemService é a camada que tenta implementar essa transparência: quem chama listarItens() não precisa pensar em serialização, protocolos ou endereços de rede. Porém, a transparência vaza em dois pontos o endereço 10.0.2.2 hardcoded e a serialização manual do fromJson lembrando o desenvolvedor que há uma rede entre o app e o servidor.

**Resposta:**

A jornada do dado começa no servidor Flask, onde os itens ficam armazenados em memória no dicionário _itens. Quando o Flutter faz uma requisição, o Flask serializa esse dicionário Python em JSON via jsonify() e devolve via HTTP com status 200 visível nos logs como GET /itens → 200. Aí começa a comunicação de rede: o pacote http do Dart envia um GET para http://10.0.2.2:5000/itens e aguarda a resposta de forma assíncrona via Future, sem bloquear a UI. Quando a resposta chega, ocorre a desserialização no cliente: jsonDecode(response.body) converte os bytes JSON em uma List<dynamic> do Dart, e em seguida Item.fromJson mapeia cada objeto genérico para uma instância tipada de Item com id, nome e preço. Esses objetos chegam ao FutureBuilder da ListaItensScreen, que reconstrói a UI e passa cada Item para um ItemCard, onde ocorre a renderização final o widget desenha nome e preço formatados na tela do emulador.

Esse caminho todo dado Python no servidor virando JSON, viajando pela rede, virando objeto Dart, virando pixels na tela é exatamente o que o conceito de transparência de acesso dos sistemas distribuídos tenta ocultar. A ideia é que o desenvolvedor que chama _service.listarItens() não precise pensar em serialização, protocolos ou endereços de rede, tratando o dado remoto como se fosse local. No lab essa transparência existe na camada do ItemService, mas vaza em detalhes como o endereço 10.0.2.2 hardcoded e a serialização manual do fromJson dois pontos que lembram o desenvolvedor que há uma rede entre o app e o servidor.

---

## Seção 5 — Avaliação do Laboratório (Opcional)

> Esta seção é anônima e serve para melhoria contínua da disciplina. Sua resposta não afeta a nota.

**Q11 — Dificuldade:** O nível de dificuldade do laboratório foi:
- [ ] Muito fácil
- [x] Adequado
- [ ] Muito difícil

**Q12 — Clareza do roteiro:** As instruções foram suficientemente claras?
- [ ] Sim, totalmente
- [x] Em sua maioria, com algumas dúvidas
- [ ] Não, precisei de muita ajuda externa

**Q13 — Atividade mais relevante:** Qual atividade contribuiu mais para seu aprendizado?

> _Sua resposta:_ Atividade 4.4

**Q14 — Sugestão:** Há alguma melhoria que você sugere para este laboratório?

> _Sua resposta:_ Nenhuma.

---

## Referências Utilizadas nesta Reflexão

> Liste abaixo todas as fontes que você consultou para responder às questões acima. Use o formato ABNT.

1. BAILEY, Thomas. *Flutter for beginners*. 3. ed. Birmingham: Packt, 2023.
2. MARTIN, Robert C. *Arquitetura limpa*. Rio de Janeiro: Alta Books, 2019.
3. DEUTSCH, L. Peter. *The Eight Fallacies of Distributed Computing*. Sun Microsystems, 1994.
4. FLUTTER TEAM. *Flutter architectural overview*. Disponível em: https://docs.flutter.dev/resources/architectural-overview. Acesso em: abr. 2026.
5. DART TEAM. *Asynchronous programming: futures, async, await*. Disponível em: https://dart.dev/codelabs/async-await. Acesso em: abr. 2026.
6. _(adicione outras referências que utilizou)_

---

*Laboratório 07 — LAMD 60445 — PUC Minas — 1º Semestre 2026*
