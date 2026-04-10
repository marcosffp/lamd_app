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
        Text(
          '${widget.label}: $_contagem',
          style: Theme.of(context).textTheme.headlineSmall,
        ),
        ElevatedButton(
          onPressed: _incrementar,
          child: const Text('Incrementar'),
        ),
      ],
    );
  }
}
