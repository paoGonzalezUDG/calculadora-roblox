from PyQt6.QtWidgets import QWidget, QLabel
from PyQt6.QtGui import QPainter, QColor, QPen, QFont, QPainterPath, QPixmap, QMovie, QTextOption
from PyQt6.QtCore import Qt, QPointF, QRectF, QSize

class MissionMapWidget(QWidget):
    """
    Un widget que muestra un mapa de progreso de misiones con fondo texturizado,
    personajes y animaciones.
    """
    def __init__(self, reward_manager, walking_sound=None):
        super().__init__()
        self.reward_manager = reward_manager
        self.setObjectName("MissionMapWidget")
        self.walking_sound = walking_sound
        self.sound_muted = False

        # Cargar imágenes estáticas y texturas
        self.background_texture = self._load_pixmap("assets/images/mission_map_background.png")
        self.tree_pixmap = self._load_pixmap("assets/images/mission_map_tree.png")

        # Personajes estáticos
        self.mob_pixmaps = {
            "cow2": self._load_pixmap("assets/images/map_cow2.png", 80),
            "zombie2": self._load_pixmap("assets/images/map_zombie2.png", 60),
            "pig_king": self._load_pixmap("assets/images/map_pig_king.png", 70),
            "tnt1": self._load_pixmap("assets/images/map_tnt.png", 50),
            "tnt2": self._load_pixmap("assets/images/map_tnt.png", 50), # Segundo TNT
        }

        # Posiciones relativas predefinidas
        self.tree_relative_positions = [
            (0.15, 0.1), (0.7, 0.02), (0.2, 0.5), (0.75, 0.7), (0.1, 0.85),
            (0.85, 0.9), (0.25, 0.0), (0.05, 0.4) # 3 árboles nuevos
        ]

        # Posiciones para personajes estáticos
        self.mob_relative_positions = [
            ("cow2", (0.7, 0.85)),
            ("zombie2", (0.1, 0.3)),
            ("pig_king", (0.65, 0.35)),
            ("tnt1", (0.8, 0.6)),
            ("tnt2", (0.5, 0.93)), # Segundo TNT
        ]

        # Definiciones para personajes animados
        self.animated_mob_definitions = [
            ("cow1", "assets/images/map_cow1.gif", QSize(120, 60), (0.05, 0.65)),
            ("zombie1", "assets/images/map_zombie1.gif", QSize(100, 90), (0.8, 0.20)),
            ("chicken1", "assets/images/map_chicken1.gif", QSize(50, 50), (0.85, 0.55)),
            ("villager1", "assets/images/map_villager.gif", QSize(40, 77), (0.3, 0.75)),
            ("villager2", "assets/images/map_villager.gif", QSize(40, 77), (0.2, 0.05)), # Segundo aldeano
        ]

        self.level_positions = []
        self._setup_animated_labels()

    def force_update(self):
        """Fuerza la actualización de las posiciones de los GIFs."""
        self._calculate_positions()
        self.update()

    def set_sound_muted(self, is_muted):
        self.sound_muted = is_muted

    def _on_player_frame_changed(self):
        if self.walking_sound and not self.sound_muted:
            if self.player_movie.currentFrameNumber() in [0, self.player_movie.frameCount() // 2]:
                self.walking_sound.play()

    def _load_pixmap(self, path, size=0):
        pixmap = QPixmap(path)
        if pixmap.isNull():
            print(f"Advertencia: No se pudo cargar la imagen en '{path}'")
            return QPixmap()
        if size > 0:
            return pixmap.scaled(size, size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        return pixmap

    def _setup_animated_labels(self):
        """Configura las etiquetas para TODOS los elementos animados del mapa."""
        self.locked_labels = []
        self.unlocked_labels = []
        self.animated_mob_labels = {}

        # Jugador
        self.player_label = QLabel(self)
        self.player_movie = QMovie("assets/images/player.gif")
        player_size = QSize(58, 67)
        self.player_movie.setScaledSize(player_size)
        self.player_label.setMovie(self.player_movie)
        self.player_label.setFixedSize(player_size)
        self.player_label.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.player_label.hide()
        self.player_movie.frameChanged.connect(self._on_player_frame_changed)
        self.player_movie.start()

        # Niveles Bloqueados y Desbloqueados
        self._create_level_dots()

        # Crear etiquetas para personajes animados
        for name, path, size, _ in self.animated_mob_definitions:
            label = QLabel(self)
            movie = QMovie(path)
            movie.setScaledSize(size)
            label.setMovie(movie)
            label.setFixedSize(size)
            label.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
            label.hide()
            movie.start()
            self.animated_mob_labels[name] = label

    def _create_level_dots(self):
        # Niveles Bloqueados
        self.locked_movie = QMovie("assets/images/level_dot_locked.gif")
        locked_size = QSize(30, 30)
        self.locked_movie.setScaledSize(locked_size)
        for _ in range(15):
            label = QLabel(self)
            label.setMovie(self.locked_movie)
            label.setFixedSize(locked_size)
            label.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
            label.hide()
            self.locked_labels.append(label)
        self.locked_movie.start()

        # Niveles Desbloqueados
        self.unlocked_movie = QMovie("assets/images/level_dot.gif")
        unlocked_size = QSize(33, 33)
        self.unlocked_movie.setScaledSize(unlocked_size)
        for _ in range(15):
            label = QLabel(self)
            label.setMovie(self.unlocked_movie)
            label.setFixedSize(unlocked_size)
            label.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
            label.hide()
            self.unlocked_labels.append(label)
        self.unlocked_movie.start()

    def _calculate_positions(self):
        """Calcula y actualiza todas las posiciones de los elementos del mapa."""
        w, h = self.width(), self.height()

        self.level_positions = self._generate_level_positions()
        self.tree_positions = [(self.tree_pixmap, QPointF(w * rx, h * ry)) for rx, ry in self.tree_relative_positions]

        # Mantiene los personajes estáticos que queden
        self.mob_positions = []
        for name, (rx, ry) in self.mob_relative_positions:
            pixmap = self.mob_pixmaps.get(name)
            if pixmap:
                self.mob_positions.append((pixmap, QPointF(w * rx, h * ry)))

        self.update_animated_labels()

    def update_animated_labels(self):
        """Actualiza la visibilidad y posición de TODOS los GIFs en el mapa."""
        if not self.level_positions:
            return

        w, h = self.width(), self.height()
        missions_completed = self.reward_manager.get_missions_completed()
        current_level = missions_completed // 3

        # Posicionar Niveles y Jugador
        for i, pos in enumerate(self.level_positions):
            if i == current_level:
                # Muestra al jugador en la posición actual
                self.player_label.move(int(pos.x() - self.player_label.width() / 2), int(pos.y() - self.player_label.height() / 2))
                self.player_label.show()
                # CORRECCIÓN: Oculta el candado y el punto de nivel en la posición del jugador
                self.locked_labels[i].hide()
                self.unlocked_labels[i].hide()
            elif i < current_level:
                # Muestra el punto de nivel completado
                self.unlocked_labels[i].move(int(pos.x() - self.unlocked_labels[i].width() / 2), int(pos.y() - self.unlocked_labels[i].height() / 2))
                self.unlocked_labels[i].show()
                self.locked_labels[i].hide()
            else:
                # Muestra el candado para niveles futuros
                self.locked_labels[i].move(int(pos.x() - self.locked_labels[i].width() / 2), int(pos.y() - self.locked_labels[i].height() / 2))
                self.locked_labels[i].show()
                self.unlocked_labels[i].hide()

        if current_level >= len(self.level_positions):
            self.player_label.hide()

        # Posicionar personajes animados
        for name, _, _, (rx, ry) in self.animated_mob_definitions:
            label = self.animated_mob_labels.get(name)
            if label:
                x = w * rx
                y = h * ry
                label.move(int(x - label.width() / 2), int(y - label.height() / 2))
                label.show()

    def resizeEvent(self, event):
        self._calculate_positions()
        super().resizeEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        if not self.background_texture.isNull():
            painter.drawTiledPixmap(self.rect(), self.background_texture)
        else:
            painter.fillRect(self.rect(), QColor("#5D9C59"))

        all_static_items = self.mob_positions + self.tree_positions
        all_static_items.sort(key=lambda item: item[1].y() + item[0].height())
        for pixmap, pos in all_static_items:
            if not pixmap.isNull():
                painter.drawPixmap(pos, pixmap)

        path = QPainterPath()
        if self.level_positions:
            path.moveTo(self.level_positions[0])
            for i in range(len(self.level_positions) - 1):
                p1, p2 = self.level_positions[i], self.level_positions[i+1]
                path.cubicTo(QPointF((p1.x() + p2.x()) / 2, p1.y()), QPointF((p1.x() + p2.x()) / 2, p2.y()), p2)
        pen = QPen(QColor("#D2B48C"), 10, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin)
        painter.strokePath(path, pen)

        painter.setPen(QColor("white"))
        painter.setFont(QFont("Gill Sans Ultra Bold", 10))
        missions_completed = self.reward_manager.get_missions_completed()
        current_level = missions_completed // 3
        for i in range(current_level):
            pos = self.level_positions[i]
            painter.drawText(QRectF(pos.x() - 15, pos.y() - 15, 30, 30), str(i + 1), QTextOption(Qt.AlignmentFlag.AlignCenter))

    def _generate_level_positions(self):
        positions = []
        num_levels = 15
        margin_x, margin_y = self.width() * 0.3, self.height() * 0.1
        path_width, path_height = self.width() - (2 * margin_x), self.height() - (2 * margin_y)
        for i in range(num_levels):
            progress = i / (num_levels - 1)
            x_var = path_width / 2 * (1 + 0.8 * ((i % 4) / 2 - 1) * (-1 if (i // 2) % 2 == 0 else 1))
            x = margin_x + x_var
            y = margin_y + (progress * path_height)
            positions.append(QPointF(x, y))
        return positions


