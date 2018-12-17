# -*- coding: utf-8 -*-

""" v_ping
サーバーが生きていることの確認ページ
"""
from flask import Flask, render_template, request


def main():
    return render_template(
        'ping.html'
    )
