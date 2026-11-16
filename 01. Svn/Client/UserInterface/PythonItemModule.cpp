// void initItem() icinde:
// Ara:
	PyModule_AddIntConstant(poModule, "DS_SLOT4", CItemData::DS_SLOT4);
	PyModule_AddIntConstant(poModule, "DS_SLOT5", CItemData::DS_SLOT5);
	PyModule_AddIntConstant(poModule, "DS_SLOT6", CItemData::DS_SLOT6);

// Altina ekle:
#ifdef ENABLE_DRAGON_SOUL_7_SLOT
	PyModule_AddIntConstant(poModule, "DS_SLOT7", CItemData::DS_SLOT7);
#endif

