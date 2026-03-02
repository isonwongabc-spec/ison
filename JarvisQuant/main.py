# Jarvis Quant Trader v1.0
# Professional Crypto Trading Desktop Application

from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtCharts import *
import sys
import json
import os
from datetime import datetime
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))
from trading.okx_trader import OKXTrader

class TradingThread(QThread):
    """Background trading thread"""
    signal_update = pyqtSignal(dict)
    signal_trade = pyqtSignal(dict)
    signal_alert = pyqtSignal(str)
    
    def __init__(self, trader, config):
        super().__init__()
        self.trader = trader
        self.config = config
        self.running = True
        self.daily_pnl = 0
        
    def run(self):
        while self.running:
            try:
                # Check ETH and BTC
                for symbol in ['ETH-USDT-SWAP', 'BTC-USDT-SWAP']:
                    ticker = self.trader.get_ticker(symbol)
                    if ticker.get('data'):
                        price = float(ticker['data'][0]['last'])
                        self.signal_update.emit({
                            'symbol': symbol,
                            'price': price,
                            'timestamp': datetime.now().isoformat()
                        })
                
                self.sleep(5)  # Update every 5 seconds
            except Exception as e:
                self.signal_alert.emit(f"Error: {str(e)}")
                self.sleep(5)
    
    def stop(self):
        self.running = False

