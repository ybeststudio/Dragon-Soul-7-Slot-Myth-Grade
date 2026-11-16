#
# File Name : uidragonsoulautorefine.py
# Author    : BestStudio
# Version   : 1.1
# Date      : 2026-11-15
#
#

if __USE_DYNAMIC_MODULE__:
	import pyapi

app = __import__(pyapi.GetModuleName("app"))
net = __import__(pyapi.GetModuleName("net"))
player = __import__(pyapi.GetModuleName("player"))

import ui
import chat
import item
import localeInfo
import uiScriptLocale

COMMON = "d:/ymir work/ui/game/common/"

TAB_GRADE, TAB_STEP, TAB_STRENGTH = range(3)
STEP_COUNT = 5			# mat .. kusursuz
STRENGTH_MAX = 6		# +0 .. +6
STEP_DELAY = 0.35		# seconds between two refine requests
ANSWER_TIMEOUT = 4.0

COR_VNUMS = (50255, 50260, 51501, 51502, 51503, 51504, 51505, 51506)
BEAN_VNUMS = (100300, 100400, 100500)


def _GradeCount():
	return player.DRAGON_SOUL_PAGE_COUNT


def _ItemName(vnum):
	item.SelectItem(vnum)
	return item.GetItemName()


def _FindItem(vnum):
	for slot in xrange(player.INVENTORY_PAGE_SIZE * player.INVENTORY_PAGE_COUNT):
		if player.GetItemIndex(player.INVENTORY, slot) == vnum:
			return (player.INVENTORY, slot)
	if app.ENABLE_SPECIAL_INVENTORY:
		size = player.SPECIAL_INVENTORY_PAGE_SIZE * player.SPECIAL_INVENTORY_PAGE_COUNT
		for slotType in (player.SLOT_TYPE_UPGRADE_ITEMS_INVENTORY, player.SLOT_TYPE_STONE_INVENTORY, player.SLOT_TYPE_GIFT_BOX_INVENTORY, player.SLOT_TYPE_CHANGERS_INVENTORY, player.SLOT_TYPE_SKILL_BOOK_INVENTORY):
			window = player.SlotTypeToInvenType(slotType)
			for slot in xrange(size):
				if player.GetItemIndex(window, slot) == vnum:
					return (window, slot)
	return None


class Combo(ui.ComboBoxImage):

	def __init__(self, parent, x, y):
		ui.ComboBoxImage.__init__(self, parent, COMMON + "bg_value3.png", x - 1, y - 1)
		self.index = 0
		self.names = []
		self.onSelect = None
		ui.ComboBoxImage.SetEvent(self, ui.__mem_func__(self.__OnSelect))
		self.listBox.Hide()
		self.listBox = ui.ComboBoxImage.ListBoxWithBoard("TOP_MOST")
		self.listBox.SetPickAlways()
		self.listBox.SetEvent(ui.__mem_func__(self.OnSelectItem))
		self.listBox.Hide()
		self.Show()

	def __del__(self):
		ui.ComboBoxImage.__del__(self)

	def SetOptions(self, names, index):
		self.ClearItem()
		self.names = list(names)
		for i, name in enumerate(self.names):
			self.InsertItem(i, name)
		self.index = index
		self.SetCurrentItem(self.names[index])

	def GetIndex(self):
		return self.index

	def OnMouseLeftButtonUp(self):
		ui.ComboBoxImage.OnMouseLeftButtonUp(self)
		if self.isListOpened:
			x, y = self.GetGlobalPosition()
			self.listBox.SetPosition(x, y + self.GetHeight() + 5)
			self.listBox.SetWidth(self.GetWidth())
			self.listBox.SetTop()

	def __OnSelect(self, index):
		self.index = index
		self.SetCurrentItem(self.names[index])


