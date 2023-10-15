# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['lvl_creator.py'],
    pathex=[],
    binaries=[],
    datas=[],
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
)
build_options = {
    'build': {
        'force_32bit': True,  # Compilar para 32 bits
        'optimize': 2,  # Nivel de optimización
        'include_msvcr': True,  # Incluir MSVCR
        'disable_python_cache': True,  # Deshabilitar caché de Python
        'preload': ['numpy'],  # Precargar librerías (en este caso, numpy)
        'zip_include_packages': '*',  # Incluir todos los paquetes en el archivo zip
        'pycache_prefix': 'p',  # Prefijo para los archivos de caché
    },
}
coll = COLLECT(
    exe,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='lvl_creator',
    **build_options
)
