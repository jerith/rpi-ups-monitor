rpi-ups-monitor
===============

This is some Ansible magic to turn a mostly-fresh Raspbian installation (as of
February 2019) into a UPS monitor with nut, prometheus, and grafana.

Requirements
------------

You'll need ansible installed, and you'll need to be able to ssh to the target
pi with key-based authentication and passwordless sudo. You'll also need to
figure out what nut driver configuration you'll need for the UPS.

Usage
-----

* Edit `ansible/hosts` to replace my rpi's hostname with the address of your rpi.
* Edit `ansible/ups-monitor-playbook.yml` to replace my UPS configuration with your own.
* Run ansible to make the magic happen. I use the following command from the repo root:
  `time (cd ansible/; ansible-playbook ups-monitor-playbook.yml)`
