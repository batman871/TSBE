from flask import Flask, request, render_template_string, session, redirect, url_for
import os
import random
import string

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Session için key

# Yeni kişi verileri (aileler alt listeler halinde, il ve ilçe İstanbul/Bahçelievler olarak güncellendi)
kisi_verileri = [
    # Aile 1: Yıldız Ailesi
    [
        {"yakınlık": "Kardeşi", "tc": "39797226454", "isim": "JİYAN", "soyisim": "YILDIZ", "dogum_tarihi": "22.11.2010", "anne_adi": "TÜRKAN", "anne_tc": "65917297196", "baba_adi": "ŞEFİK", "baba_tc": "19445845404", "gsm": "+905356439879", "il": "İstanbul", "ilce": "Bahçelievler"},
        {"yakınlık": "Kendisi", "tc": "46720304264", "isim": "MERT", "soyisim": "YILDIZ", "dogum_tarihi": "24.1.2009", "anne_adi": "TÜRKAN", "anne_tc": "65917297196", "baba_adi": "ŞEFİK", "baba_tc": "19445845404", "gsm": "+905336147020", "il": "İstanbul", "ilce": "Bahçelievler"},
        {"yakınlık": "Kardeşi", "tc": "39886532374", "isim": "MUHAMMED FURKAN", "soyisim": "YILDIZ", "dogum_tarihi": "16.7.2007", "anne_adi": "TÜRKAN", "anne_tc": "65917297196", "baba_adi": "ŞEFİK", "baba_tc": "19445845404", "gsm": "Bulunamadı", "il": "İstanbul", "ilce": "Bahçelievler"},
        {"yakınlık": "Annesi", "tc": "65917297196", "isim": "TÜRKAN", "soyisim": "YILDIZ", "dogum_tarihi": "10.9.1988", "anne_adi": "Emine", "anne_tc": "65938296468", "baba_adi": "BİŞAR", "baba_tc": "65941296394", "gsm": "+905356439879", "il": "İstanbul", "ilce": "Bahçelievler"},
        {"yakınlık": "Babası", "tc": "19445845404", "isim": "ŞEFİK", "soyisim": "YILDIZ", "dogum_tarihi": "15.9.1988", "anne_adi": "SACİDE", "anne_tc": "19448845340", "baba_adi": "YUSUF", "baba_tc": "19544842120", "gsm": "+905545844072 +905415008592 +905394242232 +905356439879 +905336147021", "il": "İstanbul", "ilce": "Bahçelievler"},
    ],
    # Aile 2: Uludağ Ailesi
    [
        {"yakınlık": "Kardeşi", "tc": "12609133690", "isim": "KADİR", "soyisim": "ULUDAĞ", "dogum_tarihi": "3.2.2012", "anne_adi": "BESNA", "anne_tc": "50710487226", "baba_adi": "BİLGİN", "baba_tc": "53527393636", "gsm": "+905462565856", "il": "İstanbul", "ilce": "Bahçelievler"},
        {"yakınlık": "Kardeşi", "tc": "76654004428", "isim": "AYŞENUR", "soyisim": "ULUDAĞ", "dogum_tarihi": "13.3.2016", "anne_adi": "BESNA", "anne_tc": "50710487226", "baba_adi": "BİLGİN", "baba_tc": "53527393636", "gsm": "+905462565856", "il": "İstanbul", "ilce": "Bahçelievler"},
        {"yakınlık": "Annesi", "tc": "50710487226", "isim": "BESNA", "soyisim": "ULUDAĞ", "dogum_tarihi": "4.12.1991", "anne_adi": "KADRİYE", "anne_tc": "50770485286", "baba_adi": "SABRİ", "baba_tc": "50833483150", "gsm": "+905462565856", "il": "İstanbul", "ilce": "Bahçelievler"},
        {"yakınlık": "Babası", "tc": "53527393636", "isim": "BİLGİN", "soyisim": "ULUDAĞ", "dogum_tarihi": "1.8.1985", "anne_adi": "AYŞE", "anne_tc": "53608390936", "baba_adi": "ABDULLAH", "baba_tc": "53647389656", "gsm": "+905468597653 +905462565856 +905433626074", "il": "İstanbul", "ilce": "Bahçelievler"},
    ],
    # Aile 3: Dinar Ailesi
    [
        {"yakınlık": "Kardeşi", "tc": "41854058892", "isim": "ROSİDA", "soyisim": "DİNAR", "dogum_tarihi": "12.8.2013", "anne_adi": "SERAYİ", "anne_tc": "12740048792", "baba_adi": "KEREM", "baba_tc": "42286063584", "gsm": "Bulunamadı", "il": "İstanbul", "ilce": "Bahçelievler"},
        {"yakınlık": "Kendisi", "tc": "22879690878", "isim": "BİLAL", "soyisim": "DİNAR", "dogum_tarihi": "13.5.2011", "anne_adi": "SERAYİ", "anne_tc": "12740048792", "baba_adi": "KEREM", "baba_tc": "42286063584", "gsm": "Bulunamadı", "il": "İstanbul", "ilce": "Bahçelievler"},
        {"yakınlık": "Kardeşi", "tc": "11684063694", "isim": "EDA NUR", "soyisim": "DİNAR", "dogum_tarihi": "10.1.2006", "anne_adi": "SERAYİ", "anne_tc": "12740048792", "baba_adi": "KEREM", "baba_tc": "42286063584", "gsm": "Bulunamadı", "il": "İstanbul", "ilce": "Bahçelievler"},
        {"yakınlık": "Kardeşi", "tc": "11684063458", "isim": "ÖZNUR", "soyisim": "DİNAR", "dogum_tarihi": "24.7.2000", "anne_adi": "SERAYİ", "anne_tc": "12740048792", "baba_adi": "KEREM", "baba_tc": "42286063584", "gsm": "+905454711264", "il": "İstanbul", "ilce": "Bahçelievler"},
        {"yakınlık": "Kardeşi", "tc": "14710962718", "isim": "NİSANUR", "soyisim": "DİNAR", "dogum_tarihi": "12.1.2018", "anne_adi": "SERAYİ", "anne_tc": "12740048792", "baba_adi": "KEREM", "baba_tc": "42286063584", "gsm": "Bulunamadı", "il": "İstanbul", "ilce": "Bahçelievler"},
        {"yakınlık": "Kardeşi", "tc": "11684063526", "isim": "ÖZGE", "soyisim": "DİNAR", "dogum_tarihi": "18.2.2004", "anne_adi": "SERAYİ", "anne_tc": "12740048792", "baba_adi": "KEREM", "baba_tc": "42286063584", "gsm": "Bulunamadı", "il": "İstanbul", "ilce": "Bahçelievler"},
        {"yakınlık": "Babası", "tc": "42286063584", "isim": "KEREM", "soyisim": "DİNAR", "dogum_tarihi": "9.3.1976", "anne_adi": "HARİKA", "anne_tc": "42340061730", "baba_adi": "MEHMET ŞERİF", "baba_tc": "Bulunamadı", "gsm": "+905535804584 +905320636737 +905318508221 +905320636737", "il": "İstanbul", "ilce": "Bahçelievler"},
        {"yakınlık": "Annesi", "tc": "12740048792", "isim": "SERAYİ", "soyisim": "YATÇİ", "dogum_tarihi": "24.4.1979", "anne_adi": "VAZİFE", "anne_tc": "12746048574", "baba_adi": "NİMET", "baba_tc": "12875044270", "gsm": "Bulunamadı", "il": "İstanbul", "ilce": "Bahçelievler"},
        {"yakınlık": "Kardeşi", "tc": "11684063380", "isim": "ÖZCAN", "soyisim": "DİNAR", "dogum_tarihi": "20.9.1999", "anne_adi": "SERAYİ", "anne_tc": "12740048792", "baba_adi": "KEREM", "baba_tc": "42286063584", "gsm": "Bulunamadı", "il": "İstanbul", "ilce": "Bahçelievler"},
    ],
    # Aile 4: Ekinci Ailesi
    [
        {"yakınlık": "Kendisi", "tc": "46939987296", "isim": "SİPAN BARAN", "soyisim": "EKİNCİ", "dogum_tarihi": "8.4.2010", "anne_adi": "GÜNEŞ", "anne_tc": "25787474622", "baba_adi": "HAMİT", "baba_tc": "12219086324", "gsm": "+905373507364", "il": "İstanbul", "ilce": "Bahçelievler"},
        {"yakınlık": "Kardeşi", "tc": "15579035308", "isim": "ÖMER", "soyisim": "EKİNCİ", "dogum_tarihi": "8.3.2012", "anne_adi": "GÜNEŞ", "anne_tc": "25787474622", "baba_adi": "HAMİT", "baba_tc": "12219086324", "gsm": "+905373507364", "il": "İstanbul", "ilce": "Bahçelievler"},
        {"yakınlık": "Kardeşi", "tc": "48151256518", "isim": "ARMANÇ", "soyisim": "EKİNCİ", "dogum_tarihi": "31.7.2008", "anne_adi": "GÜNEŞ", "anne_tc": "25787474622", "baba_adi": "HAMİT", "baba_tc": "12219086324", "gsm": "Bulunamadı", "il": "İstanbul", "ilce": "Bahçelievler"},
        {"yakınlık": "Babası", "tc": "12219086324", "isim": "HAMİT", "soyisim": "EKİNCİ", "dogum_tarihi": "12.2.1970", "anne_adi": "REMZİYE", "anne_tc": "12231085978", "baba_adi": "MEHMET TAYYİP", "baba_tc": "12234085814", "gsm": "+905399383688 +905373507364", "il": "İstanbul", "ilce": "Bahçelievler"},
        {"yakınlık": "Annesi", "tc": "25787474622", "isim": "GÜNEŞ", "soyisim": "EKİNCİ", "dogum_tarihi": "15.5.1980", "anne_adi": "DİLNAVAZ", "anne_tc": "25856472368", "baba_adi": "MEHMET", "baba_tc": "25904470742", "gsm": "+905373507364", "il": "İstanbul", "ilce": "Bahçelievler"},
    ],
    # Aile 5: Taşer Ailesi
    [
        {"yakınlık": "Kardeşi", "tc": "52315005348", "isim": "BÜŞRA NUR", "soyisim": "TAŞER", "dogum_tarihi": "7.5.1999", "anne_adi": "LEYLA", "anne_tc": "52327004902", "baba_adi": "ÖKKEŞ", "baba_tc": "52357003982", "gsm": "+905386063350", "il": "İstanbul", "ilce": "Bahçelievler"},
        {"yakınlık": "Kardeşi", "tc": "52318005284", "isim": "BURAK KAAN", "soyisim": "TAŞER", "dogum_tarihi": "30.3.1996", "anne_adi": "LEYLA", "anne_tc": "52327004902", "baba_adi": "ÖKKEŞ", "baba_tc": "52357003982", "gsm": "+905453270557 +905063641446", "il": "İstanbul", "ilce": "Bahçelievler"},
        {"yakınlık": "Annesi", "tc": "52327004902", "isim": "LEYLA", "soyisim": "ÇATALÇAM", "dogum_tarihi": "5.7.1971", "anne_adi": "ŞAHİNAZ", "anne_tc": "52534054738", "baba_adi": "MAHMUT", "baba_tc": "52543054446", "gsm": "+905454933553 +905412919186 +905454933553", "il": "İstanbul", "ilce": "Bahçelievler"},
        {"yakınlık": "Babası", "tc": "52357003982", "isim": "ÖKKEŞ", "soyisim": "TAŞER", "dogum_tarihi": "11.4.1976", "anne_adi": "MÜNEVVER", "anne_tc": "52366003690", "baba_adi": "ALİ", "baba_tc": "52378003244", "gsm": "+905413672734 +905322805946", "il": "İstanbul", "ilce": "Bahçelievler"},
        {"yakınlık": "Kendisi", "tc": "34694395418", "isim": "ALİ EFE", "soyisim": "TAŞER", "dogum_tarihi": "31.8.2010", "anne_adi": "LEYLA", "anne_tc": "52327004902", "baba_adi": "ÖKKEŞ", "baba_tc": "52357003982", "gsm": "Bulunamadı", "il": "İstanbul", "ilce": "Bahçelievler"},
    ],
    # Aile 6: Ayhan Ailesi
    [
        {"yakınlık": "Annesi", "tc": "74899019962", "isim": "SERAP", "soyisim": "AYHAN", "dogum_tarihi": "13.5.1989", "anne_adi": "SAKİN", "anne_tc": "74908019648", "baba_adi": "NECATİ", "baba_tc": "75034015498", "gsm": "+905326154860 +905326154860", "il": "İstanbul", "ilce": "Bahçelievler"},
        {"yakınlık": "Kendisi", "tc": "58477600018", "isim": "ZEHRA NEHİR", "soyisim": "AYHAN", "dogum_tarihi": "2.12.2009", "anne_adi": "SERAP", "anne_tc": "74899019962", "baba_adi": "ÜMİT", "baba_tc": "52204137846", "gsm": "+905326154860", "il": "İstanbul", "ilce": "Bahçelievler"},
        {"yakınlık": "Kardeşi", "tc": "33290447316", "isim": "YUSUF NURİ", "soyisim": "AYHAN", "dogum_tarihi": "17.5.2013", "anne_adi": "SERAP", "anne_tc": "74899019962", "baba_adi": "ÜMİT", "baba_tc": "52204137846", "gsm": "Bulunamadı", "il": "İstanbul", "ilce": "Bahçelievler"},
        {"yakınlık": "Babası", "tc": "52204137846", "isim": "ÜMİT", "soyisim": "AYHAN", "dogum_tarihi": "14.12.1981", "anne_adi": "MENEVŞE", "anne_tc": "52210137618", "baba_adi": "NURİ", "baba_tc": "52213137554", "gsm": "+905322850177", "il": "İstanbul", "ilce": "Bahçelievler"},
    ],
    # Aile 7: Biçer Ailesi
    [
        {"yakınlık": "Kardeşi", "tc": "27370949258", "isim": "AZRA ELİF", "soyisim": "BİÇER", "dogum_tarihi": "10.7.2006", "anne_adi": "ŞERİFE", "anne_tc": "58363053126", "baba_adi": "YALÇIN", "baba_tc": "25483912374", "gsm": "+905327469764", "il": "İstanbul", "ilce": "Bahçelievler"},
        {"yakınlık": "Kendisi", "tc": "37916289106", "isim": "ARDA", "soyisim": "BİÇER", "dogum_tarihi": "12.11.2010", "anne_adi": "ŞERİFE", "anne_tc": "58363053126", "baba_adi": "YALÇIN", "baba_tc": "25483912374", "gsm": "Bulunamadı", "il": "İstanbul", "ilce": "Bahçelievler"},
        {"yakınlık": "Babası", "tc": "25483912374", "isim": "YALÇIN", "soyisim": "BİÇER", "dogum_tarihi": "19.7.1976", "anne_adi": "HATİCE", "anne_tc": "25489912156", "baba_adi": "KEMAL", "baba_tc": "25522911030", "gsm": "+905363721544 +905327469764", "il": "İstanbul", "ilce": "Bahçelievler"},
        {"yakınlık": "Annesi", "tc": "58363053126", "isim": "ŞERİFE", "soyisim": "SARI BİÇER", "dogum_tarihi": "25.6.1979", "anne_adi": "GÜLBAHAR", "anne_tc": "58378052626", "baba_adi": "CELAL", "baba_tc": "58411051500", "gsm": "Bulunamadı", "il": "İstanbul", "ilce": "Bahçelievler"},
    ],
    # Aile 8: Öztok Ailesi
    [
        {"yakınlık": "Kardeşi", "tc": "66751334498", "isim": "DENİZ", "soyisim": "ÖZTOK", "dogum_tarihi": "18.5.2014", "anne_adi": "Ebru", "anne_tc": "27622441974", "baba_adi": "VOLKAN", "baba_tc": "52225628248", "gsm": "Bulunamadı", "il": "İstanbul", "ilce": "Bahçelievler"},
        {"yakınlık": "Kendisi", "tc": "41516168068", "isim": "ÇINAR", "soyisim": "ÖZTOK", "dogum_tarihi": "9.6.2010", "anne_adi": "Ebru", "anne_tc": "27622441974", "baba_adi": "VOLKAN", "baba_tc": "52225628248", "gsm": "+905358131067", "il": "İstanbul", "ilce": "Bahçelievler"},
        {"yakınlık": "Annesi", "tc": "27622441974", "isim": "Ebru", "soyisim": "PİYADE", "dogum_tarihi": "3.11.1983", "anne_adi": "AYŞE", "anne_tc": "27625441810", "baba_adi": "ABDULKADİR", "baba_tc": "27658440736", "gsm": "Bulunamadı", "il": "İstanbul", "ilce": "Bahçelievler"},
        {"yakınlık": "Babası", "tc": "52225628248", "isim": "VOLKAN", "soyisim": "ÖZTOK", "dogum_tarihi": "25.12.1977", "anne_adi": "FATMA", "anne_tc": "52237627802", "baba_adi": "Erol", "baba_tc": "52240627738", "gsm": "+905496183444 +905423597959", "il": "İstanbul", "ilce": "Bahçelievler"},
    ],
    # Aile 9: Bay Ailesi
    [
        {"yakınlık": "Kendisi", "tc": "40304209518", "isim": "GÖKHAN", "soyisim": "BAY", "dogum_tarihi": "11.11.2010", "anne_adi": "BETÜL", "anne_tc": "18962040224", "baba_adi": "YÜCEL", "baba_tc": "23866876770", "gsm": "+905304060585", "il": "İstanbul", "ilce": "Bahçelievler"},
        {"yakınlık": "Kardeşi", "tc": "63718452950", "isim": "BERİL SARE", "soyisim": "BAY", "dogum_tarihi": "20.5.2021", "anne_adi": "BETÜL", "anne_tc": "18962040224", "baba_adi": "YÜCEL", "baba_tc": "23866876770", "gsm": "+905072166109", "il": "İstanbul", "ilce": "Bahçelievler"},
        {"yakınlık": "Babası", "tc": "23866876770", "isim": "YÜCEL", "soyisim": "BAY", "dogum_tarihi": "27.3.1981", "anne_adi": "DURSUNE", "anne_tc": "23899875696", "baba_adi": "MUSTAFA", "baba_tc": "23920874926", "gsm": "+905324206359 +905324206359", "il": "İstanbul", "ilce": "Bahçelievler"},
        {"yakınlık": "Annesi", "tc": "18962040224", "isim": "BETÜL", "soyisim": "BAY", "dogum_tarihi": "3.11.1990", "anne_adi": "NERMİN", "anne_tc": "18974039810", "baba_adi": "BİROL", "baba_tc": "19022038274", "gsm": "+905396157428 +905072302628 +905072166109 +905072166109", "il": "İstanbul", "ilce": "Bahçelievler"},
        {"yakınlık": "Kardeşi", "tc": "61015525780", "isim": "AYŞE ERVA", "soyisim": "BAY", "dogum_tarihi": "28.9.2016", "anne_adi": "BETÜL", "anne_tc": "18962040224", "baba_adi": "YÜCEL", "baba_tc": "23866876770", "gsm": "+905072166109", "il": "İstanbul", "ilce": "Bahçelievler"},
    ],
    # Aile 10: Dakina Ailesi
    [
        {"yakınlık": "Kendisi", "tc": "11609866232", "isim": "BERAT BERKAY", "soyisim": "DAKİNA", "dogum_tarihi": "11.4.2010", "anne_adi": "ŞAZİYE", "anne_tc": "26648364380", "baba_adi": "MEVLÜT", "baba_tc": "65470171438", "gsm": "Bulunamadı", "il": "İstanbul", "ilce": "Bahçelievler"},
        {"yakınlık": "Kardeşi", "tc": "47884758450", "isim": "BEYZA", "soyisim": "DAKİNA", "dogum_tarihi": "10.1.2013", "anne_adi": "ŞAZİYE", "anne_tc": "26648364380", "baba_adi": "MEVLÜT", "baba_tc": "65470171438", "gsm": "Bulunamadı", "il": "İstanbul", "ilce": "Bahçelievler"},
        {"yakınlık": "Babası", "tc": "65470171438", "isim": "MEVLÜT", "soyisim": "DAKİNA", "dogum_tarihi": "19.12.1977", "anne_adi": "NAHİDE", "anne_tc": "65476171210", "baba_adi": "BEKİR", "baba_tc": "65500170486", "gsm": "+905331363348 +905331363319 +905336174458", "il": "İstanbul", "ilce": "Bahçelievler"},
        {"yakınlık": "Kardeşi", "tc": "52774811498", "isim": "BEKİRCAN", "soyisim": "DAKİNA", "dogum_tarihi": "1.9.2015", "anne_adi": "ŞAZİYE", "anne_tc": "26648364380", "baba_adi": "MEVLÜT", "baba_tc": "65470171438", "gsm": "Bulunamadı", "il": "İstanbul", "ilce": "Bahçelievler"},
        {"yakınlık": "Annesi", "tc": "26648364380", "isim": "ŞAZİYE", "soyisim": "DAKİNA", "dogum_tarihi": "16.6.1978", "anne_adi": "NAZMİYE", "anne_tc": "26663363870", "baba_adi": "YÜKSEL", "baba_tc": "26714362180", "gsm": "Bulunamadı", "il": "İstanbul", "ilce": "Bahçelievler"},
    ],
    # Aile 11: Menevşe Ailesi
    [
        {"yakınlık": "Kardeşi", "tc": "55813691402", "isim": "ŞEVVAL", "soyisim": "MENEVŞE", "dogum_tarihi": "28.12.2009", "anne_adi": "SONGÜL", "anne_tc": "50674172282", "baba_adi": "OLCAY", "baba_tc": "39376348812", "gsm": "Bulunamadı", "il": "İstanbul", "ilce": "Bahçelievler"},
        {"yakınlık": "Annesi", "tc": "50674172282", "isim": "SONGÜL", "soyisim": "MENEVŞE", "dogum_tarihi": "15.9.1982", "anne_adi": "NESİBE", "anne_tc": "50680172054", "baba_adi": "BEKİR", "baba_tc": "50683171900", "gsm": "+905424472528", "il": "İstanbul", "ilce": "Bahçelievler"},
        {"yakınlık": "Kendisi", "tc": "55816691348", "isim": "BERKAY", "soyisim": "MENEVŞE", "dogum_tarihi": "28.12.2009", "anne_adi": "SONGÜL", "anne_tc": "50674172282", "baba_adi": "OLCAY", "baba_tc": "39376348812", "gsm": "Bulunamadı", "il": "İstanbul", "ilce": "Bahçelievler"},
        {"yakınlık": "Babası", "tc": "39376348812", "isim": "OLCAY", "soyisim": "MENEVŞE", "dogum_tarihi": "24.12.1981", "anne_adi": "ÖZGÜL", "anne_tc": "39382348684", "baba_adi": "AHMET", "baba_tc": "39460346038", "gsm": "+905427642628", "il": "İstanbul", "ilce": "Bahçelievler"},
    ]
]

