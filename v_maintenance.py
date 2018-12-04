# -*- coding: utf-8 -*-

""" v_maintenance
メンテ画面
"""
from flask import Flask, render_template, request


def main():
    return render_template(
        'maintenance.html'
    )
