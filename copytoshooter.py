import shutil

shutil.rmtree('../Shooter/Assets/Message/generated')
shutil.copytree('generated', '../Shooter/Assets/Message/generated')
