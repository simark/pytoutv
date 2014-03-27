from pkg_resources import resource_filename
from PyQt4 import Qt, QtCore
from toutvqt.emissions_treemodel import EmissionsTreeModelEmission, EmissionsTreeModelEpisode, EmissionsTreeModelSeason


class QEmissionsTreeView(Qt.QTreeView):
    def __init__(self, model):
        super(QEmissionsTreeView, self).__init__()

        self._setup(model)

    emission_selected = QtCore.pyqtSignal(object)
    season_selected = QtCore.pyqtSignal(object, int)
    episode_selected = QtCore.pyqtSignal(object)
    none_selected = QtCore.pyqtSignal()

    def _setup(self, model):
        self.setModel(model)
        self.expanded.connect(model.item_expanded)

        selection_model = Qt.QItemSelectionModel(model)
        self.setSelectionModel(selection_model)

        selection_model.selectionChanged.connect(self.item_selection_changed)

    def item_selection_changed(self, selected, deselected):
        indexes = selected.indexes()

        if len(indexes) == 0:
            self.none_selected.emit()
            return

        index = indexes[0]
        item = index.internalPointer()
        if type(item) == EmissionsTreeModelEmission:
            self.emission_selected.emit(item.bo)
        elif type(item) == EmissionsTreeModelSeason:
            self.season_selected.emit(item.emission.bo, item.number)
        elif type(item) == EmissionsTreeModelEpisode:
            self.episode_selected.emit(item.bo)
        else:
            self.none_selected.emit()