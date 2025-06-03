import logging
from os import path
from meta import meta, getRelativePathToFile
from mkdocs.plugins import event_priority

from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.files import Files
from mkdocs.structure.pages import Page

log = logging.getLogger("mkdocs")

def on_files(files: Files, config: MkDocsConfig):
  for file in files.documentation_pages():
    filePath = getRelativePathToFile(file)
    fileName = file.name
    [parentPath, fullFileName] = path.split(filePath)
    [aboveParent, parentName] = path.split(parentPath)
    # TODO: if 'folder-note' metadata exists, use to definitively mark as folder note
    if parentName == fileName:
      fileMeta = meta.ensureFileMetaByRelativeSourcePath(file)
      dirMeta = meta.ensureMetaForDirectory(parentPath)
      if fileMeta.slug and not dirMeta.slug and fileMeta.slug != "index":
        dirMeta.slug = fileMeta.slug
      fileMeta.folderNote = True
      fileMeta.slug = "index"
      fileMeta.hoist = 1

@event_priority(100)
def on_page_content(html: str, page: Page, config: MkDocsConfig, files: Files):
  fileMeta = meta.getFileByRelativeSourcePath(page.file)
  if fileMeta and fileMeta.folderNote == True:
    page.meta["folder_note"] = True