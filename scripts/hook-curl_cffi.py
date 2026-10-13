# -*- coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_all

datas, binaries, hiddenimports = collect_all("curl_cffi")
hiddenimports.append("_cffi_backend")
