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
          // Estado: dados recebidos
          final itens = snapshot.data!;
          if (itens.isEmpty) {
            return const Center(child: Text('Nenhum item cadastrado.'));
          }
          return ListView.builder(
            itemCount: itens.length,
            itemBuilder: (ctx, index) =>
                ItemCard(nome: itens[index].nome, preco: itens[index].preco),
          );
        },
      ),
    );
  }
}
