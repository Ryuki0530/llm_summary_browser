from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout,QWidget, QLineEdit, QPushButton, QSplitter, QTextEdit
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import Qt, QUrl, QEvent
from PyQt5.QtGui import QKeySequence
from core.browser_controller import BrowserController
"""
メインウィンドウのUI設計とレイアウト管理
"""
class MainWindow(QMainWindow):
    def __init__ (self):
        super().__init__()
        # メインウィンドウの初期化
        self.setWindowTitle("LLM Summary Browser")
        self.setGeometry(100, 100, 1200, 800)

        # アイコンの設定(未定)
        # self.setWindowIcon(QIcon("icon.png"))

        self.controller = BrowserController()

        # URL関連
        # URL入力バーの追加
        self.url_bar = QLineEdit()
        # URL入力バーのボタン
        self.go_button = QPushButton("Go")
        self.go_button.clicked.connect(self.load_url)

        # 戻る・進む・リロードボタン
        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.go_back)
        self.forward_button = QPushButton("Forward")
        self.forward_button.clicked.connect(self.go_forward)
        self.reload_button = QPushButton("Reload")
        self.reload_button.clicked.connect(self.reload_page)

        
        
        # WEBエンジンビューの追加
        self.browser_view = QWebEngineView()
        self.browser_view.setUrl(QUrl("https://www.google.com"))

        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.addWidget(self.browser_view)
        self.splitter.setSizes([800, 400])

        #リボンのレイアウト
        url_bar_layout = QHBoxLayout()
        url_bar_layout.addWidget(self.url_bar)
        url_bar_layout.addWidget(self.go_button)
        
        mainribbon_layout = QHBoxLayout()
        mainribbon_layout.addWidget(self.back_button)
        mainribbon_layout.addWidget(self.reload_button)
        mainribbon_layout.addWidget(self.forward_button)
        mainribbon_layout.addLayout(url_bar_layout)
        
        ribbon_layout = QVBoxLayout()
        ribbon_layout.addLayout(mainribbon_layout)
        
        # 全体レイアウト
        main_layout = QVBoxLayout()
        main_layout.addLayout(ribbon_layout)
        main_layout.addWidget(self.splitter)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # ショートカットキー
        self.shortcut_reload = QKeySequence("Ctrl+R")
        self.shortcut_back = QKeySequence("Alt+A")
        self.shortcut_forward = QKeySequence("Alt+D")
        self.installEventFilter(self)
        


    # 各種の操作メソッド
    def load_url(self):
        url = self.url_bar.text().strip()
        self.controller.load_url(self.browser_view, url)

    def reload_page(self):
        self.controller.reload_page(self.browser_view)

    def go_back(self):
        self.controller.go_back(self.browser_view)
    
    def go_forward(self):
        self.controller.go_forward(self.browser_view)


    # イベントフィルター
    def eventFilter(self, source, event):
        # キーボードショートカット処理
        if event.type() == QEvent.KeyPress:
            if event.matches(QKeySequence.Refresh) or (event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_R):
                self.reload_page()
                return True
        
            elif event.matches(QKeySequence.Back) or (event.modifiers() == Qt.AltModifier and event.key() == Qt.Key_A):
                self.go_back()
                return True
            
            elif event.matches(QKeySequence.Forward) or (event.modifiers() == Qt.AltModifier and event.key() == Qt.Key_D):
                self.go_forward()
                return True
        
        # マウスボタン処理
        elif event.type() == QEvent.MouseButtonPress:
            if event.button() == Qt.BackButton:  # マウスの戻るボタン
                print("Back button pressed")
                self.go_back()
                return True
            elif event.button() == Qt.ForwardButton:  # マウスの進むボタン
                print("Forward button pressed")
                self.go_forward()
                return True
        
        return super().eventFilter(source, event)