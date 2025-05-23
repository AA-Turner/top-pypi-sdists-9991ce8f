import os
import pytest

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("agent")


def test_zabbixagent_running_and_enabled(host, zabbix_agent_service):
    assert zabbix_agent_service.is_running
    assert zabbix_agent_service.is_enabled


def test_zabbix_agent_dot_conf(zabbix_agent_conf):
    assert zabbix_agent_conf.user == "root"
    assert zabbix_agent_conf.group == "root"
    assert zabbix_agent_conf.mode == 0o644

    assert zabbix_agent_conf.contains("Server=192.168.3.33")
    assert zabbix_agent_conf.contains("ServerActive=192.168.3.33")
    assert zabbix_agent_conf.contains("DebugLevel=3")

    assert zabbix_agent_conf.contains("TLSConnect=psk")
    assert zabbix_agent_conf.contains("TLSAccept=psk,cert")
    assert zabbix_agent_conf.contains("TLSCertFile=/etc/zabbix/cert")
    assert zabbix_agent_conf.contains("TLSKeyFile=/etc/zabbix/key")
    assert zabbix_agent_conf.contains("TLSCAFile=/etc/zabbix/ca")


def test_zabbix_include_dir(zabbix_agent_include_dir):
    assert zabbix_agent_include_dir.is_directory
    assert zabbix_agent_include_dir.user == "root"
    assert zabbix_agent_include_dir.group == "root"
    assert zabbix_agent_include_dir.mode == 0o755


def test_socket(host):
    assert host.socket("tcp://0.0.0.0:10050").is_listening


# def test_zabbix_package(host, zabbix_agent_package):
#     assert zabbix_agent_package.is_installed

#     if host.system_info.distribution == "debian":
#         if host.system_info.codename in ["bullseye", "focal"]:
#             assert zabbix_agent_package.version.startswith("1:6.4")
#         else:
#             assert zabbix_agent_package.version.startswith("1:6.0")
#     if host.system_info.distribution == "centos":
#         assert zabbix_agent_package.version.startswith("6.4")
