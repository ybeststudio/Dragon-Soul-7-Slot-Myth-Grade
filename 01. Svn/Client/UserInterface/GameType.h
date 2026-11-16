// Ara:
	DRAGON_SOUL_GRADE_RARE,
	DRAGON_SOUL_GRADE_ANCIENT,
	DRAGON_SOUL_GRADE_LEGENDARY,

// Altina ekle:
#ifdef ENABLE_DS_GRADE_MYTH
	DRAGON_SOUL_GRADE_MYTH,
#endif


// Bul:
const DWORD c_DragonSoul_Equip_Slot_Max = 6;

// Degistir:
#ifdef ENABLE_DRAGON_SOUL_7_SLOT
const DWORD c_DragonSoul_Equip_Slot_Max = 7;
#else
const DWORD c_DragonSoul_Equip_Slot_Max = 6;
#endif

