"""Create necessary compiled types for pyRevit bundles."""
from pyrevit import coreutils
from pyrevit.coreutils import logger

from pyrevit.loader import basetypes


#pylint: disable=W0703,C0302,C0103
mlogger = logger.get_logger(__name__)


def create_bundle_type(
        module_builder,
        type_name,
        bundle_script,
        bundle_config_script,
        bundle_search_paths,
        bundle_arguments,
        bundle_help_url,
        bundle_name,
        bundle_full_name,
        bundle_extension_name,
        bundle_unique_name,
        bundle_requires_clean_engine,
        bundle_requires_fullframe_engine,
        bundle_requires_persistent_engine,
    ):
    coreutils.create_type(
        module_builder,
        basetypes.CMD_EXECUTOR_TYPE,
        type_name,
        coreutils.create_ext_command_attrs(),
        bundle_script,
        bundle_config_script,
        coreutils.join_strings(bundle_search_paths),
        coreutils.join_strings(bundle_arguments),
        bundle_help_url,
        bundle_name,
        bundle_full_name,
        bundle_extension_name,
        bundle_unique_name,
        int(bundle_requires_clean_engine),
        int(bundle_requires_fullframe_engine),
        int(bundle_requires_persistent_engine))


def create_executor_type(extension, module_builder, cmd_component):
    mlogger.debug('Creating executor type for: %s', cmd_component)
    mlogger.debug('%s uses clean engine: %s',
                  cmd_component.name, cmd_component.requires_clean_engine)
    mlogger.debug('%s requires Fullframe engine: %s',
                  cmd_component.name, cmd_component.requires_fullframe_engine)
    mlogger.debug('%s requires Fullframe engine: %s',
                  cmd_component.name, cmd_component.requires_fullframe_engine)

    create_bundle_type(
        module_builder=module_builder,
        type_name=cmd_component.unique_name,
        bundle_script=cmd_component.script_file,
        bundle_config_script=cmd_component.config_script_file,
        bundle_search_paths=cmd_component.module_paths,
        bundle_arguments=cmd_component.arguments,
        bundle_help_url=cmd_component.help_url,
        bundle_name=cmd_component.name,
        bundle_full_name=cmd_component.get_full_bundle_name(),
        bundle_extension_name=extension.name,
        bundle_unique_name=cmd_component.unique_name,
        bundle_requires_clean_engine=cmd_component.requires_clean_engine,
        bundle_requires_fullframe_engine=\
            cmd_component.requires_fullframe_engine,
        bundle_requires_persistent_engine=\
            cmd_component.requires_persistent_engine
        )

    mlogger.debug('Successfully created executor type for: %s', cmd_component)


def create_selection_avail_type(module_builder, cmd_component):
    coreutils.create_type(module_builder,
                          basetypes.CMD_AVAIL_TYPE_SELECTION,
                          cmd_component.avail_class_name,
                          [],
                          cmd_component.context)


def create_zerodoc_avail_type(module_builder, cmd_component):
    coreutils.create_type(module_builder,
                          basetypes.CMD_AVAIL_TYPE_ZERODOC,
                          cmd_component.avail_class_name,
                          [])


def create_extended_avail_type(module_builder, cmd_component):
    coreutils.create_type(module_builder,
                          basetypes.CMD_AVAIL_TYPE_EXTENDED,
                          cmd_component.avail_class_name,
                          [],
                          cmd_component.context)
