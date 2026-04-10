import 'package:flutter/material.dart';
import 'package:lamd_app/widgets/contador_widget.dart';
import 'package:lamd_app/widgets/item_card.dart';
import 'screens/lista_itens_screen.dart';

void main() => runApp(const LamdApp());

class LamdApp extends StatelessWidget {
  const LamdApp({super.key});
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'LAMD - Lab 07',
      theme: ThemeData(colorSchemeSeed: Colors.blue, useMaterial3: true),
      home: const ListaItensScreen(),
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
