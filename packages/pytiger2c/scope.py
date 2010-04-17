# -*- coding: utf-8 -*-

"""
Clases C{Scope} y C{RootScope} que representan ámbitos de ejecución en Tiger.
"""

from pytiger2c.types.tigertype import TigerType
from pytiger2c.types.functiontype import FunctionType
from pytiger2c.types.integertype import IntegerType
from pytiger2c.types.stringtype import StringType


class Scope(object):
    """
    Clase C{Scope} que representa un ámbito de ejecución de Tiger.
    
    Esta clase gestiona los tipos, variables y funciones disponibles
    en un ámbito de ejecución en Tiger. Además mantiene una referencia
    a un ámbito padre donde se encuentra contenido este ámbito.
    """
    
    def _get_parent(self):
        """
        Método para obtener el valor de la propiedad C{parent}.
        """
        return self._parent
    
    parent = property(_get_parent)
    
    def _get_code_name(self):
        """
        Método para obtener el valor de la propiedad C{code_name}.
        """
        return self._code_name
    
    code_name = property(_get_code_name)
    
    def _get_code_type(self):
        """
        Método para obtener el valor de la propiedad C{code_type}.
        """
        return self._code_type    
    
    code_type = property(_get_code_type)    
    
    def __init__(self, parent):
        """
        Inicializa la clase C{Scope}.
        
        @type parent: C{Scope}
        @param parent: Ámbito en el que se define este nuevo ámbito. 
        """
        self._parent = parent
        self._types = {}
        self._members = {}
        self._code_name = None
        self._code_type = None

    def generate_code(self, generator):
        """
        Genera una estructura del lenguaje C que contiene las definiciones
        de las variables incluídas en este ámbito de ejecución.
        
        @type generator: C{CodeGenerator}
        @param generator: Clase auxiliar utilizada en la generación del 
            código C correspondiente a un programa Tiger.
        """
        if self._code_type is None:
            names = self._members.keys()
            members = self._members.values()
            parent = self.parent.code_name if (self.parent is not None) else None
            code_name, code_type = generator.define_scope(names, members, parent)
            self._code_name = code_name
            self._code_type = code_type
    
    def get_variable_code(self, name):
        """
        Genera el código necesario para acceder a una variable definida en 
        este ámbito o en alguno superior.
        
        Una variable definida en un ámbito superior puede ser accedida desde 
        cualquier ámbito inferior por lo que la variable en cuestión puede 
        estar definida en el ámbito actual, en su padre o en algún ancestro.
        
        @type name: C{str}
        @param name: Cadena de caracteres correspondiente al nombre de la 
            variable. 
            
        @rtype: C{str}
        @return: Cadena de caracteres correspondiente al código C necesario 
            para acceder a la variable.            
        """
        raise NotImplementedError()
        
    def define_type(self, name, tiger_type):
        """
        Añade una definición de tipos al ámbito actual.
        
        Un tipo puede definirse con el mismo nombre que alguno contenido en 
        algún ámbito superior y este nuevo tipo oculta al existente en el 
        ámbito superior. En caso de que el nuevo tipo tenga el mismo nombre 
        que alguno definido en el mismo ámbito, ocurre un error.        
        
        @type name: C{str}
        @param name: Cadena de caracteres correspondiente al nombre del 
            tipo que se declara.
        
        @type type: C{TigerType}
        @param type: Instancia de C{TigerType} correspondiente a la 
            declaración de tipo.
        
        @raise ValueError: Se lanza una excepción C{ValueError} si 
            el tipo que se intenta declarar fue definido anteriormente 
            en este ámbito. 
        """
        if not (name in self._types):
            self._types[name] = tiger_type
        else:
            raise ValueError('Type already defined in this scope')
        
    def get_type_definition(self, name):
        """
        Retorna la definición de tipos correspondiente al nombre dado. Si
        el tipo no se encuentra en el ámbito actual se buscará en los
        ancestros hasta llegar al ámbito raíz que lanzará una excepción
        si una definición de tipo para el nombre dado no es encontrado 
        finalmente.
        
        @type name: C{str}
        @param name: Cadena de caracteres correspondiente al nombre del 
            tipo que se quiere obtener.
        
        @rtype: C{TigerType}
        @return: Instancia de C{TigerType} correspondiente a la definición 
            de tipo buscada.
            
        @raise KeyError: Se lanza una excepción C{KeyError} si el tipo no 
            está definido en este ámbito o en alguno superior.
        """
        if name in self._types:
            return self._types[name]
        else:
            return self._parent.get_type_definition(name)
    
    def define_function(self, name, function_type):
        """
        Añade una definición de funciones al ámbito actual.
        
        Una función puede definirse con el mismo nombre que alguna contenido en 
        algún ámbito superior y esta nueva función oculta a la existente en el 
        ámbito superior. En caso de que la nueva función tenga el mismo nombre
        que alguna definida en el mismo ámbito, ocurre un error. 
        
        @type name: C{str}
        @param name: Cadena de caracteres correspondiente al nombre de la 
            función que se declara.
            
        @type function_type: C{FunctionType}
        @param function_type: Instancia de C{FunctionType} correspondiente a la 
            definición de función.
            
        @raise ValueError: Se lanza una excepción C{ValueError} si la función 
            que se intenta definir se definió anteriormente en este ámbito. 
        """
        if not (name in self._members):
            self._members[name] = function_type
        else:
            raise ValueError('Function already defined in this scope')
    
    def get_function_definition(self, name):
        """
        Retorna la definición de la función correspondiente al nombre dado.
        
        @type name: C{str}
        @param name: Cadena de caracteres correspondiente al nombre de la 
            función.
        
        @rtype: C{FunctionType}
        @return: Instancia de C{FunctionType} correspondiente a la definición 
            de la función.
        
        @raise KeyError: Se lanza un C{KeyError} si la función no está
            definida en este scope o en alguno superior.

        @raise ValueError: Se lanza una expceción C{ValueError} si existe
            un miembro en algún ámbito con el nombre dado pero no es una
            función.
        """
        if name in self._members:
            function_type = self._members[name]
            if isinstance(function_type, FunctionType):
                return function_type
            else:
                raise ValueError('The member of the scope is not a function')
        else:
            return self.parent.get_function_definition(name)
    
    def define_variable(self, name, tiger_type):
        """
        Añade una definición de variable al ámbito actual.
        
        Una variable puede definirse con el mismo nombre que alguna contenida 
        en algún ámbito superior y esta nueva variable oculta a la existente en
        el ámbito superior. En caso de que la nueva variable tenga el mismo 
        nombre que alguna definida en el mismo ámbito, ocurre un error.
        
        @type name: C{str}
        @param name: Cadena de caracteres correspondiente al nombre de la 
            variable que se declara.
            
        @type tiger_type: C{VariableType}
        @param tiger_type: Instancia de C{VariableType} correspondiente a la 
            definición de la variable que se quiere definir.
             
        @raise ValueError: Se lanza una excepción C{ValueError} si la variable
            que se intenta definir se definió anteriormente en este ámbito.        
        """
        if not (name in self._members):
            self._members[name] = tiger_type
        else:
            raise ValueError('Variable already defined in this scope')
        
    def get_variable_definition(self, name):
        """
        Retorna la definición de una variable de este ámbito o algún ámbito 
        ancestro.
        
        @type name: C{str}
        @param name: Cadena de caracteres correspondiente al nombre de la 
            variable.
        
        @rtype: C{VariableType}
        @return: Instancia de C{VariableType} correspondiente a la declaración
            de la variable.
            
        @raise KeyError: Se lanza una excepción C{KeyError} si la variable 
            no está definida en este ámbito o en alguno superior.
            
        @raise ValueError: Se lanza una expceción C{ValueError} si existe
            un miembro en algún ámbito con el nombre dado pero no es una
            variable.             
        """
        if name in self._members:
            variable_type = self._members[name]
            if isinstance(variable_type, FunctionType):
                raise ValueError('The member of the scope is not a variable')
            else:
                return variable_type
        else:
            return self.parent.get_variable_definition(name)
        