# Admin ve kullanıcı key'leri
admin_key = "TSBEHACK7234"
kullanici_keyleri = ["TSBE", "denemelik01"]

# Rastgele key oluşturma fonksiyonu
def generate_key(length=10):
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

# Giriş Sayfası Şablonu
login_template = """
<!DOCTYPE html>
<html>
<head>
    <title>TSBE GAMİNG - Giriş</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            display: flex; 
            justify-content: center; 
            align-items: center; 
            height: 100vh; 
            margin: 0; 
            background: linear-gradient(45deg, #2F3A44, #1C2526, #2F3A44); 
            background-size: 200% 200%; 
            animation: gradientMove 10s ease infinite; 
        }
        @keyframes gradientMove {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        .login-box { background-color: #1C2526; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
        input[type="text"] { padding: 10px; width: 200px; margin-bottom: 10px; background-color: #3A4A56; border: 1px solid #5A6A76; color: white; }
        input[type="submit"] { padding: 10px; background-color: #4CAF50; color: white; border: none; cursor: pointer; }
        input[type="submit"]:hover { background-color: #45a049; }
        .error { color: red; }
        h2 { color: white; animation: colorChange 2s infinite; }
        .tsbe-brand { position: absolute; top: 20px; left: 20px; font-size: 24px; font-weight: bold; animation: colorChange 2s infinite; }
        @keyframes colorChange {
            0% { color: yellow; }
            50% { color: red; }
            100% { color: yellow; }
        }
    </style>
</head>
<body>
    <div class="tsbe-brand">TSBE GAMİNG</div>
    <div class="login-box">
        <h2>Giriş</h2>
        <form method="POST">
            <input type="text" name="key" placeholder="Key giriniz" required>
            <input type="submit" value="Giriş Yap">
        </form>
        {% if error %}
            <p class="error">{{ error }}</p>
        {% endif %}
    </div>
</body>
</html>
"""

