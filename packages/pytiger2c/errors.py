# -*- coding: utf-8 -*-

"""
Jerarquía de las excepciones lanzadas en el paquete.
"""


class PyTiger2CError(Exception):
    """
    Base de todas las excepciones lanzadas en el paquete.
    """
    
    def __init__(self, error_type='Error', error_msg='An error occurred during the execution of PyTiger2C'):   
        super(PyTiger2CError, self).__init__()
        self._error_type = error_type
        self._error_msg = error_msg
        
    def __str__(self):
        return '{type}: {msg}.'.format(type=self._error_type, msg=self._error_msg)        
        

class SyntacticError(PyTiger2CError):
    """
    Excepción lanzada durante el análisis léxico-gráfico y sintáctico.
    """
    
    def __init__(self, error_msg='An error occurred during the syntax analysis'):
        super(SyntacticError, self).__init__('Syntactic Error', error_msg)


class SemanticError(PyTiger2CError):
    """
    Excepción lanzada durante el análisis semántico.
    """
    
    def __init__(self, error_msg='An error occurred during the semantic analysis'):
        super(SemanticError, self).__init__('Semantic Error', error_msg)


class CodeGenerationError(PyTiger2CError):
    """
    Excepción lanzadas durante la generación de código.
    """
    
    def __init__(self, error_msg='An error occurred during the code generation'):
        super(CodeGenerationError, self).__init__('Code Generation Error', error_msg)
