# Expanded 2026 Comprehensive Hero Meta Tier Database with Asset Routing
heroes_pool = pd.DataFrame([
    # S Tier
    {"Hero": "Augran", "Role": "Jungle", "Meta_Tier": "S", "Win_Rate": 54.8, "Ban_Rate": 74.5, "Counter": "Biron", "Seed": "ag", "Image_Url": "https://img.vgn.cn/hok/hero/head/548.png"},
    {"Hero": "Loong", "Role": "Farm Lane", "Meta_Tier": "S", "Win_Rate": 53.9, "Ban_Rate": 68.2, "Counter": "Lam", "Seed": "lg", "Image_Url": "https://img.vgn.cn/hok/hero/head/544.png"},
    {"Hero": "Da Qiao", "Role": "Roamer", "Meta_Tier": "S", "Win_Rate": 54.2, "Ban_Rate": 71.0, "Counter": "Augran", "Seed": "dq", "Image_Url": "https://img.vgn.cn/hok/hero/head/190.png"},
    {"Hero": "Daji", "Role": "Mid Lane", "Meta_Tier": "S", "Win_Rate": 53.2, "Ban_Rate": 55.1, "Counter": "Sun Ce", "Seed": "dj", "Image_Url": "https://img.vgn.cn/hok/hero/head/109.png"},
    {"Hero": "Lam", "Role": "Jungle", "Meta_Tier": "S", "Win_Rate": 52.8, "Ban_Rate": 62.4, "Counter": "Dolia", "Seed": "lm", "Image_Url": "https://img.vgn.cn/hok/hero/head/534.png"},
    {"Hero": "Sun Ce", "Role": "Clash Lane", "Meta_Tier": "S", "Win_Rate": 53.1, "Ban_Rate": 48.0, "Counter": "Li Xin", "Seed": "sc", "Image_Url": "https://img.vgn.cn/hok/hero/head/510.png"},
    {"Hero": "Li Xin", "Role": "Clash Lane", "Meta_Tier": "S", "Win_Rate": 52.9, "Ban_Rate": 46.5, "Counter": "Biron", "Seed": "lx", "Image_Url": "https://img.vgn.cn/hok/hero/head/513.png"},
    {"Hero": "Arke", "Role": "Jungle", "Meta_Tier": "S", "Win_Rate": 52.7, "Ban_Rate": 50.2, "Counter": "Da Qiao", "Seed": "ak", "Image_Url": "https://img.vgn.cn/hok/hero/head/107.png"},
    {"Hero": "Yaria", "Role": "Roamer", "Meta_Tier": "S", "Win_Rate": 52.6, "Ban_Rate": 49.8, "Counter": "Loong", "Seed": "yr", "Image_Url": "https://img.vgn.cn/hok/hero/head/505.png"},

    # A Tier
    {"Hero": "Angela", "Role": "Mid Lane", "Meta_Tier": "A", "Win_Rate": 51.5, "Ban_Rate": 24.3, "Counter": "Daji", "Seed": "an", "Image_Url": "https://img.vgn.cn/hok/hero/head/142.png"},
    {"Hero": "Biron", "Role": "Clash Lane", "Meta_Tier": "A", "Win_Rate": 50.8, "Ban_Rate": 12.4, "Counter": "Sun Ce", "Seed": "br", "Image_Url": "https://img.vgn.cn/hok/hero/head/503.png"},
    {"Hero": "Garo", "Role": "Farm Lane", "Meta_Tier": "A", "Win_Rate": 51.2, "Ban_Rate": 30.5, "Counter": "Lam", "Seed": "gr", "Image_Url": "https://img.vgn.cn/hok/hero/head/508.png"},
    {"Hero": "Dolia", "Role": "Roamer", "Meta_Tier": "A", "Win_Rate": 51.9, "Ban_Rate": 45.2, "Counter": "Augran", "Seed": "dl", "Image_Url": "https://img.vgn.cn/hok/hero/head/543.png"},
    {"Hero": "Arthur", "Role": "Clash Lane", "Meta_Tier": "A", "Win_Rate": 51.1, "Ban_Rate": 15.0, "Counter": "Li Xin", "Seed": "rt", "Image_Url": "https://img.vgn.cn/hok/hero/head/166.png"},
    {"Hero": "Wukong", "Role": "Jungle", "Meta_Tier": "A", "Win_Rate": 50.9, "Ban_Rate": 35.4, "Counter": "Dian Wei", "Seed": "wk", "Image_Url": "https://img.vgn.cn/hok/hero/head/167.png"},
    {"Hero": "Yixing", "Role": "Mid Lane", "Meta_Tier": "A", "Win_Rate": 50.4, "Ban_Rate": 18.2, "Counter": "Yaria", "Seed": "yx", "Image_Url": "https://img.vgn.cn/hok/hero/head/501.png"},

    # B Tier
    {"Hero": "Dian Wei", "Role": "Jungle", "Meta_Tier": "B", "Win_Rate": 49.8, "Ban_Rate": 12.1, "Counter": "Lam", "Seed": "dw", "Image_Url": "https://img.vgn.cn/hok/hero/head/127.png"},
    {"Hero": "Milady", "Role": "Mid Lane", "Meta_Tier": "B", "Win_Rate": 49.5, "Ban_Rate": 14.5, "Counter": "Angela", "Seed": "ml", "Image_Url": "https://img.vgn.cn/hok/hero/head/504.png"},
    {"Hero": "Lady Sun", "Role": "Farm Lane", "Meta_Tier": "B", "Win_Rate": 49.6, "Ban_Rate": 22.1, "Counter": "Garo", "Seed": "ls", "Image_Url": "https://img.vgn.cn/hok/hero/head/111.png"},
    {"Hero": "Cai Yan", "Role": "Roamer", "Meta_Tier": "B", "Win_Rate": 49.1, "Ban_Rate": 10.8, "Counter": "Da Qiao", "Seed": "cy", "Image_Url": "https://img.vgn.cn/hok/hero/head/184.png"},
    {"Hero": "Lu Bu", "Role": "Clash Lane", "Meta_Tier": "B", "Win_Rate": 48.9, "Ban_Rate": 8.5, "Counter": "Biron", "Seed": "lb", "Image_Url": "https://img.vgn.cn/hok/hero/head/123.png"},
    {"Hero": "Li Bai", "Role": "Jungle", "Meta_Tier": "B", "Win_Rate": 48.5, "Ban_Rate": 11.2, "Counter": "Arke", "Seed": "lb_j", "Image_Url": "https://img.vgn.cn/hok/hero/head/131.png"},

    # C Tier
    {"Hero": "Diaochan", "Role": "Mid Lane", "Meta_Tier": "C", "Win_Rate": 47.5, "Ban_Rate": 8.0, "Counter": "Daji", "Seed": "dc", "Image_Url": "https://img.vgn.cn/hok/hero/head/141.png"},
    {"Hero": "Han Xin", "Role": "Jungle", "Meta_Tier": "C", "Win_Rate": 47.1, "Ban_Rate": 9.4, "Counter": "Wukong", "Seed": "hx", "Image_Url": "https://img.vgn.cn/hok/hero/head/150.png"},
    {"Hero": "Di Renjie", "Role": "Farm Lane", "Meta_Tier": "C", "Win_Rate": 47.8, "Ban_Rate": 5.2, "Counter": "Loong", "Seed": "dr", "Image_Url": "https://img.vgn.cn/hok/hero/head/133.png"},
    {"Hero": "Zilong", "Role": "Jungle", "Meta_Tier": "C", "Win_Rate": 47.2, "Ban_Rate": 6.1, "Counter": "Augran", "Seed": "zl", "Image_Url": "https://img.vgn.cn/hok/hero/head/105.png"},
    {"Hero": "Sakeer", "Role": "Roamer", "Meta_Tier": "C", "Win_Rate": 46.5, "Ban_Rate": 2.5, "Counter": "Da Qiao", "Seed": "sk", "Image_Url": "https://img.vgn.cn/hok/hero/head/524.png"},

    # D Tier
    {"Hero": "Agudo", "Role": "Jungle", "Meta_Tier": "D", "Win_Rate": 45.1, "Ban_Rate": 1.2, "Counter": "Lam", "Seed": "ag_d", "Image_Url": "https://img.vgn.cn/hok/hero/head/533.png"},
    {"Hero": "Heino", "Role": "Mid Lane", "Meta_Tier": "D", "Win_Rate": 44.8, "Ban_Rate": 2.1, "Counter": "Angela", "Seed": "hn", "Image_Url": "https://img.vgn.cn/hok/hero/head/542.png"},
    {"Hero": "Huang Zhong", "Role": "Farm Lane", "Meta_Tier": "D", "Win_Rate": 45.4, "Ban_Rate": 1.5, "Counter": "Garo", "Seed": "hz", "Image_Url": "https://img.vgn.cn/hok/hero/head/187.png"},
    {"Hero": "Mulan", "Role": "Clash Lane", "Meta_Tier": "D", "Win_Rate": 44.9, "Ban_Rate": 3.0, "Counter": "Arthur", "Seed": "ml_c", "Image_Url": "https://img.vgn.cn/hok/hero/head/119.png"}
])
