// Ara:
	}
	ikashop::GetManager().RecvShopOpenClientPacket(ch, pid);
}

// Altina ekle:
#ifdef ENABLE_DRAGON_SOUL_AUTO_QUALIFY
ACMD(do_ds_refine_open)
{
	if (!ch || !ch->GetDesc() || ch->IsDead())
		return;
	if (!ch->DragonSoul_IsQualified())
	{
		ch->ChatPacket(CHAT_TYPE_INFO, LC_TEXT("You need to be at least level 30 to use Dragon Stone Alchemy."));
		return;
	}
	if (ch->GetExchange() || ch->GetMyShop() || ch->GetShopOwner() || ch->IsOpenSafebox() || ch->IsCubeOpen())
	{
		ch->ChatPacket(CHAT_TYPE_INFO, LC_TEXT("PLEASE_BEFORE_CLOSE_WINDOW_AND_USE_THIS_FUNCTION"));
		return;
	}
	ch->DragonSoul_RefineWindow_Open(ch);
}
#endif

