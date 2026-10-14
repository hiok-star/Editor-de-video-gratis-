"""Main application window."""
from __future__ import annotations
from PySide6.QtCore import Qt, QSettings, QTimer
from PySide6.QtGui import QAction, QKeySequence, QIcon
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QSplitter,
    QFileDialog, QMessageBox, QDockWidget, QMenuBar, QStatusBar,
    QToolBar, QLabel, QApplication
)

from core.models import Timeline, Track, Clip, MediaType, TimeCode
from render.engine import RenderEngine, RenderSettings
from ui.timeline import TimelineWidget
from ui.preview import PreviewWidget, PropertyPanel


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Video Editor - PySide6 + PyAV")
        self.resize(1600, 900)

        # Core
        self.timeline = Timeline(fps=30, width=1920, height=1080)
        self.render_settings = RenderSettings(fps=30, width=1920, height=1080)
        self.render_engine = RenderEngine(self.render_settings)

        # Add default tracks
        self.timeline.add_track(MediaType.VIDEO, "Video 1")
        self.timeline.add_track(MediaType.VIDEO, "Video 2")
        self.timeline.add_track(MediaType.AUDIO, "Audio 1")

        self.setup_ui()
        self.setup_menu()
        self.setup_shortcuts()
        self.load_settings()

        # Auto-update timeline duration
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.timeline.update_duration)
        self.update_timer.start(1000)

    def setup_ui(self):
        # Central widget with splitter
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Main horizontal splitter: preview (left) | properties (right)
        main_splitter = QSplitter(Qt.Horizontal)

        # Left side: preview + timeline (vertical splitter)
        left_splitter = QSplitter(Qt.Vertical)

        # Preview
        self.preview = PreviewWidget(self.timeline, self.render_engine)
        self.preview.frame_changed.connect(self.on_preview_frame_changed)
        left_splitter.addWidget(self.preview)

        # Timeline
        self.timeline_widget = TimelineWidget(self.timeline)
        self.timeline_widget.view.frame_changed.connect(self.on_timeline_frame_changed)
        self.timeline_widget.view.clip_selected.connect(self.on_clip_selected)
        self.timeline_widget.view.clip_double_clicked.connect(self.on_clip_double_clicked)
        left_splitter.addWidget(self.timeline_widget)

        left_splitter.setSizes([450, 400])
        main_splitter.addWidget(left_splitter)

        # Right side: Properties panel (dockable)
        self.properties = PropertyPanel()
        props_dock = QDockWidget("Properties", self)
        props_dock.setWidget(self.properties)
        props_dock.setAllowedAreas(Qt.RightDockWidgetArea | Qt.LeftDockWidgetArea)
        self.addDockWidget(Qt.RightDockWidgetArea, props_dock)

        layout.addWidget(main_splitter)

        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.lbl_fps = QLabel("FPS: 30")
        self.lbl_resolution = QLabel("1920x1080")
        self.lbl_duration = QLabel("Duration: 00:00:00:00")
        self.status_bar.addPermanentWidget(self.lbl_fps)
        self.status_bar.addPermanentWidget(self.lbl_resolution)
        self.status_bar.addPermanentWidget(self.lbl_duration)

    def setup_menu(self):
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("&File")

        act_new = QAction("&New Project", self)
        act_new.setShortcut(QKeySequence.New)
        act_new.triggered.connect(self.new_project)
        file_menu.addAction(act_new)

        act_open = QAction("&Open Project...", self)
        act_open.setShortcut(QKeySequence.Open)
        act_open.triggered.connect(self.open_project)
        file_menu.addAction(act_open)

        act_save = QAction("&Save Project", self)
        act_save.setShortcut(QKeySequence.Save)
        act_save.triggered.connect(self.save_project)
        file_menu.addAction(act_save)

        act_save_as = QAction("Save &As...", self)
        act_save_as.setShortcut(QKeySequence.SaveAs)
        act_save_as.triggered.connect(self.save_project_as)
        file_menu.addAction(act_save_as)

        file_menu.addSeparator()

        act_import = QAction("&Import Media...", self)
        act_import.setShortcut(QKeySequence("Ctrl+I"))
        act_import.triggered.connect(self.import_media)
        file_menu.addAction(act_import)

        file_menu.addSeparator()

        act_export = QAction("&Export Video...", self)
        act_export.setShortcut(QKeySequence("Ctrl+E"))
        act_export.triggered.connect(self.export_video)
        file_menu.addAction(act_export)

        file_menu.addSeparator()

        act_quit = QAction("&Quit", self)
        act_quit.setShortcut(QKeySequence.Quit)
        act_quit.triggered.connect(self.close)
        file_menu.addAction(act_quit)

        # Edit menu
        edit_menu = menubar.addMenu("&Edit")

        act_undo = QAction("&Undo", self)
        act_undo.setShortcut(QKeySequence.Undo)
        edit_menu.addAction(act_undo)

        act_redo = QAction("&Redo", self)
        act_redo.setShortcut(QKeySequence.Redo)
        edit_menu.addAction(act_redo)

        edit_menu.addSeparator()

        act_cut = QAction("Cu&t", self)
        act_cut.setShortcut(QKeySequence.Cut)
        edit_menu.addAction(act_cut)

        act_copy = QAction("&Copy", self)
        act_copy.setShortcut(QKeySequence.Copy)
        edit_menu.addAction(act_copy)

        act_paste = QAction("&Paste", self)
        act_paste.setShortcut(QKeySequence.Paste)
        edit_menu.addAction(act_paste)

        # View menu
        view_menu = menubar.addMenu("&View")

        act_fullscreen = QAction("&Fullscreen Preview", self)
        act_fullscreen.setShortcut(QKeySequence("Ctrl+`"))
        act_fullscreen.triggered.connect(self.toggle_fullscreen_preview)
        view_menu.addAction(act_fullscreen)

        # Track menu
        track_menu = menubar.addMenu("&Track")

        act_add_video = QAction("Add &Video Track", self)
        act_add_video.triggered.connect(lambda: self.add_track(MediaType.VIDEO))
        track_menu.addAction(act_add_video)

        act_add_audio = QAction("Add &Audio Track", self)
        act_add_audio.triggered.connect(lambda: self.add_track(MediaType.AUDIO))
        track_menu.addAction(act_add_audio)

        # Tools menu
        tools_menu = menubar.addMenu("&Tools")

        act_render_settings = QAction("&Render Settings...", self)
        act_render_settings.triggered.connect(self.show_render_settings)
        tools_menu.addAction(act_render_settings)

    def setup_shortcuts(self):
        # Space = play/pause
        from PySide6.QtGui import QShortcut
        QShortcut(QKeySequence(Qt.Key_Space), self, self.preview.toggle_play)
        # Left/Right = frame step
        QShortcut(QKeySequence(Qt.Key_Left), self, self.preview.prev_frame)
        QShortcut(QKeySequence(Qt.Key_Right), self, self.preview.next_frame)
        # Delete = delete selected clip
        QShortcut(QKeySequence(Qt.Key_Delete), self, self.delete_selected_clip)

    def on_preview_frame_changed(self, tc: TimeCode):
        self.timeline_widget.view.set_playhead(tc.frames)
        self.lbl_duration.setText(f"Duration: {self.timeline.duration}")

    def on_timeline_frame_changed(self, tc: TimeCode):
        self.preview.seek(tc.frames)

    def on_clip_selected(self, clip: Clip):
        self.properties.set_clip(clip)
        self.status_bar.showMessage(f"Selected: {clip.name}")

    def on_clip_double_clicked(self, clip: Clip):
        # Open effect editor or keyframe editor
        self.status_bar.showMessage(f"Edit clip: {clip.name}")

    def add_track(self, media_type: MediaType):
        track = self.timeline.add_track(media_type)
        self.timeline_widget.view._build_tracks()
        self.status_bar.showMessage(f"Added {media_type.value} track: {track.name}")

    def delete_selected_clip(self):
        # TODO: implement
        pass

    def new_project(self):
        self.timeline = Timeline(fps=30, width=1920, height=1080)
        self.timeline.add_track(MediaType.VIDEO, "Video 1")
        self.timeline.add_track(MediaType.VIDEO, "Video 2")
        self.timeline.add_track(MediaType.AUDIO, "Audio 1")
        self.timeline_widget.timeline = self.timeline
        self.timeline_widget.view.timeline = self.timeline
        self.timeline_widget.view._build_tracks()
        self.preview.timeline = self.timeline
        self.preview.slider.setRange(0, self.timeline.duration.frames)
        self.status_bar.showMessage("New project created")

    def open_project(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open Project", "", "Video Editor Project (*.vep)")
        if path:
            self.status_bar.showMessage(f"Opened: {path}")
            # TODO: implement project loading

    def save_project(self):
        self.status_bar.showMessage("Project saved")
        # TODO: implement project saving

    def save_project_as(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save Project As", "", "Video Editor Project (*.vep)")
        if path:
            self.status_bar.showMessage(f"Saved: {path}")

    def import_media(self):
        paths, _ = QFileDialog.getOpenFileNames(
            self, "Import Media", "",
            "Video Files (*.mp4 *.mov *.avi *.mkv);;Audio Files (*.wav *.mp3 *.aac);;Image Files (*.png *.jpg *.jpeg);;All Files (*)"
        )
        for path in paths:
            self.add_media_to_timeline(path)

    def add_media_to_timeline(self, path: str):
        # Simple import - add to first video track at end
        from core.models import Clip, MediaType, TimeCode
        import os

        ext = os.path.splitext(path)[1].lower()
        if ext in ['.mp4', '.mov', '.avi', '.mkv']:
            media_type = MediaType.VIDEO
        elif ext in ['.wav', '.mp3', '.aac', '.flac']:
            media_type = MediaType.AUDIO
        elif ext in ['.png', '.jpg', '.jpeg', '.bmp', '.tiff']:
            media_type = MediaType.IMAGE
        else:
            media_type = MediaType.VIDEO

        clip = Clip(
            name=os.path.basename(path),
            media_path=path,
            media_type=media_type,
            timeline_in=self.timeline.duration
        )

        # Find first compatible track
        for track in self.timeline.tracks:
            if track.type == media_type:
                track.add_clip(clip)
                break
        else:
            # Create new track
            track = self.timeline.add_track(media_type)
            track.add_clip(clip)

        self.timeline.update_duration()
        self.timeline_widget.view._build_tracks()
        self.preview.slider.setRange(0, self.timeline.duration.frames)
        self.status_bar.showMessage(f"Imported: {clip.name}")

    def export_video(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "Export Video", "",
            "MKV (*.mkv);;MP4 (*.mp4);;MOV (*.mov);;AVI (*.avi);;All Files (*)"
        )
        if path:
            self.status_bar.showMessage("Exporting...")
            QApplication.processEvents()
            try:
                self.render_engine.export(self.timeline, path, self._export_progress)
                self.status_bar.showMessage(f"Exported: {path}")
                QMessageBox.information(self, "Export Complete", f"Video exported to:\n{path}")
            except Exception as e:
                self.status_bar.showMessage(f"Export failed: {e}")
                QMessageBox.critical(self, "Export Failed", str(e))

    def _export_progress(self, progress: float):
        self.status_bar.showMessage(f"Exporting: {int(progress * 100)}%")
        QApplication.processEvents()

    def show_render_settings(self):
        from PySide6.QtWidgets import QDialog, QFormLayout, QSpinBox, QDoubleSpinBox, QComboBox, QDialogButtonBox, QCheckBox

        dialog = QDialog(self)
        dialog.setWindowTitle("Render Settings")
        layout = QFormLayout(dialog)

        fps = QDoubleSpinBox()
        fps.setRange(1, 120)
        fps.setValue(self.render_settings.fps)
        layout.addRow("FPS:", fps)

        width = QSpinBox()
        width.setRange(128, 7680)
        width.setValue(self.render_settings.width)
        layout.addRow("Width:", width)

        height = QSpinBox()
        height.setRange(128, 4320)
        height.setValue(self.render_settings.height)
        layout.addRow("Height:", height)

        codec = QComboBox()
        codec.addItems(["libx264", "libx265", "libvpx-vp9", "mpeg4"])
        codec.setCurrentText(self.render_settings.codec)
        layout.addRow("Codec:", codec)

        crf = QSpinBox()
        crf.setRange(0, 51)
        crf.setValue(self.render_settings.crf)
        layout.addRow("CRF (quality):", crf)

        preset = QComboBox()
        preset.addItems(["ultrafast", "superfast", "veryfast", "faster", "fast", "medium", "slow", "slower", "veryslow"])
        preset.setCurrentText(self.render_settings.preset)
        layout.addRow("Preset:", preset)

        hw_accel = QComboBox()
        hw_accel.addItems(["None", "d3d11va", "cuda", "qsv", "dxva2"])
        if self.render_settings.hw_accel:
            hw_accel.setCurrentText(self.render_settings.hw_accel)
        layout.addRow("HW Accel:", hw_accel)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addRow(buttons)

        if dialog.exec() == QDialog.Accepted:
            self.render_settings.fps = fps.value()
            self.render_settings.width = width.value()
            self.render_settings.height = height.value()
            self.render_settings.codec = codec.currentText()
            self.render_settings.crf = crf.value()
            self.render_settings.preset = preset.currentText()
            self.render_settings.hw_accel = hw_accel.currentText() if hw_accel.currentText() != "None" else None
            self.render_engine = RenderEngine(self.render_settings)
            self.preview.render_engine = self.render_engine
            self.status_bar.showMessage("Render settings updated")

    def toggle_fullscreen_preview(self):
        # TODO: implement fullscreen preview
        pass

    def load_settings(self):
        settings = QSettings("VideoEditor", "VideoEditor")
        geometry = settings.value("geometry")
        if geometry:
            self.restoreGeometry(geometry)
        state = settings.value("windowState")
        if state:
            self.restoreState(state)

    def save_settings(self):
        settings = QSettings("VideoEditor", "VideoEditor")
        settings.setValue("geometry", self.saveGeometry())
        settings.setValue("windowState", self.saveState())

    def closeEvent(self, event):
        self.save_settings()
        super().closeEvent(event)


def main():
    from PySide6.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    # Dark theme
    from PySide6.QtGui import QPalette, QColor
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(30, 30, 30))
    palette.setColor(QPalette.WindowText, QColor(220, 220, 220))
    palette.setColor(QPalette.Base, QColor(20, 20, 20))
    palette.setColor(QPalette.AlternateBase, QColor(35, 35, 35))
    palette.setColor(QPalette.ToolTipBase, QColor(30, 30, 30))
    palette.setColor(QPalette.ToolTipText, QColor(220, 220, 220))
    palette.setColor(QPalette.Text, QColor(220, 220, 220))
    palette.setColor(QPalette.Button, QColor(40, 40, 40))
    palette.setColor(QPalette.ButtonText, QColor(220, 220, 220))
    palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
    palette.setColor(QPalette.Link, QColor(100, 180, 255))
    palette.setColor(QPalette.Highlight, QColor(60, 120, 180))
    palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
    app.setPalette(palette)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()