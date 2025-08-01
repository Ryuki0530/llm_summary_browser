from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtWidgets import QMenu
from PyQt5.QtCore import QUrl, Qt

class BrowserController:
    def load_url(self, browser, url):
        if not url.startswith("http"):
            url = "https://" + url
        browser.setUrl(QUrl(url))

    def reload_page(self, browser):
        if browser:
            browser.reload()

    def go_back(self, browser):
        if browser and browser.history().canGoBack():
            browser.back()

    def go_forward(self, browser):
        if browser and browser.history().canGoForward():
            browser.forward()

    def add_new_tab(self, tab_widget, url, label):
        browser = QWebEngineView()
        browser.setUrl(QUrl(url))
        browser.titleChanged.connect(lambda title, browser=browser: self.update_tab_title(tab_widget, browser, title))
        browser.page().createWindow = lambda _type: self.handle_new_window(tab_widget)

        browser.setContextMenuPolicy(Qt.CustomContextMenu)
        browser.customContextMenuRequested.connect(lambda pos, browser=browser: self.show_context_menu(tab_widget, browser, pos))

        index = tab_widget.addTab(browser, label)
        tab_widget.setCurrentIndex(index)

    def handle_new_window(self, tab_widget):
        new_browser = QWebEngineView()
        new_browser.titleChanged.connect(lambda title, browser=new_browser: self.update_tab_title(tab_widget, browser, title))
        new_browser.page().createWindow = lambda _type: self.handle_new_window(tab_widget)

        new_browser.setContextMenuPolicy(Qt.CustomContextMenu)
        new_browser.customContextMenuRequested.connect(lambda pos, browser=new_browser: self.show_context_menu(tab_widget, browser, pos))

        index = tab_widget.addTab(new_browser, "New Tab")
        tab_widget.setCurrentIndex(index)
        return new_browser.page()

    def update_tab_title(self, tab_widget, browser, title):
        index = tab_widget.indexOf(browser)
        if index != -1:
            tab_widget.setTabText(index, title)

    def show_context_menu(self, tab_widget, browser, pos):
        menu = QMenu(browser)

        js_code = f'''
        (function() {{
            var element = document.elementFromPoint({pos.x()}, {pos.y()});
            if (element && element.tagName === 'A' && element.href) {{
                return element.href;
            }}
            return null;
        }})();
        '''

        def handle_js_result(result):
            if result:
                open_action = menu.addAction("Open in New Tab")
                open_action.triggered.connect(lambda: self.add_new_tab(tab_widget, result, "New Tab"))
                menu.addSeparator()

            back_action = menu.addAction("Back")
            back_action.triggered.connect(lambda: self.go_back(browser))
            back_action.setEnabled(browser.history().canGoBack())

            forward_action = menu.addAction("Forward")
            forward_action.triggered.connect(lambda: self.go_forward(browser))
            forward_action.setEnabled(browser.history().canGoForward())

            reload_action = menu.addAction("Reload")
            reload_action.triggered.connect(lambda: self.reload_page(browser))

            menu.exec_(browser.mapToGlobal(pos))

        browser.page().runJavaScript(js_code, handle_js_result)
