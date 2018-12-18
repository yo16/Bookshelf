# -*- coding: utf-8 -*-

""" v_mainte_pub
Publisherメンテ画面
"""
from flask import Flask, render_template, request


def main():
    return render_template(
        'mainte_pub.html'
    )
