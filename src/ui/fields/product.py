from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLineEdit, QSpinBox, QLabel

from entities import Product


class ProductFiled(QWidget):
    def __init__(self, parent, product: Product):
        super(ProductFiled, self).__init__(parent=parent)

        self.dialog = parent
        self.product = product
        self.initUI()
        self.initBinds()

    def initUI(self):
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.titleW = QLineEdit(self.product.name, self)
        self.layout.addWidget(self.titleW)

        amount = self.product.amount
        self.amountW = QSpinBox()
        self.amountW.setValue(amount)
        self.amountW.setFrame(0)
        self.layout.addWidget(self.amountW)

        self.editButton = QPushButton("🗑️")
        self.editButton.setMaximumWidth(30)
        self.layout.addWidget(self.editButton)

    def initBinds(self):
        self.editButton.clicked.connect(self.deleteEvent)

    def deleteEvent(self):
        self.dialog.delete_product(self)

    @property
    def title(self) -> str: return self.titleW.text()

    @title.setter
    def title(self, value: str): self.titleW.setText(value)

    @property
    def amount(self) -> int: return self.amountW.value()

    @amount.setter
    def amount(self, value: int): self.volumeW.setValue(value)

    @property
    def new_product(self) -> Product:
        return Product(self.title, self.amount)


class ProductDeliveryField(QWidget):
    def __init__(self, parent, product: Product, picked=True):
        super(ProductDeliveryField, self).__init__(parent=parent)

        self.product = product
        self.picked = picked
        self.initUI()

    def initUI(self):
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.layout.addWidget(QLabel('<-' if self.picked else '->', self))

        self.titleW = QLabel(self.product.name, self)
        self.layout.addWidget(self.titleW)

        amount = self.product.amount
        self.amountW = QLabel(str(amount), self)
        self.layout.addWidget(self.amountW)
