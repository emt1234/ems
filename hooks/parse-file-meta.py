from os import path
import logging
from re import Match
from mkdocs.exceptions import PluginError
import yaml
from yaml import SafeLoader
from mkdocs.utils.meta import YAML_RE
from meta import meta

from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.files import Files, File

log = logging.getLogger("mkdocs")

def get_meta(file: File, config: MkDocsConfig):
  docs = path.relpath(config.docs_dir)
  filePath = path.relpath(file.abs_src_path, docs)
  with open(file.abs_src_path, encoding = "utf-8-sig") as f:
    md = f.read()
    match: Match = YAML_RE.match(md)
    if not match:
      return {}
      # TODO: always ignore if no metadata? could create setting
      raise PluginError(
        f"Error reading metadata of post '{filePath}' in '{docs}':\n"
        f"Expected metadata to be defined but found nothing"
      )
    try:
      meta = yaml.load(match.group(1), SafeLoader) or {}
      # md = md[match.end():].lstrip("\n")
      return meta
    except Exception as e:
      raise PluginError(
          f"Error reading metadata of post '{filePath}' in '{docs}':\n"
          f"{e}"
      )

def on_files(files: Files, config: MkDocsConfig):
  for file in files.documentation_pages():
    fileMeta = meta.ensureFileMetaByRelativeSourcePath(file)
    frontmatter = get_meta(file, config)

    filePath = frontmatter.get("path") # TODO: make meta field name configurable
    if filePath:
      fileMeta.dest = filePath

    slug = frontmatter.get("slug") # TODO: make meta field name configurable
    if slug:
      fileMeta.slug = slug
