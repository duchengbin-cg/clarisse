# This script creates a MaterialPhysicalStandard shader from a folder
# containing images comming from Substance Painter.
#
# It will create a context with the same name as the folder, it will
# import all images and make the correct connections to have a similar
# shader as the one in Subtance Painter. The shader is the same as the
# tutorial posted in isotropix's website.
#
# It won't assign the shader to a geometry.
#
# This script was made by modifying the ibl.py script provided by Clarisse.
#
# Luis Montemayor
#
#
from os import listdir
from os.path import isfile, join

suffix = 'tx'
upper_suffix = "TX"

extensions = 'All Known Files...\t.1001*.tx\n\
%s \t.1001*.{%s}'%(upper_suffix, suffix)

import re
regString = '([\w]+).(\d+).(%s)'%suffix
print regString

compile = re.compile(regString)
def convert_to_udim_style(files):
    ret = []
    for f in files:
        match_group = compile.match(f)
        if match_group:
            new_f_name = match_group.group(1) + "." + "<UDIM>" + "." + match_group.group(3)
            if new_f_name not in ret:
                ret.append(new_f_name)
    return ret


file = ix.api.GuiWidget.open_file(ix.application, '', 'Browse for an image', extensions)
if file != "":
    ix.begin_command_batch("Build Shader")
    path = file.split('/')
    path.pop(-1)
    folder_name = file.split('/').pop(-2)
    context = ix.cmds.CreateContext(folder_name)
    path =  "/".join(path)
    _onlyfiles = [f for f in listdir(path) if isfile(join(path, f)) and f.endswith('.tx')]
    onlyfiles = convert_to_udim_style(_onlyfiles)
    print "only filter files:"
    print onlyfiles
    txEmissive = '';
    for file in onlyfiles:
        if '_Normal.' in file:
            normal_tx = path + '/' + file
            txNormal = ix.cmds.CreateObject(folder_name + '_Normal_tx', 'TextureStreamedMapFile', context)
            txNormal.attrs.filename = normal_tx
            txNormal.attrs.color_space_auto_detect = False
            txNormal.attrs.file_color_space = 'linear'

        elif '_Specular.' in file:
            specular_tx = path + '/' + file
            txSpecular = ix.cmds.CreateObject(folder_name + '_Specular_tx', 'TextureStreamedMapFile', context)
            txSpecular.attrs.filename = specular_tx
            txSpecular.attrs.color_space_auto_detect = False
            txSpecular.attrs.file_color_space = 'sRGB'

        elif '_Roughness.' in file:
            roughness_tx = path + '/' + file
            txRougness = ix.cmds.CreateObject(folder_name + '_Roughness_tx', 'TextureStreamedMapFile', context)
            txRougness.attrs.filename = roughness_tx
            txRougness.attrs.color_space_auto_detect = False
            txRougness.attrs.file_color_space = 'linear'

        elif '_ior.' in file:
            ior_tx = path + '/' + file
            txIor = ix.cmds.CreateObject(folder_name + '_ior_tx', 'TextureStreamedMapFile', context)
            txIor.attrs.filename = ior_tx
            txIor.attrs.color_space_auto_detect = False
            txIor.attrs.file_color_space = 'linear'

        elif '_Height.' in file:
            height_tx = path + '/' + file
            txHeight = ix.cmds.CreateObject(folder_name + '_Height_tx', 'TextureStreamedMapFile', context)
            txHeight.attrs.filename = height_tx
            txHeight.attrs.color_space_auto_detect = False
            txHeight.attrs.file_color_space = 'linear'

        elif '_Diffuse.' in file:
            diffuse_tx = path + '/' + file
            txDiffuse = ix.cmds.CreateObject(folder_name + '_Diffuse_tx', 'TextureStreamedMapFile', context)
            txDiffuse.attrs.filename = diffuse_tx
            txDiffuse.attrs.color_space_auto_detect = False
            txDiffuse.attrs.file_color_space = 'sRGB'

        elif '_Emissive.' in file:
            emissive_tx = path + '/' + file
            txEmissive = ix.cmds.CreateObject(folder_name + '_Emissive_tx', 'TextureStreamedMapFile', context)
            txEmissive.attrs.filename = emissive_tx
            txEmissive.attrs.color_space_auto_detect = False
            txEmissive.attrs.file_color_space = 'sRGB'

    stand_mat = ix.cmds.CreateObject(folder_name, 'MaterialPhysicalStandard', context)
    ix.cmds.SetTexture([stand_mat.get_full_name() + ".diffuse_front_color"], txDiffuse.get_full_name())
    ix.cmds.SetTexture([stand_mat.get_full_name() + ".specular_1_color"], txSpecular.get_full_name())

    txNM = ix.cmds.CreateObject("normal_map", "TextureNormalMap", "", context)
    ix.cmds.SetTexture([stand_mat.get_full_name() + ".normal_input"], txNM.get_full_name())
    ix.cmds.SetTexture([txNM.get_full_name() + ".input"], txNormal.get_full_name())
    txDivide = ix.cmds.CreateObject("divide_IOR", "TextureDivide", "", context)
    ix.cmds.SetTexture([stand_mat.get_full_name() + ".specular_1_index_of_refraction"], txDivide.get_full_name())
    ix.cmds.SetValues([txDivide.get_full_name() + ".input1"], ["1", "1", "1"])
    txRescale = ix.cmds.CreateObject("rescale_IOR", "TextureRescale", "", context)
    ix.cmds.SetTexture([txDivide.get_full_name() + ".input2"], txRescale.get_full_name())
    ix.cmds.SetValues([txRescale.get_full_name() + ".output_min"], [".001", ".001", ".001"])


    txReorder = ix.cmds.CreateObject("reorder_roughness", "TextureReorder", "", context)
    ix.cmds.SetTexture([stand_mat.get_full_name() + ".specular_1_roughness"], txReorder.get_full_name())
    ix.cmds.SetValues([txReorder.get_full_name() + ".channel_order[0]"], ["rrrr"])
    ix.cmds.SetTexture([txReorder.get_full_name() + ".input"], txRougness.get_full_name())



    txReorder = ix.cmds.CreateObject("reorder_IOR", "TextureReorder", "", context)
    ix.cmds.SetTexture([txReorder.get_full_name() + ".input"], txIor.get_full_name())
    ix.cmds.SetValues([txReorder.get_full_name() + ".channel_order[0]"], ["rrrr"])
    ix.cmds.SetTexture([txRescale.get_full_name() + ".input"], txReorder.get_full_name())





    if txEmissive != "":
        ix.cmds.SetValues([stand_mat.get_full_name() + ".emission_strength"], ["1"])
        ix.cmds.SetTexture([stand_mat.get_full_name() + ".emission_color"], txEmissive.get_full_name())

    ix.end_command_batch()

else:
    ix.log_warning('This script has been aborted.')
