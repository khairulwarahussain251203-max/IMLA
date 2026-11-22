"""
Seed lexicon: canonical spelling -> hand-written noisy variants.

Format of every line:   canonical: variant variant variant ...

CANONICAL CONVENTION (also stated in proposal.md)
  1. lowercase, letters only
  2. the most common "dictionary style" spelling, chosen by the author
  3. one canonical form per word (gender / number forms are different words)
  4. English words used in Roman Urdu (quality, delivery ...) keep their
     standard English spelling as the canonical form

The generator in data_gen.py adds many more machine-made variants on top
of the hand-written ones, so this file only needs a few per word.
"""

from .lexicon_more import LEX_MORE  # third vocabulary block (see lexicon_more.py)

LEX_TEXT = """
hai: hay hy hei
hain: hen hein hn hayn
tha: thaa tah
thi: thee thy thii
hoga: hogaa hoga
hogi: hogee hogy
kya: kia kyaa kyah kiaa
kyun: kyu kyon kiun kyunn
kaise: kese kaisay kesay kaisey
kahan: kahaan kahn
kab: kabb
kaun: kon kaaun kown
kitna: kitnaa ktna
kitni: kitnee ktni
koi: koee koyi
kuch: kch kuchh kuchch
bohat: bohot bahut bhot bht bohut boht bahot
nahi: nahin nahee nhi nai nahe nhin
haan: han haa haaan hann
acha: achha accha achaa achcha achhaa
achi: achhi acchi achee achy achhy
bura: buraa bora
buri: buree
behtareen: behtrin bhetreen behtarin
zabardast: zabrdast zabardasst zabardust zaberdast
kamal: kamaal kmal kamall
shandar: shandaar shaandar shanadar
mazedar: mazaydar mazedaar mazadar
mehngi: mahngi mehangi mehngee mahengi
mehnga: mahnga mehanga mehngaa
sasta: sastaa sastha
kharab: kharaab khrab kharabb kharap
theek: thik thek thikk theeek
sahi: sahee shi sahih
galat: ghalat galt galatt
pasand: psnd pasandd pasaand
pyara: piara pyaara pyaraa
khoobsurat: khubsurat khoobsoorat khubsoorat
bekar: bekaar bakaar bekarr
bakwas: bakwaas bakvas bkwas bakwass
shukriya: shukria shukriyaa shukriyah
mubarak: mubaarak mubarik mubarakk
dost: dosst dos
yaar: yar yaaar yaarr
bhai: bhae bhaii bhay bhaee
ammi: ami amiii
abbu: abu abbo
ghar: ghr ghur gher
paisa: pesa paise paisay
kaam: kaaam kaama
log: logg
waqt: wakt waqat wqt
din: dinn
raat: raatt rat
subah: subha sbah
shaam: sham shaaam
aaj: aj ajj
kal: kall
abhi: abi abhee abhii
phir: fir phr pher fer
lekin: lekn laikin lakin
magar: mgr mager magarr
aur: or our aor awr
agar: agr aggar
bhi: bhee bi bhii
sirf: srf sirff
bas: bus bass
bilkul: bilkl bilcul bilkull
zaroor: zarur zaror zarroor
pehle: pehlay pahle pehly
baad: bad baaad
saath: sath saaath
sab: sub
mujhe: mujhy mjhe mujhay mujhey
tumhein: tumhe tumhain tmhe
hamein: hamen humein hmen
apna: apnaa
apni: apnee apny
mera: meraa mra
meri: merii mri
tumhara: tumhaara tumhra
unka: unkaa
uska: uskaa
wala: walaa vala
wali: valee walee
lagta: lagtaa lagtta
karna: krna karnaa
karo: kro karoo
dekho: dkho dekhoo
suno: sunoo
batao: btao bataao
chalo: chlo chaloo
aao: ao aaoo
jao: jaao jaoo
jana: jaana jaanaa jna
aana: ana aanaa
dena: denaa
khana: khaana khanaa
peena: pina pena
rehna: rahna rehnaa
kehna: kahna kehnaa
samajh: samjh samaj smjh
pata: pta pataa
maloom: malum maaloom mloom
chahiye: chahiyay chaiye chahye chahiey
chahta: chahtaa chahtha
mushkil: mushkill mushkl
asaan: asan aasan
zyada: zyadah ziada zada jyada zayada ziyada
kam: kamm
thora: thoda thorra thoraa
bara: bada barra baraa
chota: chotaa chhota chotta
naya: nayaa nya
purana: puraana prana
quality: qwality qualiti kwality quolity qualty
delivery: delivry delivary delivri dilivery
service: sarvis servis sarvice
price: prise prais pries
product: prodect prduct prodact
order: ordar oder ordr
time: tym taim tiem
phone: fone phon foon
battery: batry bettery batary
camera: kamera camra
packing: pakeging pakking packaging
size: sise saiz
color: colur kalar
fast: fst faast
slow: slo sloww
original: orignal orijinal originl
fake: fek faake
refund: rifund refnd
return: ritrn retrun
money: mani muney
wasool: wasul vasool
mazay: maze mazey
dukaan: dukan dukaann
jaldi: jldi jaldee jaldy
der: derr
insaan: insan insaaan
zindagi: zindgi zindagee zindagy
pyar: piyar pyaar pyaaar
dil: dill
sach: sachh
jhoot: jhut jhoott
masla: maslaa mussla mesla
dua: duaa duaaa
wapas: wapis vapas wapass
naraz: naraaz narazz
khush: khushh khusssh
udaas: udas udaaas
kafi: kaafi kafee
poora: pura puraa
alag: alg
mehfooz: mahfooz mehfuz
maine: mene meine mainay
tum: tm tumm
aap: ap aapp
hum: hm humm
woh: wo voh
yeh: ye yh
yahan: yahaan yhan yaha
wahan: wahaan whan waha
isliye: isliay islie isleye
kyunke: kyunki kyuke kiunke
jab: jabb
tab: tabb
raha: rha rahaa
rahi: rhi rahee
rahe: rhe rahay
gaya: gya gayaa
gayi: gyi gai gayee
gaye: gye gaey
hua: huaa hwa
hui: huee hwi
hue: huay hwe
ke: kay
ki: kee ky
ka: kaa
ko: koo
se: say sy
ne: nay
par: pr parr
mein: maiin meinn mn
tak: takk
liye: liay lie liey
bahar: bahir bahaar bhr
andar: ander andr
upar: oper upr ooper
neeche: neechay niche nichay
sabse: sabsay sbse
salam: slam salaam
assalamualaikum: asalamualaikum aslamualaikum salamalaikum
inshallah: inshaallah inshaallh inshalla
mashallah: mashaallah mashaalah
alhamdulillah: alhamdullilah alhamdulilah
"""


