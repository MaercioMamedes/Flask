from flask import render_template, request, redirect, session, url_for
from main import repository, app
import yfinance as yf


@app.route('/add-ticker', methods=['POST'])
def add_ticker():
    ticker = request.form['ticker']
    repository.download_b3(ticker.upper() + '.SA')
    lista = repository.list_asset
    return render_template('cockpit.html', user_logged=session['user_logged'], title='Cockpit do Trader',
                           title_page='Cockpit', list_assets=lista)


@app.route('/portfolio')
def portfolio():
    if 'user_logged' not in session or session['user_logged'] is None:
        return redirect('/login?next=portfolio')

    return render_template('portfolio.html', title='Cadastro de Ativos',
                           user_logged=session['user_logged'],
                           title_page='Portfólio')


@app.route('/portfolio-register', methods=['POST', ])
def portfolio_register():
    asset = request.form['asset']
    ticker = asset.upper() + '.SA'
    b3 = yf.download(ticker, period='1mo', auto_adjust=True)
    print(b3['Close'])
    return redirect(url_for('index'))












