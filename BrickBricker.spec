# -*- mode: python ; coding: utf-8 -*-


# Brickbricker
a = Analysis(
    ['BrickBricker.py'],
    datas=[
        ('./Assets/Fuentes/*.ttf', './Assets/Fuentes/'),
        ('./Assets/images/pelota.png','./Assets/images/'),
        ('./Assets/images/explosion_3_40_128.webp','./Assets/images/'),
        ('./Assets/sounds/*.ogg','./Assets/sounds'),
        ('./Assets/sounds/*.mp3','./Assets/sounds'),
        ('./Screenshot_10.ico','./'),
        ('./lvl_c.ico','./'),
        ('./lvls.sqlite3','./'),
        ('./instrucciones.txt','./')
    ],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    name='BrickBricker',
    exclude_binaries=True,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='Screenshot_10.ico',
)

# Lvl Creator
a_2 = Analysis(
    ['lvl_creator.py'],
    datas=[
        ('./lvl_c.ico','./'),
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    noarchive=False,
)
pyz_2 = PYZ(a.pure, a.zipped_data)

exe_2 = EXE(
    pyz_2,
    a_2.scripts,
    exclude_binaries=True,
    name='lvl_creator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='lvl_c.ico',
)


build_options = {
    'build': {
        'optimize': 2,
        'include_msvcr': True,
        'preload': ['numpy'],
        'zip_include_packages': '*',
        'pycache_prefix': 'p',
    },
}
coll = COLLECT(
    exe,
    exe_2,
    a.binaries,
    a.datas,
    a_2.datas,
    strip=False,
    upx=True,
    name='BrickBricker',
    **build_options
)