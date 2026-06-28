#!/usr/bin/python3
"""Fabric script that creates and distributes an archive to the web servers"""

from fabric.api import env, local, put, run
from datetime import datetime
from os.path import exists, isdir

env.hosts = ['52.90.67.39', '44.208.165.54']
env.user = 'ubuntu'


def do_pack():
    """Generate a tgz archive from web_static folder.

    Returns the archive path on success, None otherwise.
    """
    try:
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        if not isdir("versions"):
            local("mkdir versions")
        file_name = "versions/web_static_{}.tgz".format(date)
        local("tar -cvzf {} web_static".format(file_name))
        return file_name
    except Exception:
        return None


def do_deploy(archive_path):
    """Distribute an archive to the web servers.

    Returns True on success, False otherwise.
    """
    if not exists(archive_path):
        return False
    try:
        file_n = archive_path.split("/")[-1]
        no_ext = file_n.split(".")[0]
        release_path = "/data/web_static/releases/{}/".format(no_ext)

        put(archive_path, '/tmp/')
        run('mkdir -p {}'.format(release_path))
        run('tar -xzf /tmp/{} -C {}'.format(file_n, release_path))
        run('rm /tmp/{}'.format(file_n))
        run('mv {0}web_static/* {0}'.format(release_path))
        run('rm -rf {}web_static'.format(release_path))
        run('rm -rf /data/web_static/current')
        run('ln -sf {} /data/web_static/current'.format(release_path))
        print("New version deployed!")
        return True
    except Exception:
        return False


def deploy():
    """Create and distribute a new archive to the web servers.

    Returns True on success, False otherwise.
    """
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
