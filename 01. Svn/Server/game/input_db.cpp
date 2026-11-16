// void CInputDB::ItemLoad(LPDESC d, const char * c_pData) icinde:
// Ara:
		if (false == item->OnAfterCreatedItem())
			sys_err("Failed to call ITEM::OnAfterCreatedItem (vnum: %d, id: %d)", item->GetVnum(), item->GetID());
		item->SetSkipSave(false);

// Altina ekle:
#ifdef ENABLE_DS_GRADE_MYTH
		if (item->IsDragonSoul())
			DSManager::instance().RepairEmptyAttributes(item);
#endif