class RootScope(Scope):
    """
    Clase C{RootScope} que representa el ámbito raíz de un programa Tiger.
    
    Esta clase gestiona los tipos, variables y funciones disponibles
    en un ámbito de ejecución detereminado en Tiger.
    
    En esta clase se encuentran las definiciones de las funciones de 
    la librería estándar y tipos básicos de Tiger. Además, esta clase
    es la encargada de detener la búsqueda de tipos, funciones y 
    variables por los ámbitos padres lanzando una excepción C{KeyError}
    si no se encuentra una definición en este ámbito.
    """
    
    def __init__(self):
        """
        Inicializa el ámbito raíz de un programa de Tiger.
        
        Inicializa las declaraciones de las funciones de la biblioteca standard
        y los tipos básicos.
        """
        super(RootScope, self).__init__(None)
        self._init_types()
        self._init_functions()
        
    def _init_types(self):
        """
        Inicializa los tipos básicos del lenguaje Tiger definidos implícitamente 
        en el ámbito raíz.
        """
        self.define_type('int', IntegerType())
        self.define_type('string', StringType())
    
    def _init_functions(self):
        """
        Inicializa las funciónes de la biblioteca standard del lenguaje Tiger
        definidas implícitamente el ámbito raíz.
        """
        int_type = IntegerType()
        string_type = StringType()
        
        print_type = FunctionType(None, [string_type], [''])
        print_type.code_name = 'tiger_print'
        printi_type = FunctionType(None, [int_type], [''])
        printi_type.code_name = 'tiger_printi'
        flush_type = FunctionType(None, [], [])
        flush_type.code_name = 'tiger_flush'
        getchar_type = FunctionType(string_type, [], [])
        getchar_type.code_name = 'tiger_getchar'
        ord_type = FunctionType(int_type, [string_type], [''])
        ord_type.code_name = 'tiger_ord'
        chr_type = FunctionType(string_type, [int_type], [''])
        chr_type.code_name = 'tiger_chr'
        size_type = FunctionType(int_type, [string_type], [''])
        size_type.code_name = 'tiger_size'
        substring_type = FunctionType(string_type, [string_type, int_type, int_type], ['', '', ''])
        substring_type.code_name = 'tiger_substring'
        concat_type = FunctionType(string_type, [string_type, string_type], ['', ''])
        concat_type.code_name = 'tiger_concat'
        not_type = FunctionType(int_type, [int_type], [''])
        not_type.code_name = 'tiger_not'
        exit_type = FunctionType(None, [int_type], [''])
        exit_type.code_name = 'tiger_exit'

        self.define_function('print', print_type)
        self.define_function('printi', printi_type)
        self.define_function('flush', flush_type)
        self.define_function('getchar', getchar_type)
        self.define_function('ord', ord_type)
        self.define_function('chr', chr_type)
        self.define_function('size', size_type)
        self.define_function('substring', substring_type)
        self.define_function('concat', concat_type)
        self.define_function('not', not_type)
        self.define_function('exit', exit_type)
        
    def get_type_definition(self, name):
        """
        Para obtener información acerca de los parámetros recibidos por
        este método consulte la documentación del método C{get_type_definition}
        en la clase C{Scope}.
        """
        return self._types[name]

    def get_function_definition(self, name):
        """
        Para obtener información acerca de los parámetros recibidos por
        este método consulte la documentación del método C{get_function_definition}
        en la clase C{Scope}.
        """
        function_type = self._members[name]
        if isinstance(function_type, FunctionType):
            return function_type
        else:
            raise ValueError('The member of the scope is not a function')

    def get_variable_definition(self, name):
        """
        Para obtener información acerca de los parámetros recibidos por
        este método consulte la documentación del método C{get_variable_definition}
        en la clase C{Scope}.
        """
        variable_type = self._members[name]
        if isinstance(variable_type, FunctionType):
            raise ValueError('The member of the scope is not a variable')
        else:
            return variable_type


