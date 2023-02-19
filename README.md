# Python 3 "Violent Python" Kaynak Kodu

TJ O'Connor tarafından yazılan "Violent Python" kitabının kaynak kodları. Kodlar tamamen Python 3'e dönüştürüldü, PEP8 standartlarına uyacak şekilde yeniden biçimlendirildi ve kullanımdan kalkan kütüphanelerden kaynaklanan sorunları ortadan kaldırmak için yeniden düzenlendi.

*Buna benzer bir çeviri, Justin Seitz'in "Black Hat Python" kitabının kaynak kodunda da yapılıp kullanıma sunulmuştur. Henüz bakmadıysanız [buradan](https://github.com/EONRaider/blackhat-python3) göz atabilirsiniz.*

## Nasıl Kullanılır?
Projeyi `git clone` kullanarak klonlayacağınız dizini (DIR) seçin, bunun için yeni sanal bir ortam veya `venv` oluşturmanız önerilir. Ardından `pip install` kullanarak gereksinimleri yükleyin.

```
user@host:~/DIR$ git clone https://github.com/EONRaider/violent-python3
user@host:~/DIR$ python3 -m venv venv
user@host:~/DIR$ source venv/bin/activate
(venv) user@host:~/DIR$ pip install -r requirements.txt
```

## Notlar
- Dizinler ve dosyalar, her bölümde sunulan içerikle kolayca bağlantı kurulabilmesi için yeniden adlandırılmıştır.
- Daha fazla okunabilirlik sağlamak ve daha modern bir standarda uymak için yazar tarafından sık sık "string concatenation" kullanımı, "string interpoltion" ile değiştirilmiştir.
- Dosyaların, değişkenlerin, fonksiyonların, sınıfların ve methodların adları artık PEP 8 isimlendirme standartlarına uygundur.
- Artık kullanılmayan `optparse` kütüphanesi, bütün kodların tamamında `argparse` ile değiştirilmiştir. Tüm bağımsız değişken ayrıştırma işlemleri artık her dosya için `__main__` kapsamı altında yer almaktadır. Komut dosyalarının çalıştrılması için zorunlu olan ancak orijinal kodda isteğe bağlı olarak değerlendirilen tüm CLI bağımsız değişkenleri artık konumsal olarak uygulanmaktadır. CLI'ye bir -h argümanı sağlayarak `argparse` kullanan tüm scriptler için artık bir *usage* fonksiyonu mevcuttur. Hem sınır hem de denetleyici nesnesinin sorumluluklarını CLI ayrıştırıcısına bırakmak, yazılım mimarisi açısından kesinlikle en iyi seçim değildir, ancak kodu yazan kişinin amacına uygunluk gerekliliği nedeniyle olduğu gibi bırakılmıştır.
- `PEP 8: E722 do not use bare except` ihlalleri, daha spesifik istisnai maddelerle yeniden düzenlendi.
- Yazarın, açık dosya/veritabanı nesnelerinde `close()` methodunu çağırmak yerine dosyaları/veritabanlarını açıp bu durumda bırakma alışkanlığı vardır. Bu nedenle, tüm dosya ve veritabanı örnekleri, içerik yöneticileri kullanılarak yeniden düzenlenmiştir.
- Python için varsayılan kodlama olarak UTF-8'in standartlaştırılması nedeniyle yorumlayıcı tarafından kullanılacak kodlamaya (yani, `# -*- coding: utf-8 -*-`) atıfta bulunan yorumların kullanımı ortadan kaldırıldı 3 (Python 2'den ASCII'nin yerine).
- İyi uygulamalar açısından tamamen yetersiz olsa da, orijinal kodun mantığından ağır olarak sapmak yerine global değişkenlerin kullanımına dokunulmadı.
- Kitabın 5. Bölümünde yer alan kod, pratik açıdan iyi olsa de yeniden düzenlendi. İşlevselliğinin çoğu, yalnızca yazar tarafından örnek olarak belirtilen çok özel durumlara bağlı değildir, aynı zamanda son birkaç yılda gerçekçi olmaktan çıkan güvenlik açıklarından da yararlanır (örneğin, trafik için hala WEP güvenlik algoritmasına dayanan 802.11 kablosuz ağlardan gelen trafiği koklamak gibi). şifreleme veya en kötüsü, hiçbir güvenlik sağlamayan) veya kodu çalışırken görmek istiyorsa, okuyucu tarafından belirli bir İHA modelinin elde edilmesinin saçma beklentisi vardı. Bu bölümü okumak için harcanan çabanın neredeyse anlamsız olduğunu hemen belirtmekten kaçınmak için, yine de, araştırma ve işaret isteklerinin koklanmasıyla ilgili koddan bazı faydalı çıkarımların yapılabileceğini ekleyebilirim.
- Bölüm 6'da yer alan ve Google ve Twitter'a atıfta bulunan kodun, mevcut API'leri işleme biçimleri açısından yeniden düzenleme zahmetine değmeyecek kadar eski olduğu ortaya çıktı. Onlarla ilgilenmek isterseniz, yeniden düzenleyin ve bu repoya bir "pull request" gönderin.

