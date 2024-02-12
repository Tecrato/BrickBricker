# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['BrickBricker.py'],
    pathex=[],
    binaries=[],
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
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    name='BrickBricker',
    exclude_binaries=True,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='Screenshot_10.ico',
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
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='BrickBricker',
    **build_options
)