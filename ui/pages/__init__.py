"""
Pages package initialization
"""

from .aur import AurPage
from .delete_page import DeletePage
from .download_page import DownloadPage
from .search_page import SearchPage
from .dev_info_page import DevInfoPage

__all__ = [
    'AurPage',
    'DeletePage',
    'DownloadPage',
    'SearchPage',
    'DevInfoPage'
]