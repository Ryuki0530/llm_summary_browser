from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView

class BrowserController:
    def load_url(self, browser: QWebEngineView, url: str):
        if not url.startswith("http"):
            url = "http://" + url
        browser.setUrl(QUrl(url))
