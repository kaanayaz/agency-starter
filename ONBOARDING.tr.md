# agency-starter'a hoş geldiniz

3 adımlık hızlı başlangıç. "Claude Code yüklü" durumundan "Claude ilk işimi yürütüyor" durumuna yaklaşık 90 dakikada geçirir.

Teknik bilgi gerekmez. Asla kod yazmayacaksınız. Slash komutları her şeyi halleder.

---

## Adım 1 — Eklentiyi yükleyin

Claude Code masaüstü uygulamasını açın. Herhangi bir sohbete şunu yapıştırın:

> Lütfen `https://github.com/kaanayaz/agency-starter` adresini bir Claude Code marketplace olarak ekleyin ve oradan agency-starter eklentisini yükleyin.

Claude yükleme izni isteyecek — **Allow**'a tıklayın. Onaylandığında, **Claude Code'u tamamen kapatıp yeniden açın** (Mac'te Cmd+Q, sonra tekrar açın). Yeni eklentinin temiz yüklenebilmesi için yeniden başlatma gereklidir.

Claude Code tekrar açıldığında şunu yazın:

```
/start
```

`/start` bir kurulum kontrol listesi yazdırmalı. Yazıyorsa, hazırsınız. (Terminal yok, JSON düzenleme yok — yüklemeyi sizin için Claude halleder.)

---

## Adım 2 — Claude in Chrome eklentisini yükleyin

Bazı kurulum adımları sizi web akışları boyunca yönlendirir (Slack uygulamanızı oluşturma, Notion entegrasyonunuzu kurma). Claude in Chrome bu işlemlerde size sayfa üzerinde rehberlik eder.

1. https://claude.ai/download adresine gidin
2. Chrome eklentisini yükleyin
3. Claude Code için kullandığınız hesapla giriş yapın

---

## Adım 3 — `/start` yazın (herhangi bir dilde)

Yeni bir Claude Code sohbeti açıp şunu yazın:

```
/start
```

Bunu istediğiniz dilde yazabilirsiniz — `/start`, `/başla`, `/iniciar` hepsi aynı şekilde çalışır. Sistemin yaptığı ilk şey, sizinle hangi dilde konuşmasını istediğinizi sormaktır. Bir kez seçin; hatırlar. (Slack taslakları, sunum metinleri ve outreach için ayrı bir dil ayarı keşif aşamasında belirlenir — gerekirse müşteri bazında özel diller sonradan eklenebilir.)

Claude neyin kurulu olduğunu, neyin eksik olduğunu tespit eder ve geri kalan her şey için size yön verir. Sırayla geçeceğiniz kurulum komutları:

| Komut | Ne yapar | Süre |
|---|---|---|
| `/setup-mcps` | Claude'u Notion, Slack, Gmail ve Google Drive'a bağlar | ~10 dk |
| `/setup-slack` | Slack uygulamanızı ve `#ops` kanalınızı oluşturmanızı adım adım yönetir | ~15 dk |
| `/setup-notion` | Agency Ops çalışma alanınızı (7 veritabanı) Notion'da kurar | ~5 dk |
| `/setup-discovery` | Ekibinizi, marka sesinizi ve araçlarınızı dolduran röportaj | ~30 dk |
| `/setup-smoke-test` | Her şeyin uçtan uca bağlı olduğunu doğrular | ~2 dk |
| `/first-task` | Claude ile ilk gerçek görevinizi adım adım yapar, sonra bir sonraki sefer için tek tıkla çalışan bir komut olarak kaydeder | ~30 dk |
| `/import-cowork` | (isteğe bağlı) Claude Cowork kullanıyorsanız, sistem geçmiş oturumlarınızı tarar; kaydedilmeye değer görevleri, kuralları ve referans verilerini bulur | ~15 dk |

Herhangi bir noktada duraklayıp devam edebilirsiniz. Her komut idempotenttir — bir kısmını zaten yaptıysanız, yeniden çalıştırma kaldığınız yerden devam eder.

---

## Bir şey bozulduğunda

`/setup-help` yazın. Ne yapıyor olduğunuzu yakalar ve sizin kendi Gmail hesabınızdan bize e-posta gönderir. Genellikle bir iş günü içinde yanıtlarız.

Sohbete token veya şifre yapıştırmayın — `/setup-help` bunları otomatik olarak temizler, ancak en güvenli yol başta yapıştırmamaktır.

---

## Süreç sonunda elinizde ne olacak

Adım 3'ün sonunda:

- Notion'unuzda ekibinizin doğrudan düzenleyebileceği eksiksiz bir operasyon çalışma alanı
- Slack'inizde Claude'un incelemeniz için taslakları yayınladığı bir kanal
- İlk tekrar eden göreviniz artık istediğiniz zaman yeniden çalıştırabileceğiniz bir `/<görev-adı>` komutu
- Claude, oturumlarınız arasındaki kalıpları fark etmeye başlayacak ve bunları kısayol olarak kaydetmek isteyip istemediğinizi soracak (evet veya hayır deyin — kurulum gerektirmez)

4. haftaya gelindiğinde, bu tek tıklı komutlardan yaklaşık 10 tane olacak ve sistem kendi başına planlı işleri yürütmeye başlayacak — Pazartesileri haftalık raporunuzu hazırlamak, Çarşambaları fatura incelemenizi kuyruğa eklemek vb. — harici olarak bir şey göndermeden önce her zaman onayınızı bekleyecek.

Hoş geldiniz.
