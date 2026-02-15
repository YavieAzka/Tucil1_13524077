import sys
import os
import subprocess
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QSpinBox, 
                             QMessageBox, QTableWidget, QTableWidgetItem,
                             QHeaderView, QDialog, QScrollArea)
from PyQt6.QtGui import QColor, QFont, QBrush
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFileDialog

class IterationViewerDialog(QDialog):
    def __init__(self, iteration_file, grid_size, colors, grid_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Viewer Iterasi")
        self.setGeometry(150, 150, 900, 700)
        
        self.grid_size = grid_size
        self.colors = colors
        self.grid_data = grid_data
        self.iterations = []
        
        self.load_iterations(iteration_file)
        self.init_ui()
    
    def load_iterations(self, filepath):
        if not os.path.exists(filepath):
            return
        
        with open(filepath, 'r') as f:
            lines = f.read().splitlines()
        
        current_iteration = None
        current_board = []
        
        for line in lines:
            if line.startswith("---ITERATION"):
                if current_iteration is not None and current_board:
                    self.iterations.append({
                        'number': current_iteration,
                        'board': current_board
                    })
                
                try:
                    parts = line.split("ITERATION ")
                    if len(parts) >= 2:
                        number_part = parts[1].replace("---", "").strip()
                        current_iteration = int(number_part)
                    else:
                        current_iteration = None
                except (ValueError, IndexError):
                    current_iteration = None
                    
                current_board = []
                
            elif line.startswith("---END---"):
                continue
                
            elif line.strip() == "":
                continue
                
            else:
                current_board.append(line)
        
        if current_iteration is not None and current_board:
            self.iterations.append({
                'number': current_iteration,
                'board': current_board
            })
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        header = QLabel(f"<b>Total Iterasi Tercatat: {len(self.iterations)}</b>")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setFont(QFont("Arial", 12))
        layout.addWidget(header)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        
        for iter_data in self.iterations:
            iter_widget = self.create_iteration_widget(iter_data)
            scroll_layout.addWidget(iter_widget)
        
        scroll.setWidget(scroll_widget)
        layout.addWidget(scroll)
        
        btn_close = QPushButton("Tutup")
        btn_close.clicked.connect(self.close)
        layout.addWidget(btn_close)
    
    def create_iteration_widget(self, iter_data):
        widget = QWidget()
        widget.setStyleSheet("background-color: #f0f0f0; border: 1px solid #ccc; border-radius: 5px; padding: 10px;")
        layout = QVBoxLayout(widget)
        
        # Perbaikan: Tambahkan background gelap dan teks putih untuk header
        label = QLabel(f"<b>Iterasi #{iter_data['number']}</b>")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        label.setStyleSheet("""
            background-color: #2c3e50; 
            color: white; 
            padding: 8px; 
            border-radius: 5px;
            margin-bottom: 5px;
        """)
        layout.addWidget(label)
        
        table = QTableWidget()
        table.setRowCount(self.grid_size)
        table.setColumnCount(self.grid_size)
        table.horizontalHeader().setVisible(False)
        table.verticalHeader().setVisible(False)
        table.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        
        cell_size = 40
        for i in range(self.grid_size):
            table.setRowHeight(i, cell_size)
            table.setColumnWidth(i, cell_size)
        
        table.setFixedSize(self.grid_size * cell_size + 20, self.grid_size * cell_size + 20)
        
        for r, line in enumerate(iter_data['board']):
            if r >= self.grid_size:
                break
            for c, char in enumerate(line):
                if c >= self.grid_size:
                    break
                
                color_idx = self.grid_data[r][c]
                if color_idx == -1:
                    color = Qt.GlobalColor.white
                elif color_idx < len(self.colors):
                    color = self.colors[color_idx]
                else:
                    color = Qt.GlobalColor.white
                
                item = QTableWidgetItem()
                item.setBackground(QBrush(color))
                
                if char == '#':
                    item.setText("♛")
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    item.setFont(QFont("Segoe UI Symbol", 16, QFont.Weight.Bold))
                    item.setForeground(QBrush(Qt.GlobalColor.black))
                
                table.setItem(r, c, item)
        
        layout.addWidget(table, alignment=Qt.AlignmentFlag.AlignCenter)
        return widget

class QueensGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tucil 1 - Queens Solver")
        self.setGeometry(100, 100, 1100, 750)

        self.grid_size = 5
        self.colors = [
            QColor("#FF9999"), QColor("#99FF99"), QColor("#9999FF"), 
            QColor("#FFFF99"), QColor("#FF99FF"), QColor("#99FFFF"),
            QColor("#FFCC99"), QColor("#CCCCCC")
        ]
        self.current_color_idx = 0
        
        self.grid_data = [[-1 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.iteration_file = None

        self.init_ui()

    def init_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        header_layout = QHBoxLayout()
        
        lbl_size = QLabel("Ukuran Papan (N x N):")
        lbl_size.setFont(QFont("Arial", 11))
        self.spin_size = QSpinBox()
        self.spin_size.setRange(1, 20)
        self.spin_size.setValue(self.grid_size)
        self.spin_size.setFixedWidth(60)
        self.spin_size.setStyleSheet("font-size: 14px; padding: 5px;")
        
        btn_resize = QPushButton("Atur Ulang / Reset")
        btn_resize.setStyleSheet("padding: 5px 10px;")
        btn_resize.clicked.connect(self.resize_board)

        btn_load = QPushButton("Load dari TXT")
        btn_load.setStyleSheet("padding: 5px 10px;")
        btn_load.clicked.connect(self.load_from_txt)

        header_layout.addWidget(btn_load)
        header_layout.addWidget(lbl_size)
        header_layout.addWidget(self.spin_size)
        header_layout.addWidget(btn_resize)
        header_layout.addStretch()
        
        main_layout.addLayout(header_layout)

        boards_layout = QHBoxLayout()

        input_container = QVBoxLayout()
        lbl_input = QLabel("<b>Konfigurasi Input</b>")
        lbl_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_hint = QLabel("(Klik palet warna di bawah, lalu klik sel papan)")
        lbl_hint.setStyleSheet("color: gray; font-size: 10px;")
        lbl_hint.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.table_input = QTableWidget()
        self.setup_table(self.table_input, editable=True)
        self.table_input.cellClicked.connect(self.paint_cell)
        self.table_input.cellEntered.connect(self.paint_cell_drag)
        
        input_container.addWidget(lbl_input)
        input_container.addWidget(lbl_hint)
        input_container.addWidget(self.table_input)

        output_container = QVBoxLayout()
        lbl_output = QLabel("<b>Hasil Solusi</b>")
        lbl_output.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_info = QLabel("(Posisi Queens akan muncul di sini)")
        lbl_info.setStyleSheet("color: gray; font-size: 10px;")
        lbl_info.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.table_output = QTableWidget()
        self.setup_table(self.table_output, editable=False)

        output_container.addWidget(lbl_output)
        output_container.addWidget(lbl_info)
        output_container.addWidget(self.table_output)

        boards_layout.addLayout(input_container)
        boards_layout.addLayout(output_container)
        main_layout.addLayout(boards_layout)

        controls_frame = QHBoxLayout()
        
        palette_layout = QVBoxLayout()
        lbl_palette = QLabel("Palet Warna (Pilih salah satu):")
        self.color_buttons_layout = QHBoxLayout()
        self.refresh_color_buttons()
        
        btn_add_color = QPushButton("+ Warna Baru")
        btn_add_color.setFixedWidth(100)
        btn_add_color.clicked.connect(self.add_new_color)

        palette_layout.addWidget(lbl_palette)
        palette_layout.addLayout(self.color_buttons_layout)
        palette_layout.addWidget(btn_add_color)
        
        controls_frame.addLayout(palette_layout)
        controls_frame.addStretch()

        buttons_layout = QVBoxLayout()
        
        self.btn_solve = QPushButton("SOLVE")
        self.btn_solve.setFixedSize(150, 60)
        self.btn_solve.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        self.btn_solve.setStyleSheet("""
            QPushButton {
                background-color: #007BFF; 
                color: white; 
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        self.btn_solve.clicked.connect(self.run_process)
        
        self.btn_view_iterations = QPushButton("Lihat Iterasi")
        self.btn_view_iterations.setFixedSize(150, 40)
        self.btn_view_iterations.setFont(QFont("Arial", 11))
        self.btn_view_iterations.setStyleSheet("""
            QPushButton {
                background-color: #28a745; 
                color: white; 
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """)
        self.btn_view_iterations.clicked.connect(self.view_iterations)
        self.btn_view_iterations.setEnabled(False)
        
        buttons_layout.addWidget(self.btn_solve)
        buttons_layout.addWidget(self.btn_view_iterations)
        
        controls_frame.addLayout(buttons_layout)
        main_layout.addLayout(controls_frame)

        self.status_label = QLabel("Silakan warnai area pada papan input.")
        self.statusBar().addWidget(self.status_label)

        self.render_grid(self.table_input)
        self.render_grid(self.table_output)
        
        self.is_mouse_pressed = False
        self.table_input.setMouseTracking(True)

    def mousePressEvent(self, event):
        self.is_mouse_pressed = True
        super().mousePressEvent(event)
    
    def mouseReleaseEvent(self, event):
        self.is_mouse_pressed = False
        super().mouseReleaseEvent(event)

    def setup_table(self, table, editable):
        table.setRowCount(self.grid_size)
        table.setColumnCount(self.grid_size)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table.horizontalHeader().setVisible(False)
        table.verticalHeader().setVisible(False)
        table.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        table.setFocusPolicy(Qt.FocusPolicy.NoFocus)

    def resize_board(self):
        new_size = self.spin_size.value()
        self.grid_size = new_size
        self.grid_data = [[-1 for _ in range(new_size)] for _ in range(new_size)]
        
        self.setup_table(self.table_input, True)
        self.setup_table(self.table_output, False)
        self.render_grid(self.table_input)
        self.table_output.clearContents()
        self.status_label.setText("Papan di-reset. Silakan warnai ulang.")
        self.btn_view_iterations.setEnabled(False)

    def refresh_color_buttons(self):
        for i in reversed(range(self.color_buttons_layout.count())): 
            self.color_buttons_layout.itemAt(i).widget().setParent(None)

        for idx, color in enumerate(self.colors):
            btn = QPushButton(chr(65+idx))
            btn.setFixedSize(40, 40)
            border = "3px solid black" if idx == self.current_color_idx else "1px solid gray"
            btn.setStyleSheet(f"background-color: {color.name()}; border: {border}; font-weight: bold;")
            btn.clicked.connect(lambda checked, i=idx: self.select_color(i))
            self.color_buttons_layout.addWidget(btn)

    def add_new_color(self):
        import random
        r = lambda: random.randint(100, 255)
        self.colors.append(QColor(f"#{r():02x}{r():02x}{r():02x}"))
        self.refresh_color_buttons()

    def select_color(self, index):
        self.current_color_idx = index
        self.refresh_color_buttons()

    def paint_cell(self, row, col):
        self.grid_data[row][col] = self.current_color_idx
        self.render_single_cell(self.table_input, row, col, self.current_color_idx)

    def paint_cell_drag(self, row, col):
        if self.is_mouse_pressed:
            self.paint_cell(row, col)

    def render_grid(self, table):
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                self.render_single_cell(table, r, c, self.grid_data[r][c])

    def render_single_cell(self, table, r, c, color_idx):
        if color_idx == -1:
            color = Qt.GlobalColor.white
        elif color_idx < len(self.colors):
            color = self.colors[color_idx]
        else:
            color = Qt.GlobalColor.white

        item = table.item(r, c)
        if not item:
            item = QTableWidgetItem()
            table.setItem(r, c, item)
        
        item.setBackground(QBrush(color))
        if table == self.table_input: 
            item.setText("")

    def validate_regions(self):
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                if self.grid_data[r][c] == -1:
                    QMessageBox.warning(self, "Konfigurasi Tidak Lengkap", 
                                        "Semua kotak harus diwarnai!\nMasih ada kotak berwarna putih.")
                    return False

        region_cells = {}
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                cid = self.grid_data[r][c]
                if cid not in region_cells: region_cells[cid] = []
                region_cells[cid].append((r, c))

        for cid, cells in region_cells.items():
            if not cells: continue
            start = cells[0]
            queue = [start]
            visited = {start}
            count = 0
            
            while queue:
                curr_r, curr_c = queue.pop(0)
                count += 1
                for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
                    nr, nc = curr_r + dr, curr_c + dc
                    if (nr, nc) in cells and (nr, nc) not in visited:
                        visited.add((nr, nc))
                        queue.append((nr, nc))
            
            if count != len(cells):
                char_region = chr(65 + cid)
                QMessageBox.critical(self, "Region Invalid", 
                                     f"Region warna '{char_region}' terputus (tidak menyatu).\n"
                                     "Semua kotak dengan warna yang sama harus saling menempel (vertikal/horizontal).")
                return False

        return True

    def run_process(self):
        if not self.validate_regions():
            return

        input_path = os.path.join("test", "input.txt")
        output_path = os.path.join("test", "output.txt")
        self.iteration_file = os.path.join("test", "iterations.txt")
        os.makedirs("test", exist_ok=True)

        try:
            with open(input_path, "w") as f:
                for r in range(self.grid_size):
                    line = ""
                    for c in range(self.grid_size):
                        line += chr(65 + self.grid_data[r][c])
                    f.write(line + "\n")
        except Exception as e:
            QMessageBox.critical(self, "File Error", f"Gagal menulis input: {e}")
            return

        exe_path = os.path.join("bin", "solver.exe") if os.name == 'nt' else os.path.join("bin", "solver")
        
        if not os.path.exists(exe_path):
            QMessageBox.critical(self, "Executable Missing", 
                                 f"File solver tidak ditemukan di:\n{exe_path}\n\n"
                                 "Pastikan Anda sudah meng-compile kode C++.")
            return

        self.status_label.setText("Sedang mencari solusi...")
        self.btn_solve.setEnabled(False)
        self.btn_solve.setText("Thinking...")
        self.btn_view_iterations.setEnabled(False)
        QApplication.processEvents()

        try:
            subprocess.run([exe_path, input_path], check=True)
            self.read_output(output_path)
            self.btn_view_iterations.setEnabled(True)
        except subprocess.CalledProcessError:
            QMessageBox.critical(self, "Solver Error", "Program C++ mengalami crash.")
        except Exception as e:
            QMessageBox.critical(self, "System Error", str(e))
        finally:
            self.btn_solve.setEnabled(True)
            self.btn_solve.setText("SOLVE")
    
    def read_output(self, filepath):
        if not os.path.exists(filepath):
            return

        with open(filepath, "r") as f:
            lines = f.read().splitlines()

        if not lines: return

        self.table_output.clearContents()

        if lines[0] == "No Solution":
             QMessageBox.information(self, "Hasil", "Tidak ada solusi yang mungkin untuk konfigurasi ini.")
             self.status_label.setText("Selesai: Tidak ada solusi.")
             
             for r in range(self.grid_size):
                for c in range(self.grid_size):
                     self.render_single_cell(self.table_output, r, c, self.grid_data[r][c])
             return

        grid_lines = []
        meta_lines = []
        is_meta = False

        for line in lines:
            if line == "---META---":
                is_meta = True
                continue
            if is_meta:
                meta_lines.append(line)
            else:
                grid_lines.append(line)

        for r, line in enumerate(grid_lines):
            if r >= self.grid_size: break
            for c, char in enumerate(line):
                if c >= self.grid_size: break
                
                color_idx = self.grid_data[r][c]
                
                self.render_single_cell(self.table_output, r, c, color_idx)
                
                if char == '#':
                    item = self.table_output.item(r, c)
                    item.setText("♛")
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    item.setFont(QFont("Segoe UI Symbol", 20, QFont.Weight.Bold))
                    item.setForeground(QBrush(Qt.GlobalColor.black))

        msg = "Solusi Ditemukan!"
        if len(meta_lines) >= 2:
            time_ms = meta_lines[0]
            iterations = meta_lines[1]
            self.status_label.setText(f"Selesai: {time_ms} ms, {iterations} iterasi")
            msg += f"\n\nWaktu Eksekusi: {time_ms} ms\nJumlah Iterasi: {iterations}"
        
        QMessageBox.information(self, "Sukses", msg)

    def view_iterations(self):
        if not self.iteration_file or not os.path.exists(self.iteration_file):
            QMessageBox.warning(self, "File Tidak Ditemukan", 
                              "File iterasi tidak ditemukan.\nJalankan solver terlebih dahulu.")
            return
        
        dialog = IterationViewerDialog(self.iteration_file, self.grid_size, 
                                       self.colors, self.grid_data, self)
        dialog.exec()

    def load_from_txt(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Pilih File TXT", 
            "", 
            "Text Files (*.txt)"
        )

        if not file_path:
            return

        try:
            with open(file_path, "r") as f:
                lines = [line.strip() for line in f.readlines() if line.strip()]

            size = len(lines)
            if size == 0:
                raise ValueError("File kosong.")

            for line in lines:
                if len(line) != size:
                    raise ValueError("Papan harus berbentuk persegi (NxN).")

            unique_chars = sorted(set("".join(lines)))

            while len(self.colors) < len(unique_chars):
                self.add_new_color()

            char_to_index = {char: idx for idx, char in enumerate(unique_chars)}

            self.grid_size = size
            self.spin_size.setValue(size)

            self.grid_data = [
                [char_to_index[char] for char in line]
                for line in lines
            ]

            self.setup_table(self.table_input, True)
            self.setup_table(self.table_output, False)
            self.render_grid(self.table_input)
            self.table_output.clearContents()

            self.status_label.setText(f"Berhasil load file: {os.path.basename(file_path)}")
            self.btn_view_iterations.setEnabled(False)

        except Exception as e:
            QMessageBox.critical(self, "Error Load File", str(e))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QueensGUI()
    window.show()
    sys.exit(app.exec())