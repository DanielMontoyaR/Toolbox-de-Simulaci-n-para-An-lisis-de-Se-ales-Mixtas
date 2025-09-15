from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import pyqtSignal, Qt

class ClickableLabel(QLabel):
    clicked = pyqtSignal()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()

    @classmethod
    def copyAttributes(cls, new_label, old_label):
        new_label.setGeometry(old_label.geometry())
        new_label.setText(old_label.text())
        new_label.setAlignment(Qt.AlignCenter)
        new_label.setStyleSheet(old_label.styleSheet())
        new_label.setFont(old_label.font())
        new_label.setFrameShape(old_label.frameShape())
        new_label.setFrameShadow(old_label.frameShadow())
    
    @classmethod
    def replaceLabelInLayout(cls, old_label, new_label):
        """
        Replace a Qlabel with a ClickableLabel in its parent layout.
        Args:
            old_label: Original QLabel to be replaced
            new_label: The new ClickableLabel instance
        """
        parent_widget = old_label.parent()
        
        if parent_widget and parent_widget.layout():
            layout = parent_widget.layout()
            
            # Buscar la posición del label original en el layout
            for i in range(layout.count()):
                item = layout.itemAt(i)
                if item.widget() == old_label:
                    # Remover el label viejo y insertar el nuevo en la misma posición
                    layout.removeWidget(old_label)
                    layout.insertWidget(i, new_label)
                    return True
        
        # Si no hay layout, simplemente copiar atributos geométricos
        cls.copyAttributes(new_label, old_label)
        return False