LAMD (60445) — Lab 07: Introdução ao Flutter | PUC Minas — Engenharia de Software
Pontifícia Universidade Católica de Minas Gerais
Curso de Engenharia de Software
60445 — Laboratório de Desenvolvimento de Aplicações Móveis e Distribuídas
Roteiro de Laboratório 07
Introdução ao Flutter: Fundamentos e Primeira Aplicação
Distribuída
Unidade 4 — Desenvolvimento Móvel
Disciplina 60445 — LAMD
Unidade Unidade 4 — Desenvolvimento Móvel
Professores Cleiton Silva e Cristiano Neto
Carga Horária 2 horas/aula (1 encontro)
Pré-requisitos Labs 01–06 concluídos; noções de POO; REST (Lab 05)
Prof. Cleiton Silva e Cristiano Neto - Página 1
LAMD (60445) — Lab 07: Introdução ao Flutter | PUC Minas — Engenharia de Software
1. Contextualização e Objetivos
Até este ponto do curso, construímos serviços distribuídos em Python usando XML-RPC, gRPC e
REST com Flask. Esses serviços produzem dados que precisam ser consumidos por clientes — e,
no contexto de sistemas distribuídos modernos, os clientes são frequentemente dispositivos
móveis.
Este laboratório marca o início da Unidade 4 e apresenta o Flutter como o framework para
construção de interfaces móveis que se comunicam com os backends distribuídos desenvolvidos
anteriormente.
Por que Flutter?
Flutter é o SDK open-source do Google para desenvolvimento de aplicações nativas
compiladas a partir de uma única base de código para mobile (Android e iOS), web e
desktop. Lançado em 2018, utiliza a linguagem Dart e seu próprio motor de
renderização (Skia/Impeller), o que garante desempenho próximo ao nativo e
comportamento visual consistente entre plataformas.
No contexto da disciplina, o Flutter representa a camada cliente de uma arquitetura
distribuída: ele consome APIs REST (Flask) ou gRPC — integrando ao vivo os conceitos
das Unidades 1 a 3.
1.1 Objetivos de Aprendizagem
Ao concluir este laboratório, o aluno será capaz de:
• Configurar o ambiente de desenvolvimento Flutter/Dart e executar o fluxo básico de
criação de projeto;
• Compreender a arquitetura baseada em widgets e a diferença entre StatelessWidget e
StatefulWidget;
• Implementar gerenciamento de estado local usando setState e identificar suas limitações
de escala;
• Construir uma interface que consome uma API REST previamente desenvolvida (Flask -
Lab 05);
• Relacionar o modelo de widgets reativos do Flutter ao padrão MVC/MVP discutido na
Unidade 3.
1.2 Mapa Conceitual da Sessão
Conceito Onde aparece no Flutter Referência anterior no curso
Reatividade / Estado setState / rebuild da árvore de
widgets
Publish/Subscribe (Unidade 2)
Separação de
responsabilidades
Widget de UI vs. camada de
serviço (http)
MVC — Unidade 3
Comunicação cliente–servidor http.get / http.post → API Flask REST — Lab 05
Serialização de dados jsonDecode / jsonEncode
(dart:convert)
Protocol Buffers — Lab 03
Prof. Cleiton Silva e Cristiano Neto - Página 2
LAMD (60445) — Lab 07: Introdução ao Flutter | PUC Minas — Engenharia de Software
Assincronismo Future / async-await asyncio — Labs 04 e 06
Prof. Cleiton Silva e Cristiano Neto - Página 3
LAMD (60445) — Lab 07: Introdução ao Flutter | PUC Minas — Engenharia de Software
2. Fundamentação Teórica Mínima
Esta seção apresenta os conceitos essenciais para a execução do laboratório. Não é um tutorial
exaustivo; o objetivo é fornecer âncoras conceituais para que as observações práticas façam
sentido.
2.1 A Arquitetura de Widgets
No Flutter, a interface é inteiramente descrita por uma árvore de widgets. Widgets são objetos
imutáveis que descrevem como um trecho da interface deve ser renderizado — analogamente à
forma como nós de um DOM descrevem uma página HTML. O framework Flutter mantém
internamente uma árvore de elementos (Element Tree) e uma árvore de objetos de renderização
(RenderObject Tree), atualizando-as eficientemente quando o estado muda.
StatelessWidget — descreve partes da UI que não dependem de estado mutável. São sempre
idempotentes: dado o mesmo conjunto de parâmetros de entrada (propriedades), produzem
sempre a mesma saída visual. São reconstruídos sempre que o widget pai é reconstruído.
StatefulWidget — associa-se a um objeto State que persiste entre reconstruções. Quando
setState() é chamado, o Flutter agenda uma reconstrução do subárvore afetado, atualizando a
UI de forma reativa.
💡 Dica
A distinção StatelessWidget vs. StatefulWidget é análoga à distinção entre componentes
controlados e não-controlados em React. Se você já estudou React, o mecanismo de
rebuild é conceitualmente similar ao re-render disparado por setState() naquele
framework.
2.2 Gerenciamento de Estado com setState
O setState é a forma mais simples de gerenciamento de estado no Flutter. Ele notifica o
framework que o estado interno mudou e que o widget deve ser reconstruído. Contudo, seu
escopo é limitado: o estado gerenciado por setState é local ao widget que o detém e não pode ser
compartilhado facilmente entre widgets distantes na árvore.
Para sistemas distribuídos com múltiplas telas e fontes de dados assíncronos (como chamadas de
rede), soluções mais robustas como Provider, Riverpod ou BLoC são recomendadas. Neste
laboratório, usamos setState para manter o foco nos fundamentos; os limites dessa abordagem
serão evidentes nas questões de reflexão.
2.3 Comunicação HTTP em Dart
O pacote http (publicado em pub.dev) fornece uma API de alto nível para requisições
HTTP/HTTPS. Toda comunicação de rede em Dart é intrinsecamente assíncrona: as funções
retornam objetos Future<T>, que representam valores que estarão disponíveis no futuro.
Prof. Cleiton Silva e Cristiano Neto - Página 4
LAMD (60445) — Lab 07: Introdução ao Flutter | PUC Minas — Engenharia de Software
O padrão async/await do Dart — herdado de linguagens como JavaScript e C# — permite
escrever código assíncrono com aparência síncrona, melhorando a legibilidade. O widget
FutureBuilder do Flutter integra essa assincronicidade diretamente ao ciclo de vida da UI.
Referências Bibliográficas desta Seção
BAILEY, Thomas. Flutter for Beginners. 3. ed. Birmingham: Packt, 2023. Cap. 1–3
(Ambiente e Widgets), Cap. 6 (Estado).
MARTIN, Robert C. Arquitetura Limpa. Rio de Janeiro: Alta Books, 2019. Cap. 22 (Clean
Architecture — separação de camadas).
Flutter Team. Flutter architectural overview. Disponível em:
https://docs.flutter.dev/resources/architectural-overview. Acesso em: abr. 2026.
Prof. Cleiton Silva e Cristiano Neto - Página 5
LAMD (60445) — Lab 07: Introdução ao Flutter | PUC Minas — Engenharia de Software
3. Preparação do Ambiente
3.1 Instalação do Flutter SDK
⚠ Atenção
Se o laboratório for realizado nos computadores do campus, verifique se o Flutter já está
instalado antes de executar os passos abaixo. Execute: flutter --version
1. Acesse https://flutter.dev/docs/get-started/install e baixe o SDK para seu sistema
operacional.
2. Extraia o arquivo em um diretório sem espaços no caminho (ex.: C:\src\flutter no Windows
ou ~/flutter no Linux/macOS).
3. Adicione o diretório bin do Flutter ao PATH do sistema.
4. Execute o diagnóstico do ambiente:
flutter doctor
5. Corrija os itens marcados com [!] antes de prosseguir. Para este laboratório, o mínimo
necessário é:
◦ Flutter SDK instalado
◦ Android SDK instalado (ou Xcode no macOS para iOS)
◦ Um emulador Android configurado ou dispositivo físico com depuração USB ativada
3.2 Configuração da IDE
Recomenda-se o VS Code com a extensão Flutter (ID: dart-code.flutter) ou o Android Studio com
o plugin Flutter. Ambos oferecem hot reload, inspeção da árvore de widgets e depurador
integrado.
6. Instale a extensão Flutter no VS Code:
code --install-extension dart-code.flutter
7. Verifique que a extensão Dart foi instalada automaticamente como dependência.
8. Abra a Paleta de Comandos (Ctrl+Shift+P) e execute: Flutter: Run Flutter Doctor.
3.3 Backend de Apoio (API Flask — Lab 05)
Este laboratório reutiliza a API REST desenvolvida no Lab 05 como backend. O serviço Flask
deve estar em execução durante os exercícios práticos.
⚠ Atenção
Verifique se você possui o código do Lab 05. Se não, solicite ao professor o arquivo de
referência antes do início dos exercícios práticos.
A API deve estar acessível em http://localhost:5000. Confirme com: curl
http://localhost:5000/itens
Prof. Cleiton Silva e Cristiano Neto - Página 6
LAMD (60445) — Lab 07: Introdução ao Flutter | PUC Minas — Engenharia de Software
Caso o Lab 05 não esteja disponível, o professor disponibilizará uma API de substituição com
contrato equivalente.
Prof. Cleiton Silva e Cristiano Neto - Página 7
LAMD (60445) — Lab 07: Introdução ao Flutter | PUC Minas — Engenharia de Software
4. Atividades Práticas
Atividade 4.1 — Criação do Projeto e Exploração da Estrutura
Nesta atividade, você criará seu primeiro projeto Flutter e explorará a estrutura de arquivos gerada
automaticamente pelo framework.
Passo 1 — Criar o projeto
flutter create lamd_app
cd lamd_app
flutter run
O comando flutter run compilará o projeto e o executará no emulador ou dispositivo conectado.
Observe o tempo de compilação — as execuções subsequentes serão mais rápidas graças ao
cache incremental.
Passo 2 — Estrutura de diretórios
Explore o diretório gerado e identifique:
Diretório/Arquivo Finalidade
lib/main.dart Ponto de entrada da aplicação; contém a função main() e o
widget raiz.
lib/ Todo o código Dart da aplicação. Organize aqui seus widgets,
serviços e modelos.
pubspec.yaml Manifesto do projeto: dependências, assets e metadados
(análogo ao package.json do npm).
android/ e ios/ Projetos nativos gerados automaticamente. Raramente editados
diretamente.
test/ Testes unitários e de widget (não abordados neste laboratório).
Passo 3 — Hot Reload
Com o aplicativo em execução, abra lib/main.dart e altere o texto 'You have pushed the button this
many times:' para 'Cliques registrados:'. Salve o arquivo (Ctrl+S). Observe que a interface é
atualizada em menos de 1 segundo sem reiniciar o aplicativo.
💡 Dica
Hot Reload (r no terminal) injeta o código modificado na VM Dart sem reiniciar o estado.
Hot Restart (R) reinicia completamente, perdendo o estado. Use hot reload durante o
desenvolvimento iterativo para maior produtividade.
Atividade 4.2 — StatelessWidget vs. StatefulWidget
Nesta atividade você criará dois widgets personalizados — um stateless e um stateful — para
compreender na prática a diferença entre eles.
Prof. Cleiton Silva e Cristiano Neto - Página 8
LAMD (60445) — Lab 07: Introdução ao Flutter | PUC Minas — Engenharia de Software
Passo 1 — Widget de exibição (Stateless)
Crie o arquivo lib/widgets/item_card.dart com o conteúdo abaixo:
import 'package:flutter/material.dart';
class ItemCard extends StatelessWidget {
 final String nome;
 final double preco;
 // Construtor com parâmetros nomeados obrigatórios
 const ItemCard({super.key, required this.nome, required this.preco});
 @override
 Widget build(BuildContext context) {
 return Card(
 margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
 child: ListTile(
 leading: const Icon(Icons.shopping_bag_outlined),
 title: Text(nome),
 trailing: Text(
 'R\$ ${preco.toStringAsFixed(2)}',
 style: const TextStyle(fontWeight: FontWeight.bold),
 ),
 ),
 );
 }
}
Passo 2 — Widget com contador (Stateful)
Crie o arquivo lib/widgets/contador_widget.dart:
import 'package:flutter/material.dart';
class ContadorWidget extends StatefulWidget {
 final String label;
 const ContadorWidget({super.key, required this.label});
 @override
 State<ContadorWidget> createState() => _ContadorWidgetState();
}
class _ContadorWidgetState extends State<ContadorWidget> {
 int _contagem = 0;
 void _incrementar() {
 setState(() {
 _contagem++;
 });
 }
 @override
 Widget build(BuildContext context) {
 return Column(
 mainAxisSize: MainAxisSize.min,
 children: [
 Text('${widget.label}: $_contagem',
 style: Theme.of(context).textTheme.headlineSmall),
 ElevatedButton(
 onPressed: _incrementar,
 child: const Text('Incrementar'),
 ),
 ],
Prof. Cleiton Silva e Cristiano Neto - Página 9
LAMD (60445) — Lab 07: Introdução ao Flutter | PUC Minas — Engenharia de Software
 );
 }
}
Passo 3 — Integração na tela principal
Substitua o conteúdo de lib/main.dart pelo código a seguir, que usa ambos os widgets:
import 'package:flutter/material.dart';
import 'widgets/item_card.dart';
import 'widgets/contador_widget.dart';
void main() => runApp(const LamdApp());
class LamdApp extends StatelessWidget {
 const LamdApp({super.key});
 @override
 Widget build(BuildContext context) {
 return MaterialApp(
 title: 'LAMD - Lab 07',
 theme: ThemeData(colorSchemeSeed: Colors.blue, useMaterial3: true),
 home: const TelaPrincipal(),
 );
 }
}
class TelaPrincipal extends StatelessWidget {
 const TelaPrincipal({super.key});
 @override
 Widget build(BuildContext context) {
 return Scaffold(
 appBar: AppBar(title: const Text('LAMD App')),
 body: Column(
 children: [
 const ContadorWidget(label: 'Requisicoes'),
 const Divider(),
 ItemCard(nome: 'Notebook', preco: 3499.90),
 ItemCard(nome: 'Mouse sem fio', preco: 89.90),
 ],
 ),
 );
 }
}
Execute o aplicativo e interaja com o botão de incremento. Observe que o valor do contador é
atualizado apenas dentro do ContadorWidget, sem afetar os ItemCard ao redor.
Atividade 4.3 — Consumo da API REST (Integração Distribuída)
Esta é a atividade central do laboratório: integrar o cliente Flutter ao serviço Flask desenvolvido no
Lab 05. Aqui o sistema distribuído torna-se completo — backend Python servindo dados via HTTP
e frontend Dart consumindo-os de forma assíncrona.
Passo 1 — Adicionar dependência http
Abra pubspec.yaml e adicione a dependência na seção dependencies:
Prof. Cleiton Silva e Cristiano Neto - Página 10
LAMD (60445) — Lab 07: Introdução ao Flutter | PUC Minas — Engenharia de Software
dependencies:
 flutter:
 sdk: flutter
 http: ^1.2.0
