# -*- coding: utf-8 -*-

"""
Script para compilar y ejecutar los programas de prueba.
"""

import os
import unittest
import subprocess


SRC_DIR = os.path.join(os.path.dirname(__file__), os.pardir)

PYTIGER2C_SCRIPT = os.path.abspath(os.path.join(SRC_DIR, 'scripts', 'pytiger2c'))

PYTIGER2C_CMD = ['python', PYTIGER2C_SCRIPT]

TESTS_DIR = os.path.abspath(os.path.join(SRC_DIR, 'tests'))

SUCCCESS_DIR = os.path.abspath(os.path.join(TESTS_DIR, 'success'))

FAIL_DIR = os.path.abspath(os.path.join(TESTS_DIR, 'fail'))


class TigerTestCase(unittest.TestCase):
    """
    Clase base para ambos tipos de pruebas.
    """
    
    def __init__(self, parent_dir, tiger_file):
        """
        Inicializa la prueba.
        """
        super(TigerTestCase, self).__init__()
        self._tiger_file = os.path.join(parent_dir, tiger_file)
        self._exec_file = os.path.join(parent_dir, tiger_file[:-4])
        self._pytiger2c_cmd = PYTIGER2C_CMD + [self._tiger_file, '--output', self._exec_file]
        self._in_file = os.path.join(parent_dir, tiger_file[:-4] + '.in')
        if not os.path.isfile(self._in_file):
            self._in_file = None
        self._out_file = os.path.join(parent_dir, tiger_file[:-4] + '.out')
        if not os.path.isfile(self._out_file):
            self._out_file = None
        self._err_file = os.path.join(parent_dir, tiger_file[:-4] + '.err')
        if not os.path.isfile(self._err_file):
            self._err_file = None
        self._tmp_file = os.path.join(parent_dir, tiger_file[:-4] + '.tmp')
        
    def shortDescription(self):
        """
        Retorna una descripción corta de la prueba.
        """
        return os.path.basename(self._tiger_file)
   
    def failIfDifferent(self, first_file, second_file):
        """
        Falla si los archivos son diferentes.
        """
        diff_cmd = ['diff', first_file, second_file]
        if subprocess.call(diff_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE) != 0:
            self.fail('Output does not match!')
        
    def tearDown(self):
        """
        Limpia el ambiente luego de ejecutar la prueba.
        """
        if os.path.isfile(self._exec_file):
            os.remove(self._exec_file)        
        if os.path.isfile(self._tmp_file):
            os.remove(self._tmp_file)


class SuccessTigerTestCase(TigerTestCase):
    """
    Representa una prueba de éxito.
    
    El programa Tiger utilizado en esta prueba deberá compilarse sin errores
    y al ejecutarse, recibiendo el archivo .in como entrada standard, su 
    salida debe coincidir con el contenido del archivo .out. 
    """
    
    def runTest(self):
        """
        Ejecuta la prueba.
        """
        # Compile the program.
        if subprocess.call(self._pytiger2c_cmd) != 0 or not os.path.isfile(self._exec_file):
            self.fail('Compilation failed!')
        # Execute the program.
        exec_stdin = open(self._in_file) if self._in_file else None
        with open(self._tmp_file, 'w') as exec_stdout:
            subprocess.call([self._exec_file], stdin=exec_stdin, stdout=exec_stdout)
            if exec_stdin is not None:
                exec_stdin.close()
        # Compare the output of the programs.
        self.failIfDifferent(self._tmp_file, self._out_file)                    
        
    
class FailTigerTestCase(TigerTestCase):
    """
    Representa una prueba de fallo.
    
    PyTiger2C deberá fallar al intentar compilar el programa Tiger utilizado en
    esta prueba y el mensaje de error que imprima en la salida estándard de
    errores deberá coincidir con el contenido del archivo .err.
    """
    
    def runTest(self):
        """
        Ejecuta la prueba.
        """
        # Try to compile the program.
        with open(self._tmp_file, 'w') as pytiger2c_stderr: 
            if subprocess.call(self._pytiger2c_cmd, stderr=pytiger2c_stderr) != 1:
                self.fail('Compilation succeded and it should fail!')
        # Compare the error output.
        self.failIfDifferent(self._tmp_file, self._err_file)


def main():
    """
    Función principal del script.
    """
    suite = unittest.TestSuite()
    runner = unittest.TextTestRunner(verbosity=2);
    for tiger_file in [f for f in os.listdir(SUCCCESS_DIR) if f.endswith('.tig')]:
        test_case = SuccessTigerTestCase(SUCCCESS_DIR, tiger_file)
        suite.addTest(test_case)
    for tiger_file in [f for f in os.listdir(FAIL_DIR) if f.endswith('.tig')]:
        test_case = FailTigerTestCase(FAIL_DIR, tiger_file)
        suite.addTest(test_case)        
    runner.run(suite)


if __name__ == '__main__':
    main()