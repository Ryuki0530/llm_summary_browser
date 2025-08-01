from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, QPushButton, QSplitter, QTextEdit, QTabWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtCore import Qt, QUrl, QEvent
from PyQt5.QtGui import QKeySequence
from core.browser_controller import BrowserController
"""
メインウィンドウのUI設計とレイアウト管理
"""
class MainWindow(QMainWindow):
    def __init__ (self):
        super().__init__()
        self.setWindowTitle("LLM Summary Browser")
        self.setGeometry(100, 100, 1200, 800)

        self.controller = BrowserController()

        self.url_bar = QLineEdit()
        self.go_button = QPushButton("Go")
        self.go_button.clicked.connect(self.load_url)

        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.go_back)
        self.forward_button = QPushButton("Forward")
        self.forward_button.clicked.connect(self.go_forward)
        self.reload_button = QPushButton("Reload")
        self.reload_button.clicked.connect(self.reload_page)

        self.new_tab_button = QPushButton("New Tab")
        self.new_tab_button.clicked.connect(lambda: self.add_new_tab("https://www.google.com", "New Tab"))

        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        self.tab_widget.currentChanged.connect(self.tab_changed)
        self.tab_widget.tabBarDoubleClicked.connect(lambda index: self.add_new_tab("https://www.google.com", "New Tab"))

        self.add_new_tab("https://www.google.com", "New Tab")

        url_bar_layout = QHBoxLayout()
        url_bar_layout.addWidget(self.url_bar)
        url_bar_layout.addWidget(self.go_button)
        url_bar_layout.addWidget(self.new_tab_button)

        mainribbon_layout = QHBoxLayout()
        mainribbon_layout.addWidget(self.back_button)
        mainribbon_layout.addWidget(self.reload_button)
        mainribbon_layout.addWidget(self.forward_button)
        mainribbon_layout.addLayout(url_bar_layout)

        ribbon_layout = QVBoxLayout()
        ribbon_layout.addLayout(mainribbon_layout)

        main_layout = QVBoxLayout()
        main_layout.addLayout(ribbon_layout)
        main_layout.addWidget(self.tab_widget)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self.installEventFilter(self)

    def add_new_tab(self, url, label):
        browser = QWebEngineView()
        browser.setUrl(QUrl(url))
        browser.titleChanged.connect(lambda title, browser=browser: self.update_tab_title(browser, title))
        browser.page().createWindow = self.handle_new_window
        index = self.tab_widget.addTab(browser, label)
        self.tab_widget.setCurrentIndex(index)

    def handle_new_window(self, _type):
        new_browser = QWebEngineView()
        new_browser.titleChanged.connect(lambda title, browser=new_browser: self.update_tab_title(browser, title))
        new_browser.page().createWindow = self.handle_new_window
        index = self.tab_widget.addTab(new_browser, "New Tab")
        self.tab_widget.setCurrentIndex(index)
        return new_browser.page()

    def update_tab_title(self, browser, title):
        index = self.tab_widget.indexOf(browser)
        if index != -1:
            self.tab_widget.setTabText(index, title)

    def close_tab(self, index):
        if self.tab_widget.count() > 1:
            self.tab_widget.removeTab(index)

    def tab_changed(self, index):
        current_browser = self.current_browser()
        if current_browser:
            self.url_bar.setText(current_browser.url().toString())

    def current_browser(self):
        return self.tab_widget.currentWidget()

    def load_url(self):
        url = self.url_bar.text().strip()
        self.controller.load_url(self.current_browser(), url)

    def reload_page(self):
        self.controller.reload_page(self.current_browser())

    def go_back(self):
        self.controller.go_back(self.current_browser())

    def go_forward(self):
        self.controller.go_forward(self.current_browser())

    def eventFilter(self, source, event):
        if event.type() == QEvent.KeyPress:
            if (event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_R):
                self.reload_page()
                return True
            elif (event.modifiers() == Qt.AltModifier and event.key() == Qt.Key_A):
                self.go_back()
                return True
            elif (event.modifiers() == Qt.AltModifier and event.key() == Qt.Key_D):
                self.go_forward()
                return True
            elif (event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_T):
                self.add_new_tab("https://www.google.com", "New Tab")
                return True
        elif event.type() == QEvent.MouseButtonPress:
            if event.button() == Qt.BackButton:
                print("Back button pressed")
                self.go_back()
                return True
            elif event.button() == Qt.ForwardButton:
                print("Forward button pressed")
                self.go_forward()
                return True
        return super().eventFilter(source, event)
