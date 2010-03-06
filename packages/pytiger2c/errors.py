# -*- coding: utf-8 -*-

"""
Jerarquía de las excepciones lanzadas durante la ejecución de PyTiger2C.
"""


class PyTiger2CError(Exception):
    """
    Clase base de todas las excepciones lanzadas en el paquete.
    """
    
    def __init__(self, error='Error', message='An error occurred during the execution of PyTiger2C'):
        """
        Representa un error ocurrido durante la ejecución de PyTiger2C.
        
        @type error: C{str}
        @param error: Tipo de error.
        
        @type message: C{str}
        @param message: Descripción del error.
        """
        super(PyTiger2CError, self).__init__()
        self.error = error
        self.message = message
        
    def __str__(self):
        """
        Retorna una cadena con el tipo de error ocurrido y una descripción del error.
        """
        return '{error}: {message}.'.format(error=self.error, message=self.message)        
        

class SyntacticError(PyTiger2CError):
    """
    Excepción lanzada durante el análisis léxico-gráfico y sintáctico.
    """
    
    def __init__(self, message='An error occurred during the syntactic analysis'):
        """
        Representa un error de sintáxis en un programa Tiger.
        
        @type message: C{str}
        @param message: Descripción del error.
        """
        super(SyntacticError, self).__init__('Syntactic Error', message)


class SemanticError(PyTiger2CError):
    """
    Excepción lanzada durante el análisis semántico.
    """
    
    def __init__(self, messages=None):
        """
        Representa un error semántico en un programa Tiger.
        
        @type messages: C{list}
        @param message: Lista de los mensajes de error ocurridos durante el
            análisis semántico..        
        """
        if messages is None:
            messages = ['An error occurred during the semantic analysis']
        self.messages = messages
        if len(self.messages) == 1:
            message = self.messages[0]
        else:
            message = 'Various semantic errors'
        super(SemanticError, self).__init__('Semantic Error', message)
        
    def __str__(self):
        """
        Retorna una cadena con el tipo de error ocurrido y una descripción del error.
        """
        messages = ['{error}: {message}.'.format(error=self.error, message=message) for message in self.messages]
        return '\n'.join(messages)
            

class CodeGenerationError(PyTiger2CError):
    """
    Excepción lanzadas durante la generación de código.
    """
    
    def __init__(self, message='An error occurred during the code generation'):
        """
        Representa un error ocurrido durante la generación de código.
        
        @type message: C{str}
        @param message: Descripción del error.        
        """
        super(CodeGenerationError, self).__init__('Code Generation Error', message)
