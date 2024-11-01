from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from forms import ClienteForm, ProdutoForm, VendaForm
from models import db, Cliente, Produto, Venda

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
app.config['SECRET_KEY'] = 'minha-chave-secreta'


db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('base.html')

# Rota principal
#@app.route('/base')
#def index():
   # return render_template('base.html')

# Rotas para Clientes
@app.route('/clientes')
def lista_clientes():
    clientes = Cliente.query.all()
    return render_template('clientes.html', clientes=clientes)

@app.route('/cliente/novo', methods=['GET', 'POST'])
def novo_cliente():
    form = ClienteForm()
    if form.validate_on_submit():
        cliente = Cliente(
            nome=form.nome.data,
            idade=form.idade.data,
            cpf=form.cpf.data,
            email=form.email.data,
            endereco=form.endereco.data
        )
        db.session.add(cliente)
        db.session.commit()
        flash('Cliente cadastrado com sucesso!')
        return redirect(url_for('lista_clientes'))
    return render_template('form_cliente.html', form=form)

@app.route('/cliente/editar/<int:id>', methods=['GET', 'POST'])
def editar_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    form = ClienteForm(obj=cliente)
    if form.validate_on_submit():
        form.populate_obj(cliente)
        db.session.commit()
        flash('Cliente atualizado com sucesso!')
        return redirect(url_for('lista_clientes'))
    return render_template('form_cliente.html', form=form)

@app.route('/cliente/deletar/<int:id>')
def deletar_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    db.session.delete(cliente)
    db.session.commit()
    flash('Cliente deletado com sucesso!')
    return redirect(url_for('lista_clientes'))

# Rotas para Produtos
@app.route('/produtos')
def lista_produtos():
    produtos = Produto.query.all()
    return render_template('produtos.html', produtos=produtos)

@app.route('/produto/novo', methods=['GET', 'POST'])
def novo_produto():
    form = ProdutoForm()
    if form.validate_on_submit():
        produto = Produto(
            nome=form.nome.data,
            preco=form.preco.data,
            descricao=form.descricao.data,
            quantidade_estoque=form.quantidade_estoque.data,
            imagem=form.imagem.data.filename
        )
        db.session.add(produto)
        db.session.commit()
        flash('Produto cadastrado com sucesso!')
        return redirect(url_for('lista_produtos'))
    return render_template('form_produto.html', form=form)

@app.route('/produto/editar/<int:id>', methods=['GET', 'POST'])
def editar_produto(id):
    produto = Produto.query.get_or_404(id)
    form = ProdutoForm(obj=produto)
    if form.validate_on_submit():
        form.populate_obj(produto)
        db.session.commit()
        flash('Produto atualizado com sucesso!')
        return redirect(url_for('lista_produtos'))
    return render_template('form_produto.html', form=form)

@app.route('/produto/deletar/<int:id>')
def deletar_produto(id):
    produto = Produto.query.get_or_404(id)
    db.session.delete(produto)
    db.session.commit()
    flash('Produto deletado com sucesso!')
    return redirect(url_for('lista_produtos'))

# Rotas para Vendas
@app.route('/vendas')
def vendas():
    vendas = Venda.query.all()
    return render_template('vendas.html', vendas=vendas)

@app.route('/venda/nova', methods=['GET', 'POST'])
def nova_venda():
    form = VendaForm()
    if form.validate_on_submit():
        venda = Venda(
            cliente_id=form.cliente_id.data,
            produto_id=form.produto_id.data,
            quantidade=form.quantidade.data
        )
        produto = Produto.query.get(venda.produto_id)
        if produto.quantidade_estoque >= venda.quantidade:
            produto.quantidade_estoque -= venda.quantidade
            db.session.add(venda)
            db.session.commit()
            flash('Venda registrada com sucesso!')
        else:
            flash('Estoque insuficiente para a venda.')
        return redirect(url_for('vendas'))
    return render_template('form_venda.html', form=form)

# Rota para Relatórios e Gráficos
@app.route('/relatorios')
def relatorios():
    # Aqui você pode adicionar a lógica de geração de gráficos e relatórios
    # Exemplo fictício de dados para relatórios:
    vendas_por_cliente = {
        'João': 5,
        'Maria': 3,
        'Carlos': 8
    }
    return render_template('relatorios.html', vendas_por_cliente=vendas_por_cliente)

@app.route('/test_db')
def test_db():
    try:
        # Consulta o primeiro cliente na tabela
        cliente = Cliente.query.first()
        if cliente:
            return f"Banco de dados está funcionando! Primeiro cliente: {cliente.nome}"
        else:
            return "Banco de dados está funcionando, mas não há clientes cadastrados."
    except Exception as e:
        return f"Ocorreu um erro ao acessar o banco de dados: {e}"


if __name__ == '__main__':
    app.run(debug=True)
