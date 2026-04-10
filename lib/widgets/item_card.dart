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
