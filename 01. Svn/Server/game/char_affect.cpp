// void CHARACTER::LoadAffect(DWORD dwCount, TPacketAffectElement * pElements) icinde:
// Ara:
	// Loading and resetting Dragon Soul Stone settings
	DragonSoul_Initialize();

// Altina ekle:
#ifdef ENABLE_DRAGON_SOUL_AUTO_QUALIFY
	if (IsPC() && GetLevel() >= 30 && !DragonSoul_IsQualified())
		DragonSoul_GiveQualification();
#endif

