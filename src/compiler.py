"""
FunLang - Compilador Principal
Integra todas las fases del compilador
"""

import os
from pathlib import Path
from .lexer import create_lexer
from .parser import create_parser
from .semantic import create_analyzer
from .codegen import create_generator


class FunLangCompiler:
    """Compilador integrado de FunLang"""
    
    def __init__(self, output_dir: str = "output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        self.lexer = create_lexer()
        self.parser = create_parser()
        self.analyzer = create_analyzer()
        self.generator = create_generator()
    
    def compile(self, source: str, output_name: str = "output") -> dict:
        """Compila código fuente FunLang a C++"""
        result = {
            'success': False,
            'tokens': [],
            'ast': None,
            'cpp_code': None,
            'output_file': None,
            'errors': []
        }
        
        # Fase 1: Análisis Léxico
        try:
            tokens = self.lexer.tokenize(source)
            result['tokens'] = tokens
            if self.lexer.errors:
                result['errors'].extend(self.lexer.errors)
                return result
        except Exception as e:
            result['errors'].append(f"Error léxico: {str(e)}")
            return result
        
        # Fase 2: Análisis Sintáctico
        try:
            ast = self.parser.parse(source)
            result['ast'] = ast
            if self.parser.errors:
                result['errors'].extend(self.parser.errors)
                return result
            if ast is None:
                result['errors'].append("Error: No se pudo generar el AST")
                return result
        except Exception as e:
            result['errors'].append(f"Error sintáctico: {str(e)}")
            return result
        
        # Fase 3: Análisis Semántico
        try:
            if not self.analyzer.analyze(ast):
                result['errors'].extend(self.analyzer.errors)
                return result
        except Exception as e:
            result['errors'].append(f"Error semántico: {str(e)}")
            return result
        
        # Fase 4: Generación de Código
        try:
            cpp_code = self.generator.generate(ast)
            result['cpp_code'] = cpp_code
            
            # Guardar archivo
            output_file = self.output_dir / f"{output_name}.cpp"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(cpp_code)
            result['output_file'] = str(output_file)
            
        except Exception as e:
            result['errors'].append(f"Error en generación: {str(e)}")
            return result
        
        result['success'] = True
        return result
    
    def compile_file(self, filepath: str) -> dict:
        """Compila un archivo .fun"""
        path = Path(filepath)
        
        if not path.exists():
            return {'success': False, 'errors': [f"Archivo no encontrado: {filepath}"]}
        
        with open(path, 'r', encoding='utf-8') as f:
            source = f.read()
        
        output_name = path.stem
        return self.compile(source, output_name)


def create_compiler(output_dir: str = "output") -> FunLangCompiler:
    """Factory function para crear un compilador"""
    return FunLangCompiler(output_dir)
