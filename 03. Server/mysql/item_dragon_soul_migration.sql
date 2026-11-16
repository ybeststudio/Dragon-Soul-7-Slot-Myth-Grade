-- Ejderha tasi envanter pozisyonlari derece sayisina bagli: pos = (type * GRADE_MAX + grade) * 32 + i
-- 5 dereceden 6 dereceye (Efsane) geciste mevcut DS esyalari tasinmali. Sunucu KAPALIYKEN calistir, once yedek al.
UPDATE `item` SET `pos` = FLOOR(`pos` / 160) * 192 + (`pos` % 160) WHERE `window` = 'DRAGON_SOUL_INVENTORY';
-- Kontrol: bir esyanin bulunmasi gereken kutu = (vnum / 10000 - 11) * 192 + (vnum / 1000 % 10) * 32
-- Eski duzende zaten tasmis (derece 5) esyalar varsa formul onlari yanlis tasir; bu satirlari elle duzelt.