# Ana Sayfa ve Sorgu Sayfası Şablonu
main_template = """
<!DOCTYPE html>
<html>
<head>
    <title>TSBE GAMİNG - Sorgu Paneli</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            margin: 0; 
            background: linear-gradient(45deg, #2F3A44, #1C2526, #2F3A44); 
            background-size: 200% 200%; 
            animation: gradientMove 10s ease infinite; 
            color: white; 
        }
        @keyframes gradientMove {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        .sidebar { height: 100%; width: 0; position: fixed; z-index: 1; top: 0; left: 0; background-color: #1C2526; overflow-x: hidden; transition: 0.5s; padding-top: 60px; }
        .sidebar a { padding: 8px 8px 8px 32px; text-decoration: none; font-size: 18px; color: #818181; display: block; transition: 0.3s; }
        .sidebar a:hover { color: #f1f1f1; }
        .sidebar .closebtn { position: absolute; top: 0; right: 25px; font-size: 36px; margin-left: 50px; }
        .openbtn { font-size: 20px; cursor: pointer; background-color: #2F3A44; color: white; padding: 10px 15px; border: none; position: fixed; top: 10px; left: 10px; }
        .openbtn:hover { background-color: #444; }
        #main { transition: margin-left .5s; padding: 20px; }
        h2 { margin-top: 50px; }
        .search-box { margin-bottom: 20px; }
        .search-box label { display: block; margin-bottom: 5px; animation: colorChange 2s infinite; }
        .search-box input[type="text"] { width: 300px; padding: 10px; background-color: #3A4A56; border: 1px solid #5A6A76; color: white; margin-bottom: 10px; }
        .search-box input[type="submit"] { padding: 10px; background-color: #4A5A66; color: white; border: none; cursor: pointer; }
        .search-box input[type="submit"]:hover { background-color: #5A6A76; }
        .result-box { margin-top: 20px; }
        .result-box div { margin-bottom: 10px; }
        .result-box label { font-weight: bold; animation: colorChange 2s infinite; }
        .result-box span { animation: colorChange 2s infinite; }
        .sorgu-menu { display: none; }
        .sorgu-menu.active { display: block; }
        .admin-menu { display: none; }
        .admin-menu.active { display: block; }
        .welcome-message { margin-top: 20px; animation: colorChange 2s infinite; }
        .rules { margin-top: 20px; }
        .rules h3 { animation: colorChange 2s infinite; }
        .rules p { animation: colorChange 2s infinite; }
        .animated-text { animation: colorChange 2s infinite; }
        .tsbe-brand { position: absolute; top: 20px; right: 20px; font-size: 24px; font-weight: bold; animation: colorChange 2s infinite; }
        .tsbe-footer { position: fixed; bottom: 20px; left: 20px; font-size: 18px; animation: colorChange 2s infinite; }
        @keyframes colorChange {
            0% { color: yellow; }
            50% { color: red; }
            100% { color: yellow; }
        }
    </style>
</head>
<body>
    <div class="sidebar" id="mySidebar">
        <a href="javascript:void(0)" class="closebtn" onclick="closeNav()">×</a>
        <a href="/">Ana Sayfa</a>
        <a href="#" onclick="toggleSorgu()">Sorgular</a>
        <div class="sorgu-menu" id="sorguMenu">
            <a href="/ad_soyad_sorgu">Ad Soyad Sorgu</a>
            <a href="/gsm_tc_sorgu">GSM → TCKN</a>
            <a href="/tc_gsm_sorgu">TCKN → GSM</a>
            <a href="/aile_sorgu">Aile Sorgu</a>
        </div>
        {% if is_admin %}
            <a href="#" onclick="toggleAdmin()">ADMİN</a>
            <div class="admin-menu" id="adminMenu">
                <a href="/kullanici_key_olustur">Kullanıcı Keyi Oluştur</a>
                <a href="/kullanici_banla">Kullanıcı Banla</a>
                <a href="/kullanicilara_goz_at">Kullanıcılara Göz At</a>
            </div>
        {% endif %}
        <a href="/cikis_yap">Çıkış Yap</a>
    </div>

    <div id="main">
        <button class="openbtn" onclick="openNav()">☰</button>
        <div class="tsbe-brand">TSBE GAMİNG</div>
        <h2 class="animated-text">{% if page_title %}{{ page_title }}{% else %}Ana Sayfa{% endif %}</h2>
        {% if page_title == "Ana Sayfa" %}
            <div class="welcome-message">
                <p>TSBE GAMİNG SORGU PANELİNE HOŞ GELDİNİZ İYİ KULLANIMLAR</p>
            </div>
            <div class="rules">
                <h3>Kurallar</h3>
                <p>istediğin gibi kullan kural mural yok sikerim</p>
            </div>
        {% endif %}
        {% if form %}
            <div class="search-box">
                {{ form | safe }}
            </div>
        {% endif %}
        {% if sonuclar %}
            <div class="result-box">
                {% for kisi in sonuclar %}
                    <div>
                        <label>YAKINLIK:</label> <span>{{ kisi.yakınlık }}</span><br>
                        <label>ADI:</label> <span>{{ kisi.isim }}</span><br>
                        <label>SOYADI:</label> <span>{{ kisi.soyisim }}</span><br>
                        <label>DOĞUM TARİHİ:</label> <span>{{ kisi.dogum_tarihi }}</span><br>
                        <label>ANNE ADI:</label> <span>{{ kisi.anne_adi }}</span><br>
                        <label>ANNE TCKN:</label> <span>{{ kisi.anne_tc }}</span><br>
                        <label>BABA ADI:</label> <span>{{ kisi.baba_adi }}</span><br>
                        <label>BABA TCKN:</label> <span>{{ kisi.baba_tc }}</span><br>
                        <label>GSM:</label> <span>{{ kisi.gsm }}</span><br>
                        <label>TCKN:</label> <span>{{ kisi.tc }}</span><br>
                        <label>İL:</label> <span>{{ kisi.il }}</span><br>
                        <label>İLÇE:</label> <span>{{ kisi.ilce }}</span><br>
                    </div>
                {% endfor %}
            </div>
        {% endif %}
        {% if key_listesi %}
            <div class="result-box">
                <h3 class="animated-text">Mevcut Key'ler</h3>
                {% for key in key_listesi %}
                    <p class="animated-text">{{ key }}</p>
                {% endfor %}
            </div>
        {% endif %}
        {% if yeni_key %}
            <div class="result-box">
                <h3 class="animated-text">Yeni Oluşturulan Key</h3>
                <p class="animated-text">{{ yeni_key }}</p>
            </div>
        {% endif %}
        {% if mesaj %}
            <div class="result-box">
                <p class="animated-text">{{ mesaj }}</p>
            </div>
        {% endif %}
        <div class="tsbe-footer">TSBE GAMİNG</div>
    </div>

    <script>
        function openNav() {
            document.getElementById("mySidebar").style.width = "250px";
            document.getElementById("main").style.marginLeft = "250px";
        }
        function closeNav() {
            document.getElementById("mySidebar").style.width = "0";
            document.getElementById("main").style.marginLeft = "0";
            document.getElementById("sorguMenu").classList.remove("active");
            document.getElementById("adminMenu").classList.remove("active");
        }
        function toggleSorgu() {
            var menu = document.getElementById("sorguMenu");
            var adminMenu = document.getElementById("adminMenu");
            menu.classList.toggle("active");
            adminMenu.classList.remove("active");
        }
        function toggleAdmin() {
            var menu = document.getElementById("adminMenu");
            var sorguMenu = document.getElementById("sorguMenu");
            menu.classList.toggle("active");
            sorguMenu.classList.remove("active");
        }
    </script>
</body>
</html>
"""

