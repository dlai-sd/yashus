#!/usr/bin/env python3
# generate-docker-compose.py
# Generates docker-compose.yml from devconfig.yaml
# Maintains single source of truth while supporting multiple environments

import yaml
import sys
import os
from pathlib import Path
from typing import Dict, Any, List

class DockerComposeGenerator:
    def __init__(self, devconfig_path: str):
        self.devconfig_path = devconfig_path
        self.config = self._load_devconfig()
    
    def _load_devconfig(self) -> Dict[str, Any]:
        """Load and parse devconfig.yaml"""
        with open(self.devconfig_path, 'r') as f:
            return yaml.safe_load(f)
    
    def generate_compose(self, environment: str = 'local') -> Dict[str, Any]:
        """Generate docker-compose.yml for given environment"""
        
        compose = {
            'version': '3.9',
            'services': {},
            'volumes': {},
            'networks': {}
        }
        
        # Build services section
        for service_name, service_config in self.config.get('services', {}).items():
            if not service_config.get('enabled', True):
                continue
            
            compose_service = self._build_service_config(
                service_name, 
                service_config, 
                environment
            )
            
            if compose_service:
                compose['services'][service_name] = compose_service
        
        # Add volumes
        if 'volumes' in self.config:
            compose['volumes'] = self.config['volumes']
        
        # Add networks
        if 'networks' in self.config:
            compose['networks'] = self.config['networks']
        
        return compose
    
    def _build_service_config(self, name: str, config: Dict, environment: str) -> Dict:
        """Build service configuration for docker-compose"""
        
        service = {}
        
        # Handle image
        if 'build' in config:
            service['build'] = self._build_build_config(config['build'])
        elif 'image' in config:
            image_config = config['image']
            if environment == 'local':
                service['image'] = image_config.get('local', image_config['name'])
            else:
                registry = self.config['environments'][environment]['registry']
                service['image'] = f"{registry}/{image_config['registry']}:{image_config['tags'][0]}"
        
        # Handle ports
        if 'ports' in config:
            ports = config['ports']
            if environment in ports:
                service['ports'] = [ports[environment]]
        
        # Handle volumes
        if environment == 'local' and 'volumes_dev' in config:
            service['volumes'] = config['volumes_dev']
        elif 'volumes' in config:
            service['volumes'] = config['volumes'].get('persistent', [])
        
        # Handle environment variables
        env_vars = config.get('env_vars', {})
        service['environment'] = env_vars
        
        # Handle health check
        if 'healthcheck' in config:
            hc = config['healthcheck']
            service['healthcheck'] = {
                'test': ['CMD', 'curl', '-f', hc.get('endpoint', '')] 
                        if 'endpoint' in hc else ['CMD', hc.get('command', '')],
                'interval': hc.get('interval', '30s'),
                'timeout': hc.get('timeout', '10s'),
                'retries': hc.get('retries', 3),
                'start_period': hc.get('start_period', '40s')
            }
        
        # Handle dependencies
        if config.get('depends_on'):
            service['depends_on'] = {
                dep: {'condition': 'service_healthy'} 
                for dep in config['depends_on']
            }
        
        # Handle resource limits
        if 'deployment' in config:
            deploy = config['deployment']
            service['deploy'] = {
                'resources': {
                    'limits': {
                        'memory': deploy.get('memory', '512Mi'),
                        'cpus': deploy.get('cpu', '500m')
                    }
                }
            }
        
        # Network
        service['networks'] = [self.config['global'].get('docker_network', 'hunter-network')]
        
        return service
    
    def _build_build_config(self, build_config: Dict) -> Dict:
        """Build build section configuration"""
        return {
            'context': build_config.get('context', '.'),
            'dockerfile': build_config.get('dockerfile', 'Dockerfile'),
            'target': build_config.get('target', 'production'),
            'args': build_config.get('args', {}),
            'cache_from': build_config.get('cache_from', [])
        }
    
    def save_compose_file(self, compose_config: Dict, output_path: str):
        """Save generated compose config to file"""
        with open(output_path, 'w') as f:
            yaml.dump(compose_config, f, default_flow_style=False, sort_keys=False)
        print(f"Generated: {output_path}")

def main():
    script_dir = Path(__file__).parent.parent
    devconfig_path = script_dir.parent / 'devconfig.yaml'
    
    if not devconfig_path.exists():
        print(f"Error: devconfig.yaml not found at {devconfig_path}", file=sys.stderr)
        sys.exit(1)
    
    environment = sys.argv[1] if len(sys.argv) > 1 else 'local'
    
    generator = DockerComposeGenerator(str(devconfig_path))
    compose_config = generator.generate_compose(environment)
    
    # Save to appropriate location
    if environment == 'local':
        output_path = script_dir.parent / 'TheHunter' / 'docker-compose.yml'
    else:
        output_path = script_dir.parent / f'docker-compose.{environment}.yml'
    
    generator.save_compose_file(compose_config, str(output_path))
    print(f"✓ Docker Compose file generated for environment: {environment}")

if __name__ == '__main__':
    main()