class PriceChart(QChartView):
    """Real-time price chart"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.chart = QChart()
        self.chart.setTitle("ETH/USDT Price")
        self.chart.setAnimationOptions(QChart.AnimationType.NoAnimation)
        
        self.series = QLineSeries()
        self.series.setName("Price")
        
        self.chart.addSeries(self.series)
        
        self.axis_x = QDateTimeAxis()
        self.axis_x.setFormat("HH:mm:ss")
        self.chart.addAxis(self.axis_x, Qt.AlignmentFlag.AlignBottom)
        self.series.attachAxis(self.axis_x)
        
        self.axis_y = QValueAxis()
        self.chart.addAxis(self.axis_y, Qt.AlignmentFlag.AlignLeft)
        self.series.attachAxis(self.axis_y)
        
        self.setChart(self.chart)
        self.price_data = []
        
    def update_price(self, price):
        now = QDateTime.currentDateTime()
        self.series.append(now.toMSecsSinceEpoch(), price)
        
        # Keep last 100 points
        if self.series.count() > 100:
            self.series.remove(0)
        
        self.axis_x.setRange(
            QDateTime.fromMSecsSinceEpoch(int(self.series.at(0).x())),
            QDateTime.fromMSecsSinceEpoch(int(self.series.at(self.series.count()-1).x()))
        )
        
        min_price = min([self.series.at(i).y() for i in range(self.series.count())])
        max_price = max([self.series.at(i).y() for i in range(self.series.count())])
        self.axis_y.setRange(min_price * 0.999, max_price * 1.001)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Jarvis Quant Trader v1.0")
        self.setGeometry(100, 100, 1400, 900)
        
        # Initialize trader
        self.trader = OKXTrader(
            api_key='112e3b78-387e-4df7-95ee-4f92f15d7d69',
            api_secret='4BF0777097F46740226B055B896D2CB1',
            passphrase='Abc32421.'
        )
        
        self.config = {
            'symbols': ['ETH-USDT-SWAP', 'BTC-USDT-SWAP'],
            'auto_trading': False,
            'max_position': 20,
            'leverage': 3
        }
        
        self.init_ui()
        self.start_trading_thread()
        
    def init_ui(self):
        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        layout = QHBoxLayout(central)
        
        # Left panel - Controls
        left_panel = self.create_left_panel()
        layout.addWidget(left_panel, 1)
        
        # Middle panel - Chart
        middle_panel = self.create_middle_panel()
        layout.addWidget(middle_panel, 3)
        
        # Right panel - Positions & Logs
        right_panel = self.create_right_panel()
        layout.addWidget(right_panel, 1)
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready - Connected to OKX")
        
    def create_left_panel(self):
        panel = QGroupBox("Trading Controls")
        layout = QVBoxLayout()
        
        # Account Info
        account_group = QGroupBox("Account")
        account_layout = QFormLayout()
        self.lbl_balance = QLabel("Loading...")
        self.lbl_available = QLabel("Loading...")
        account_layout.addRow("Total Balance:", self.lbl_balance)
        account_layout.addRow("Available:", self.lbl_available)
        account_group.setLayout(account_layout)
        layout.addWidget(account_group)
        
        # Auto Trading
        auto_group = QGroupBox("Auto Trading")
        auto_layout = QVBoxLayout()
        
        self.btn_auto = QPushButton("Start Auto Trading")
        self.btn_auto.setCheckable(True)
        self.btn_auto.setStyleSheet("""
            QPushButton:checked {
                background-color: #ff4444;
                color: white;
            }
            QPushButton {
                background-color: #44ff44;
                color: black;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
            }
        """)
        self.btn_auto.clicked.connect(self.toggle_auto_trading)
        auto_layout.addWidget(self.btn_auto)
        
        self.chk_eth = QCheckBox("Trade ETH")
        self.chk_eth.setChecked(True)
        self.chk_btc = QCheckBox("Trade BTC")
        self.chk_btc.setChecked(True)
        auto_layout.addWidget(self.chk_eth)
        auto_layout.addWidget(self.chk_btc)
        
        auto_group.setLayout(auto_layout)
        layout.addWidget(auto_group)
        
        # Manual Trading
        manual_group = QGroupBox("Manual Trading")
        manual_layout = QFormLayout()
        
        self.cmb_symbol = QComboBox()
        self.cmb_symbol.addItems(["ETH-USDT-SWAP", "BTC-USDT-SWAP"])
        manual_layout.addRow("Symbol:", self.cmb_symbol)
        
        self.cmb_side = QComboBox()
        self.cmb_side.addItems(["Buy (Long)", "Sell (Short)"])
        manual_layout.addRow("Side:", self.cmb_side)
        
        self.spn_size = QDoubleSpinBox()
        self.spn_size.setRange(0.01, 100)
        self.spn_size.setValue(0.01)
        self.spn_size.setDecimals(2)
        manual_layout.addRow("Size:", self.spn_size)
        
        self.spn_leverage = QSpinBox()
        self.spn_leverage.setRange(1, 10)
        self.spn_leverage.setValue(3)
        manual_layout.addRow("Leverage:", self.spn_leverage)
        
        btn_manual = QPushButton("Place Order")
        btn_manual.setStyleSheet("""
            QPushButton {
                background-color: #4488ff;
                color: white;
                padding: 10px;
                font-weight: bold;
            }
        """)
        btn_manual.clicked.connect(self.place_manual_order)
        manual_layout.addRow(btn_manual)
        
        btn_close = QPushButton("Close All Positions")
        btn_close.setStyleSheet("""
            QPushButton {
                background-color: #ff4444;
                color: white;
                padding: 10px;
                font-weight: bold;
            }
        """)
        btn_close.clicked.connect(self.close_all_positions)
        manual_layout.addRow(btn_close)
        
        manual_group.setLayout(manual_layout)
        layout.addWidget(manual_group)
        
        # Risk Settings
        risk_group = QGroupBox("Risk Settings")
        risk_layout = QFormLayout()
        
        self.spn_stop_loss = QDoubleSpinBox()
        self.spn_stop_loss.setRange(0.1, 10)
        self.spn_stop_loss.setValue(2)
        self.spn_stop_loss.setSuffix(" %")
        risk_layout.addRow("Stop Loss:", self.spn_stop_loss)
        
        self.spn_take_profit = QDoubleSpinBox()
        self.spn_take_profit.setRange(0.5, 50)
        self.spn_take_profit.setValue(6)
        self.spn_take_profit.setSuffix(" %")
        risk_layout.addRow("Take Profit:", self.spn_take_profit)
        
        risk_group.setLayout(risk_layout)
        layout.addWidget(risk_group)
        
        layout.addStretch()
        
        panel.setLayout(layout)
        panel.setMaximumWidth(350)
        return panel
        
    def create_middle_panel(self):
        panel = QWidget()
        layout = QVBoxLayout()
        
        # Price display
        price_widget = QWidget()
        price_layout = QHBoxLayout()
        
        self.lbl_eth_price = QLabel("ETH: $--.--")
        self.lbl_eth_price.setStyleSheet("font-size: 24px; font-weight: bold; color: #00aa00;")
        price_layout.addWidget(self.lbl_eth_price)
        
        self.lbl_btc_price = QLabel("BTC: $--.--")
        self.lbl_btc_price.setStyleSheet("font-size: 24px; font-weight: bold; color: #00aa00;")
        price_layout.addWidget(self.lbl_btc_price)
        
        price_layout.addStretch()
        price_widget.setLayout(price_layout)
        layout.addWidget(price_widget)
        
        # Chart
        self.chart = PriceChart()
        layout.addWidget(self.chart)
        
        panel.setLayout(layout)
        return panel
        
    def create_right_panel(self):
        panel = QWidget()
        layout = QVBoxLayout()
        
        # Positions
        pos_group = QGroupBox("Open Positions")
        pos_layout = QVBoxLayout()
        
        self.tbl_positions = QTableWidget()
        self.tbl_positions.setColumnCount(5)
        self.tbl_positions.setHorizontalHeaderLabels(["Symbol", "Side", "Size", "Entry", "PnL"])
        self.tbl_positions.horizontalHeader().setStretchLastSection(True)
        pos_layout.addWidget(self.tbl_positions)
        
        self.lbl_total_pnl = QLabel("Total Unrealized PnL: $0.00")
        self.lbl_total_pnl.setStyleSheet("font-size: 16px; font-weight: bold;")
        pos_layout.addWidget(self.lbl_total_pnl)
        
        pos_group.setLayout(pos_layout)
        layout.addWidget(pos_group)
        
        # Trading Log
        log_group = QGroupBox("Trading Log")
        log_layout = QVBoxLayout()
        
        self.txt_log = QTextEdit()
        self.txt_log.setReadOnly(True)
        self.txt_log.setMaximumBlockCount(1000)
        log_layout.addWidget(self.txt_log)
        
        log_group.setLayout(log_layout)
        layout.addWidget(log_group)
        
        panel.setLayout(layout)
        panel.setMaximumWidth(400)
        return panel
        
    def start_trading_thread(self):
        self.trading_thread = TradingThread(self.trader, self.config)
        self.trading_thread.signal_update.connect(self.on_price_update)
        self.trading_thread.signal_alert.connect(self.on_alert)
        self.trading_thread.start()
        
        # Timer for UI updates
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_account_info)
        self.update_timer.start(5000)  # Every 5 seconds
        
    def on_price_update(self, data):
        symbol = data['symbol']
        price = data['price']
        
        if 'ETH' in symbol:
            self.lbl_eth_price.setText(f"ETH: ${price:,.2f}")
            self.chart.update_price(price)
        elif 'BTC' in symbol:
            self.lbl_btc_price.setText(f"BTC: ${price:,.2f}")
            
    def on_alert(self, message):
        self.log_message(message)
        
    def update_account_info(self):
        try:
            # Update balance
            balance = self.trader.get_balance()
            if balance.get('data') and balance['data'][0].get('details'):
                for detail in balance['data'][0]['details']:
                    if detail.get('ccy') == 'USDT':
                        eq = float(detail.get('eq', 0))
                        avail = float(detail.get('availBal', 0))
                        self.lbl_balance.setText(f"${eq:.2f}")
                        self.lbl_available.setText(f"${avail:.2f}")
                        break
            
            # Update positions
            positions = self.trader.get_positions()
            self.tbl_positions.setRowCount(0)
            total_pnl = 0
            
            if positions.get('data'):
                row = 0
                for pos in positions['data']:
                    if float(pos.get('pos', 0)) != 0:
                        self.tbl_positions.insertRow(row)
                        self.tbl_positions.setItem(row, 0, QTableWidgetItem(pos.get('instId', '')))
                        side = 'LONG' if float(pos['pos']) > 0 else 'SHORT'
                        self.tbl_positions.setItem(row, 1, QTableWidgetItem(side))
                        self.tbl_positions.setItem(row, 2, QTableWidgetItem(str(abs(float(pos['pos'])))))
                        self.tbl_positions.setItem(row, 3, QTableWidgetItem(f"${float(pos.get('avgPx', 0)):.2f}"))
                        upl = float(pos.get('upl', 0))
                        total_pnl += upl
                        pnl_item = QTableWidgetItem(f"${upl:.4f}")
                        if upl >= 0:
                            pnl_item.setForeground(QBrush(QColor("green")))
                        else:
                            pnl_item.setForeground(QBrush(QColor("red")))
                        self.tbl_positions.setItem(row, 4, pnl_item)
                        row += 1
                        
            self.lbl_total_pnl.setText(f"Total Unrealized PnL: ${total_pnl:.4f}")
            if total_pnl >= 0:
                self.lbl_total_pnl.setStyleSheet("font-size: 16px; font-weight: bold; color: green;")
            else:
                self.lbl_total_pnl.setStyleSheet("font-size: 16px; font-weight: bold; color: red;")
                
        except Exception as e:
            self.log_message(f"Error updating account: {e}")
            
    def toggle_auto_trading(self):
        if self.btn_auto.isChecked():
            self.config['auto_trading'] = True
            self.btn_auto.setText("Stop Auto Trading")
            self.log_message("Auto trading STARTED")
            self.status_bar.showMessage("Auto Trading: ON")
        else:
            self.config['auto_trading'] = False
            self.btn_auto.setText("Start Auto Trading")
            self.log_message("Auto trading STOPPED")
            self.status_bar.showMessage("Auto Trading: OFF")
            
    def place_manual_order(self):
        symbol = self.cmb_symbol.currentText()
        side_text = self.cmb_side.currentText()
        side = 'buy' if 'Buy' in side_text else 'sell'
        pos_side = 'long' if 'Buy' in side_text else 'short'
        size = self.spn_size.value()
        
        try:
            self.log_message(f"Placing manual order: {side.upper()} {size} {symbol}")
            result = self.trader.place_order(symbol, side, pos_side, size)
            
            if result.get('code') == '0':
                self.log_message(f"Order placed successfully!")
                QMessageBox.information(self, "Success", f"Order placed: {side.upper()} {size} {symbol}")
            else:
                error_msg = result.get('msg', 'Unknown error')
                self.log_message(f"Order failed: {error_msg}")
                QMessageBox.warning(self, "Error", f"Order failed: {error_msg}")
        except Exception as e:
            self.log_message(f"Error placing order: {e}")
            QMessageBox.critical(self, "Error", str(e))
            
    def close_all_positions(self):
        reply = QMessageBox.question(self, 'Confirm', 
                                   'Close all positions?',
                                   QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.log_message("Closing all positions...")
                for symbol in self.config['symbols']:
                    result = self.trader.close_position(symbol)
                    if result.get('code') == '0':
                        self.log_message(f"Closed {symbol}")
                self.log_message("All positions closed")
                QMessageBox.information(self, "Done", "All positions closed")
            except Exception as e:
                self.log_message(f"Error closing positions: {e}")
                QMessageBox.critical(self, "Error", str(e))
                
    def log_message(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.txt_log.append(f"[{timestamp}] {message}")
        
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Confirm Exit',
                                   'Stop trading and exit?',
                                   QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            self.trading_thread.stop()
            self.trading_thread.wait()
            event.accept()
        else:
            event.ignore()

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    # Dark theme
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(30, 30, 30))
    palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
    palette.setColor(QPalette.ColorRole.Base, QColor(40, 40, 40))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(50, 50, 50))
    palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
    palette.setColor(QPalette.ColorRole.Button, QColor(50, 50, 50))
    palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
    app.setPalette(palette)
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