class FakeScope(Scope):
    """
    Clase C{FakeScope} que representa un ámbito falso de un programa de Tiger.
       
    Este ámbito recibe el calificativo de falso porque no guardará 
    definiciones de tipos, ni variables, ni funciones; cualquier consulta
    con el objetivo de definir u obtener un miembro del ámbito la redigirá 
    al ámbito padre. El objetivo de este ámbito es detectar la declaración 
    de funciones o tipos mutuamente recursivos en grupos de declaraciones 
    diferentes. Si la situación anterior se detecta se lanzará una excepción 
    indicando que el tipo no está definido en lugar de continuar la búsqueda 
    a través del ámbito padre.
    """
    
    def _get_current_member(self):
        """
        Método para obtener el valor de la propiedad C{current_member}.        
        """
        return self._current_member
    
    def _set_current_member(self, member):
        """
        Método para cambiar el valor de la propiedad C{current_member}.
        """
        self._current_member = member
        
    current_member = property(_get_current_member, _set_current_member)
    
    def _get_current_siblings(self):
        """
        Método para obtener el valor de la propiedad C{current_siblings}.        
        """
        return self._current_siblings
    
    def _set_current_siblings(self, siblings):
        """
        Método para cambiar el valor de la propiedad C{current_siblings}.
        """
        self._current_siblings = siblings
        
    current_siblings = property(_get_current_siblings, _set_current_siblings)
    
    def _get_relationships(self):
        """
        Método para obtener el valor de la propiedad C{relationships}.        
        """
        return self._relationships
    
    relationships = property(_get_relationships)
    
    def _get_max_depth(self):
        """
        Método para obtener el valor de la propiedad C{max_depth}.
        """
        return self._max_depth
    
    def _set_max_depth(self, value):
        """
        Método para cambiar el valor de la propiedad C{max_depth}.
        """
        self._max_depth = value
    
    max_depth = property(_get_max_depth, _set_max_depth)
    
    def __init__(self, parent):
        """
        Para obtener información acerca de los parámetros recibidos por
        este método consulte la documentación del método C{__init__}
        en la clase C{Scope}.
        """
        super(FakeScope, self).__init__(parent)
        self._current_member = None
        self._current_siblings = None
        self._relationships = {}
        self._max_depth = 5

    def define_type(self, name, tiger_type):
        """
        Para obtener información acerca de los parámetros recibidos por
        este método consulte la documentación del método con el mismo nombre
        en la clase C{Scope}.
        """
        self.parent.define_type(self, name, tiger_type)

    def define_function(self, name, function_type):
        """
        Para obtener información acerca de los parámetros recibidos por
        este método consulte la documentación del método con el mismo nombre
        en la clase C{Scope}.
        """
        self.parent.define_function(name, function_type)

    def define_variable(self, name, tiger_type):
        """
        Para obtener información acerca de los parámetros recibidos por
        este método consulte la documentación del método con el mismo nombre
        en la clase C{Scope}.
        """
        self.parent.define_variable(name, tiger_type)
        
    def generate_code(self, generator):
        """
        Para obtener información acerca de los parámetros recibidos por
        este método consulte la documentación del método con el mismo nombre
        en la clase C{Scope}.
        """
        self.parent.generate_code()

    def get_variable_code(self, name):
        """
        Para obtener información acerca de los parámetros recibidos por
        este método consulte la documentación del método con el mismo nombre
        en la clase C{Scope}.
        """
        return self.parent.get_variable_code(name)
    
    def get_variable_definition(self, name):
        """
        Para obtener información acerca de los parámetros recibidos por
        este método consulte la documentación del método con el mismo nombre
        en la clase C{Scope}.
        """
        return self.parent.get_variable_definition(name)   
        
    def get_type_definition(self, name):
        """
        Para obtener información acerca de los parámetros recibidos por
        este método consulte la documentación del método con el mismo nombre
        en la clase C{Scope}.
        
        En este método se implementa la comprobación de la definición de 
        tipos mutuamente recursivos, consulte la documentación del método
        C{check_mutual_recursion} para más información.
        """
        self.check_mutual_recursion(name)
        return self.parent.get_type_definition(name)

    def get_function_definition(self, name):
        """
        Para obtener información acerca de los parámetros recibidos por
        este método consulte la documentación del método con el mismo nombre
        en la clase C{Scope}.
        
        En este método se implementa la comprobación de la definición de 
        funciones o procedimientos mutuamente recursivos, consulte la 
        documentación del método C{check_mutual_recursion} para más 
        información.        
        """
        self.check_mutual_recursion(name)
        return self.parent.get_function_definition(name)
        
    def check_mutual_recursion(self, name):
        """
        Este método es utilizado por los métodos C{get_function_definition} y
        C{get_type_definition} para comprobar que el tipo, función o procedimiento
        identificado por el nombre dado C{name} no tenga una definición mutualmente
        recursiva en función de un tipo, función o procedimiento de otro grupo
        de definiciones.
        
        Si el miembro C{name} se encuentra definido en un grupo de definiciones
        hermano del grupo actual se comprobará que no exista una definición
        mutuamente recursiva. En caso de que todavía no se tenga suficiente
        información para afirmar o negar que exista una definición mutuamente
        recursiva se actualizará el diccionario de relaciones para que la 
        definición mutuamente recursiva, si existe, sea detectada cuando
        se compruebe la definición del otro tipo, función o procedimiento.
        
        @type name: C{str}
        @param name: Nombre del tipo, función o procedimiento para el cual
            se debe realizar la comprobación.
            
        @raise KeyError: Se lanza una excepción C{KeyError} si el miembro del 
            scope identificado por el nombre C{name} tiene una definición
            mutuamente recursiva con otro miembro de un grupo de definiciones
            diferente.
        """
        if self.current_member != None and self.current_siblings != None:
            if name in self.current_siblings:
                name_relationships = list(self._relationships.get(name, set()))
                current = 0
                while len(name_relationships) > 0 and current < self.max_depth:
                    if self.current_member in name_relationships:
                        raise KeyError('Mutually recursive type or function definition')
                    next = name_relationships[0]
                    name_relationships.remove(next)
                    name_relationships.extend(self._relationships.get(next, set()))
                    current += 1
            current_relationships = self.relationships.get(self.current_member, set())
            current_relationships.add(name)
            self.relationships[self.current_member] = current_relationships
