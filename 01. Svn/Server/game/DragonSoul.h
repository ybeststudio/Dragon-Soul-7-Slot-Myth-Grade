// Ara:
		bool	ActivateDragonSoul(LPITEM pItem);
		bool	DeactivateDragonSoul(LPITEM pItem, bool bSkipRefreshOwnerActiveState = false);
		bool	IsActiveDragonSoul(LPITEM pItem) const;

// Altina ekle:
#ifdef ENABLE_DS_GRADE_MYTH
		bool	RepairEmptyAttributes(LPITEM pItem);
#endif

