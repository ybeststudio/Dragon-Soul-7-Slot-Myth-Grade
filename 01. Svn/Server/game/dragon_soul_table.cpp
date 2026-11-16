// Ara:
	"grade_rare",
	"grade_ancient",
	"grade_legendary",

// Altina ekle:
#ifdef ENABLE_DS_GRADE_MYTH
	"grade_myth",
#endif


// bool DragonSoulTable::CheckRefineStepTables () icinde:
// Bul:
				if (DRAGON_SOUL_GRADE_MAX != vec_probs.size())
				{
					sys_err ("In %s group of RefineStepTables, probability list size is not %d.", 
						m_vecDragonSoulNames[i].c_str(), DRAGON_SOUL_GRADE_MAX);

// Degistir:
#ifdef ENABLE_DS_GRADE_MYTH
				if (DRAGON_SOUL_STEP_MAX != vec_probs.size())
				{
					sys_err ("In %s group of RefineStepTables, probability list size is not %d.", 
						m_vecDragonSoulNames[i].c_str(), (int)DRAGON_SOUL_STEP_MAX);
#else
				if (DRAGON_SOUL_GRADE_MAX != vec_probs.size())
				{
					sys_err ("In %s group of RefineStepTables, probability list size is not %d.", 
						m_vecDragonSoulNames[i].c_str(), DRAGON_SOUL_GRADE_MAX);
#endif

