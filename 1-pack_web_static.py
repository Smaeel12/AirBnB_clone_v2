#!/usr/bin/python3
""" Fabric script that generates a .tgz archive from the contents of the
web_static folder of your AirBnB Clone repo, using the function do_pack
"""
from datetime import datetime
from fabric.api import local
from os import path


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
