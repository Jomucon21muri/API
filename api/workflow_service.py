"""
Servicio de lectura de flujos de trabajo de automatización.

Este módulo proporciona funcionalidades para leer y analizar workflows
de diferentes plataformas de automatización (n8n, Make, Zapier).

Clases:
    WorkflowReader: Lector de workflows de múltiples plataformas
    
Funciones:
    get_workflows_summary: Obtener resumen de todos los workflows
"""

import json
import os
from pathlib import Path
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)


class WorkflowReader:
    """
    Lector de workflows de plataformas de automatización.
    
    Soporta lectura y análisis de workflows de n8n, Make y Zapier.
    Para n8n, lee archivos JSON con la definición completa del workflow.
    Para Make y Zapier, extrae información desde archivos README.
    
    Attributes:
        base_path: Ruta base del proyecto
        workflows: Diccionario con workflows organizados por plataforma
    """
    
    def __init__(self, base_path: Path):
        """
        Inicializa el lector de workflows.
        
        Args:
            base_path: Ruta base del proyecto
        """
        self.base_path = Path(base_path)
        self.workflows: Dict[str, List[Dict[str, Any]]] = {
            'n8n': [],
            'make': [],
            'zapier': []
        }
    
    def read_n8n_workflows(self) -> List[Dict[str, Any]]:
        """
        Lee workflows de n8n desde archivos JSON.
        
        Busca archivos JSON en el directorio integraciones/n8n y extrae
        información relevante de cada workflow.
        
        Returns:
            List[Dict]: Lista de workflows con su información
        """
        n8n_path = self.base_path / 'integraciones' / 'n8n'
        
        if not n8n_path.exists():
            logger.warning(f'Directorio n8n no encontrado: {n8n_path}')
            return []
        
        workflows = []
        for json_file in n8n_path.glob('*.json'):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                    workflow_info = {
                        'platform': 'n8n',
                        'name': data.get('name', json_file.stem),
                        'file': json_file.name,
                        'nodes': len(data.get('nodes', [])),
                        'connections': len(data.get('connections', {})),
                        'triggers': self._count_triggers(data),
                        'description': self._extract_description(data),
                        'active': data.get('active', False)
                    }
                    
                    workflows.append(workflow_info)
                    logger.info(f'Workflow n8n cargado: {workflow_info["name"]}')
                    
            except json.JSONDecodeError as e:
                logger.error(f'Error al parsear JSON de {json_file}: {e}')
            except Exception as e:
                logger.error(f'Error leyendo {json_file}: {e}')
        
        return workflows
    
    def read_make_workflows(self) -> List[Dict[str, Any]]:
        """
        Lee información de workflows de Make desde README.
        
        Returns:
            List[Dict]: Lista con información de workflows de Make
        """
        make_path = self.base_path / 'integraciones' / 'make'
        readme_path = make_path / 'README.md'
        
        if not readme_path.exists():
            logger.warning(f'README de Make no encontrado: {readme_path}')
            return []
        
        workflows = []
        try:
            with open(readme_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                if 'workflow' in content.lower() or 'scenario' in content.lower():
                    workflow_info = {
                        'platform': 'make',
                        'name': 'Integración Make',
                        'file': 'README.md',
                        'description': 'Consultar README para detalles de configuración',
                        'status': 'Documentado'
                    }
                    workflows.append(workflow_info)
                    logger.info('Integración de Make documentada')
                    
        except Exception as e:
            logger.error(f'Error leyendo Make README: {e}')
        
        return workflows
    
    def read_zapier_workflows(self) -> List[Dict[str, Any]]:
        """
        Lee información de workflows de Zapier desde README.
        
        Returns:
            List[Dict]: Lista con información de workflows de Zapier
        """
        zapier_path = self.base_path / 'integraciones' / 'zapier'
        readme_path = zapier_path / 'README.md'
        
        if not readme_path.exists():
            logger.warning(f'README de Zapier no encontrado: {readme_path}')
            return []
        
        workflows = []
        try:
            with open(readme_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                if 'workflow' in content.lower() or 'zap' in content.lower():
                    workflow_info = {
                        'platform': 'zapier',
                        'name': 'Integración Zapier',
                        'file': 'README.md',
                        'description': 'Consultar README para detalles de configuración',
                        'status': 'Documentado'
                    }
                    workflows.append(workflow_info)
                    logger.info('Integración de Zapier documentada')
                    
        except Exception as e:
            logger.error(f'Error leyendo Zapier README: {e}')
        
        return workflows
    
    def get_all_workflows(self) -> List[Dict[str, Any]]:
        """
        Obtiene todos los workflows de todas las plataformas.
        
        Returns:
            List[Dict]: Lista consolidada de todos los workflows
        """
        all_workflows = []
        
        # Leer workflows de n8n
        n8n_workflows = self.read_n8n_workflows()
        all_workflows.extend(n8n_workflows)
        self.workflows['n8n'] = n8n_workflows
        
        # Leer workflows de Make
        make_workflows = self.read_make_workflows()
        all_workflows.extend(make_workflows)
        self.workflows['make'] = make_workflows
        
        # Leer workflows de Zapier
        zapier_workflows = self.read_zapier_workflows()
        all_workflows.extend(zapier_workflows)
        self.workflows['zapier'] = zapier_workflows
        
        logger.info(f'Total de workflows cargados: {len(all_workflows)}')
        
        return all_workflows
    
    def _count_triggers(self, workflow_data: Dict[str, Any]) -> int:
        """
        Cuenta los triggers en un workflow de n8n.
        
        Args:
            workflow_data: Datos del workflow en formato JSON
            
        Returns:
            int: Número de triggers encontrados
        """
        count = 0
        for node in workflow_data.get('nodes', []):
            node_type = node.get('type', '')
            if 'trigger' in node_type.lower():
                count += 1
        return count
    
    def _extract_description(self, workflow_data: Dict[str, Any]) -> str:
        """
        Extrae descripción del workflow.
        
        Args:
            workflow_data: Datos del workflow en formato JSON
            
        Returns:
            str: Descripción del workflow
        """
        # Buscar descripción explícita
        if 'description' in workflow_data:
            return workflow_data['description']
        
        # Generar descripción basada en estructura
        num_nodes = len(workflow_data.get('nodes', []))
        num_triggers = self._count_triggers(workflow_data)
        
        return f'{num_nodes} nodos, {num_triggers} triggers'


def get_workflows_summary(base_path: Path) -> Dict[str, Any]:
    """
    Obtiene resumen de todos los workflows.
    
    Args:
        base_path: Ruta base del proyecto
        
    Returns:
        Dict: Resumen con totales por plataforma y lista de workflows
    """
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
        if 'nodes' in wf:
            print(f"  Nodos: {wf['nodes']}")
            print(f"  Triggers: {wf['triggers']}")
        print(f"  {wf.get('description', 'Sin descripción')}")
