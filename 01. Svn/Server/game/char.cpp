// void CHARACTER::PointChange(BYTE type, int amount, bool bAmount, bool bBroadcast) icinde:
// Ara:
			SetLevel (GetLevel() + amount);
			val = GetLevel();
			sys_log(0, "LEVELUP: %s %d NEXT EXP %d", GetName(), GetLevel(), GetNextExp());

// Altina ekle:
#ifdef ENABLE_DRAGON_SOUL_AUTO_QUALIFY
			if (IsPC() && IsLoadedAffect() && val >= 30 && !DragonSoul_IsQualified())
				DragonSoul_GiveQualification();
#endif