# Giriş Sayfası
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        key = request.form.get("key", "").strip()
        if key == admin_key or key in kullanici_keyleri:
            session["authenticated"] = True
            session["is_admin"] = (key == admin_key)
            return redirect(url_for("index"))
        else:
            return render_template_string(login_template, error="Geçersiz key!")
    return render_template_string(login_template)

# Çıkış Yap
@app.route("/cikis_yap")
def cikis_yap():
    session.pop("authenticated", None)
    session.pop("is_admin", None)
    return redirect(url_for("login"))

# Ana Sayfa
@app.route("/")
def index():
    if not session.get("authenticated"):
        return redirect(url_for("login"))
    is_admin = session.get("is_admin", False)
    return render_template_string(main_template, page_title="Ana Sayfa", is_admin=is_admin)

# Ad Soyad Sorgu (İl ve ilçe eklendi)
@app.route("/ad_soyad_sorgu", methods=["GET", "POST"])
def ad_soyad_sorgu():
    if not session.get("authenticated"):
        return redirect(url_for("login"))
    is_admin = session.get("is_admin", False)
    sonuclar = []
    form = """
        <form method="POST">
            <label>Adı</label>
            <input type="text" name="isim" placeholder="Adı">
            <label>Soyadı</label>
            <input type="text" name="soyisim" placeholder="Soyadı">
            <label>İl</label>
            <input type="text" name="il" placeholder="İl">
            <label>İlçe</label>
            <input type="text" name="ilce" placeholder="İlçe">
            <input type="submit" value="Sorgula">
        </form>
    """
    mesaj = None
    if request.method == "POST":
        isim = request.form.get("isim", "").lower().strip()
        soyisim = request.form.get("soyisim", "").lower().strip()
        il = request.form.get("il", "").lower().strip()
        ilce = request.form.get("ilce", "").lower().strip()
        for aile in kisi_verileri:
            for kisi in aile:
                if (not isim or isim in kisi["isim"].lower()) and \
                   (not soyisim or soyisim in kisi["soyisim"].lower()) and \
                   (not il or il in kisi["il"].lower()) and \
                   (not ilce or ilce in kisi["ilce"].lower()):
                    sonuclar.append(kisi)
        if not sonuclar:
            mesaj = "Sonuç bulunamadı."
    return render_template_string(main_template, page_title="Ad Soyad Sorgu", form=form, sonuclar=sonuclar, mesaj=mesaj, is_admin=is_admin)

