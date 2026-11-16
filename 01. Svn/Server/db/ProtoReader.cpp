// int32_t get_Item_SubType_Value(uint32_t type_value, const string &inputString) icinde:
// Ara:
		"DS_SLOT4",
		"DS_SLOT5",
		"DS_SLOT6"

// Altina ekle:
#ifdef ENABLE_DRAGON_SOUL_7_SLOT
		,"DS_SLOT7"	// amethyst (17xxxx): numeric subtype 6 fell back to 0 = diamond page
#endif

