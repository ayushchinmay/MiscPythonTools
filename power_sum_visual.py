"""
#		AUTHOR      :   Ayush Chinmay
#		DATE CREATED:   12 Aug 2025
#		
#		DESCRIPTION : A PyQt6 application for visualizing power sum combinations with interactive plotting.
#                       - This application computes and visualizes unique combinations of power sums.
#                       - For a given power (2, 3, 4, or 5) and maximum sum threshold, it finds all unique
#                       - unordered pairs (a,b) where a^power + b^power <= max_sum, then plots the 
#                       - count of combinations for each sum value up to the threshold.
#		
#       INSTALLATION:
#                       - pip install PyQt6 matplotlib numpy
#		
#		? CHANGELOG ?
#			* [12 Aug 2025] - Application initial creation.
#			* [15 Aug 2025] - Implemented interactive plotting functionality.
#			* [20 Aug 2025] - Optimized computation engine performance.
#			* [22 Aug 2025] - Added export functionality for PNG and CSV.
#		
#		
#		! TODO !
#			- [x] Enhance progress bar update mechanism. (Achieved)
#			- [-] Add comprehensive unit tests.
#			- [x] Improve UI styling and layout. (Achieved)
"""

import sys
import csv
from typing import Dict, List, Tuple, Optional
from collections import defaultdict
from dataclasses import dataclass

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QRadioButton, QButtonGroup, QLineEdit, QLabel, QPushButton,
    QCheckBox, QTextEdit, QSplitter, QGroupBox, QMessageBox,
    QFileDialog, QProgressBar
)
from PyQt6.QtCore import (
    QThread, QObject, pyqtSignal, QRunnable, QThreadPool,
    Qt, QTimer
)
from PyQt6.QtGui import QFont, QIntValidator

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.patches as patches
import numpy as np


@dataclass
class ComputationResult:
    """Data class for computation results."""
    power: int
    max_num: int
    sum_combinations: Dict[int, List[Tuple[int, int]]]
    computation_time: float


class ComputationEngine(QObject):
    """Performs power sum calculations in a separate thread."""
    
    finished = pyqtSignal(object)  # ComputationResult
    error = pyqtSignal(str)
    progress = pyqtSignal(int, int)  # current, total
    
    def __init__(self):
        super().__init__()
        self.should_stop = False
    
    def stop_computation(self):
        """Signal to stop the current computation."""
        self.should_stop = True
    
    def compute_power_sums(self, power: int, max_sum: int):
        """
        Compute unique unordered pairs for power sums up to max_sum threshold.
        
        Args:
            power: The power to raise numbers to (2, 3, 4, or 5)
            max_sum: Maximum sum value threshold (positive integer)
        """
        try:
            import time
            start_time = time.time()
            
            self.should_stop = False
            sum_combinations = defaultdict(list)
            
            # Calculate reasonable upper bound for iteration
            # We need a^power + b^power <= max_sum, so maximum a or b is approximately max_sum^(1/power)
            max_individual = int(max_sum ** (1.0 / power)) + 1
            total_pairs = (max_individual * (max_individual + 1)) // 2
            current_pair = 0
            
            # Iterate through unique unordered pairs
            for a in range(1, max_individual + 1):
                if self.should_stop:
                    return
                
                a_power = a ** power
                if a_power > max_sum:  # Early termination if a^power alone exceeds max_sum
                    break
                
                for b in range(a, max_individual + 1):  # b >= a for unordered pairs
                    if self.should_stop:
                        return
                    
                    b_power = b ** power
                    power_sum = a_power + b_power
                    
                    # Only include pairs where sum <= max_sum
                    if power_sum <= max_sum:
                        sum_combinations[power_sum].append((a, b))
                    elif b == a:  # If a == b and sum exceeds max_sum, no need to check larger b
                        break
                    
                    current_pair += 1
                    if current_pair % 1000 == 0:  # Update progress every 1000 pairs
                        self.progress.emit(current_pair, total_pairs)
            
            computation_time = time.time() - start_time
            result = ComputationResult(
                power=power,
                max_num=max_sum,  # Store as max_num for compatibility
                sum_combinations=dict(sum_combinations),
                computation_time=computation_time
            )
            
            self.finished.emit(result)
            
        except Exception as e:
            self.error.emit(f"Computation error: {str(e)}")


