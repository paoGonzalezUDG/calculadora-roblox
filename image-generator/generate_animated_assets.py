from PyQt6.QtWidgets import QWidget, QLabel
from PyQt6.QtGui import QPainter, QColor, QBrush, QPen, QFont, QPainterPath, QPixmap, QLinearGradient, QMovie
from PyQt6.QtCore import Qt, QPointF, QRectF, QSize
from PyQt6.QtGui import QTextOption

class MissionMapWidget(QWidget):
    """
    Un widget que muestra un mapa de progreso con GIFs animados para los niveles.
    """
    def __init__(self, reward_manager):
        super().__init__()
        self.reward_manager = reward_manager
        self.setObjectName("MissionMapWidget")

        # Cargar imágenes estáticas
        self.player_icon = self._load_pixmap("assets/images/pig_head.png", 40)
        self.background_texture = self._load_pixmap("assets/images/mission_map_background.png")
        self.tree_pixmap = self._load_pixmap("assets/images/mission_map_tree.png")

        # Cargar personajes
        self.mob_pixmaps = {
            "cow1": self._load_pixmap("assets/images/map_cow1.png", 80),
            "cow2": self._load_pixmap("assets/images/map_cow2.png", 80),
            "zombie1": self._load_pixmap("assets/images/map_zombie1.png", 60),
            "zombie2": self._load_pixmap("assets/images/map_zombie2.png", 60),
            "pig_king": self._load_pixmap("assets/images/map_pig_king.png", 80),
            "chicken1": self._load_pixmap("assets/images/map_chicken1.png", 50),
            "tnt": self._load_pixmap("assets/images/map_tnt.png", 50)
        }

        self.level_positions = []
        self.tree_positions = []
        self.mob_positions = []

        self.tree_relative_positions = [(0.15, 0.1), (0.7, 0.05), (0.2, 0.5), (0.75, 0.7), (0.1, 0.85)]
        self.mob_relative_positions = [
            ("cow1", (0.05, 0.65)), ("cow2", (0.7, 0.85)), ("zombie1", (0.8, 0.15)),
            ("zombie2", (0.1, 0.3)), ("pig_king", (0.65, 0.35)), ("chicken1", (0.1, 0.45)),
            ("tnt", (0.8, 0.6))
        ]

        self.num_levels = 15
        self._setup_animated_labels()

    def _setup_animated_labels(self):
        """Crea las etiquetas que contendrán los GIFs animados de los niveles."""
        self.locked_level_labels = []
        self.completed_level_labels = []

        for _ in range(self.num_levels):
            # Etiquetas para candados
            lock_label = QLabel(self)
            lock_label.setStyleSheet("background: transparent;")
            lock_movie = QMovie("assets/images/level_dot_locked.gif")
            lock_movie.setScaledSize(QSize(30, 30))
            lock_label.setMovie(lock_movie)
            lock_movie.start()
            lock_label.hide()
            self.locked_level_labels.append(lock_label)

            # Etiquetas para niveles completados
            dot_label = QLabel(self)
            dot_label.setStyleSheet("background: transparent;")
            dot_movie = QMovie("assets/images/level_dot.gif")
            dot_movie.setScaledSize(QSize(35, 35))
            dot_label.setMovie(dot_movie)
            dot_movie.start()
            dot_label.hide()
            self.completed_level_labels.append(dot_label)


    def _load_pixmap(self, path, size=0):
        pixmap = QPixmap(path)
        if pixmap.isNull():
            print(f"Advertencia: No se pudo cargar la imagen en '{path}'")
            return QPixmap()
        if size > 0:
            return pixmap.scaled(size, size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        return pixmap

    def _update_positions_and_visibility(self):
        """Calcula todas las posiciones y actualiza la visibilidad de los elementos."""
        w, h = self.width(), self.height()
        self.level_positions = self._generate_level_positions(w, h)
        self.tree_positions = self._generate_static_positions(self.tree_relative_positions, w, h)
        self.mob_positions = self._generate_static_positions(self.mob_relative_positions, w, h, self.mob_pixmaps)

        missions_completed = self.reward_manager.get_missions_completed()
        current_level = missions_completed // 3

        for i in range(self.num_levels):
            if i < len(self.level_positions):
                pos = self.level_positions[i]

                # Nivel completado
                if i < current_level:
                    label = self.completed_level_labels[i]
                    label_size = label.movie().scaledSize()
                    label.move(int(pos.x() - label_size.width() / 2), int(pos.y() - label_size.height() / 2))
                    label.show()
                    self.locked_level_labels[i].hide()
                # Nivel bloqueado
                elif i > current_level:
                    label = self.locked_level_labels[i]
                    label_size = label.movie().scaledSize()
                    label.move(int(pos.x() - label_size.width() / 2), int(pos.y() - label_size.height() / 2))
                    label.show()
                    self.completed_level_labels[i].hide()
                # Nivel actual (se dibuja el ícono del jugador, así que se ocultan ambos)
                else:
                    self.completed_level_labels[i].hide()
                    self.locked_level_labels[i].hide()

        self.update()

    def _generate_level_positions(self, w, h):
        positions = []
        margin_x, margin_y = w * 0.3, h * 0.1
        path_width, path_height = w - (2 * margin_x), h - (2 * margin_y)

        for i in range(self.num_levels):
            progress = i / (self.num_levels - 1)
            x_variation = path_width / 2 * (1 + 0.8 * ((i % 4) / 2 - 1) * (-1 if (i // 2) % 2 == 0 else 1))
            x = margin_x + x_variation
            y = margin_y + (progress * path_height)
            positions.append(QPointF(x, y))
        return positions

    def _generate_static_positions(self, relative_positions, w, h, pixmap_dict=None):
        positions = []
        pixmap_source = self.tree_pixmap if not pixmap_dict else None

        for item in relative_positions:
            name_or_pos, rel_pos = (None, item) if not pixmap_dict else item
            pixmap = pixmap_dict.get(name_or_pos) if pixmap_dict else pixmap_source

            if pixmap and not pixmap.isNull():
                x = w * rel_pos[0]
                y = h * rel_pos[1]
                positions.append((pixmap, QPointF(x, y)))
        return positions

    def resizeEvent(self, event):
        self._update_positions_and_visibility()

    def update_map(self):
        self._update_positions_and_visibility()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Fondo
        if not self.background_texture.isNull():
            painter.drawTiledPixmap(self.rect(), self.background_texture)
        else:
            painter.fillRect(self.rect(), QColor("#5D9C59"))

        # Escenario
        all_static_items = self.mob_positions + self.tree_positions
        all_static_items.sort(key=lambda item: item[1].y() + item[0].height())
        for pixmap, pos in all_static_items:
            painter.drawPixmap(pos, pixmap)

        # Camino
        path = QPainterPath()
        if self.level_positions:
            path.moveTo(self.level_positions[0])
            for i in range(len(self.level_positions) - 1):
                p1, p2 = self.level_positions[i], self.level_positions[i+1]
                ctrl_p1 = QPointF((p1.x() + p2.x()) / 2, p1.y())
                ctrl_p2 = QPointF((p1.x() + p2.x()) / 2, p2.y())
                path.cubicTo(ctrl_p1, ctrl_p2, p2)
        pen = QPen(QColor("#D2B48C"), 10, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin)
        painter.strokePath(path, pen)

        # Números de nivel y jugador actual
        missions_completed = self.reward_manager.get_missions_completed()
        current_level = missions_completed // 3
        for i, pos in enumerate(self.level_positions):
            # Dibuja el número para los niveles completados
            if i < current_level:
                painter.setPen(QColor("white"))
                painter.setFont(QFont("Gill Sans Ultra Bold", 10))
                painter.drawText(QRectF(pos.x() - 15, pos.y() - 15, 30, 30), str(i + 1), QTextOption(Qt.AlignmentFlag.AlignCenter))
            # Dibuja el ícono del jugador en el nivel actual
            elif i == current_level:
                if not self.player_icon.isNull():
                    painter.drawPixmap(int(pos.x() - self.player_icon.width() / 2), int(pos.y() - self.player_icon.height() / 2), self.player_icon)

