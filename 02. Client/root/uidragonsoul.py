# DragonSoulRefineWindow.__LoadWindow icinde ara:
			self.openAutoButton = self.GetChild("open_auto")
			self.openAutoButton.SetEvent(ui.__mem_func__(self.ToggleAutoRefinePanel))

# Altina ekle:
			import uiDragonSoulAutoRefine
			self.autoPanel = uiDragonSoulAutoRefine.AutoRefinePanel(self)

