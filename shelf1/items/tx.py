import os

sellist = ix.selection
for sel in sellist:
    path = sel.attrs.filename[0] # getting the path to the texture file

    command = 'start /B maketx "%s"'%(path) # defining the external command. quotation marks around the path for DOS spaces in names
    os.system (command) # executing command

    (prefix, sep, suffix) = path.rpartition('.') # splitting the filepath string
    txpath = prefix + '.tx' # replacing the suffix with the .tx ending

    nodename = sel.get_name() # get the name of the selected node
    new_nodename="streamed_"+nodename # creating name for new streamed texture file node
    newnode=ix.cmds.CreateObject(new_nodename, "TextureStreamedMapFile") # creating streamedTexturefile node
    newnode.attrs.filename[0] = txpath # setting the texture file of new node to the TX texture.