# ----------------------------------------------------------------------------
# Extended vocabulary (everyday words: family, places, food, tech, school,
# numbers, colours, emotions, verbs, adjectives, connectors, code-mixed English)
# ----------------------------------------------------------------------------
LEX_EXTRA = """
dekh: dekhh dkh
ho: hoo
aya: aaya ayaa
zaya: zayaa zaaya
umeed: umid ummeed
aisi: aesi aisee
lena: lenaa
main: mai mainn
beta: betaa bta
beti: betii betee
behen: bhen behn behan
bhabhi: bhabi bhabhii
dada: daada dadaa
dadi: daadi dadii
nana: naana nanaa
nani: naani nanii
chacha: chachaa chachha
mama: maama mamaa
khala: khalaa khalla
phupho: phuppo phuphoo
biwi: bivi beewi
shohar: shauhar shohr
bacha: bachaa bcha
bachay: bachey bache bchay
larka: larkaa laraka
larki: larkee larky
admi: aadmi admee
aurat: orat awrat
banda: bandaa bnda
sahab: sahib saahab
sir: ser
madam: madm madum
teacher: techer tcher teachr
student: studnt stdnt studant
family: fmly famly
school: skool scool skul
college: colege collage
university: universty univrsity
office: ofice offis
bazaar: bazar bazr
shehar: sheher shehr
gaon: gaaon gaoon
masjid: masjd masjeed
lahore: lahor lahaur
karachi: krachi karchi
islamabad: islmabad islamabaad
rawalpindi: rawalpindy rawalpndi
pakistan: pakstan paksitan
kitab: kitaab ketab
paani: pani paanee
chai: chae chay
doodh: dudh dood
roti: rotee rooti
chawal: chaawal chawl
gosht: gost goshat
sabzi: sabzee sabji
mithai: methai mithae
cheeni: chini cheni
namak: namk namack
mirch: mirchh
anda: andaa
biryani: biriyani biryaani
nashta: nasta nashtaa
dopahar: dopehar dupehar
mobile: mobil mobail
laptop: laptp labtop
internet: intarnet internt
wifi: wyfi waifai
app: appp
software: softwear sftware
computer: comptr computr kamputar
video: vedio vidio
photo: foto phto
message: msg mesage massage
call: kaal cal
number: nmbr numbr
password: pasword passwrd
account: acount accnt
online: onlin onlne
offline: ofline offlin
email: emal imail
game: gem gaim
movie: moovie muvi
song: songg
music: musik mujik
party: partee pary
job: jobb jub
boss: bos bs
meeting: meting miting
project: projct prjct
report: reprt ripot
assignment: asignment assignmnt
exam: eksam egzam
paper: pepar paaper
result: rizult resalt
marks: marx
fee: fees
bank: bnk bankk
card: kard
cash: kash caash
discount: discont diskount
sale: sel sael
offer: ofer ofr
shopping: shoping shopng
cricket: crickt kricket
match: mach matc
team: tim teem
friend: frnd frend
love: luv lov
life: laif lyf
happy: hapy haapy
sad: sadd
good: gud gd
nice: nise nyc
best: bst
very: vry
sorry: sory soory
please: plz pls plis
thanks: thx thnx thanx
welcome: welcom wlcm
hello: helo hellow
ok: okay okk
hafta: haftaa
mahina: mahena maheena
saal: sal saall
parson: parsoon prson
ek: aik ik
do: doo
teen: tin teeen
char: chaar
paanch: panch paach
das: dus
hazaar: hazar hazaaar
lakh: lakhh lac
laal: lal laall
neela: nila neelaa
peela: pila peelaa
hara: haraa
kala: kalaa
safed: safaid saafed
gussa: ghussa gusa
khushi: khushee khushii
dukh: dukhh
dar: darr
pareshan: pareshaan parishan
thaka: thakaa thka
bimar: beemar bimaar
sehat: sehet sehhat
hairan: hairaan hayran
parhna: padhna prhna parhnaa
likhna: likna likhnaa
sunna: sunnaa
bolna: bolnaa
sochna: sochnaa
bhoolna: bhulna bhoolnaa
yaad: yad yaaad
kholna: kholnaa
band: bandd
dhoondna: dhundna dhoondnaa
bhejna: bhejnaa
lana: laana
rakhna: rkhna rakhnaa
uthna: uthnaa
baithna: bethna baithnaa
khelna: kehlna khelnaa
hasna: hasnaa
rona: ronaa
chalna: chlna chalnaa
rukna: ruknaa
daudna: dodna daudnaa
sikhna: seekhna sikhnaa
jeetna: jitna jeetnaa
sakta: saktaa skta
sakti: saktee skti
aata: ata atta
jata: jaata jta
karta: kartaa krta
karti: kartee krti
karein: karain karen
milta: miltaa
hota: hotaa
hoti: hotee
lamba: lambaa
moota: mota mootaa
patla: patlaa
garam: garm garamm
thanda: thandaa thanda
saaf: saf
ganda: gandaa gnda
tez: taiz tezz
dheema: dhima
bhaari: bhari bhaaree
halka: halkaa
zaroori: zaruri zarori zarooree
khaas: khas khass
aam: aaam
sachcha: sacha sachha
nazdeek: nazdik nazdeeq
door: dur dorr
warna: varna warnaa
yani: yaani yaanee
matlab: matlb mtlb
aisa: aesa aysa
waisa: vaisa waesa
jaisa: jesa jaisaa
is: iss
us: uss
unhone: unhoun unhon
usne: usnay
isne: isnay
humne: hamne humnay
tumne: tmne tumnay
humara: hamara humaara
wah: waah wahh
khaya: khaaya khya
piya: pia piyaa
diya: dia diyaa
liya: lia liyaa
kiya: kiyaa
dekha: dekhaa
suna: sunaa
bola: bolaa
socha: sochaa
samjha: samjhaa samjah
likha: likhaa
parha: padha parhaa
chala: chalaa
mila: milaa
kaha: kahaa
bhaga: bhagaa
sikha: sikhaa
bheja: bhejaa
laya: layaa
rakha: rakhaa
uth: uthh
baith: baithh
chup: chupp
arre: are arey
oye: oy oyee
uff: uf ufff
khuda: khudaa
allah: alah allaah
hafiz: hafeez hafiiz
maaf: maf maff
shukar: shukr shukkar
afsos: afsoos afsus
mat: matt
zara: zra zarah
hamesha: hmesha humesha
kabhi: kabi kabhee
shayad: shyd shaayad
"""