class CheckBox(ui.Window):

	def __init__(self, parent, y, text):
		ui.Window.__init__(self)
		self.SetParent(parent)
		self.checked = False
		box = ui.ImageBox()
		box.SetParent(self)
		box.LoadImage(COMMON + "checkbox2_no.png")
		box.AddFlag("not_pick")
		box.Show()
		self.box = box
		check = ui.ImageBox()
		check.SetParent(self)
		check.LoadImage(COMMON + "checkbox2_check.png")
		check.AddFlag("not_pick")
		check.Hide()
		self.check = check
		label = ui.TextLine()
		label.SetParent(self)
		label.SetPosition(20, -2)
		label.SetText(text)
		label.AddFlag("not_pick")
		label.Show()
		self.label = label
		self.SetSize(20 + label.GetTextSize()[0], 29)
		self.SetPosition(0, y)
		self.SetWindowHorizontalAlignCenter()
		self.Show()

	def __del__(self):
		ui.Window.__del__(self)

	def IsChecked(self):
		return self.checked

	def OnMouseLeftButtonUp(self):
		self.checked = not self.checked
		if self.checked:
			self.check.Show()
		else:
			self.check.Hide()
		return True


class BeanRow(ui.Window):
	def __init__(self, owner, index):
		ui.Window.__init__(self)
		self.owner = owner
		self.index = index

	def __del__(self):
		ui.Window.__del__(self)

	def OnMouseLeftButtonUp(self):
		self.owner.Choose(self.index)
		return True


class BeanSelector(ui.Window):

	def __init__(self, parent, x, y):
		ui.Window.__init__(self)
		self.SetParent(parent)
		self.SetPosition(x, y)
		self.SetSize(120, 24)
		self.index = 0
		bar = ui.Bar()
		bar.SetParent(self)
		bar.SetSize(120, 24)
		bar.SetColor(ui.BACKGROUND_COLOR)
		bar.AddFlag("not_pick")
		bar.Show()
		self.bar = bar
		text = ui.TextLine()
		text.SetParent(self)
		text.SetPosition(60, 12)
		text.SetHorizontalAlignCenter()
		text.SetVerticalAlignCenter()
		text.AddFlag("not_pick")
		text.Show()
		self.text = text

		pop = ui.Bar("TOP_MOST")
		pop.SetColor(ui.BACKGROUND_COLOR)
		pop.SetSize(190, 2 + 34 * len(BEAN_VNUMS) + 2)
		pop.Hide()
		self.pop = pop
		from _weakref import proxy
		self.rows = []
		for i, vnum in enumerate(BEAN_VNUMS):
			row = BeanRow(proxy(self), i)
			row.SetParent(pop)
			row.SetPosition(2, 2 + 34 * i)
			row.SetSize(186, 34)
			row.Show()
			icon = ui.ExpandedImageBox()
			icon.SetParent(row)
			icon.SetPosition(2, 1)
			item.SelectItem(vnum)
			icon.LoadImage(item.GetIconImageFileName())
			icon.AddFlag("not_pick")
			icon.Show()
			mark = ui.ExpandedImageBox()
			mark.SetParent(row)
			mark.SetPosition(17, 17)
			mark.LoadImage(COMMON + "checkbox_new_selected.png")
			mark.AddFlag("not_pick")
			mark.Hide()
			name = ui.TextLine()
			name.SetParent(row)
			name.SetPosition(40, 17)
			name.SetVerticalAlignCenter()
			name.SetText(_ItemName(vnum))
			name.AddFlag("not_pick")
			name.Show()
			self.rows.append((row, icon, mark, name))
		self.Choose(0, False)
		self.Show()

	def __del__(self):
		ui.Window.__del__(self)

	def GetIndex(self):
		return self.index

	def Choose(self, index, close = True):
		self.index = index
		self.text.SetText(_ItemName(BEAN_VNUMS[index]))
		for i, (row, icon, mark, name) in enumerate(self.rows):
			if i == index:
				mark.Show()
			else:
				mark.Hide()
		if close:
			self.pop.Hide()

	def OnMouseLeftButtonUp(self):
		if self.pop.IsShow():
			self.pop.Hide()
		else:
			x, y = self.GetGlobalPosition()
			self.pop.SetPosition(x, y + 26)
			self.pop.Show()
			self.pop.SetTop()
		return True

	def ClosePopover(self):
		self.pop.Hide()


