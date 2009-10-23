# -*- coding: utf-8 -*-

"""
Script para compilar y ejecutar los programas de prueba.
"""

import os
import unittest
import subprocess


SRC_DIR = os.path.join(os.path.dirname(__file__), os.pardir)

TIGER2C_SCRIPT = os.path.abspath(os.path.join(SRC_DIR, 'scripts', 'tiger2c.py'))

TIGER2C_CMD = ['python', TIGER2C_SCRIPT, '-c']

TEST_DIR = os.path.abspath(os.path.join(SRC_DIR, 'tests'))


class TigerTestCase(unittest.TestCase):
    """
    Representa la ejecución de un programa Tiger de prueba.
    """
    
    def __init__(self, tiger_file):
        """
        Inicializa el la prueba.
        """
        super(TigerTestCase, self).__init__()
        self._tiger_file = os.path.join(TEST_DIR, tiger_file)
        self._exec_file = os.path.join(TEST_DIR, tiger_file[:-4])
        self._tiger2c_cmd = TIGER2C_CMD
        self._tiger2c_cmd.append(self._tiger_file)
        self._tiger2c_cmd.append(self._exec_file)
        self._in_file = os.path.join(TEST_DIR, tiger_file[:-4] + '.in')
        if not os.path.isfile(self._in_file):
            self._in_file = None
        self._out_file = os.path.join(TEST_DIR, tiger_file[:-4] + '.out')
        if not os.path.isfile(self._out_file):
            self._out_file = None
        self._tmp_file = os.path.join(TEST_DIR, tiger_file[:-4] + '.tmp')
        
    def shortDescription(self):
        """
        Retorna una descripción corta de la prueba.
        """
        return os.path.basename(self._tiger_file)
   
    def runTest(self):
        """
        Ejecuta la prueba.
        """
        # Compile the program.
        if subprocess.call(self._tiger2c_cmd) != 0 or not os.path.isfile(self._exec_file):
            self.fail('Compilation failed!')
        # Execute the program.
        exec_stdin = open(self._in_file) if self._in_file is not None else self._in_file
        exec_stdout = open(self._tmp_file, 'w')
        subprocess.call([self._exec_file], stdin=exec_stdin, stdout=exec_stdout)
        if exec_stdin is not None:
            exec_stdin.close()
        exec_stdout.close()
        # Compare the output of the programs.
        diff_cmd = ['diff', self._tmp_file, self._out_file]
        with  open('/dev/null', 'w') as devnull:
            if subprocess.call(diff_cmd, stdout=devnull, stderr=devnull) != 0:
                self.fail('Output does not match!')
        
    def tearDown(self):
        """
        Limpia el ambiente luego de ejecutar la prueba.
        """
        if os.path.isfile(self._exec_file):
            os.remove(self._exec_file)        
        if os.path.isfile(self._tmp_file):
            os.remove(self._tmp_file)


def main():
    """
    Función principal del script.
    """
    suite = unittest.TestSuite()
    runner = unittest.TextTestRunner(verbosity=2);
    for tiger_file in [f for f in os.listdir(TEST_DIR) if f.endswith('.tig')]:
        test_case = TigerTestCase(tiger_file)
        suite.addTest(test_case)
    runner.run(suite)


if __name__ == '__main__':
    main()