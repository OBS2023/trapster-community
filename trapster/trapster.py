import asyncio
import json
import netifaces
import os
from argparse import ArgumentParser

from trapster.modules import *
from trapster.logger import *


class TrapsterManager:
    def __init__(self, config):
        self.logger = None
        self.config = config

    def get_ip(self, config_interface):
        for interface in netifaces.interfaces():
            if interface == config_interface:
                return netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['addr']
        print(f"Interface {config_interface} does not exist")
        return

    async def start(self):
        ip = self.get_ip(self.config['interface'])

        for service_type in self.config['services']:
            for service_config in self.config['services'][service_type]:

                if service_type == 'ftp':
                    server = FtpHoneypot(service_config, self.logger, bindaddr=ip)
                elif service_type == 'http':
                    server = HttpHoneypot(service_config, self.logger, bindaddr=ip)
                elif service_type == 'ssh':
                    server = SshHoneypot(service_config, self.logger, bindaddr=ip)
                elif service_type == 'dns':
                    server = DnsHoneypot(service_config, self.logger, bindaddr=ip, proxy_dns_ip="127.0.0.1")
                elif service_type == 'vnc':
                    server = VncHoneypot(service_config, self.logger, bindaddr=ip)
                elif service_type == 'mysql':
                    server = MysqlHoneypot(service_config, self.logger, bindaddr=ip)
                elif service_type == 'postgres':
                    server = PostgresHoneypot(service_config, self.logger, bindaddr=ip)
                elif service_type == 'ldap':
                    server = LdapHoneypot(service_config, self.logger, bindaddr=ip)
                elif service_type == 'telnet':
                    server = TelnetHoneypot(service_config, self.logger, bindaddr=ip)
                else:
                    print(f"[-] Unrecognized service {service_type}")
                    break
                try:
                    print(f"[+] Starting service {service_type} on port {service_config['port']}")
                    await server.start()
                except Exception as e:
                    print(e)

        while True:
            await asyncio.sleep(10)


def load_config(config_path):
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            return json.load(f)
    else:
        print(f'[-] Config file not found: {config_path}')
        return None


def save_config(config_data, config_path):
    with open(config_path, 'w') as f:
        json.dump(config_data, f, indent=4)
    print("[+] Configuration updated successfully.")


def start_trapster(config_path):
    print('[+] Starting trapster')
    config = load_config(config_path)
    if not config:
        return

    manager = TrapsterManager(config)

    logger = JsonLogger(config['id'])
    logger.whitelist_ips = []

    manager.logger = logger

    try:
        asyncio.run(manager.start())
    except KeyboardInterrupt:
        print('Finishing')


def modify_configuration(config_path):
    config_data = load_config(config_path)
    print("\nCurrent Configuration:")
    print(json.dumps(config_data, indent=4))
    if not config_data:
        return

    change_interface = input(f"Current interface is {config_data['interface']}. Do you want to change it? (y/n): ")
    if change_interface.lower() == 'y':
        config_data['interface'] = input("Enter new interface name: ")

    service_changes = {}

    for service_type, services in config_data['services'].items():
        print(f"Configuring {service_type} service:")
        service_changes[service_type] = []
        for service_config in services:
            new_service_config = {}
            for key in ['username', 'password']:
                if key in service_config:
                    change_key = input(
                        f"Do you want to change {key} for {service_type} service (current: {service_config[key]})? (y/n): ")
                    if change_key.lower() == 'y':
                        new_service_config[key] = input(f"Enter new {key} for {service_type} service: ")
            service_changes[service_type].append(new_service_config)

    for service_type, services in service_changes.items():
        for idx, service in enumerate(services):
            if 'username' in service:
                config_data['services'][service_type][idx]['username'] = service['username']
            if 'password' in service:
                config_data['services'][service_type][idx]['password'] = service['password']

    save_config(config_data, config_path)


def menu():
    parser = ArgumentParser(description="Trapster Menu")
    parser.add_argument("command", choices=["start", "config"], help="Command to execute")
    parser.add_argument("--config", type=str, default="data/trapster.conf", help="Path to config file")

    args = parser.parse_args()

    if args.command == "start":
        start_trapster(args.config)
    elif args.command == "config":
        modify_configuration(args.config)


if __name__ == "__main__":
    menu()