# GSM → TCKN Sorgu
@app.route("/gsm_tc_sorgu", methods=["GET", "POST"])
def gsm_tc_sorgu():
    if not session.get("authenticated"):
        return redirect(url_for("login"))
    is_admin = session.get("is_admin", False)
    sonuclar = []
    form = """
        <form method="POST">
            <label>GSM</label>
            <input type="text" name="gsm" placeholder="GSM">
            <input type="submit" value="Sorgula">
        </form>
    """
    mesaj = None
    if request.method == "POST":
        gsm = request.form.get("gsm", "").strip().lower()
        for aile in kisi_verileri:
            for kisi in aile:
                if gsm and gsm in kisi["gsm"].lower():
                    sonuclar.append(kisi)
        if not sonuclar:
            mesaj = "Sonuç bulunamadı."
    return render_template_string(main_template, page_title="GSM → TCKN", form=form, sonuclar=sonuclar, mesaj=mesaj, is_admin=is_admin)

# TCKN → GSM Sorgu
@app.route("/tc_gsm_sorgu", methods=["GET", "POST"])
def tc_gsm_sorgu():
    if not session.get("authenticated"):
        return redirect(url_for("login"))
    is_admin = session.get("is_admin", False)
    sonuclar = []
    form = """
        <form method="POST">
            <label>TCKN</label>
            <input type="text" name="tc" placeholder="TCKN">
            <input type="submit" value="Sorgula">
        </form>
    """
    mesaj = None
    if request.method == "POST":
        tc = request.form.get("tc", "").strip().lower()
        for aile in kisi_verileri:
            for kisi in aile:
                if tc and tc == kisi["tc"].lower():
                    sonuclar.append(kisi)
                    break  # TC eşleşti, daha fazla aramaya gerek yok
        if not sonuclar:
            mesaj = "Sonuç bulunamadı."
    return render_template_string(main_template, page_title="TCKN → GSM", form=form, sonuclar=sonuclar, mesaj=mesaj, is_admin=is_admin)