# Everyday words that are deliberately NOT in the lexicon. They are used only to
# test "leave unknown words alone" (gold answer = the word itself). They never
# appear in training and are never known to the dictionary.
OOV_WORDS = """
mausam bijli sadak imtihan natija sawal jawab kahani taleem sarkar awam mohabbat tareef khayal
tohfa mehman shadi eid namaz safar manzil rasta mitti aasman zameen sooraj chand taray barish hawa
aag darya pahar jangal khidmat insaaf izzat ilm pardes watan azadi jashan tehzeeb zubaan lafz shair
ghazal qissa dastaan tasveer aaina khidki darwaza chhat deewar kursi mez bistar kambal chabi taala
ghari chasma joota kameez shalwar dupatta topi angoothi bartan chamach table window bag pen notebook
shirt jacket shoes bottle glass plate ticket signal petrol engine tyre bike taxi hotel hospital
doctor medicine injection mask tablet fridge fan light switch camel horse sheep goat tiger parrot
sparrow garden flower tree river ocean island bridge station airport passport visa
""".split()


def parse_lexicon(text: str = None):
    """Return {canonical: [hand-written variants]} (order preserved).

    Default text = LEX_TEXT + LEX_EXTRA + LEX_MORE. If a canonical word appears
    in more than one block its variants are merged instead of overwritten.
    """
    if text is None:
        text = LEX_TEXT + "\n" + LEX_EXTRA + "\n" + LEX_MORE
    lex = {}
    for line in text.strip().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        canon, variants = line.split(":", 1)
        canon = canon.strip()
        bucket = lex.setdefault(canon, [])
        for v in variants.split():
            if v and v not in bucket:
                bucket.append(v)
    return lex


# Words that carry sentiment in the synthetic review generator. They are always
# kept in the *training* word split so the extrinsic experiment measures
# normalization quality, not whether a sentiment word happened to be held out.
POS_NONGENDER = ["behtareen", "zabardast", "kamal", "shandar", "mazedar"]
NEG_NONGENDER = ["kharab", "bekar", "bakwas", "galat"]
NOUNS_M = ["product", "phone", "camera", "order", "size", "price"]
NOUNS_F = ["quality", "delivery", "service", "battery", "packing"]
