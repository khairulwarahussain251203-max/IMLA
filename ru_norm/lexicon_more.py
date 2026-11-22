"""
Extra vocabulary (third block). Same line format as lexicon.py:

    canonical: variant variant variant ...

Lines that start with # or have no colon are ignored by the parser, so the
section titles below are plain comments.

Rules used while writing this block (same convention as proposal.md):
  * lowercase letters only, one canonical spelling per word
  * 2-4 realistic hand-written variants per word; the generator adds more
  * words listed in OOV_WORDS (lexicon.py) are NOT added here, because they are
    reserved as the "unknown word, must stay unchanged" test set
"""

LEX_MORE = """
# ---------------- pronouns, postpositions, connectors ----------------
tumhari: tumhaari tmhari tumhri
tumhare: tumhaare tmhare
hamari: humari hmari hamaari
hamare: humare hmare hamaare
mere: meray merey
tera: teraa tra
teri: terii tri
tere: teray terey
uski: uskee usky
uske: uskay uskey
unki: unkee unky
unke: unkay unkey
iska: iskaa
iski: iskee isky
iske: iskay iskey
aapka: apka aapkaa
aapki: apki aapkee
aapke: apke aapkay
jis: jiss
jo: joo
kis: kiss
kisi: kisee kisy
har: harr
sabhi: sabi sabhee
dono: donon donoo
dusra: doosra dusraa
pehla: pahla pehlaa
pehli: pehlee pahli
doosri: dusri doosree
teesra: tisra teesraa
aakhri: akhri aakhiri
hi: hee
to: toh tou
na: naa
ya: yaa
tarah: tarha tarahh
bina: beena bnaa
baghair: bagair baghayr bghair
taake: taaki take taki
chunke: chunkay chunki
halanke: halaanke halankay
jabke: jabki jabkay
jaise: jaisay jese jesay
waise: waisay wese
tabhi: tabi tabhee
jahan: jahaan jahn
idhar: idher idhr
udhar: udher udhr
kidhar: kidher kidhr
kahin: kahee kahi
ab: abb
wajah: wajha wajh
alawa: aalawa ilawa
darmiyan: darmiyaan darmian
beech: bich beechh
samne: saamne samnay samney
peeche: pichay piche pichhay
aage: aagay agay agey
kareeb: qareeb karib
shuru: shuroo shru shuruu
khatam: khtm khatm khatamm
mukammal: mukamal mukammil mukmmal
adha: aadha adhaa
saara: sara saaraa
dobara: dubara dobarah dobaarah
ekdam: ekdum ikdam
yaqeenan: yakeenan yaqinan
fauran: fawran foran
turant: turrant turat
aksar: aksr akser
ajkal: aajkal ajkl
roz: rooz rozz
rozana: rozaana rozanaa
seedha: sidha seedhaa
ulta: ultaa

# ---------------- verbs: infinitives and common forms ----------------
dekhna: dekhnaa dkhna
dekhta: dekhtaa
dekhti: dekhtee
dekhte: dekhtay dekhty
suniye: suniay suniyay
bolo: boloo
boli: bolee
bole: bolay
bolta: boltaa
kehta: kehtaa kahta
kehti: kehtee kahti
kehte: kehtay kahte
likho: likhoo
parho: padho parhoo
parhta: padhta parhtaa
parhai: padhai parhaee
khelo: khailo kheloo
khao: khaao khaoo
piyo: peeyo piyoo
sona: sonaa
soya: soyaa
jagna: jaagna jagnaa
uthao: uthaao
uthana: uthaana uthanaa
dijiye: dijyay dijiey
lijiye: lijye lijiey
dein: den deen
lein: len leen
lo: loo
dega: degaa daega
degi: degee degy
lega: legaa
legi: legee
ayenge: aayenge aaenge
aunga: aaunga aaonga
aungi: aaungi aaongi
jaunga: jaoonga jaonga
jaungi: jaoongi jaongi
jayenge: jaenge jaengay
chalega: chalgaa chalegaa
chalta: chaltaa
chalti: chaltee
chalte: chaltay
chale: chalay
chali: chalee
bhejo: bhejoo
bhej: bhejj
batana: bataana batanaa
bata: bataa
bataiye: bataye batayie
bataein: batayen bataen
samjhana: samjhaana samjhanaa
samjho: samjhoo
samajhna: samjhna samajhnaa
sikho: seekho sikhoo
karwana: karwaana karwanaa
karwa: karwaa
banana: banaana bananaa
bana: banaa
bani: banee
bane: banay
banao: banaao
banaya: banaaya bnaya
khareedna: kharidna khareednaa
khareda: kharida khareedaa
bechna: bechnaa
becha: bechaa
bikna: biknaa
bik: bikk
kamana: kamaana kamanaa
kharch: kharcha kharchh
bachana: bachaana bachanaa
bachao: bachaao
pakarna: pakadna pakarnaa
pakro: pakdo pakroo
chorna: chhorna chodna chornaa
rok: rokk
rokna: roknaa
roko: rokoo
tod: todd
torna: todna tornaa
jodna: jorna jodnaa
bharna: bharnaa
nikalna: nikaalna nikalnaa
nikal: nikaal nikall
nikla: niklaa
daalna: dalna daalnaa
daal: dal daall
lagana: lagaana laganaa
lagao: lagaao
hatao: hataao
hatna: hatnaa
chhupna: chupna chhupnaa
dikhana: dikhaana dikhanaa
dikha: dikhaa
dikhao: dikhaao
dikhai: dikhae dikhaee
sunai: sunae sunaee
milao: milaao
pahunchna: pohnchna pohchna pahuchna
pahunch: pohnch pohanch pahuch
ruk: rukk
ruko: rukoo
dhoond: dhund dhoondh
bhool: bhol bhooll
yaadein: yadein yaaden
sahna: sehna sahnaa
mangna: maangna mangnaa
maang: mang maangg
poochna: puchna poochnaa
poocho: puchho poochho
poocha: puchha poochha
manna: maanna mannaa
chahna: chahnaa
chaha: chahaa
hansi: hasi hansee
darna: darnaa
dara: daraa
roya: royaa roiya
royi: roee
jeena: jina jeenaa
marna: mrna marnaa
mara: maraa
mar: marr
maro: maroo
pitna: pitnaa
girna: girnaa
gira: giraa
gir: girr
tootna: tutna tootnaa
toota: tuta tootaa
tooti: tuti tootee
phatna: fatna phatnaa
jalna: jlna jalnaa
bujhna: bujhnaa
bujh: bujhh
badalna: badalnaa
badal: bdl badall
badla: badlaa
badli: badlee
sudharna: sudharnaa
bigarna: bigadna bigarnaa
bigra: bigdaa bigraa
bigar: bigad bigarr
bigri: bigdi bigree
chalana: chalaana chalanaa
chalao: chalaao
kholo: kholoo
khula: khulaa
khuli: khulee
khule: khulay
khulna: khulnaa
rakho: rakhoo
utho: uthoo
baitho: baithoo
baitha: baithaa bethaa
leta: letaa
leti: letee
lete: letay
deta: detaa
deti: detee
dete: detay
jati: jaati jatee
jate: jaate jatay
aati: aatee ati
aate: aatay atay
hote: hotay hotey
sakte: saktay sakty
sakein: sakain saken
chahun: chahoon
chahein: chahain chahen
chahti: chahtee chahty
chahte: chahtay chahtey
lagti: lagtee lagty
lagte: lagtay lagtey
lagi: lagee lagy
laga: lagaa
lage: lagay
milna: milnaa
mile: milay
mili: milee
milega: milegaa milaga
milegi: milegee milegy
kar: kr karr
karke: krke karkay
kare: karay karey
karega: kareyga karaga
karegi: karegee karegy
karenge: karengay karenga
karunga: karoonga karonga
karungi: karoongi karongi
kiye: kiyay keye
hoon: hun hu hoonn
hona: honaa
hone: honay honey
honge: hongay hongey
the: thay thae
rahega: rehega rahegaa
rahenge: rahengay rehenge
rahta: rehta rahtaa
rahti: rehti rahtee
ayi: aayi aai aee
aye: aaye ae ayay
jaye: jaaye jae jayay
jayega: jaega jayegaa
bhaag: bhag bhaagg
bhaagna: bhagna bhaagnaa
pakar: pakad pakarr
pehen: pahen pehan
pehenna: pehanna pahenna
nahana: nahaana nahanaa
dhona: dhonaa
pakana: pakaana pakanaa
safai: safayi safaee
sambhalna: sanbhalna sambhalnaa
sambhal: sanbhal sambhall
bachna: bchna bachnaa
phenkna: phaink phainknaa
ghoomna: ghumna ghoomnaa
ghoom: ghum ghoomm
sunao: sunaao
gaana: gaanaa gana
gaao: gao gaaoo
nachna: nachnaa
chillana: chilana chillaana
hilna: hilnaa
sambhaalo: sambhalo sambaalo
dekhiye: dekhiay dekhye
suniyega: suniega suniyegaa
kijiye: kijye kijiey

# ---------------- adjectives and adverbs ----------------
sundar: sundr sundarr
badsurat: badsoorat badsurat
mazboot: mazbut mazboott
kamzor: kamzoor kamzorr
sust: sustt
chalaak: chalak chaalak
bewakoof: bewaqoof bevakoof bewkoof
pagal: pagall paagal
samajhdar: samjhdar samajhdaar
bahadur: bahadar bahaadur
ameer: amir ameerr
ghareeb: gharib ghareb
mashhoor: mashoor mashhur
mehnati: mehnti mehantee
imandar: eemandar imaandar
jhoota: jhota jhootaa
jawan: jawaan jawann
boorha: burha boorhaa
meetha: mitha meethaa
namkeen: namkin namkeeen
teekha: tikha teekhaa
khatta: khata khattaa
kadwa: kadva kadwaa
gila: gilaa geela
sookha: sukha sookhaa
bhara: bharaa
khali: khaali khalee
ajeeb: ajib ajeb ajeeeb
zabardasti: zabrdasti zabardastee
lazmi: lazimi lazmee
mumkin: mumkn mumkinn
namumkin: nammumkin namumkn
asli: aslee asly
nakli: naqli naklee
naye: naey nae nayay
nayi: nayee naee
barhiya: barhia bariya
ghatiya: ghatia ghatiyaa
lajawab: lajawaab lajawb lajvab
umda: umdaa umdah
sabar: sabr sabaar
himmat: himat himmt
taqat: takat taakat
sukoon: sakoon sukun
aaram: araam aaraam
chain: chen chayn
neend: nend neendh
bhook: bhuk bhookh
pyaas: pyas pyaaas
thakan: thkan thakaan
dard: dardd
bukhar: bukhaar bukhr
khansi: khaansi khasi
sardi: sardee sardy
garmi: garmee garmy
bimari: beemari bimaari
dawai: dawayi dawae
dawa: dawaa dava
ilaaj: ilaj elaj ilaaaj
zakhm: zakham zaqm
khoon: khun khoonn
gulabi: gulaabi gulabee
narangi: narangee norangi
bhura: bhoora bhuraa
bhookha: bhooka bhukha
pyaasa: pyasa pyaasaa
pakka: paka pakkaa
kachcha: kacha kachha kachchaa
asal: asl asall
faltu: fultu faaltu phaltu
behuda: behooda bahuda
farzi: farzee farzy
khamosh: khamoosh khamush
mast: mastt masst
waqai: waqayi waqae

# ---------------- body, health, family, people ----------------
dimagh: dimag dimaagh dmagh
aankh: ankh aankhh
aankhein: ankhein aankhen
naak: nak naaq
kaan: kan kaann
munh: muh moonh mun
daant: dant daaant
haath: hath haat
paon: paaon pao paoon
pet: pett
kamar: kmar kamarr
baal: bal baall
chehra: chehraa chehrah chera
jism: jisim jsm
jaan: jan jaaan
saans: sans sanss
walida: walidah valida
baap: bap baaap
maa: ma maaa
chachi: chachee chachhi
mamoo: mamu mamuu
mumani: mamani mumaani
khaloo: khalu khalo
phuphi: phupi phuppi
dulha: doolha dulhaa
dulhan: dulhn dulhann
saas: sas saass
sasur: susar sasar
saali: sali saalee
bhanja: bhanjaa
bhatija: bhateeja bhatijaa
pota: potaa
poti: potee
saheli: saheeli sahelee
parosi: padosi parosee
bachi: bachee bchi
bhaiya: bhaiyaa bhayya bhaia
aapi: api aapee
baji: bajee baaji
uncle: unkal ankal uncal
aunty: anty aunti anti
malik: maalik malk malikk
nokar: naukar nokr naukr
naukri: nokri naukree nokree
mazdoor: mazdur mazduur
kisaan: kisan kissan
dukandar: dukaandar dukandaar
driver: draiver driwar drivar
bhikari: bhikaari bhekari
chor: chorr choor
police: polis polic pulis
wakeel: vakeel wakil
dushman: dushmn dushmann
dushmani: dushmni dushmanee
rishta: rishtah rishtaa
nikah: nikaah nikkah
mehndi: mehendi mehandi
barat: baraat barrat
walima: waleema valima
jahez: jehaz jahaiz

# ---------------- home and everyday objects ----------------
kamra: kamraa kamrah
gas: gass
pankha: pankhaa pnkha
chaadar: chadar chaadr
takia: takya takiya
gadda: gada gaddaa
sofa: sofaa sofah
almari: alamari almaari
sheesha: shisha sheeshaa
pyala: piyala pyalaa
katora: katoraa katoara
thali: thaali thalee
churi: churee chhuri
chaaku: chaku chaqu
sui: soi suee
dhaaga: dhaga dhagaa
kapra: kapda kapraa
kapray: kapre kapde
libaas: libas libaass
chappal: chapal chappl chapall
jurab: jurrab jarab
cheez: chiz cheeez
saman: samaan saaman
copy: kapi copi kopi
pencil: pensil pencel pensel
rubber: rabar rubbar
ruler: roolar rular
diary: dairy daiary
file: fyle fiel
screen: skreen scren
charger: chargar charjar charjr
earphones: earfones iarphones
headphones: hedfones headfones
cable: kebal cabel
speaker: spekar speakar
remote: remot rimote
tv: tvv
ac: acc
heater: heatar hitar
shop: shap shopp
mall: mal maal
market: markit markat
road: rod roadd
gali: galee galli
chowk: chok chauk
mohalla: mohallah muhalla mohala
society: socity sosaiti
flat: flatt
plot: plott
makaan: makan makaaan
kiraya: kiraaya kirayah

# ---------------- food and drink ----------------
chicken: chiken chikan chikn
mutton: muttan mutan
beef: bif beaf
machli: machhli machlee
aloo: alu alloo
pyaz: piyaz pyaaz
tamatar: tamater tamatr tmatar
lehsan: lahsan lehsun
adrak: adrakk adrk
dhaniya: dhania dhaniyaa
haldi: haldee haaldi
zeera: jeera zeeraa jira
masala: masalah masaala
tel: tail tell
ghee: ghi gheee
makhan: makkhan makhn
dahi: dahee dahy
lassi: lassee lasi
paneer: panir paneerr
bread: bred breadd
biscuit: biskut biscut biskit
chocolate: chocolat choclate chocolet
icecream: iscream aiskreem icecrem
cake: kek caek
pizza: pitza piza
burger: burgar bargar
fries: fraiz frys
juice: jus juce
coffee: cofee kofi coffe
sharbat: sharbet sharbut
iftar: iftaar ifter
sehri: sahri sehree
saag: sag saagg
karela: karaila karelaa
bhindi: bhindee bhindy
gobi: gobhi gobee
matar: mattar matr
palak: palaak palk
seb: saib seeb
kela: kelaa kayla
angoor: angur anguur
santra: santara santraa
tarbooz: tarbuz tarboz
kharbooza: kharbuza kharbuzaa
anar: anaar anarr
khajoor: khajur khajuur
badam: baadam badaam
kaju: kajoo kaaju
pista: pistaa pistha
kishmish: kishmis kishmsh
maida: maidaa maeda
shehad: shahad shehd
nihari: nehari nihaari
haleem: halim haleemm
kabab: kebab kabaab
tikka: tika tikkaa
samosa: samosay samossa
pakora: pakoda pakoraa
chaat: chat chaatt
paratha: parantha parathaa parata
naan: nan naaan
halwa: halva halwaa
kheer: khir kheeer
jalebi: jalaibi jalebee
kulfi: kulfee kulfy
falooda: faluda faloodaa
karahi: karai karhai
korma: qorma kormaa
pulao: pulaao pulaw
sandwich: sandwitch sandwhich sandwch
roll: rol rolll
lunch: lanch lunc
dinner: dinar dinnr
breakfast: brekfast brakfast breakfst

# ---------------- places, nature, travel ----------------
mulk: mulq mulkk
duniya: dunya duniyaa
jagah: jaga jageh jgah
park: paark parkk
clinic: clinik clinc
train: tren trein
gaari: gari gaadi gaarhi
rickshaw: rikshaw rikshw riksha
flight: flite flaight
jahaz: jahaaz jahaj
samundar: samandar samundr
sehra: sahara sehraa
barf: baraf barff
dhoop: dhup dhoopp
city: siti sity
area: eria aria
block: blok blck
sector: sectar sekter
traffic: trafik trafic
parking: parkng parkin
diesel: dezal diesl

# ---------------- time and numbers ----------------
ghanta: ghantaa ghnta
minute: minat minit
second: secnd sekand
chheh: chhe chhey
saat: sat saaat
aath: ath aaath
nau: naw nao
gyarah: gyara gyaara
bees: bis beess
tees: tis teess
chalis: chalees chaalis
pachas: pachaas pachass
crore: karor kror
dedh: derh dehd
dugna: dugnaa
night: nait nyt naight
week: wik weak
month: manth munth
today: todai tdy
tomorrow: tomorow tmrw tommorow
yesterday: yesterdy yestrday
late: let lait
early: arly erly

# ---------------- education and work ----------------
class: clas klass cls
lecture: lecter lectur lacture
lab: labb
syllabus: silabus sylabus
degree: digree degri
course: cors kors
subject: subjct sabject
grade: grad gred
test: tast tesst
quiz: kwiz quizz
homework: homwork homewrk
principal: principle prinsipal
ustad: ustaad ustd
sabaq: sabak sbaq
fail: fel faail
position: posishan pozition
scholarship: scolarship scholership
admission: admisn admishan
semester: semister semestr
campus: campas kampus
library: libarary librery laibrary
hostel: hostal hostl
cafe: caffe kefe
canteen: canten canteeen
presentation: presentaton presantation
slides: slaids slaides
group: grup groop
leader: leedar lidar
manager: manajer manegar
company: compny kampany
business: bizness bussiness busines
salary: salry salari sallary
staff: stf staaf
client: clint cliant
customer: custmer kastmer
shift: shiift
duty: dyuti dooty
chutti: chhutti chuti
interview: intervew intarview
resume: rezume resum
deadline: dedline deadlin
task: taask
work: wrk wark
data: datta daata
system: sistem systm
website: websit websight
link: lnk linkk
server: sarver servar
code: kod codee
bug: bagg
update: apdate updat
install: instal instaal
download: downlod dawnload
upload: uplod apload

# ---------------- social media, tech, shopping, money ----------------
google: gogle googel
youtube: yutube utube youtub
facebook: fcebook fesbuk facbook
instagram: instgram instagrm
whatsapp: watsapp whatsap
tiktok: tiktock tictok
status: stetus statuss
story: stori
post: postt
comment: coment commnt
like: laik likee
share: shayr shaer
follow: folow folo
follower: folower followr
subscribe: subscrib sabscribe
channel: chanel chanal
live: lyv laiv
profile: profil prfile
picture: pikchar pictur
selfie: selfy selfee
network: netwrk netwark
package: pakage pakej
sim: simm
balance: balnce balans
load: lod loadd
notification: notifiction notfication
settings: setings setting
android: andriod androied
iphone: iphon ifone aiphone
samsung: samsng samsang
smartphone: smartfone smartphon
keyboard: kibord keybord
mouse: maus mowse
printer: printar prntr
hotspot: hotspt hotspott
gaming: gamng gameing
player: playar plyr
digital: digtal digitl
technology: tecnology techology tecnolgy
sound: saund sond
volume: volyum volum
display: displey disply
touch: tach tuch
memory: memry memori
storage: storege stoarge
processor: procesor prosesar
performance: perfomance parformance
review: reveiw riview
rating: reting ratng
seller: seler sellar
buyer: bayer baiyar
rider: raider raidar
tracking: trakking traking
rupay: rupaye rupee rupye
qeemat: keemat qimat
daam: dam daaam
khareedari: kharidari khareedaari
qarz: karz qarzz
qist: kist kisst
bill: bil billl
tax: taks taxx
amount: amnt amaunt
total: totl tottal
free: fri freee
extra: extrra ekstra
rate: ret raet
payment: paymnt peyment
parcel: parsal parcl pasal
courier: koriyar courior courer
address: adress adres addres
brand: brend brant
warranty: warrenty warrantee waranty
guarantee: garanty gurantee garantee
available: avilable availble
cancel: cancle kansal
exchange: exchenge exchang
complaint: complent complant
shikayat: shikayt shikaayat shikayet
fraud: frod frawd
scam: skam scamm
dhoka: dhokha dhokaa
tension: tenshan tenshun
loan: lon lown
insurance: insurnce inshurance
license: lisence licence liscense

# ---------------- feelings, ideas, abstract nouns ----------------
ishq: ishk ishqq
nafrat: nfrat nafratt
gham: ghm ghamm
intezar: intizar intazar
bharosa: bharoosa bharosaa bharosha
shak: shakk
sharam: sharm shaaram
sharminda: sharmindah sharmenda
fikar: fikr fiqr
hosla: housla hausla
jealous: jelous jalus
akela: akelaa akaila
tanha: tanhaa tanhah
dukhi: dukhee dukhy
bore: boar bor
mazaq: mazak mazaaq
muskurahat: muskuraht muskrahat
aansu: aansoo ansu
khwab: khawab khuwab
soch: sochh
dhyan: dhiyan dhyaan
yaqeen: yakeen yakin
imaan: iman eman eeman
sachai: sachayi sachae
haqeeqat: haqiqat haqeeqt
raaz: raz raaaz
dosti: dostee dosty
aqal: akal aql
zimmedari: zimadari zimmedaari
ghalti: galti ghalati
saza: sazaa
inaam: inam inaaam
mashwara: mashwra mashwarah
madad: madat madadd
kamyabi: kamyabee kamiyabi
nakami: nakaami nakamee
koshish: kosish koshis
mehnat: mehant mehnt
faida: fayda faidaa
nuqsan: nuksan nuqsaan
farq: fark farak
tareeka: tariqa tareeqa
tareekh: tarikh tareekhh
khabar: khabr khabarr
afwah: afwa afwaah
baat: bat baaat
batein: baatein baten
awaz: awaaz aawaz
lehja: lehjaa lehjah
naam: nam naaam
pehchan: pehchaan pehchan
umar: umr umarr
azmaish: azmaaish aazmaish
mauqa: moqa mouqa
zaroorat: zarurat zrurat
sahulat: sahoolat sahulut
dikkat: diqqat dikat
pareshani: pareshaani parishani
andaza: andaaza andazah
tajurba: tajruba tajarba
wada: waada vaada
naseeb: nasib naseb nasseb
qismat: kismat qismet
maut: mout mautt
janam: jannam janm
shabash: shabaash shabas
mubarakbad: mubarakbaad mubarkbad
khair: khayr khehr
khairiyat: khairiat khairyat khariyat
ji: jee jiii
haye: hae hayee
chakkar: chakar chakkr
tamasha: tamaasha tmasha
nakhray: nakhre nakhry
shor: shorr
abay: abe abey
chalein: chalain chalen

# ---------------- religion and culture ----------------
roza: rozaa roja
ramzan: ramazan ramadan
hajj: haj hajjj
umrah: umra umrahh
quran: qurran quraan kuran
hadees: hadis hadith
jannat: jannah jannt
jahannum: jahanum jahannam
gunah: gunaah gunha
sawab: sawaab swab
tauba: toba tobah
qasam: kasam qsam
fajar: fajr fjr
zuhr: zohr zuhar
maghrib: magrib maghreb
isha: esha ishaa
jumma: juma jumah
ameen: amin aameen
subhanallah: subhanalah subhanallh
bismillah: bismilah bismillh
astaghfirullah: astagfirullah astaghfirulla
rasool: rasul rassol
nabi: nabee nabii
maulana: molana moulana
dargah: dargaah darghah
milad: meelad milaad
naat: nat naaat
shayari: shairi shayri
film: filam fillm
drama: dramma dramaa
actor: acter aktor
actress: actres aktress
hero: heero heroo
singer: singar sinjer
naach: nach naaach
dance: dans dancce
funny: funy phunny
joke: jok joak
comedy: comdy kamedi
horror: horar horrer
action: acshan akshan
trailer: trailar trelar
cinema: sinema cenima
concert: consert konsert
mela: melaa
festival: festivl fastival

# ---------------- sports and fitness ----------------
football: footbal futbal
hockey: hocky hoki
tennis: tenis tenns
kabaddi: kabadi kabbadi
wicket: wiket wickt
batting: bating battng
bowling: boling bowlng
bowler: bowlar boler
batsman: batsmen betsman
chakka: chaka chakkaa
chauka: chowka chaukaa
out: aut owt
captain: kaptan captan
score: skor scor
win: winn wen
winner: winar
champion: champian chempion
trophy: trofi trophi
final: fainal finall
tournament: tornament tournment
stadium: stadum staduim
umpire: ampire umpyar
coach: coch koach
gym: jim gimm
workout: workot wrkout
diet: dyt daiet
exercise: exersize excercise
walk: wolk wak

# ---------------- English words in everyday Roman Urdu ----------------
thankyou: thanku thnku thankew
bye: baye byee
busy: bizzy bisy
ready: redy raidy
sure: shur shure
really: rely realy
maybe: mebe maibe
problem: prblm problam prob
solution: solusion salution
issue: ishu isue
idea: aidea idia
plan: plaan plann
program: progrm porgram
point: pont poit
question: qestion questin kwestion
answer: anser answr
correct: corect corrct
wrong: wrng rong
right: rite raiyt
danger: dangr denger
dangerous: dangrous dengerous
risk: rsk
help: hlp helpp
support: sapport suport
enjoy: enjoi anjoy
fun: funn phun
mood: mud moodd
style: stail stile
fashion: fashn feshion
look: luk lok
smart: smrt
cute: kyoot cutee
cool: kool cul
super: supar soper
perfect: perfct parfect
excellent: excelent exelent
awesome: awsome osm awesum
amazing: amazin amzing
worst: wrst warst
waste: west wastee
useless: useles uselss
damage: damege damaj
broken: brokn brokan
working: wrking workin
"""
