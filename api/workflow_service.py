"""
Servicio para leer workflows de diferentes plataformas de automatización
"""

import json
import os
from pathlib import Path


class WorkflowReader:
    """Lector de workflows de n8n, Make y Zapier"""
    
    def __init__(self, base_path):
        self.base_path = Path(base_path)
        self.workflows = {
            'n8n': [],
            'make': [],
            'zapier': []
        }
    
    def read_n8n_workflows(self):
        """Leer workflows de n8n desde archivos JSON"""
        n8n_path = self.base_path / 'integraciones' / 'n8n'
        
        if not n8n_path.exists():
            return []
        
        workflows = []
        for json_file in n8n_path.glob('*.json'):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                    # Extraer información relevante
                    workflow_info = {
                        'platform': 'n8n',
                        'name': data.get('name', json_file.stem),
                        'file': json_file.name,
                        'nodes': len(data.get('nodes', [])),
                        'connections': len(data.get('connections', {})),
                        'triggers': self._count_triggers(data),
                        'description': self._extract_description(data)
                    }
                    
                    workflows.append(workflow_info)
            except Exception as e:
                print(f"Error leyendo {json_file}: {e}")
        
        return workflows
    
    def read_make_workflows(self):
        """Leer información de workflows de Make desde README"""
        make_path = self.base_path / 'integraciones' / 'make'
        readme_path = make_path / 'README.md'
        
        if not readme_path.exists():
            return []
        
        workflows = []
        try:
            with open(readme_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Buscar información de workflows
                # Esto es básico, se puede mejorar con regex
                if 'workflow' in content.lower():
                    workflow_info = {
                        'platform': 'make',
                        'name': 'Make Integration',
                        'file': 'README.md',
                        'description': 'Ver README para más detalles',
                        'status': 'Documentado'
                    }
                    workflows.append(workflow_info)
        except Exception as e:
            print(f"Error leyendo Make README: {e}")
        
        return workflows
    
    def read_zapier_workflows(self):
        """Leer información de workflows de Zapier desde README"""
        zapier_path = self.base_path / 'integraciones' / 'zapier'
        readme_path = zapier_path / 'README.md'
        
        if not readme_path.exists():
            return []
        
        workflows = []
        try:
            with open(readme_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                if 'workflow' in content.lower() or 'zap' in content.lower():
                    workflow_info = {
                        'platform': 'zapier',
                        'name': 'Zapier Integration',
                        'file': 'README.md',
                        'description': 'Ver README para más detalles',
                        'status': 'Documentado'
                    }
                    workflows.append(workflow_info)
        except Exception as e:
            print(f"Error leyendo Zapier README: {e}")
        
        return workflows
    
    def get_all_workflows(self):
        """Obtener todos los workflows de todas las plataformas"""
        all_workflows = []
        
        # n8n
        n8n_workflows = self.read_n8n_workflows()
        all_workflows.extend(n8n_workflows)
        self.workflows['n8n'] = n8n_workflows
        
        # Make
        make_workflows = self.read_make_workflows()
        all_workflows.extend(make_workflows)
        self.workflows['make'] = make_workflows
        
        # Zapier
        zapier_workflows = self.read_zapier_workflows()
        all_workflows.extend(zapier_workflows)
        self.workflows['zapier'] = zapier_workflows
        
        return all_workflows
    
    def _count_triggers(self, workflow_data):
        """Contar triggers en un workflow de n8n"""
        count = 0
        for node in workflow_data.get('nodes', []):
            node_type = node.get('type', '')
            if 'trigger' in node_type.lower():
                count += 1
        return count
    
    def _extract_description(self, workflow_data):
        """Extraer descripción del workflow"""
        # Buscar en nodes que puedan tener descripción
        for node in workflow_data.get('nodes', []):
            if node.get('name') == 'Schedule Trigger':
                return f"Ejecuta cada {self._get_schedule_interval(node)}"
        
        return f"{len(workflow_data.get('nodes', []))} nodos, {self._count_triggers(workflow_data)} triggers"
    
    def _get_schedule_interval(self, node):
        """Obtener intervalo de ejecución de un trigger programado"""
        try:
            params = node.get('parameters', {})
            rule = params.get('rule', {})
            interval = rule.get('interval', [{}])[0]
            
            field = interval.get('field', '')
            value = interval.get(f'{field}Interval', 1)
            
            return f"{value} {field}"
        except:
            return "intervalo configurado"


def get_workflows_summary(base_path):
    """Obtener resumen de todos los workflows"""
    reader = WorkflowReader(base_path)
    workflows = reader.get_all_workflows()
    
    summary = {
        'total': len(workflows),
        'by_platform': {
            'n8n': len(reader.workflows['n8n']),
            'make': len(reader.workflows['make']),
            'zapier': len(reader.workflows['zapier'])
        },
        'workflows': workflows
    }
    
    return summary


if __name__ == '__main__':
    # Probar el lector
    import sys
    
    # Ruta base del proyecto
    base_path = Path(__file__).parent.parent
    
    print("Leyendo workflows...")
    print(f"Ruta base: {base_path}")
    
    reader = WorkflowReader(base_path)
    workflows = reader.get_all_workflows()
    
    print(f"\nTotal de workflows encontrados: {len(workflows)}")
    print(f"  - n8n: {len(reader.workflows['n8n'])}")
    print(f"  - Make: {len(reader.workflows['make'])}")
    print(f"  - Zapier: {len(reader.workflows['zapier'])}")
    
    print("\nDetalles:")
    for wf in workflows:
        print(f"\n{wf['platform'].upper()}: {wf['name']}")
        print(f"  Archivo: {wf['file']}")
        if 'nodes' in wf:
            print(f"  Nodos: {wf['nodes']}")
            print(f"  Triggers: {wf['triggers']}")
        print(f"  {wf.get('description', 'Sin descripción')}")
