#!/usr/bin/python3
""" Fabric script that generates a .tgz archive from the contents of the
web_static folder of your AirBnB Clone repo, using the function do_pack
"""
from datetime import datetime
from fabric.api import local, run, put, env
from os import path

env.hosts = ['54.157.150.179', '34.207.237.246']


def do_pack():
    """ pack function
    Return: the archive path if the archive has been correctly generated,
    otherwise, it should return None
    """
    try:
        if not path.isdir('versions'):
            local('mkdir versions')
        archive_name = 'versions/web_static_{}.tgz'.format(
            datetime.strftime(datetime.now(), '%Y%m%d%H%M%S'))
        print('Packing web_static to {}'.format(archive_name))
        local('tar -cvzf {} web_static'.format(archive_name))
        print('web_static packed: {} -> {}Bytes'.format(
            archive_name, path.getsize(archive_name)))
        return archive_name
    except BaseException:
        return None


def do_deploy(archive_path):
    """ do_deploy function
    Return: True if all operations have been done correctly,
    otherwise returns False
    """
    if not path.isfile(archive_path):
        return False

    try:
        put(archive_path, '/tmp/')
        archive_name = path.basename(archive_path).rstrip('.tgz')
        run('mkdir -p /data/web_static/releases/{}/'.format(archive_name))
        run('tar -xzf /tmp/{0}.tgz -C /data/web_static/releases/{0}'.format(
            archive_name))
        run('rm /tmp/{}.tgz'.format(archive_name))
        run('mv /data/web_static/releases/{0}/web_static/* \
            /data/web_static/releases/{0}/'.format(
            archive_name))
        run('rm -rf /data/web_static/releases/{}/web_static'.format(
            archive_name))
        run('rm -rf /data/web_static/current')
        run('ln -s /data/web_static/releases/{}/ \
            /data/web_static/current'.format(archive_name))
        print('New version deployed!')
        return True
    except Exception:
        return False