class PlotWidget(QWidget):
    """Interactive matplotlib plotting widget."""
    
    point_clicked = pyqtSignal(int, int, list)  # sum_value, count, pairs
    
    def __init__(self):
        super().__init__()
        self.figure = Figure(figsize=(10, 6))
        self.canvas = FigureCanvas(self.figure)
        self.axes = self.figure.add_subplot(111)
        
        layout = QVBoxLayout(self)
        layout.addWidget(self.canvas)
        
        # Connect click event
        self.canvas.mpl_connect('button_press_event', self._on_click)
        
        # Store current data for click detection
        self.current_data: Optional[ComputationResult] = None
        self.current_style = "scatter"
        self.show_annotations = False
        
        self._setup_initial_plot()
    
    def _setup_initial_plot(self):
        """Setup initial empty plot."""
        self.axes.clear()
        self.axes.set_xlabel("Sum Value")
        self.axes.set_ylabel("Number of Combinations")
        self.axes.set_title("Power Sum Combinations")
        self.axes.grid(True, alpha=0.3)
        self.canvas.draw()
    
    def show_placeholder(self):
        """Show placeholder message during computation."""
        self.axes.clear()
        self.axes.text(0.5, 0.5, "Please wait while the computation is completed",
                      ha='center', va='center', transform=self.axes.transAxes,
                      fontsize=14, bbox=dict(boxstyle="round,pad=0.3", 
                                           facecolor="lightblue", alpha=0.7))
        self.axes.set_xlim(0, 1)
        self.axes.set_ylim(0, 1)
        self.canvas.draw()
    
    def update_plot(self, result: ComputationResult, style: str = "scatter", 
                   show_annotations: bool = False):
        """
        Update the plot with new computation results.
        
        Args:
            result: ComputationResult object
            style: Plot style ('scatter', 'line', 'bar')
            show_annotations: Whether to show point annotations
        """
        self.current_data = result
        self.current_style = style
        self.show_annotations = show_annotations
        
        # Prepare data
        sums = sorted(result.sum_combinations.keys())
        counts = [len(result.sum_combinations[s]) for s in sums]
        
        # Clear and setup axes
        self.axes.clear()
        
        # Create plot based on style
        if style == "scatter":
            scatter = self.axes.scatter(sums, counts, alpha=0.7, s=50, 
                                      c='blue', picker=True)
        elif style == "line":
            self.axes.plot(sums, counts, 'b-o', alpha=0.7, markersize=4,
                          picker=True, pickradius=10)
        elif style == "bar":
            self.axes.bar(sums, counts, alpha=0.7, color='blue', 
                         picker=True, width=max(1, (max(sums) - min(sums)) / len(sums) * 0.8))
        
        # Add annotations if requested
        if show_annotations and len(sums) <= 50:  # Limit annotations for readability
            for i, (sum_val, count) in enumerate(zip(sums, counts)):
                self.axes.annotate(f'({sum_val},{count})', 
                                 (sum_val, count),
                                 xytext=(5, 5), textcoords='offset points',
                                 fontsize=8, alpha=0.8)
        
        # Setup axes
        self.axes.set_xlabel("Sum Value")
        self.axes.set_ylabel("Number of Combinations")
        self.axes.set_title(f"Power {result.power} Sum Combinations (Max Sum: {result.max_num})")
        self.axes.grid(True, alpha=0.3)
        
        # Ensure proper scaling
        if sums and counts:
            x_margin = (max(sums) - min(sums)) * 0.05
            y_margin = max(counts) * 0.05
            self.axes.set_xlim(min(sums) - x_margin, max(sums) + x_margin)
            self.axes.set_ylim(0, max(counts) + y_margin)
        
        self.canvas.draw()
    
    def _on_click(self, event):
        """Handle mouse click events on the plot."""
        if event.inaxes != self.axes or self.current_data is None:
            return
        
        # Find closest point
        sums = sorted(self.current_data.sum_combinations.keys())
        counts = [len(self.current_data.sum_combinations[s]) for s in sums]
        
        if not sums:
            return
        
        # Calculate distances to all points
        distances = []
        for i, (sum_val, count) in enumerate(zip(sums, counts)):
            # Transform to display coordinates for accurate distance calculation
            x_display = self.axes.transData.transform([(sum_val, 0)])[0][0]
            y_display = self.axes.transData.transform([(0, count)])[0][1]
            event_x = self.axes.transData.transform([(event.xdata, 0)])[0][0]
            event_y = self.axes.transData.transform([(0, event.ydata)])[0][1]
            
            dist = ((x_display - event_x) ** 2 + (y_display - event_y) ** 2) ** 0.5
            distances.append((dist, i))
        
        # Find closest point within reasonable distance (50 pixels)
        min_dist, closest_idx = min(distances)
        if min_dist <= 50:
            sum_val = sums[closest_idx]
            count = counts[closest_idx]
            pairs = self.current_data.sum_combinations[sum_val]
            self.point_clicked.emit(sum_val, count, pairs)
    
    def export_png(self, filename: str):
        """Export current plot as PNG."""
        try:
            self.figure.savefig(filename, dpi=300, bbox_inches='tight')
            return True
        except Exception as e:
            QMessageBox.warning(self, "Export Error", f"Failed to export PNG: {str(e)}")
            return False