class AutoRefinePanel(ui.BoardWithTitleBar):
	WIDTH = 250
	HEIGHT = 233

	def __init__(self, refineWindow):
		self.shownStone = 1
		ui.BoardWithTitleBar.__init__(self)
		from _weakref import proxy
		self.refine = proxy(refineWindow)
		self.dsWindow = None
		self.tab = TAB_GRADE
		self.running = False
		self.waiting = False
		self.nextTime = 0.0
		self.sentTime = 0.0
		self.skipGroups = set()
		self.strengthPos = None
		self.keep = []
		self.__Build()

	def __del__(self):
		ui.BoardWithTitleBar.__del__(self)

	def SetDragonSoulWindow(self, dsWindow):
		from _weakref import proxy
		self.dsWindow = proxy(dsWindow)

	def __Text(self, parent, y, text = ""):
		t = ui.TextLine()
		t.SetParent(parent)
		t.SetPosition(0, y)
		t.SetWindowHorizontalAlignCenter()
		t.SetHorizontalAlignCenter()
		t.SetText(text)
		t.Show()
		self.keep.append(t)
		return t

	def __Background(self):
		bg = ui.BorderA()
		bg.SetParent(self)
		bg.SetPosition(10, 54)
		bg.SetSize(230, 170)
		bg.Hide()
		return bg

	def __StartButton(self, parent):
		b = ui.Button()
		b.SetParent(parent)
		b.SetUpVisual(COMMON + "button_large_normal.png")
		b.SetOverVisual(COMMON + "button_large_hover.png")
		b.SetDownVisual(COMMON + "button_large_down.png")
		b.SetPosition(0, 140)
		b.SetWindowHorizontalAlignCenter()
		b.SetText(localeInfo.DRAGON_SOUL_START_AUTO)
		b.SetEvent(ui.__mem_func__(self.ToggleRun))
		b.Show()
		return b

	def __Build(self):
		self.SetSize(self.WIDTH, self.HEIGHT)
		self.SetTitleName(localeInfo.DRAGONSOUL_AUTO_REFINE_TITLE)
		self.SetCloseEvent(ui.__mem_func__(self.Close))
		self.AddFlag("float")

		# tabs: Sinif (10) / Saflik (87) / Seviye (164), 77x22
		self.tabButtons = {}
		for (tab, x, name) in ((TAB_GRADE, 10, localeInfo.DRAGON_SOUL_AUTO_TAB_1), (TAB_STEP, 87, localeInfo.DRAGON_SOUL_AUTO_TAB_3),
				(TAB_STRENGTH, 164, localeInfo.DRAGON_SOUL_AUTO_TAB_2)):
			b = ui.RadioButton()
			b.SetParent(self)
			b.SetPosition(x, 31)
			b.SetUpVisual(COMMON + "button_xsmall_norm.png")
			b.SetOverVisual(COMMON + "button_xsmall_hover.png")
			b.SetDownVisual(COMMON + "button_xsmall_down.png")
			b.SetText(name)
			b.SetEvent(ui.__mem_func__(self.SelectTab), tab)
			b.Show()
			self.tabButtons[tab] = b

		grades = [uiScriptLocale.GetText("DRAGONSOUL_PAGE_BUTTON_%d" % (i + 1)) for i in xrange(_GradeCount())]
		steps = [localeInfo.GetText("DRAGON_SOUL_STEP_LEVEL%d" % (i + 1)).replace(",", "").split(":")[-1].strip() for i in xrange(STEP_COUNT)]

		# Sinif: background_class
		bg = self.__Background()
		self.__Text(bg, 5, localeInfo.DRAGON_SOUL_AUTO_TITLE_1)
		self.__Text(bg, 25, localeInfo.DRAGON_SOUL_AUTO_CLASS_UPGRADE_DESC)
		self.kindText1 = self.__Text(bg, 42)
		self.__Text(bg, 62, localeInfo.DRAGON_SOUL_AUTO_MAX_CLASS)
		self.gradeCombo = Combo(bg, 29, 77)
		self.gradeCombo.SetOptions(grades, len(grades) - 1)
		self.corCheck = CheckBox(bg, 112, localeInfo.DRAGON_SOUL_AUTO_OPEN_COR)
		self.startButtons = [self.__StartButton(bg)]
		self.bgGrade = bg

		# Saflik: background_clarity
		bg = self.__Background()
		self.__Text(bg, 5, localeInfo.DRAGON_SOUL_AUTO_TITLE_3)
		self.__Text(bg, 29, localeInfo.DRAGON_SOUL_AUTO_UPGRADE_DESC)
		self.kindText2 = self.__Text(bg, 46)
		self.__Text(bg, 74, localeInfo.DRAGON_SOUL_AUTO_MAX_CLARITY)
		self.stepCombo = Combo(bg, 29, 90)
		self.stepCombo.SetOptions(steps, len(steps) - 1)
		self.startButtons.append(self.__StartButton(bg))
		self.bgStep = bg

		# Seviye: background_level
		bg = self.__Background()
		lines = localeInfo.DRAGON_SOUL_AUTO_SLOT_DESC.split("^")
		self.__Text(bg, 5, localeInfo.DRAGON_SOUL_AUTO_TITLE_2)
		self.__Text(bg, 24, lines[0].strip())
		self.__Text(bg, 38, lines[1].strip() if len(lines) > 1 else "")
		slotBg = ui.ExpandedImageBox()
		slotBg.SetParent(bg)
		slotBg.SetPosition(24, 52)
		slotBg.LoadImage(COMMON + "slots/slot_ds.png")
		slotBg.Show()
		self.keep.append(slotBg)
		slot = ui.SlotWindow()
		slot.SetParent(slotBg)
		slot.SetPosition(8, 8)
		slot.SetSize(32, 32)
		slot.AppendSlot(0, 0, 0, 32, 32)
		slot.SetSelectEmptySlotEvent(ui.__mem_func__(self.__OnStoneSlotEmpty))
		slot.SetSelectItemSlotEvent(ui.__mem_func__(self.__OnStoneSlotItem))
		slot.SetOverInItemEvent(ui.__mem_func__(self.__OnStoneOverIn))
		slot.SetOverOutItemEvent(ui.__mem_func__(self.__OnStoneOverOut))
		slot.Show()
		self.stoneSlot = slot
		arrow = ui.ExpandedImageBox()
		arrow.SetParent(bg)
		arrow.SetPosition(72, 67)
		arrow.LoadImage(COMMON + "arrow_r.png")
		arrow.Show()
		self.keep.append(arrow)
		self.beanSelector = BeanSelector(bg, 102, 60)
		self.__Text(bg, 93, localeInfo.DRAGON_SOUL_AUTO_MAX_REFINE)
		self.levelCombo = Combo(bg, 31, 108)
		self.levelCombo.SetOptions(["+%d" % i for i in xrange(STRENGTH_MAX + 1)], STRENGTH_MAX)
		self.startButtons.append(self.__StartButton(bg))
		self.bgLevel = bg

		self.SelectTab(TAB_GRADE)

	def SelectTab(self, tab):
		if self.running:
			self.Stop()
		self.tab = tab
		for (t, b) in self.tabButtons.items():
			if t == tab:
				b.Down()
			else:
				b.SetUp()
		self.__CloseLists()
		for (t, bg) in ((TAB_GRADE, self.bgGrade), (TAB_STEP, self.bgStep), (TAB_STRENGTH, self.bgLevel)):
			if t == tab:
				bg.Show()
			else:
				bg.Hide()
		self.RefreshTexts()

	def __CloseLists(self):
		for combo in (self.gradeCombo, self.stepCombo, self.levelCombo):
			combo.CloseListBox()
		self.beanSelector.ClosePopover()

	def RefreshTexts(self):
		self.kindText1.SetText(self.__KindName())
		self.kindText2.SetText(self.__KindName() + " [" + self.__PageName() + "]")
		text = localeInfo.DRAGON_SOUL_STOP_AUTO if self.running else localeInfo.DRAGON_SOUL_START_AUTO
		for b in self.startButtons:
			b.SetText(text)
		self.__RefreshStoneSlot()

	def __Kind(self):
		return self.dsWindow.DSKindIndex if self.dsWindow else 0

	def __Page(self):
		return self.dsWindow.inventoryPageIndex if self.dsWindow else 0

	def __KindName(self):
		return uiScriptLocale.GetText("DRAGONSOUL_TAP_TITLE_%d" % (self.__Kind() + 1), "")

	def __PageName(self):
		return uiScriptLocale.GetText("DRAGONSOUL_PAGE_BUTTON_%d" % (self.__Page() + 1), "")

	# ------------------------------------------------------------------ Seviye: stone slot (slot_stone)
	def __RefreshStoneSlot(self):
		vnum = 0
		if self.strengthPos is not None:
			vnum = player.GetItemIndex(player.DRAGON_SOUL_INVENTORY, self.strengthPos)
			if not vnum:
				self.strengthPos = None
		if vnum != self.shownStone:
			self.shownStone = vnum
			if vnum:
				self.stoneSlot.SetItemSlot(0, vnum, 0)
			else:
				self.stoneSlot.ClearSlot(0)
			self.stoneSlot.RefreshSlot()

	def __OnStoneSlotEmpty(self, slotPos):
		import mouseModule
		if not mouseModule.mouseController.isAttached():
			return
		slotType = mouseModule.mouseController.GetAttachedType()
		pos = mouseModule.mouseController.GetAttachedSlotNumber()
		mouseModule.mouseController.DeattachObject()
		if player.SlotTypeToInvenType(slotType) != player.DRAGON_SOUL_INVENTORY:
			return
		if self.running:
			self.Stop()
		self.strengthPos = pos
		self.__RefreshStoneSlot()

	def __OnStoneSlotItem(self, slotPos):
		import mouseModule
		if mouseModule.mouseController.isAttached():
			self.__OnStoneSlotEmpty(slotPos)
			return
		if self.running:
			self.Stop()
		self.strengthPos = None
		self.__RefreshStoneSlot()

	def __OnStoneOverIn(self, slotPos):
		tooltip = self.refine.tooltipItem
		if tooltip and self.strengthPos is not None:
			tooltip.SetInventoryItem(self.strengthPos, player.DRAGON_SOUL_INVENTORY)

	def __OnStoneOverOut(self):
		tooltip = self.refine.tooltipItem
		if tooltip:
			tooltip.HideToolTip()

	# ------------------------------------------------------------------ show / hide
	def Open(self):
		x, y = self.refine.GetGlobalPosition()
		self.SetPosition(max(0, x - self.WIDTH - 2), y)
		self.RefreshTexts()
		self.Show()
		self.SetTop()

	def Close(self):
		self.Stop()
		self.__CloseLists()
		self.Hide()

	def OnPressEscapeKey(self):
		self.Close()
		return True

	# ------------------------------------------------------------------ the loop
	def ToggleRun(self):
		if self.running:
			self.Stop()
		else:
			self.Start()

	def Start(self):
		if not self.refine.IsShow():
			return
		self.running = True
		self.waiting = False
		self.skipGroups = set()
		self.nextTime = app.GetTime()
		self.RefreshTexts()

	def Stop(self, message = None):
		was = self.running
		self.running = False
		self.waiting = False
		self.RefreshTexts()
		if was and message:
			chat.AppendChat(chat.CHAT_TYPE_INFO, message)

	def OnRefineResult(self, succeeded, invenType, invenPos, reason = None):
		if not self.running:
			return
		self.waiting = False
		if not succeeded and reason is not None and reason != net.DS_SUB_HEADER_REFINE_FAIL:
			self.Stop(localeInfo.DRAGON_SOUL_AUTO_STOPPED)
			return
		self.nextTime = app.GetTime() + STEP_DELAY
		if self.tab == TAB_STRENGTH and invenType == player.DRAGON_SOUL_INVENTORY:
			self.strengthPos = invenPos

	def OnUpdate(self):
		self.RefreshTexts()
		if not self.running:
			return
		if not self.refine.IsShow():
			self.Stop()
			return
		now = app.GetTime()
		if self.waiting:
			if now - self.sentTime > ANSWER_TIMEOUT:
				self.Stop(localeInfo.DRAGON_SOUL_AUTO_STOPPED)
			return
		if now < self.nextTime:
			return
		self.nextTime = now + STEP_DELAY
		if self.tab == TAB_GRADE and self.corCheck.IsChecked() and self.__OpenCor():
			return
		if self.tab == TAB_STRENGTH:
			self.__StepStrength()
		else:
			self.__StepGradeOrStep()

	def __OpenCor(self):
		for slot in xrange(player.INVENTORY_PAGE_SIZE * player.INVENTORY_PAGE_COUNT):
			if player.GetItemIndex(player.INVENTORY, slot) in COR_VNUMS:
				net.SendItemUsePacket(player.INVENTORY, slot)
				return True
		return False

	def __SetType(self, refineType):
		if self.refine.currentRefineType != refineType:
			self.refine.SelectRefineType(refineType)
			self.refine.refineChoiceButtonDict[refineType].Down()

	def __Filled(self):
		return all(i in self.refine.refineItemInfo for i in xrange(self.refine.refineSlotLockStartIndex))

	def __Send(self):
		self.refine.PressDoRefineButton()
		self.waiting = True
		self.sentTime = app.GetTime()

	def __StepGradeOrStep(self):
		isGrade = self.tab == TAB_GRADE
		target = (self.gradeCombo if isGrade else self.stepCombo).GetIndex()
		self.__SetType(self.refine.REFINE_TYPE_GRADE if isGrade else self.refine.REFINE_TYPE_STEP)
		self.refine.FlushRefineItemSlot()
		self.refine.Refresh()
		kind = self.__Kind()
		pageCount = _GradeCount()
		pages = xrange(pageCount) if isGrade else (self.__Page(),)
		slots = []
		for page in pages:
			for local in xrange(player.DRAGON_SOUL_PAGE_SIZE):
				pos = (kind * pageCount + page) * player.DRAGON_SOUL_PAGE_SIZE + local
				vnum = player.GetItemIndex(player.DRAGON_SOUL_INVENTORY, pos)
				if not vnum:
					continue
				grade = vnum % 10000 / 1000
				step = vnum % 1000 / 100
				level = grade if isGrade else step
				if level >= target:
					continue
				slots.append((vnum / 100, pos))
		groups = {}
		for key, pos in slots:
			groups.setdefault(key, []).append(pos)
		for key in sorted(groups):
			if key in self.skipGroups:
				continue
			for pos in groups[key]:
				self.refine.AutoSetItem((player.DRAGON_SOUL_INVENTORY, pos), 1)
				if self.__Filled():
					self.__Send()
					return
			self.refine.FlushRefineItemSlot()
			self.refine.Refresh()
			self.skipGroups.add(key)
		self.Stop(localeInfo.DRAGON_SOUL_AUTO_FINISHED)

	def __StepStrength(self):
		pos = self.strengthPos
		vnum = player.GetItemIndex(player.DRAGON_SOUL_INVENTORY, pos) if pos is not None else 0
		if not vnum:
			self.Stop(localeInfo.DRAGON_SOUL_AUTO_NO_STONE)
			return
		if vnum % 100 / 10 >= self.levelCombo.GetIndex():
			self.Stop(localeInfo.DRAGON_SOUL_AUTO_FINISHED)
			return
		self.__SetType(self.refine.REFINE_TYPE_STRENGTH)
		self.refine.FlushRefineItemSlot()
		self.refine.Refresh()
		beanPos = _FindItem(BEAN_VNUMS[self.beanSelector.GetIndex()])
		if not beanPos:
			self.Stop(localeInfo.DRAGON_SOUL_AUTO_NO_BEAN)
			return
		self.refine.AutoSetItem(beanPos, 1)
		self.refine.AutoSetItem((player.DRAGON_SOUL_INVENTORY, pos), 1)
		if not self.__Filled():
			self.Stop(localeInfo.DRAGON_SOUL_AUTO_NO_STONE)
			return
		self.__Send()
