# Monit-Fabric - a fabric installer for Monit on Debian Squeeze

monit-graphite is a quick'n'dirty fabric script to install [Monit](http://mmonit.com/monit/) on a debian squeeze box

## Why?
I couldn't find a backport install and I like fabric, so it keeps all the installation steps. It's easier than writing a
blog post and documenting each step

## Requirements

 * Workstation running python (version 2.7 recommended). All platforms should be supported.
 * [Fabric](http://docs.fabfile.org/en/1.4.1/index.html) - can be installed via `pip install fabric` or `easy_install fabric`
 * a server running a Debian squeeze

### Target Host

Best to execute this on a clean virtual machine running Debian 6 (Squeeze).

## Installation Instructions 

run `fab monit_install -H root@{hostname}` 
(hostname should be the name of a virtual server you're installing onto)

It might prompt you for the root password on the host you are trying to instal onto.

You can use it with a user other than root, as long as this user can `sudo`.

## DISCLAIMER

Please try this at your own risk. Please run this only with a newly installed host that you can easily throw away!
I tested it only with Debian 6 on EC2. 
