import logging
from meta import meta
from mkdocs.plugins import event_priority
from root_nav_store import root_files

from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.files import Files

log = logging.getLogger("mkdocs")

@event_priority(-50)
def on_files(files: Files, config: MkDocsConfig):
  for f in root_files:
    log.debug("Adding " + f.name + " as an included root file")
    files.append(f)
