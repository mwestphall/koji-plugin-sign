# Koji callback for writing signed rpms after signing via sign.py
# Required for package generation with strict keys in mash

from koji.plugin import register_callback
import kojihub
import logging
from configparser import ConfigParser

# Configuration file in /etc like for other plugins
config_file = '/etc/koji-hub/plugins/sign.conf'

logger = logging.getLogger('koji.plugin.post_sign')


def post_sign(cbType, sigkey=None, sighash=None, build=None, rpm=None):
    """ Run the kojihub write-signed-rpm command on rpms after they've been signed with a signing key,
    which is required for generating repos that use a specific key.
    """
    if sigkey is None or sighash is None or build is None or rpm is None:
        logger.warning("Got unexpected None argument to post_sign plugin. Skipping")
        return

    if 'buildroot_id' not in rpm or 'nvr' not in build:
        logger.warning("Expected keys missing from plugin arguments. Skipping")
        return

    buildroot = kojihub.get_buildroot(rpm['buildroot_id'])

    if buildroot is None or 'tag_name' not in buildroot:
        logger.warning("No tag name found for build. Skipping")
        return

    tag_name = buildroot['tag_name']
    logger.info("Running post-sign plugin for build %s with tag_name %s", build['nvr'], tag_name)

    config = ConfigParser()
    config.read(config_file)
    
    if not config.has_option(tag_name, "strict_keys") or not config.getboolean(tag_name, "strict_keys"):
        # Only need to write-signed-rpm for repos with strict signing enabled
        logger.info("tag_name %s doesn't have strict signing enabled. Skipping.", tag_name)
        return
    

    kojihub.write_signed_rpm(rpm, sigkey)
    logging.getLogger('koji.plugin.sign').info("write-signed-rpm task run successfully.")

register_callback('postRPMSign', post_sign)
