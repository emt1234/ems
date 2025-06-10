import pathlib
import logging
from meta import meta
from mkdocs.plugins import event_priority
from root_nav_store import root_files

from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.files import Files

log = logging.getLogger("mkdocs")

@event_priority(200)
def on_files(files: Files, config: MkDocsConfig):
  for f in files:
    if _is_path_under(base=config["site_dir"], path=f.abs_src_path):
      continue
    if len(pathlib.Path(f.src_path).parts) > 1:
      continue
    if f.name == ".nav":
      log.debug("Adding root file " + f.name)
      root_files.append(f)

# from https://github.com/oprypin/mkdocs-same-dir/blob/master/mkdocs_same_dir/plugin.py
def _is_path_under(base, path):
    try:
        pathlib.Path(path).relative_to(base)
        return True
    except ValueError:
        return False