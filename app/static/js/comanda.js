const inputQuantidade = document.getElementById('quantidade');
const selectProdutos = document.getElementById('produtos');
const pagoInput = document.getElementById('valorPago');
const trocoInput = document.getElementById('valorTroco');

let totalPago = 0;
let totalPedido = 0;

const todosProdutos = {};

const pedido = [];

pagoInput.addEventListener('input', calcularTroco);

function calcularTroco(e) {
    valorTroco.value = ((pagoInput.value * 100 - totalPedido * 100) / 100).toFixed(2);
};

function adicionarItem() {
    const produtoId = parseInt(document.getElementById('produtos').value);
    const quantidade = parseFloat(document.getElementById('quantidade').value);
    const produto = todosProdutos[produtoId];

    if (!produtoId || !produto || !quantidade || quantidade <= 0) {
        alert('Selecione um produto e uma quantidade válida.');
        return;
    }

    pedido.push({ ...produto, quantidade, id: produtoId});
    atualizarLista();
};

function limparPedido() {
    pedido.length = 0;
    atualizarLista()
};
 
function atualizarLista() {
    const tabela = document.getElementById('tabela-pedido');
    const tbody = tabela.querySelector('tbody');
    const totalMessage = tabela.querySelector('caption');
    
    totalPedido = 0;

    tbody.innerHTML = '';

    pedido.forEach(item => {
        // const li = document.createElement('li');
        // li.className = 'item-pedido';
        // li.textContent = `${item.nome} x ${item.quantidade} = R$ ${(item.valor * item.quantidade).toFixed(2)}`;
        // lista.appendChild(li);
        const tr = document.createElement('tr');
        const valor = (((item.valor * 100) * item.quantidade) / 100).toFixed(2);
        const conteudo = [item.nome, item.quantidade, 'R$ ' + valor];

        conteudo.forEach(i => {
            const td = document.createElement('td');
            td.textContent = i;
            tr.appendChild(td);
        });
        
        const td = document.createElement('td');
        const input = document.createElement('input');
        input.className = 'btnClose';
        input.type = 'button';
        input.value = '\u2715';
        input.onclick = function () {deleteItem(this);}
        
        td.appendChild(input);
        tr.appendChild(td);

        tbody.appendChild(tr);
        
        totalPedido += valor * 100;
    });
    
    totalMessage.textContent = 'Total do Pedido: R$ ' + (totalPedido / 100).toFixed(2);
    
    totalPago = (totalPedido / 100).toFixed(2);
    totalPedido = totalPago;
    
    pagoInput.value = totalPago;
    calcularTroco();
};

function enviarProduto() {
    if (pedido.length <= 0) {
        alert('Adicione pelo menos um produto no pedido.')
        return
    } else if (document.getElementById('formaPagamento').value === '') {
        alert('Escolha uma forma de pagamento para prosseguir.')
        return
    }

    const buttons = document.querySelectorAll('button');
    const itensPedido = [];
    const formaPagamento = document.getElementById('formaPagamento').value;
    const cliente = document.getElementById('nome').value;

    pedido.forEach(v => {
        itensPedido.push({'id': v.id, 'quantidade': v.quantidade})
    });

    buttons.forEach(e => {
        e.disabled = true;
    });

    fetch('/api/pedido/registrar', {
        method: 'POST',
        headers: {
        'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'itens': itensPedido,
            'forma_pagamento': formaPagamento,
            'cliente': cliente,
            'valorPago': pagoInput.value
        })
    })
    .then(response => {
        if (!response.ok) throw new Error('Erro ao enviar pedido');
        return response.json();
    })
    .then(data => {
        document.getElementById('quantidade').value = '';
        alert(data.mensagem || 'Pedido enviado com sucesso');
        pedido.length = 0;
        atualizarLista();
    })
    .catch(error => {
        console.error('Erro:', error);
        alert('Falha ao enviar o pedido');
    })
    .finally(param => {
        console.log('Parametro final', param)
        buttons.forEach(e => {
        e.disabled = false;
    });
    });}

function deleteItem(button) {
        const row = button.closest('tr');
        
        const tabela = document.getElementById('tabela-pedido');
        
        const rows = Array.from(tabela.rows);

        const index = rows.indexOf(row);

        pedido.splice(index);

        row.innerHTML = '';
    };

    
Array.from(selectProdutos.options).forEach(item => {
    if (isNaN(parseInt(item.value))) return;

    const conteudo = item.textContent.split(' - R$');
    todosProdutos[item.value] = {
        'nome': conteudo[0],
        'valor': conteudo[1]
    };
})
