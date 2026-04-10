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
    }
  }
}
