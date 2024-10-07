#!/usr/bin/python3
""" Fabric script (based on the file 1-pack_web_static.py) that distributes
an archive to your web servers, using the function do_deploy
"""
from datetime import datetime
from fabric.api import put, run, local, env, hosts
from os import path

env.hosts = ['54.157.150.179', '34.207.237.246']


def do_pack():
    """ do_pack function
    Return: the archive path if the archive has been correctly generated.
    Otherwise, it should return None
    """
    try:
        if not path.exists('versions'):
            local('mkdir -p versions')
        archive_name = 'versions/web_static_{}.tgz'.format(
            datetime.strftime(datetime.now(), '%Y%m%d%H%M%S'))
        print('Packing web_static to {}'.format(archive_name))
        local('tar -cvzf {} web_static'.format(archive_name))
        print('web_static packed: {} -> {}Bytes'.format(archive_name,
              path.getsize(archive_name)))
        return archive_name
    except BaseException:
        return None


def do_deploy(archive_path):
    """ do_deploy function
    Return: True if all operations have been done correctly,
    otherwise returns False
    """
    if not path.exists(archive_path):
        return False

    try:
        put('cp {} /tmp/'.format(archive_path))
        archive_name = path.basename(archive_path).rstrip('.tgz')
        run('mkdir -p /data/web_static/releases/{}/'.format(archive_name))
        run('tar -xzf /tmp/{0}.tgz -C /data/web_static/releases/{0}'.format(
            archive_name))
        run('rm /tmp/{}.tgz'.format(archive_name))
        run('mv /data/web_static/releases/{}.tgz'.format(archive_name))
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
    except BaseException:
        return False


def deploy():
    """ deploy function
    Return: the return value of do_deploy
    """
    archive_path = do_pack()
    if not archive_path:
        return False

    res = do_deploy(archive_path)
    return res
