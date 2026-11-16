// Ara:
ACMD(do_open_range_npc);

// Altina ekle:
#ifdef ENABLE_DRAGON_SOUL_AUTO_QUALIFY
ACMD(do_ds_refine_open);
#endif


// Ara:
	{"open_range_npc", 				do_open_range_npc, 					0, 						POS_DEAD, 			GM_PLAYER			},

// Altina ekle:
#ifdef ENABLE_DRAGON_SOUL_AUTO_QUALIFY
	{ "ds_refine_open",				do_ds_refine_open,					0,						POS_DEAD,			GM_PLAYER			},
#endif

