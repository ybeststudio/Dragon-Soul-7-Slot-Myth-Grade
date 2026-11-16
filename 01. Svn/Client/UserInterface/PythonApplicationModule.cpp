// void initapp() icinde:
// Ara:
	PyModule_AddIntConstant(poModule, "ENABLE_DRAGON_SOUL_SEAL", 0);

// Altina ekle:
#ifdef ENABLE_DRAGON_SOUL_7_SLOT
	PyModule_AddIntConstant(poModule, "ENABLE_DRAGON_SOUL_7_SLOT", 1);
#else
	PyModule_AddIntConstant(poModule, "ENABLE_DRAGON_SOUL_7_SLOT", 0);
#endif


// void initapp() icinde:
// Ara:
	PyModule_AddIntConstant(poModule, "ENABLE_DRAGON_SOUL_7_SLOT", 0);

// Altina ekle:
#ifdef ENABLE_DS_GRADE_MYTH
	PyModule_AddIntConstant(poModule, "ENABLE_DS_GRADE_MYTH", 1);
#else
	PyModule_AddIntConstant(poModule, "ENABLE_DS_GRADE_MYTH", 0);
#endif