# Aile Sorgu
@app.route("/aile_sorgu", methods=["GET", "POST"])
def aile_sorgu():
    if not session.get("authenticated"):
        return redirect(url_for("login"))
    is_admin = session.get("is_admin", False)
    sonuclar = []
    form = """
        <form method="POST">
            <label>TCKN</label>
            <input type="text" name="tc" placeholder="TCKN">
            <input type="submit" value="Sorgula">
        </form>
    """
    mesaj = None
    if request.method == "POST":
        tc = request.form.get("tc", "").strip().lower()
        if tc:
            for aile in kisi_verileri:
                for kisi in aile:
                    if tc == kisi["tc"].lower():
                        sonuclar = aile  # TC eşleşti, bu kişinin ailesindeki tüm bireyleri ekle
                        break
                if sonuclar:  # Aile bulundu, döngüden çık
                    break
            if not sonuclar:
                mesaj = "Sonuç bulunamadı."
        else:
            mesaj = "Lütfen bir TCKN girin."
    return render_template_string(main_template, page_title="Aile Sorgu", form=form, sonuclar=sonuclar, mesaj=mesaj, is_admin=is_admin)

# Kullanıcı Keyi Oluştur
@app.route("/kullanici_key_olustur", methods=["GET", "POST"])
def kullanici_key_olustur():
    if not session.get("authenticated") or not session.get("is_admin"):
        return redirect(url_for("login"))
    yeni_key = None
    form = """
        <form method="POST">
            <input type="submit" value="Yeni Key Oluştur">
        </form>
    """
    if request.method == "POST":
        yeni_key = generate_key()
        kullanici_keyleri.append(yeni_key)
    return render_template_string(main_template, page_title="Kullanıcı Keyi Oluştur", form=form, yeni_key=yeni_key, is_admin=True)

# Kullanıcı Banla (Key Silme)
@app.route("/kullanici_banla", methods=["GET", "POST"])
def kullanici_banla():
    if not session.get("authenticated") or not session.get("is_admin"):
        return redirect(url_for("login"))
    mesaj = None
    form = """
        <form method="POST">
            <label>Key</label>
            <input type="text" name="key" placeholder="Silinecek Key">
            <input type="submit" value="Banla">
        </form>
    """
    if request.method == "POST":
        key = request.form.get("key", "").strip()
        if key in kullanici_keyleri:
            kullanici_keyleri.remove(key)
            mesaj = f"Key başarıyla silindi: {key}"
        else:
            mesaj = "Geçersiz key!"
    return render_template_string(main_template, page_title="Kullanıcı Banla", form=form, mesaj=mesaj, is_admin=True)

# Kullanıcılara Göz At
@app.route("/kullanicilara_goz_at")
def kullanicilara_goz_at():
    if not session.get("authenticated") or not session.get("is_admin"):
        return redirect(url_for("login"))
    return render_template_string(main_template, page_title="Kullanıcılara Göz At", key_listesi=kullanici_keyleri, is_admin=True)

# Flask uygulamasını çalıştır
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)