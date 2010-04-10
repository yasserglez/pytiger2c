# -*- coding: utf-8 -*-

"""
Clases utilizadas en la generación de un archivo Graphviz DOT con el
árbol de sintáxis abstracta creado a partir de un programa Tiger.
"""


class DotGenerator(object):
    """
    Clase utilizada para la generación de grafos en formato Graphviz DOT. 
    """

    def __init__(self):
        """
        Esta clase es utilizada en la generación de código Graphivz DOT
        a partir de un árbol de sintáxis abstracta de un programa Tiger.
        """
        self._nodes = []
        self._edges = []
        self._num_nodes = 0
        
    def add_node(self, label):
        """
        Añade un nuevo nodo al grafo actualmente en creación.
        
        @type label: C{str}
        @param label: Nombre del nodo que se quiere añadir.
        
        @rtype: C{str}
        @return: Identificador del nuevo nodo añadido. Este identificador
            puede ser utilizado para crear nuevas aristas, utilizando
            el método C{add_edge} de esta misma clase, que tengan
            este nodo como uno de los extremos.
        """
        self._num_nodes += 1
        name = 'node{number}'.format(number=self._num_nodes)
        code = '{name} [label="{label}"];'.format(name=name, label=label)
        self._nodes.append(code)
        return name
        
    def add_edge(self, from_node, to_node):
        """
        Añade una arista no dirigida al grafo actualmente en creación.
        
        @type from_node: C{str}
        @param from_node: Cadena de caracteres que identifica un nodo 
            extremo de la arista.
        
        @type to_node: C{str}
        @param to_node: Cadena de caracteres que identifica un nodo 
            extremo de la arista.
        """
        template = '{from_node} -- {to_node};'
        code = template.format(from_node=from_node, to_node=to_node)
        self._edges.append(code)
        
    def write(self, output_fd):
        """
        Escribe el código Graphviz DOT en un descriptor de fichero.
        
        @type output_fd: C{file}
        @param output_fd: Descriptor de fichero donde se debe escribir el
            código Graphviz DOT resultante de la traducción del programa
            Tiger descrito por el árbol de sintáxis abstracta.
        """
        indent = ' ' * 4
        output_fd.write('graph AST {\n')
        output_fd.write(indent)
        output_fd.write('node [shape=record];\n\n')
        for node_code in self._nodes:
            output_fd.write(indent)
            output_fd.write(node_code)
            output_fd.write('\n')
        output_fd.write('\n')
        for edge_code in self._edges:
            output_fd.write(indent)
            output_fd.write(edge_code)
            output_fd.write('\n')
        output_fd.write('}\n')
