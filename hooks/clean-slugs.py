import logging
import os
from meta import meta
from mkdocs.plugins import event_priority

from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.files import Files

def join(base: str, path: str):
  return "" + str(base) + "/" + str(path)

log = logging.getLogger("mkdocs")

def clean(slug: str):
  cleaned = slug
  cleaned = cleaned.replace(" - ", "-")
  cleaned = cleaned.replace("%20", "-")
  cleaned = cleaned.replace(" ", "-")
  cleaned = cleaned.replace("(", "")
  cleaned = cleaned.replace(")", "")
  cleaned = cleaned.lower()
  return cleaned

@event_priority(-50)
def on_files(files: Files, config: MkDocsConfig):
  for file in files.documentation_pages():
    # TODO: ensure script works for generated files too
    data = meta.getFileByRelativeSourcePath(file)
    if data and data.dest:
      log.debug("Using absolute 'dest' (" + data.dest + ") for " + file.dest_uri)
      file.dest_uri = data.dest
      file.abs_dest_path = join(file.dest_dir, data.dest)
      continue

    filePath = os.path.relpath(file.abs_dest_path, file.dest_dir)
    [parent, fullFileName] = os.path.split(filePath)
    extSuffix = os.path.splitext(fullFileName)[1]

    builtPath = ""

    if data and data.slug:
      builtPath = "" + data.slug + extSuffix
    else:
      builtPath = clean(fullFileName)

    hoisted = 0

    while parent and parent != "" and parent != "/":
      [nextParent, dirSlug] = os.path.split(parent)
      if data and data.hoist and hoisted < data.hoist:
        hoisted = hoisted + 1
        parent = nextParent
        continue
      dirMeta = meta.getMetaForDirectory(parent)
      if dirMeta and dirMeta.dest:
        builtPath = join(dirMeta.dest, builtPath)
        break

      if dirMeta and dirMeta.slug:
        builtPath = join(dirMeta.slug, builtPath)
      else:
        builtPath = join(clean(dirSlug), builtPath)
      parent = nextParent

    log.debug("Setting path to " + os.path.relpath(file.abs_src_path, file.src_dir) + " originally " + file.dest_uri + " to " + builtPath)
    file.dest_uri = builtPath
    file.abs_dest_path = join(file.dest_dir, builtPath)
    url = builtPath
    url = url.removesuffix("index.html")
    file.url = url
