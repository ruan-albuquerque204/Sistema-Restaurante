const inputQuantidade = document.getElementById('quantidade');
const selectProdutos = document.getElementById('produtos');
const todosProdutos = {};

// const produtos = [
//   { id: 1, nome: 'Camiseta', preco: 49.90 },
//   { id: 2, nome: 'Calça Jeans', preco: 129.90 },
//   { id: 3, nome: 'Tênis', preco: 199.90 },
//   { id: 4, nome: 'Boné', preco: 39.90 }
// ];

const pedido = [];

// Preenche o dropdown com os produtos
// const selectProduto = document.getElementById('produto');
// produtos.forEach(produto => {
//   const option = document.createElement('option');
//   option.value = produto.id;
//   option.textContent = `${produto.nome} - R$ ${produto.preco.toFixed(2)}`;
//   selectProduto.appendChild(option);
// });

// document.addEventListener('DOMContentLoaded', () => {
//     fetch('api/produto')
//     .then(response => {
//         if (!response.ok) throw new Error('Não foi possível coisar');
//         return response.json()
//     })
//     .then(data => {
//         data.forEach(produto => {
//             todosProdutos[produto['id']] = produto
//         })
//     })
//     .catch(error => {
//         console.alert('Error', error)
//         alert('Falha na busca.')
//     });
// });

function adicionarItem() {
    const produtoId = parseInt(document.getElementById('produtos').value);
    const quantidade = parseFloat(document.getElementById('quantidade').value);
    const produto = todosProdutos[produtoId];

    if (!produtoId || !produto || !quantidade || quantidade <= 0) {
        alert('Selecione um produto e uma quantidade válida.');
        return;
    }

    pedido.push({ ...produto, quantidade, id: produtoId });
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

    let totalPedido = 0;

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

        tbody.appendChild(tr);
        
        totalPedido += valor * 100;
    });
    
    totalMessage.textContent = 'Total do Pedido: R$ ' + (totalPedido / 100).toFixed(2);

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
            'forma_pagamento': formaPagamento
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


Array.from(selectProdutos.options).forEach(item => {
    if (isNaN(parseInt(item.value))) return;

    const conteudo = item.textContent.split(' - R$');
    todosProdutos[item.value] = {
        'nome': conteudo[0],
        'valor': conteudo[1]
    };
})

// function formatarNumero(valor) {
//     let filtrado = valor.replace(/[^0-9.]/g, '');
    
//     const partes = filtrado.split('.');
//     if (partes.length > 2) {
//         filtrado = partes.shift() + '.' + partes.join('');
//     }
    
//     return filtrado
// }

// function validarFormatar() {
//     let val = inputQuantidade.value.trim();
    
//     val = formatarNumero(val);
    
//     if (Number(val) > 0) {
//         inputQuantidade.value = Number(val);
//     } else {
//         inputQuantidade.value = '';
//     }
// }

// // EVENTOS

// inputQuantidade.addEventListener('keydown', event => {
//     if (event.key === 'Enter') {
//         validarFormatar();
//     }
// })

// inputQuantidade.addEventListener('blur', function() {
//     validarFormatar();
// });