// WORD DSManager::GetBasePosition(const LPITEM pItem) const icinde:
// Bul:
	return col_type * DRAGON_SOUL_STEP_MAX * DRAGON_SOUL_BOX_SIZE + row_type * DRAGON_SOUL_BOX_SIZE;

// Degistir:
#ifdef ENABLE_DS_GRADE_MYTH
	return col_type * DRAGON_SOUL_GRADE_MAX * DRAGON_SOUL_BOX_SIZE + row_type * DRAGON_SOUL_BOX_SIZE;
#else
	return col_type * DRAGON_SOUL_STEP_MAX * DRAGON_SOUL_BOX_SIZE + row_type * DRAGON_SOUL_BOX_SIZE;
#endif


// Ara:
		pItem->SetSocket(ITEM_SOCKET_REMAIN_SEC, time);
	return true;
}

// Altina ekle:
#ifdef ENABLE_DS_GRADE_MYTH
bool DSManager::RepairEmptyAttributes(LPITEM pItem)
{
	if (NULL == pItem || !pItem->IsDragonSoul())
		return false;

	for (int i = 0; i < ITEM_ATTRIBUTE_MAX_NUM; ++i)
	{
		if (pItem->GetAttributeType(i))
			return false;
	}

	sys_log(0, "DS_REPAIR_ATTR: item %u vnum %u had no attributes", pItem->GetID(), pItem->GetVnum());
	return PutAttributes(pItem);
}
#endif

