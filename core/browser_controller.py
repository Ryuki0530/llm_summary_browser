from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage

class BrowserController:
    def load_url(self, browser: QWebEngineView, url: str):
        if not url.startswith("http"):
            url = "http://" + url
        browser.setUrl(QUrl(url))

    def reload_page(self, browser: QWebEngineView):
        browser.reload()
    
    def go_back(self, browser: QWebEngineView):
        if browser.history().canGoBack():
            browser.back()
    
    def go_forward(self, browser: QWebEngineView):
        if browser.history().canGoForward():
            browser.forward()
        
    def create_browser(self, url="https://www.google.com"):
            browser = QWebEngineView()
            browser.setUrl(QUrl(url))
            browser.page().setLinkDelegationPolicy(QWebEnginePage.DelegateAllLinks)
            return browser