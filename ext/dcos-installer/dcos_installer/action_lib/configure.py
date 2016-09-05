import logging
import os
import subprocess
import sys
import glob
import shutil

import gen
import pkgpanda
import gen.installer.bash
from dcos_installer.util import SERVE_DIR

log = logging.getLogger(__name__)


def get_deactivate_list(gen_config):
    deactivate_list = []

    if 'kafka_collector_hosts' in gen_config.keys():
        deactivate_list.append("kafka")
        deactivate_list.append("ingestion-collector")
        deactivate_list.append("telegraf-collector")
        deactivate_list.append("elasticsearch")
        deactivate_list.append("influxdb")
        deactivate_list.append("grafana")
    return deactivate_list

def do_configure(gen_config):
    gen_config.update(get_gen_extra_args())
    subprocess.check_output(['mkdir', '-p', SERVE_DIR])

    do_validate_gen_config(gen_config)

    gen_out = gen.generate(arguments=gen_config)
    gen.installer.bash.generate(gen_out, SERVE_DIR)
    
    deactivate_list = get_deactivate_list(gen_config)
    
    # Get bootstrap from artifacts
    fetch_bootstrap(gen_out.arguments['bootstrap_id'], deactivate_list)
    # Write some package metadata
    pkgpanda.write_json('/genconf/cluster_packages.json', gen_out.cluster_packages)


def get_gen_extra_args():
    if 'BOOTSTRAP_ID' not in os.environ:
        log.error("BOOTSTRAP_ID must be set in environment to run.")
        raise KeyError

    arguments = {
        'bootstrap_id': os.environ['BOOTSTRAP_ID'],
        'provider': 'onprem'}
    return arguments


def do_validate_gen_config(gen_config):
    # run validate first as this is the only way we have for now to remove "optional" keys
    gen_config.update(get_gen_extra_args())
    return gen.validate(arguments=gen_config)


def fetch_bootstrap(bootstrap_id, deactivate_list):
    copy_set = [
        "{}.bootstrap.tar.xz".format(bootstrap_id),
        "{}.active.json".format(bootstrap_id)]
    dest_dir = "/genconf/serve/bootstrap/"
    container_cache_dir = "/artifacts/"

    # If all the targets already exist, no-op
    dest_files = [dest_dir + filename for filename in copy_set]
    if all(map(os.path.exists, dest_files)):
        return

    # Make sure the internal cache files exist
    src_files = [container_cache_dir + filename for filename in copy_set]
    for filename in src_files:
        if not os.path.exists(filename):
            log.error("Internal Error: %s not found. Should have been in the installer container.", filename)
            raise FileNotFoundError()

    def cleanup_and_exit():
        for filename in dest_files:
            try:
                os.remove(filename)
            except OSError as ex:
                log.error("Internal error removing temporary file. Might have corrupted file %s: %s",
                          filename, ex.strerror)
        sys.exit(1)

    def delete_file_or_dir(path_file):
        for fl in glob.glob(path_file):
                if os.path.isfile(fl):
                    os.remove(fl)
                elif os.path.isdir(fl):
                    shutil.rmtree(fl)
                elif os.path.islink(fl):
                    os.remove(fl)

    # Copy out the files, rolling back if it fails
    try:
        subprocess.check_output(['mkdir', '-p', '/genconf/serve/bootstrap/'])

        # Copy across
        for filename in copy_set:
            subprocess.check_output(['cp', container_cache_dir + filename, dest_dir + filename])
        
        if len(deactivate_list) > 0:
            print("Filtering packages from bootstrap tarball, this will take a few minutes...")
            file = dest_dir + "{}.active.json".format(bootstrap_id)
            file_tar = dest_dir + "{}.bootstrap.tar.xz".format(bootstrap_id)
            subprocess.check_output(['mkdir', '-p', dest_dir + '/temp'])
            subprocess.check_output(['tar', '-xf', file_tar, '-C', dest_dir + '/temp'])
            for service in deactivate_list:
                regexpdelete = "/{}/d".format(service)
                #Modify active.json
                subprocess.check_output(['sed', '-i', '-e', regexpdelete, file])
                #Modify tar.xz
                delete_file_or_dir(dest_dir + "/temp/active/*" + service + "*")
                subprocess.check_output(['sed', '-i', '-e', regexpdelete, dest_dir + '/temp/environment'])
                subprocess.check_output(['sed', '-i', '-e', regexpdelete, dest_dir + '/temp/environment.export'])
                delete_file_or_dir(dest_dir + "/temp/packages/*" + service + "*")
            subprocess.check_output(['tar', '-czf', file_tar, '-C', dest_dir + '/temp', '.'])
            subprocess.check_output(['rm', '-rf', dest_dir + '/temp'])
            print("Filter completed")


            
    except subprocess.CalledProcessError as ex:
        log.error("Copy failed: %s\nOutput:\n%s", ex.cmd, ex.output)
        log.error("Removing partial artifacts")
        cleanup_and_exit()
    except KeyboardInterrupt:
        log.error("Copy out of installer interrupted. Removing partial files.")
        cleanup_and_exit()
