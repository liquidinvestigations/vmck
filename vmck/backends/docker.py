from .qemu import random_port, constraints, resources, services, spreads


class DockerBackend:

    def task_group(self, job, options):
        vm_port = random_port()

        docker_vm_task = {
            'name': 'vm',
            'driver': 'docker',
            'config': {
                'image': 'vmck/mock:0.0.1',
                'port_map': [
                    {'ssh': 22},
                ],
            },
            'resources': resources(vm_port, options),
            'services': services(job),
        }

        return {
            'Name': 'test',
            'Constraints': constraints(),
            'Spreads': spreads(),
            'Tasks': [
                docker_vm_task,
            ],
            'RestartPolicy': {
                'Attempts': 0,
            },
        }