## Yeniden Düzenlenenler
Aşağıda listelenmeyen dosyaların, "Notlar" bölümünde belirtildiği gibi bir şekilde yeniden düzenlendiği varsayılabilir.
- `chapter01/vuln_scanner.py`, var olmayan bir dosya çalışma zamanında bir `OSError` hatasına yol açacak şekilde yazılmış. Bu nedenle `check_vulns()` çağıran loop kontrolü, ana fonksiyonda tanımlanan koşullu ifadeye taşındı.
- `chapter02/nmap_scan.py`, yalnızca kullanımdan kaldırılmış `optparse` kütüphanesini çağırmak amacıyla bir main fonksiyon uyguluyordu ama artık bunun yerine, orijinal koddaki `optparse` çağrısının parçası olan kontrol yapısı, taranan her bağlantı noktası için nmap'e yeni bir çağrının yürütüldüğü yola uygulandı . Döngü, boşa harcanan döngüleri önlemek için `nmap_scan` işlevine taşındı.
- `chapter02/ssh_command.py` başlatma kodu `__main__` kapsamına taşındı. Fonksiyonların parametre isimleri ile çelişen dış kapsamda kullanılan değişken isimleri değiştirildi. Geri dönen bilgi istemi bilgisi orijinal olarak kodlanmıştır ve şimdi daha iyi okunabilirlik sağlamak için düzenlenmiştir.
- `chapter02/ssh_brute.py`, `pxssh` kütüphanesini bağımsız bir kütüphane olarak içe aktardı, ancak aslında bu, `pexpect` kütüphanesi altındaki bir kütüphanedir. Hata bir `ModuleNotFoundError` hatasına yol açıyordu ama düzeltildi. Kitapta sunulduğu şekliyle kodun kendisi, onu kullanılamaz hale getiren girinti hatalarıyla doluydu ve çalışır duruma getirildi.
- `chapter02/ssh_brutekey.py` çalışması için bir dizi önceden oluşturulmuş key gerektiriyordu; ayrıca kitap, okuyucuyu şu anda bir 403 yanıtı döndüren bir URL'de bu tür keyleri edinmeye yönlendiriyor. Bu nedenle, `chapter02` alt dizinine anahtarları içeren sıkıştırılmış bir arşiv eklenmiştir.
- `chapter02/ssh_botnet.py`, kaldırılan `optparse` için kullanılmayan bir import ifadesine sahipti. Bu, scripte bir CLI uygulamak için iptal edilmiş bir girişimin parçası gibi görünüyor. Şaşırtıcı bir şekilde, kitabın basılı versiyonunda bile orada kaldı. Botnet'i başlatan ve komutlarını veren kod, standardizasyon adına `__main__` kapsamı altında düzenlendi. Gereksiz sayıda döngü ifadesinden kaçınmak için botlara verilen iki komut birleştirildi.
- `chapter02/conficker.py`, `sys` kütüphanesinde kullanılmayan çağrı kaldırdı.
- `chapter03/discover_networks.py` yeniden düzenlenmek yerine yeniden uygulanmalıydı. Başlangıçta yalnızca kullanımdan kaldırılan `mechanize` kütüphanesini kullanmakla kalmadı, aynı zamanda WiGLE artık bir API sağladığında artık gerekli olmayan bir şekilde WiGLE hizmetiyle etkileşime giriyor. Bu nedenle kod standardize edildi ve WiGLE'ye kimliği doğrulanmış bir HTTP GET isteği göndermek için `requests` kütüphanesini kullanılarak yeni bir `wigle_print` fonksiyonu uygulandı. Yanıt, doğrudan erişilebilen bir JSON nesnesi döndürüyor ve `re` kütüphanesinin kullanımını da gereksiz kılıyor. Komut dosyasının API tarafından gönderilen hata yanıtı mesajlarıyla başa çıkabilmesi için hata işleme eklendi. Bu script'in, yalnızca Microsoft Windows işletim sistemi altındaki Python kurulumlarında çalışan ve Kayıt defteri anahtarlarına erişim için çalıştırma sırasında Yönetici Ayrıcalıkları gerektiren `winreg`e bağlı olduğuna dikkat edin. API'ye erişim için https://wigle.net/account adresinde bir hesap kayıtlı olmalıdır.
- `chapter03/pdf_read.py` artık kullanımdan kaldırılan `PyPDF` yerine `PyPDF4` kütüphanesini kullanıyor. Kitap, metinde belirli bir PDF dosyasına atıfta bulunuyor ve bu da `chapter03` alt dizinine eklendi.
- `chapter03/exif_fetch.py`, `BeautifulSoup` nesne constructor'una yapılan çağrıda bir `features="html.parser"` bağımsız değişkeni gerektiriyordu. 15. satıra eklendi. Bu script'e yalnızca görüntüleri `img` HTML etiketleri arasına saran web uygulamalarında çalışır (ağır bir şekilde JavaScript'e dayanan modern web uygulamalarında nadir görülen bir uygulama).
- `chapter03/skype_parse.py` örnek olarak `main.db` dosyasını kullanır. Kolaylık sağlamak için `chapter03/skype_profile` alt dizinine eklenmiştir.
- `chapter03/firefox_parse.py`, örnek olarak birkaç `.sqlite` dosyası kullanır. Kolaylık sağlamak için `chapter03/firefox_profile` alt dizinine eklenmiştir.
- `chapter03/iphone_messages.py`, yazar tarafından kullanıma sunulmamış iPhone yedekleme dosyalarına atıfta bulunur. Bu nedenle, kod yeniden düzenlendi ancak test edilmedi.
- `chapter04/geo_ip.py` kullanımdan kaldırılan `pygeoip` kütüphanesini kullanıyordu. Yaratıcısı tarafından [önerildiği](https://github.com/appliedsec/pygeoip) gibi, artık `geoip2` kullanılmalıdır. Yeni uygulanan kodun, kitaptaki orijinal uygulamaya mümkün olduğu kadar benzer tutulması için girişimde bulunuldu, ancak `geoip2`nin yeni paket yapısını ve niteliklerini barındırmak için bazı değişiklikler yapılması gerekiyordu. Komut dosyasını çalıştırmak için gerekli veritabanı dosyası [MaxMind](https://dev.maxmind.com/geoip/geoip2/downloadable/) adresinden indirildi ve `chapter04` dizininde kullanıma sunuldu. `argparse` kullanılarak bir CLI da uygulandı.
- `chapter04/print_direction.py`, dosyayı orijinal uygulamada açarken bir `UnicodeDecodeError` hatası oluşturuyordu. Dosyayı işleyen içerik yöneticisine bir *rb* argümanı eklenerek düzeltildi.
- `chapter04/find_ddos.py`, Hivemind saldırısının kaynak adresini hedef olarak yazdırdı ve çıktıyı işe yaramaz hale getiriyordu. Doğru *dst* değişkeni artık stdout'ta görüntüleniyor. Kitap, yazar tarafından kullanıma sunulmayan `traffic.pcap` adlı bir dosyaya atıfta bulunuyor, bu nedenle kod yeniden düzenlendi ancak test edilmedi.
- `chapter04/test_domain_flux.py`, yazar tarafından sağlanan pcap dosyası analiz edilirken sıfır yanıtlanmamış istek yapıldığını döndürüyor. Nedense paketlerin kendilerinde DNS Kaynak Kaydı alan değeri ayarlanmamıştır, bu nedenle *dns_QR_test* fonksiyonundaki koşul her zaman yanlış olarak değerlendirilir. Bu durumda, DNSRR alanını değerlendiren koşul, koşullu ifadeden kaldırılmıştır ve kaynağı olarak 53 numaralı bağlantı noktasına sahip olan tüm UDP paketleri analiz edilmiştir. Daha az verimli kodla sonuçlanıyor, ancak en azından sonuçları kitapta amaçlandığı gibi verir.
- `chapter05/blue_bug.py`, `PyBluez` kütüphanesini kullanır ve bu kitap da [kurulum talimatlarında](https://github.com/pybluez/pybluez/blob/master/docs/install.rst) belirtildiği gibi `BlueZ` kütüphanesinin ve başlık dosyalarını ister. Bu bağımlılıklar, bir gereksinim olarak `PyBluez` kurulmadan önce kurulmalıdır. Linux'ta bu, `apt install bluetooth libbluetooth-dev` komutu verilerek gerçekleştirilebilir. Orijinal kod, `phone_sock` ile değiştirilen var olmayan bir `client_sock` nesnesine başvuruyor.
- `chapter05/ftp_sniff.py`, `if... else` ifadesinin kötü uygulanması nedeniyle sniffer'a uğramış bir kullanıcı adı sunmasına, ancak parola olmamasına neden olan bir mantık hatasına sahipti. Koşullu ifade iç içe geçmiş bir `if` ifadesiyle değiştirilerek düzeltildi.
- `chapter05/ninja_print.py`, `obexftp` kütüphanesinin çalışmasını gerektirir. Bu kütüphane Python 2 için yazılmıştır ve bugüne kadar eşdeğer bir kitapla değiştirilmemiştir, bu nedenle kod yazar tarafından Python 2 sürümünde yazıldığı gibi kaldı.
- Modüllerin sırasıyla `chapter05/dup.py` ve `chapter06/anon_browser.py` dosyalarından içe aktarılmasını sağlamak için `chapter05/__init__.py` ve `chapter06/__init__.py` dosyaları eklendi.
- `chapter06/anon_proxy.py`, `MechanicalSoup` Python 3 kitaplığı ile yeniden uygulandı. `proxy_test.py`, `useragent_test.py` ve `print_cookies.py` için gerekli olan değişiklikleri entegre edildi.
- `chapter06/anon_browser.py` ayrıca `MechanicalSoup` ile yeniden yapılandırıldı ve kodda bazı değişiklikler yapıldı. *AnonBrowser* sınıfı için contructor'da `cookielib` kütüphanesi `http.cookiejar` ile değiştirildi ve *user_agents* parametresi artık bir tuple yerine string listesini kabul ediyor.
-`chapter06/link_parser.py`, `re` ve `bs4` uygulamalarını çalıştırmak için yeni yollar kullanılarak yeniden düzenlendi.

## Çeviriler
Diğer dillere yapılan çevirileri buradan kontrol edebilirsiniz:
- [Bedirhan Budak](https://github.com/bedirhanbudak) tarafından [Türkçe](https://github.com/EONRaider/violent-python3/tree/turkish-language) diline çevrilmiştir.

## Katkıda Bulunmak İsteyenler
Sağduyulu olmak için, önce bu repository'de yapmak istediğiniz değişikliği bir "issue" aracılığıyla tartışmaya çalışın.

1. Gerçekleştirmek istediğiniz değişiklikler için bir "pull request" açtığınızdan emin olun. Eğer bir veya iki satır değişecekse, "issue" üzerinden talep edilmelidir.
2. Eğer gerekliyse, README.md dosyasını proje yapısındaki değişikliklerle ilgili ayrıntılarla güncelleyin.
3. Değişiklikleri içeren commit mesajlarının bir standarda uyduğundan emin olun. Nasıl devam edeceğinizi bilmiyorsanız, [buradan](https://chris.beams.io/posts/git-commit/) nasıl yapılacağına dair bilgi alabilirsiniz.
4. Talebiniz, mümkün olan en kısa sürede (genellikle 48 saat içinde) incelenecektir.
