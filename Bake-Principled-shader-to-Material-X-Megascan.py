p = hou.selectedNodes()
n = p[0].parent().createNode('subnet', node_name=p[0].name() + '_mtlx')
p = p[0]
n.setPosition(p.position()+hou.Vector2(0,-5))
n.setMaterialFlag(True)
p.setMaterialFlag(False)

for i in n.children():
    i.destroy()
so = n.createNode('subnetconnector', node_name='surface_output')
so.parm('connectorkind').set(1)
so.parm('parmname').set('surface')
so.parm('parmlabel').set('surface')
so.parm('parmtype').set(24)

dis = n.createNode('subnetconnector', node_name='displacement_output')
dis.parm('connectorkind').set(1)
dis.parm('parmname').set('displacement')
dis.parm('parmlabel').set('displacement')
dis.parm('parmtype').set(25)

###########Create Albedo##########

mtlxss = n.createNode('mtlxstandard_surface')
albe = n.createNode('mtlxtiledimage', node_name='Albedo')
albe.parm('file').set(p.parm('basecolor_texture').eval())

###########Create Rough##########

rough = n.createNode('mtlxtiledimage', node_name='Roughness')
se_c = n.createNode('mtlxseparate3c')
rough.parm('file').set(p.parm('rough_texture').eval())

###########Create Normal##########

normal = n.createNode('mtlxtiledimage', node_name='Normal')
nmap = n.createNode('mtlxnormalmap')
normal.parm('file').set(p.parm('baseNormal_texture').eval())

###########Create Displacement##########

dm = n.createNode('mtlxtiledimage', node_name='Displacement')
se_c_d = n.createNode('mtlxseparate3c')
mtlre = n.createNode('mtlxremap')
mtlxd = n.createNode('mtlxdisplacement')

dm.parm('file').set(p.parm('dispTex_texture').eval())
mtlre.parm('outlow').set(-0.7)
mtlre.parm('outhigh').set(1-0.7)
mtlxd.parm('scale').set(0.05)

###########Create UV scale controler##########

uvctrl = n.createNode('mtlxconstant', node_name='UV_control')
uvctrl.parm('signature').set('vector2')
uvctrl.parm('value_vector2x').set(1)
uvctrl.parm('value_vector2y').set(1)

###########Check if there is Opacity File on Principle Shader than Create Opacity##########
check = p.parm('opaccolor_useTexture').eval()
if  check == 1:
     opac = n.createNode('mtlxtiledimage', node_name='Opacity')
     opac.parm('file').set(p.parm('opaccolor_texture').eval())
     opac.setInput(2,uvctrl,0)
     mtlxss.setInput(38,opac,0)

###########Connect node in Material X##########  
    
mtlxss.setInput(1,albe,0)
mtlxss.setInput(6,se_c,0)
mtlxss.setInput(40,nmap,0)

so.setInput(0,mtlxss,0)
se_c.setInput(0,rough,0)
nmap.setInput(0,normal,0)

dis.setInput(0,mtlxd,0)
mtlxd.setInput(0,mtlre,0)
mtlre.setInput(0,se_c_d,0)
se_c_d.setInput(0,dm,0)

albe.setInput(2,uvctrl,0)
rough.setInput(2,uvctrl,0)
normal.setInput(2,uvctrl,0)
dm.setInput(2,uvctrl,0)
    

###########Set link from Material X to parent material node##########  

n.layoutChildren()

m = p.parent()
m.parm('matnode1').set(n.path())
m.parm('matpath1').set(n.name())


