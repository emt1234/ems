from os import path
from mkdocs.structure.files import File

def getRelativePathToFile(file: File):
  return path.relpath(file.abs_src_path, file.src_dir)

class Metadata:
  slug: str | None
  """A specific slug to use for this file/directory, relative to the parent directory."""

  dest: str | None
  """A hard-coded destination path, relative to the site root."""

  def __init__(self, type: str):
    self.type = type
    self.slug = None
    self.dest = None

class DirectoryMeta(Metadata):
  def __init__(self, path: str):
    super().__init__("dir")
    self.path = path

class FileMeta(Metadata):
  folderNote: bool | None
  hoist: int | None
  """Move this file 'n' levels"""

  def __init__(self, file: File):
    super().__init__("file")
    self.file = file
    self.hoist = None
    self.folderNote = None

class Meta:
  def __init__(self):
    self.meta = []
    self.dirMeta = {}
    self.fileSourcePath = {}

  def ensureMetaForDirectory(self, path: str):
    if path not in self.dirMeta:
      meta = DirectoryMeta(path)
      self.meta.append(meta)
      self.dirMeta[path] = meta
      return meta
    return self.dirMeta.get(path)

  def ensureFileMetaByRelativeSourcePath(self, file: File):
    path = getRelativePathToFile(file)
    if path not in self.fileSourcePath:
      meta = FileMeta(file)
      self.meta.append(meta)
      self.fileSourcePath[path] = meta
      return meta
    return self.fileSourcePath.get(path)

  def getMetaForDirectory(self, path: str) -> DirectoryMeta | None:
    return self.dirMeta.get(path)

  def getFileByRelativeSourcePath(self, file: File) -> FileMeta | None:
    path = getRelativePathToFile(file)
    return self.fileSourcePath.get(path)



meta = Meta()
