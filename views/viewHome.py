from flask import render_template, request, session, flash, redirect, url_for
import helpers
from main import app
import yfinance as yf


@app.route('/ranking')
def ranking_traders():
    return render_template('ranking.html', title='Classificação', title_page='Traders',
                           user_logged=helpers.verify_user_logged())


@app.route('/assets')
def assets():
    papel = yf.Ticker('MGLU3.SA')
    dados = papel.info
    chaves = list(dados.keys())
    valores = list(dados.values())

    lista = [[chaves[x], valores[x]] for x in range(len(chaves))]
    return render_template('assets.html', title='Ativos',
                           user_logged=helpers.verify_user_logged(),
                           set_element=lista,
                           title_page='Ativos no Jogo')


@app.route('/cockpit')
def cockpit():
    if helpers.verify_user_logged():
        return render_template('cockpit.html', user_logged=helpers.verify_user_logged(), title='Cockpoit do Trader',
                               title_page='Cockpit')
    else:
        return redirect('/login?next-page=cockpit')
