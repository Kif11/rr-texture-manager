from modules.pathlib import Path
import pymel.core as pm
import shutil

class RRTextureManager(object):

    def __init__(self):
        self._file_nodes = []

    def _copy_texture(self, src, dst):
        shutil.copy2(src, dst)

    def node_count(self):
        return len(self.file_nodes)

    def add_node(self, file_node):
        """
        :param file_node: PyNode object of file type
        """
        if file_node.type() == 'file':
            self._file_nodes.append(file_node)
        else:
            raise ValueError, 'Node has to be of "file" type'

    def revert_all_paths(self):

        texture_attr = 'fileTextureName'

        for n in self.file_nodes:
            try:
                rr_tex_attr = pm.Attribute(n + '.rrTextureOriginalPath')
                n.setAttr(texture_attr, rr_tex_attr.get(), type='string')
            except pm.MayaAttributeError:
                print 'WRN: Can not revert texture on %s. ' \
                      '%s attribute does not exist' % (n.name, texture_attr)

    def change_all_paths(self, new_dir, copy=False):
        """
        Change path of all of the scene textures to a new location
        :param new_dir string: New texture directory
        :param copy bool: Copy textures to the new location. Dafault: False
        """

        new_dir = Path(new_dir)
        file_texture_name_attr = 'fileTextureName'
        rr_original_texture_attr = 'rrTextureOriginalPath'

        # Go trough every file node and change its path to new_dir
        for n in self.file_nodes:
            file_path_attr = pm.Attribute(n + '.' + file_texture_name_attr)
            original_path = Path(file_path_attr.get())
            new_path = new_dir / original_path.name

            try:
                rr_tex_attr = pm.Attribute(n + '.' + rr_original_texture_attr)
            except pm.MayaAttributeError:
                n.addAttr(rr_original_texture_attr, dt='string')
            finally:
                n.setAttr(rr_original_texture_attr, original_path, type='string')

            # Set new path to the file node
            file_path_attr.set(str(new_path))

            # Copy textures to new location for test
            if copy:
                self._copy_texture(str(original_path), str(new_path))

# Test function
def main():

    tm = RRTextureManager()
    texture_nodes = pm.ls(type='file')

    for n in texture_nodes:
        tm.add_node(n)

    tm.change_all_paths('/tmp')
    tm.revert_all_paths()
