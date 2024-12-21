from flask import render_template, request, jsonify, redirect, url_for

class ErrorCtrl:
    
    @staticmethod
    def error_404(element_type): 
        return jsonify({'error': f'{element_type} not found', 'status': '404 Not Found'}), 404

    @staticmethod
    def error_400(): 
        return jsonify({'error': 'Missing data or incorrect method', 'status': '400 Bad Request'}), 400