class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mathematical Visualization System")
        self.setGeometry(100, 100, 1400, 800)
        
        # Thread management
        self.computation_thread: Optional[QThread] = None
        self.computation_engine: Optional[ComputationEngine] = None
        
        # Current results
        self.current_result: Optional[ComputationResult] = None
        
        self._setup_ui()
        self._connect_signals()
    
    def _setup_ui(self):
        """Setup the main user interface."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout(central_widget)
        
        # Left panel for controls
        left_panel = self._create_control_panel()
        
        # Right panel with plot and info
        right_panel = self._create_plot_panel()
        
        # Splitter to allow resizing
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([300, 1100])
        
        main_layout.addWidget(splitter)
    
    def _create_control_panel(self) -> QWidget:
        """Create the left control panel."""
        panel = QWidget()
        panel.setMaximumWidth(350)
        layout = QVBoxLayout(panel)
        
        # Power selection
        power_group = QGroupBox("Power Selection")
        power_layout = QVBoxLayout(power_group)
        
        self.power_group = QButtonGroup()
        self.power_buttons = {}
        for power in [2, 3, 4, 5]:
            radio = QRadioButton(f"Power {power}")
            self.power_buttons[power] = radio
            self.power_group.addButton(radio, power)
            power_layout.addWidget(radio)
        
        self.power_buttons[2].setChecked(True)  # Default to power 2
        layout.addWidget(power_group)
        
        # Maximum sum threshold input
        max_sum_group = QGroupBox("Maximum Sum Threshold")
        max_sum_layout = QVBoxLayout(max_sum_group)
        
        self.max_sum_input = QLineEdit("1000")
        self.max_sum_input.setValidator(QIntValidator(1, 999999))
        max_sum_layout.addWidget(QLabel("Max sum value threshold:"))
        max_sum_layout.addWidget(self.max_sum_input)
        layout.addWidget(max_sum_group)
        
        # Chart style selection
        style_group = QGroupBox("Chart Style")
        style_layout = QVBoxLayout(style_group)
        
        self.style_group = QButtonGroup()
        self.style_buttons = {}
        for style in ["scatter", "line", "bar"]:
            radio = QRadioButton(style.capitalize())
            self.style_buttons[style] = radio
            self.style_group.addButton(radio)
            style_layout.addWidget(radio)
        
        self.style_buttons["scatter"].setChecked(True)  # Default to scatter
        layout.addWidget(style_group)
        
        # Options
        options_group = QGroupBox("Display Options")
        options_layout = QVBoxLayout(options_group)
        
        self.annotation_checkbox = QCheckBox("Show annotations")
        options_layout.addWidget(self.annotation_checkbox)
        layout.addWidget(options_group)
        
        # Control buttons
        buttons_group = QGroupBox("Controls")
        buttons_layout = QVBoxLayout(buttons_group)
        
        self.apply_button = QPushButton("Apply")
        self.stop_button = QPushButton("Stop")
        self.stop_button.setEnabled(False)
        
        buttons_layout.addWidget(self.apply_button)
        buttons_layout.addWidget(self.stop_button)
        layout.addWidget(buttons_group)
        
        # Export buttons
        export_group = QGroupBox("Export")
        export_layout = QVBoxLayout(export_group)
        
        self.export_png_button = QPushButton("Export PNG")
        self.export_csv_button = QPushButton("Export CSV")
        
        export_layout.addWidget(self.export_png_button)
        export_layout.addWidget(self.export_csv_button)
        layout.addWidget(export_group)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # Quit button
        self.quit_button = QPushButton("Quit")
        layout.addWidget(self.quit_button)
        
        layout.addStretch()
        return panel
    
    def _create_plot_panel(self) -> QWidget:
        """Create the right panel with plot and info."""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # Plot widget
        self.plot_widget = PlotWidget()
        
        # Info panel
        info_group = QGroupBox("Point Information")
        info_layout = QVBoxLayout(info_group)
        
        self.info_text = QTextEdit()
        self.info_text.setMaximumHeight(150)
        self.info_text.setReadOnly(True)
        self.info_text.setPlainText("Select a point for more info")
        
        info_layout.addWidget(self.info_text)
        
        # Use splitter for plot and info
        plot_splitter = QSplitter(Qt.Orientation.Vertical)
        plot_splitter.addWidget(self.plot_widget)
        plot_splitter.addWidget(info_group)
        plot_splitter.setSizes([600, 150])
        
        layout.addWidget(plot_splitter)
        return panel
    
    def _connect_signals(self):
        """Connect all UI signals to their handlers."""
        # Buttons
        self.apply_button.clicked.connect(self._on_apply)
        self.stop_button.clicked.connect(self._on_stop)
        self.quit_button.clicked.connect(self.close)
        self.export_png_button.clicked.connect(self._on_export_png)
        self.export_csv_button.clicked.connect(self._on_export_csv)
        
        # Style changes
        for button in self.style_buttons.values():
            button.toggled.connect(self._on_style_change)
        
        # Annotation toggle
        self.annotation_checkbox.toggled.connect(self._on_annotation_change)
        
        # Plot interactions
        self.plot_widget.point_clicked.connect(self._on_point_clicked)
    
    def _get_selected_power(self) -> int:
        """Get the currently selected power."""
        return self.power_group.checkedId()
    
    def _get_selected_style(self) -> str:
        """Get the currently selected chart style."""
        for style, button in self.style_buttons.items():
            if button.isChecked():
                return style
        return "scatter"
    
    def _validate_max_sum(self) -> Optional[int]:
        """Validate and return the maximum sum threshold input."""
        try:
            max_sum = int(self.max_sum_input.text())
            if max_sum <= 0:
                QMessageBox.warning(self, "Invalid Input", 
                                  "Maximum sum threshold must be positive.")
                return None
            if max_sum > 100000:
                reply = QMessageBox.question(
                    self, "Large Computation",
                    f"Computing with max sum {max_sum} may take a long time. Continue?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                )
                if reply != QMessageBox.StandardButton.Yes:
                    return None
            return max_sum
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", 
                              "Please enter a valid positive integer.")
            return None
    
    def _on_apply(self):
        """Handle apply button click."""
        # Validate input
        max_sum = self._validate_max_sum()
        if max_sum is None:
            return
        
        power = self._get_selected_power()
        
        # Setup computation
        self._start_computation(power, max_sum)
    
    def _start_computation(self, power: int, max_sum: int):
        """Start computation in a separate thread."""
        # Disable controls during computation
        self.apply_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        
        # Show placeholder
        self.plot_widget.show_placeholder()
        self.info_text.setPlainText("Computing...")
        
        # Create and start computation thread
        self.computation_thread = QThread()
        self.computation_engine = ComputationEngine()
        self.computation_engine.moveToThread(self.computation_thread)
        
        # Connect signals
        self.computation_engine.finished.connect(self._on_computation_finished)
        self.computation_engine.error.connect(self._on_computation_error)
        self.computation_engine.progress.connect(self._on_progress_update)
        
        self.computation_thread.started.connect(
            lambda: self.computation_engine.compute_power_sums(power, max_sum)
        )
        
        # Start thread
        self.computation_thread.start()
    
    def _on_stop(self):
        """Handle stop button click."""
        if self.computation_engine:
            self.computation_engine.stop_computation()
        self._cleanup_computation()
    
    def _on_computation_finished(self, result: ComputationResult):
        """Handle successful computation completion."""
        self.current_result = result
        self._update_plot_display()
        self._cleanup_computation()
        
        # Show completion message
        self.info_text.setPlainText(
            f"Computation completed in {result.computation_time:.2f} seconds.\n"
            f"Found {len(result.sum_combinations)} unique sums.\n"
            f"Select a point for more info."
        )
    
    def _on_computation_error(self, error_msg: str):
        """Handle computation error."""
        QMessageBox.critical(self, "Computation Error", error_msg)
        self._cleanup_computation()
        self.plot_widget._setup_initial_plot()
        self.info_text.setPlainText("Select a point for more info")
    
    def _on_progress_update(self, current: int, total: int):
        """Update progress bar."""
        if total > 0:
            progress = int((current / total) * 100)
            self.progress_bar.setValue(progress)
    
    def _cleanup_computation(self):
        """Clean up computation thread and restore UI."""
        if self.computation_thread and self.computation_thread.isRunning():
            self.computation_thread.quit()
            self.computation_thread.wait()
        
        self.computation_thread = None
        self.computation_engine = None
        
        # Re-enable controls
        self.apply_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.progress_bar.setVisible(False)
    
    def _update_plot_display(self):
        """Update plot with current settings."""
        if self.current_result is None:
            return
        
        style = self._get_selected_style()
        show_annotations = self.annotation_checkbox.isChecked()
        
        self.plot_widget.update_plot(
            self.current_result, style, show_annotations
        )
    
    def _on_style_change(self):
        """Handle chart style change."""
        self._update_plot_display()
    
    def _on_annotation_change(self):
        """Handle annotation toggle change."""
        self._update_plot_display()
    
    def _on_point_clicked(self, sum_value: int, count: int, pairs: List[Tuple[int, int]]):
        """Handle plot point click."""
        if not self.current_result:
            return
        
        # Format pairs for display
        power = self.current_result.power
        pairs_text = []
        for a, b in pairs:
            if a == b:
                pairs_text.append(f"2 × ({a})^{power} = {sum_value}")
            else:
                pairs_text.append(f"({a})^{power} + ({b})^{power} = {sum_value}")
        
        # Limit display for very long lists
        if len(pairs_text) > 20:
            displayed_pairs = pairs_text[:20]
            displayed_pairs.append(f"... and {len(pairs_text) - 20} more")
        else:
            displayed_pairs = pairs_text
        
        info_text = (
            f"Selected Sum: {sum_value}\n"
            f"Number of Combinations: {count}\n\n"
            f"Combinations:\n" + "\n".join(displayed_pairs)
        )
        
        self.info_text.setPlainText(info_text)
    
    def _on_export_png(self):
        """Handle PNG export."""
        if self.current_result is None:
            QMessageBox.warning(self, "No Data", "No computation results to export.")
            return
        
        filename, _ = QFileDialog.getSaveFileName(
            self, "Export PNG", f"power_{self.current_result.power}_visualization.png",
            "PNG files (*.png)"
        )
        
        if filename:
            if self.plot_widget.export_png(filename):
                QMessageBox.information(self, "Export Successful", 
                                      f"Plot exported to {filename}")
    
    def _on_export_csv(self):
        """Handle CSV export."""
        if self.current_result is None:
            QMessageBox.warning(self, "No Data", "No computation results to export.")
            return
        
        filename, _ = QFileDialog.getSaveFileName(
            self, "Export CSV", f"power_{self.current_result.power}_data.csv",
            "CSV files (*.csv)"
        )
        
        if filename:
            try:
                with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(['Sum', 'Count', 'Pairs'])
                    
                    for sum_val in sorted(self.current_result.sum_combinations.keys()):
                        pairs = self.current_result.sum_combinations[sum_val]
                        count = len(pairs)
                        pairs_str = '; '.join([f"({a},{b})" for a, b in pairs])
                        writer.writerow([sum_val, count, pairs_str])
                
                QMessageBox.information(self, "Export Successful", 
                                      f"Data exported to {filename}")
            except Exception as e:
                QMessageBox.critical(self, "Export Error", 
                                   f"Failed to export CSV: {str(e)}")
    
    def closeEvent(self, event):
        """Handle application close."""
        if self.computation_thread and self.computation_thread.isRunning():
            reply = QMessageBox.question(
                self, "Computation Running",
                "A computation is still running. Stop it and quit?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                self._on_stop()
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()


def main():
    """Main application entry point."""
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Modern look
    
    # Set application font
    font = QFont()
    font.setPointSize(9)
    app.setFont(font)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()