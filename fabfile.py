#!/usr/bin/env python
"""

monit-graphite is a fabric script to install latest monit (5.5) on debian hosts 

To execute:

    * Make sure you have fabric installed on your local host (e.g. pip install fabric)
    * run `fab monit_install -H root@{hostname}` 
      (hostname should be the name of a virtual server you're installing onto)

It might prompt you for the root password on the host you are trying to instal onto.

Best to execute this on a clean virtual machine running Debian 6 (Squeeze). 

"""

from fabric.api import cd, sudo, run, put, settings

def _check_sudo():
    with settings(warn_only=True):
        result = sudo('pwd')
        if result.failed:
            print "Trying to install sudo. Must be root"
            run('apt-get update && apt-get install -y sudo')  

def monit_install(force=False):
    """
    Installs monit 5.5
    """
    _check_sudo()
    with settings(warn_only=True):
        result = sudo('monit -V')
        if result.succeeded and "Monit version 5.5" in result and not force:
            print "Monit 5.5 already installed. Skipping."
            print "(use force=True to force install)"
            return
    sudo('apt-get update && apt-get upgrade -y')
    sudo('apt-get install -y build-essential libpam-dev libssl-dev make')
    sudo('mkdir -p /usr/local/src')
    with cd('/usr/local/src'):
        sudo('wget -N http://mmonit.com/monit/dist/monit-5.5.tar.gz')
        sudo('tar -zxvf monit-5.5.tar.gz')
    with cd('/usr/local/src/monit-5.5'):
        with settings(warn_only=True):
            result = sudo('./configure --sysconfdir=/etc/monit')
            if result.failed:
                # a workaround for ubuntu 12.04 (see
                # http://thinkinginsoftware.blogspot.de/2012/09/today-we-got-weird-error-in-one-of.html)
                sudo('./configure --sysconfdir=/etc/monit --with-ssl-lib-dir=/usr/lib/`uname -i`-linux-gnu')
        sudo('make && make install')
    sudo('mkdir -p /etc/monit')
    sudo('mkdir -p /var/lib/monit')
    put('config/init.d/monit', '/etc/init.d/', use_sudo=True)
    put('config/monitrc', '/etc/monit', use_sudo=True)
    put('config/monitrc', '/etc/monit', use_sudo=True)
    sudo('chmod 600 /etc/monit/monitrc')
    sudo('chown root /etc/monit/monitrc')
    sudo('chmod ugo+x /etc/init.d/monit')
    sudo('cd /etc/init.d && update-rc.d monit defaults')
    sudo('/etc/init.d/monit start')
