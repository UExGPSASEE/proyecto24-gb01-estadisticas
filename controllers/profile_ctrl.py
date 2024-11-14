from flask import render_template, request, jsonify, redirect, url_for
from pymongo.collection import Collection
from models.language import Language