Em seguida, execute no terminal:
flutter pub get
Passo 2 — Camada de serviço
Crie o arquivo lib/services/item_service.dart. Esta classe encapsula toda a lógica de comunicação
HTTP, separando-a da camada de UI — aplicando o princípio de separação de responsabilidades
do Clean Architecture (MARTIN, 2019).
import 'dart:convert';
import 'package:http/http.dart' as http;
class Item {
 final int id;
 final String nome;
 final double preco;
 Item({required this.id, required this.nome, required this.preco});
 // Factory constructor: converte JSON -> objeto Dart
 factory Item.fromJson(Map<String, dynamic> json) {
 return Item(
 id: json['id'] as int,
 nome: json['nome'] as String,
 preco: (json['preco'] as num).toDouble(),
 );
 }
 // Serializa objeto Dart -> JSON (para POST/PUT)
 Map<String, dynamic> toJson() => {'nome': nome, 'preco': preco};
}
class ItemService {
 // Em dispositivo real: substitua pelo IP da máquina host na rede local
 static const String _baseUrl = 'http://10.0.2.2:5000';
 Future<List<Item>> listarItens() async {
 final response = await http.get(Uri.parse('$_baseUrl/itens'));
 if (response.statusCode == 200) {
 final List<dynamic> jsonList = jsonDecode(response.body);
 return jsonList.map((json) => Item.fromJson(json)).toList();
 } else {
 throw Exception('Falha ao carregar itens: ${response.statusCode}');
 }
 }
 Future<Item> criarItem(String nome, double preco) async {
 final response = await http.post(
 Uri.parse('$_baseUrl/itens'),
 headers: {'Content-Type': 'application/json'},
 body: jsonEncode({'nome': nome, 'preco': preco}),
 );
 if (response.statusCode == 201) {
 return Item.fromJson(jsonDecode(response.body));
 } else {
 throw Exception('Falha ao criar item: ${response.statusCode}');
Prof. Cleiton Silva e Cristiano Neto - Página 11
LAMD (60445) — Lab 07: Introdução ao Flutter | PUC Minas — Engenharia de Software
 }
 }
}
⚠ Atenção
No emulador Android, o endereço 10.0.2.2 representa a máquina host (localhost do
computador). Em dispositivo físico na mesma rede Wi-Fi, use o IP real da máquina (ex.:
192.168.1.X). Nunca use localhost em dispositivos físicos — eles não têm rota para o
loopback do seu computador.
Passo 3 — Tela de listagem com FutureBuilder
Crie lib/screens/lista_itens_screen.dart:
import 'package:flutter/material.dart';
import '../services/item_service.dart';
import '../widgets/item_card.dart';
class ListaItensScreen extends StatefulWidget {
 const ListaItensScreen({super.key});
 @override
 State<ListaItensScreen> createState() => _ListaItensScreenState();
}
class _ListaItensScreenState extends State<ListaItensScreen> {
 final ItemService _service = ItemService();
 late Future<List<Item>> _futureItens;
 @override
 void initState() {
 super.initState();
 _futureItens = _service.listarItens(); // dispara a requisicao ao montar
 }
 void _recarregar() {
 setState(() {
 _futureItens = _service.listarItens(); // nova requisicao
 });
 }
 @override
 Widget build(BuildContext context) {
 return Scaffold(
 appBar: AppBar(
 title: const Text('Itens do Servidor'),
 actions: [
 IconButton(icon: const Icon(Icons.refresh), onPressed: _recarregar),
 ],
 ),
 body: FutureBuilder<List<Item>>(
 future: _futureItens,
 builder: (context, snapshot) {
 // Estado: aguardando resposta
 if (snapshot.connectionState == ConnectionState.waiting) {
 return const Center(child: CircularProgressIndicator());
 }
 // Estado: erro na requisicao
 if (snapshot.hasError) {
 return Center(child: Text('Erro: ${snapshot.error}'));
 }
Prof. Cleiton Silva e Cristiano Neto - Página 12
LAMD (60445) — Lab 07: Introdução ao Flutter | PUC Minas — Engenharia de Software
 // Estado: dados recebidos
 final itens = snapshot.data!;
 if (itens.isEmpty) {
 return const Center(child: Text('Nenhum item cadastrado.'));
 }
 return ListView.builder(
 itemCount: itens.length,
 itemBuilder: (ctx, index) => ItemCard(
 nome: itens[index].nome,
 preco: itens[index].preco,
 ),
 );
 },
 ),
 );
 }
}
Passo 4 — Atualizar main.dart para navegar para a nova tela
Altere a propriedade home do MaterialApp em lib/main.dart:
home: const ListaItensScreen(),
Execute o aplicativo com o servidor Flask em funcionamento e observe os itens sendo carregados
da API.
Atividade 4.4 — Formulário para Criar Novos Itens (Desafio)
Implemente uma tela de formulário que permita criar um novo item via POST na API. Esta
atividade é avaliada como parte da entrega do sprint.
Requisitos Mínimos
1. Campo de texto para o nome do item (TextFormField com validação: não pode ser
vazio).
2. Campo numérico para o preço (TextFormField com validação: valor maior que zero).
3. Botão 'Salvar' que dispara POST via ItemService.criarItem().
4. Feedback visual ao usuário: CircularProgressIndicator durante o envio e SnackBar de
sucesso/erro após a resposta.
5. Após criação bem-sucedida, retornar à tela de listagem e exibir os dados atualizados
(Navigator.pop + setState na tela pai).
💡 Dica
Use Navigator.push e Navigator.pop para navegar entre telas. Ao fazer pop com
Navigator.pop(context, true), a tela anterior pode detectar o retorno e chamar
_recarregar() condicionalmente.
Consulte: https://docs.flutter.dev/cookbook/navigation/returning-data
Prof. Cleiton Silva e Cristiano Neto - Página 13
LAMD (60445) — Lab 07: Introdução ao Flutter | PUC Minas — Engenharia de Software
5. Reflexão e Análise Crítica
Responda às questões abaixo no arquivo reflexao.md incluído no repositório de entrega. Cada
resposta deve citar evidências observadas durante a execução (mensagens do terminal,
comportamento da interface, tempo de resposta) e conectá-las a conceitos teóricos com
referência bibliográfica.
5.1 Arquitetura de Widgets
Q1: Explique com suas palavras a diferença entre StatelessWidget e StatefulWidget,
usando como exemplo os widgets criados nas Atividades 4.1 e 4.2. Em qual situação o
uso de setState se torna uma limitação arquitetural?
Q2: A árvore de widgets do Flutter é reconstruída a cada chamada de setState. Por que
isso não causa problema de desempenho na maioria dos casos? Que mecanismo
interno do Flutter evita reconstruções desnecessárias?
Q3: Compare o modelo de widgets do Flutter com o padrão MVC discutido na Unidade
3. O que corresponderia ao Model, View e Controller no código que você desenvolveu?
5.2 Comunicação Distribuída
Q4: O método listarItens() retorna um Future<List<Item>>. O que aconteceria com a
interface se a chamada HTTP bloqueasse a thread principal? Como o FutureBuilder
resolve esse problema?
Q5: Compare a comunicação HTTP implementada neste laboratório com a comunicação
gRPC do Lab 03. Quais são as vantagens e desvantagens de cada abordagem para um
sistema distribuído com clientes móveis?
Q6: O código ItemService usa o endereço 10.0.2.2 para o emulador. O que esse detalhe
revela sobre as diferenças de ambiente de rede entre emuladores e dispositivos físicos?
Como isso se relaciona com as Falácias da Computação Distribuída de Deutsch (1994)?
5.3 Serialização e Contratos de API
Q7: A classe Item implementa fromJson e toJson. Por que a serialização manual é
considerada frágil em projetos grandes? Que alternativas o ecossistema Dart oferece
para geração automática de código de serialização?
Prof. Cleiton Silva e Cristiano Neto - Página 14
LAMD (60445) — Lab 07: Introdução ao Flutter | PUC Minas — Engenharia de Software
Q8: O que aconteceria se a API Flask adicionasse um novo campo obrigatório ao JSON
de resposta sem atualizar o cliente Flutter? Que estratégia de versionamento de API
minimizaria esse risco?
5.4 Reflexão Arquitetural
Q9: Considere uma aplicação com 10 telas e 5 serviços diferentes que compartilham
dados. Por que o setState tornar-se-ia problemático como mecanismo de gerenciamento
de estado? Descreva brevemente como uma solução como Provider ou BLoC resolveria
esse problema.
Q10: Reflita sobre a jornada completa do dado neste laboratório: desde o
armazenamento no servidor Flask até a exibição no widget ItemCard. Mapeie cada
etapa e identifique: onde ocorre serialização, onde ocorre comunicação de rede, onde
ocorre renderização. Como esse mapeamento se relaciona com o conceito de
transparência de acesso em sistemas distribuídos?
Prof. Cleiton Silva e Cristiano Neto - Página 15
LAMD (60445) — Lab 07: Introdução ao Flutter | PUC Minas — Engenharia de Software
7. Referências
BAILEY, Thomas. Flutter for beginners: cross-platform mobile development from hello, world! to
app release with Flutter 3.10+ and Dart 3.x. 3. ed. Birmingham: Packt Publishing, 2023.
MARTIN, Robert C. Arquitetura limpa: o guia do artesão para estrutura e design de software. Rio
de Janeiro: Alta Books, 2019.
FLUTTER TEAM. Flutter architectural overview. Disponível em:
https://docs.flutter.dev/resources/architectural-overview. Acesso em: abr. 2026.
DART TEAM. A tour of the Dart language. Disponível em:
https://dart.dev/guides/language/language-tour. Acesso em: abr. 2026.
DEUTSCH, L. Peter. The eight fallacies of distributed computing. Sun Microsystems, 1994.
Disponível em:
https://web.archive.org/web/20171107014323/http://blog.fogcreek.com/eight-fallacies-of-distributed
-computing-tech-talk/. Acesso em: abr. 2026.
FLUTTER TEAM. pub.dev — pacote http. Disponível em: https://pub.dev/packages/http. Acesso
em: abr. 2026.
Prof. Cleiton Silva e Cristiano Neto - Página 16