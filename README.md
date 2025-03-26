# DPS Menu Scraper

Turn PDFs Lunch menus into Calendars.

## Setup

One-time setup:
```bash
pip install -r requirements.txt
python setup.py
```

Set up Google API access as described [here](Google_API.md), [here](https://developers.google.com/workspace/guides/get-started), and [here](https://developers.google.com/calendar/api/quickstart/python).

## Usage

To (re-)generate calendar menus:
```bash
python pdf_2_ics.py
```

The repository has also been set up to run the above script via a Github Actions workflow. It is currently configured to run once a night, for the first 5 days of each month. This creates a ZIP of the created ICS files, which can then be downloaded by the repository owners. It can then be posted as outlined below to the set of Google Calendars maintained by the same folks.

To post events to calendars (if you have write access):
```bash
python gcal.py
```

This has been tested with Python 3.11.11 and the following library versions:

```
arrow==1.3.0
attrs==25.1.0
beautifulsoup4==4.13.3
cachetools==5.5.1
certifi==2025.1.31
charset-normalizer==3.4.1
click==8.1.8
colorama==0.4.6
emoji==2.14.1
google-api-core==2.24.1
google-api-python-client==2.161.0
google-auth==2.38.0
google-auth-httplib2==0.2.0
google-auth-oauthlib==1.2.1
googleapis-common-protos==1.67.0
httplib2==0.22.0
ics==0.7.2
idna==3.10
joblib==1.4.2
lxml==5.3.1
nltk==3.9.1
oauthlib==3.2.2
proto-plus==1.26.0
protobuf==5.29.3
pyasn1==0.6.1
pyasn1_modules==0.4.1
pyparsing==3.2.1
pypdf==5.3.0
python-dateutil==2.9.0.post0
python-docx==1.1.2
pytz==2025.1
regex==2024.11.6
requests==2.32.3
requests-oauthlib==2.0.0
rsa==4.9
six==1.17.0
soupsieve==2.6
TatSu==5.13.1
tqdm==4.67.1
types-python-dateutil==2.9.0.20241206
typing_extensions==4.12.2
uritemplate==4.1.1
urllib3==2.3.0
```

## Critical Acclaim

> “Gods!! This calendar link is amazing! Thank you sooooooo much!!”

> “Thank you!! Super helpful, much appreciated!!”

> “David, this is seriously the best email I’ve ever gotten!!! Thank you so much, looking up the menu everyday was so annoying, and my only old-guy solution was printing it onto paper 😂 … AMAZING!”

> “This is amazing, David. My kiddo will not eat at school anymore (infuriating) but I know a lot of people will truly get a lot out of this. And right now, using our superpowers for the greater good is all we got! And it is extra important. Thanks“

> “You sir are the man! Well done!”

> “Incredible”

> “Not all hoagies wear capes. Thanks David!”

> “Thanks David! …  I've heard from a lot of folks that the menu situation is annoying. So definitely it would be valuable to host on [ekpowe.org](http://ekpowe.org/) for families as well.“

> “Works great!!! Thanks!”

> “This is awesome. Thanks!”

> “Those are serious superpowers, David! awesome!”

> “This is fantastic! My son asks about the menu every morning and I love having it on my calendar.”

## Get the calendars!

- [DPS - Elementary School Lunch Menu](https://calendar.google.com/calendar/embed?src=e033ace1eabc7f445f279e48c1492cd0e5db67aef703ca0c93acb5d980d6ba84%40group.calendar.google.com&ctz=America%2FNew_York) [ical](https://calendar.google.com/calendar/ical/e033ace1eabc7f445f279e48c1492cd0e5db67aef703ca0c93acb5d980d6ba84%40group.calendar.google.com/public/basic.ics)
- [DPS - Menú Almuerzo Escuela Elemental](https://calendar.google.com/calendar/embed?src=9d2d4085f41a4590166d8ffc53ddad4dda719e774d4d33199bc7a074c3644955%40group.calendar.google.com&ctz=America%2FNew_York) [ical](https://calendar.google.com/calendar/ical/9d2d4085f41a4590166d8ffc53ddad4dda719e774d4d33199bc7a074c3644955%40group.calendar.google.com/public/basic.ics)
- [DPS - Middle School Lunch Menu](https://calendar.google.com/calendar/embed?src=aa6e7d0349a33681b17ed1dcaeec77de4dd48c5c4cb3b88e5248d6970f974ea5%40group.calendar.google.com&ctz=America%2FNew_York) [ical](https://calendar.google.com/calendar/ical/aa6e7d0349a33681b17ed1dcaeec77de4dd48c5c4cb3b88e5248d6970f974ea5%40group.calendar.google.com/public/basic.ics)
- [DPS - Menú Almuerzo Escuela Secundaria](https://calendar.google.com/calendar/embed?src=2bb8971f94aec9f659533e827184663b3a997a669f4fbe4c3d6251d664545c4d%40group.calendar.google.com&ctz=America%2FNew_York) [ical](https://calendar.google.com/calendar/ical/2bb8971f94aec9f659533e827184663b3a997a669f4fbe4c3d6251d664545c4d%40group.calendar.google.com/public/basic.ics)
- [DPS - Menú Almuerzo Escuela Intermedia](https://calendar.google.com/calendar/embed?src=25481c7e9c55e194b3a403147b08a60ebb7c172ed806fa1f415006ee4279e848%40group.calendar.google.com&ctz=America%2FNew_York) [ical](https://calendar.google.com/calendar/ical/25481c7e9c55e194b3a403147b08a60ebb7c172ed806fa1f415006ee4279e848%40group.calendar.google.com/public/basic.ics)
- [DPS - High School Lunch Menu](https://calendar.google.com/calendar/embed?src=f43adf5cc404f764f1117c696a46822123284ddd9fb29787fa24987307c6ce66%40group.calendar.google.com&ctz=America%2FNew_York) [ical](https://calendar.google.com/calendar/ical/f43adf5cc404f764f1117c696a46822123284ddd9fb29787fa24987307c6ce66%40group.calendar.google.com/public/basic.ics)
- [DPS - Breakfast in Classroom School Breakfast Menu](https://calendar.google.com/calendar/embed?src=df27dbb6e42cc1d73ea68a0b347d01045e0f675bed503de0d9398a553fdfef04%40group.calendar.google.com&ctz=America%2FNew_York) [ical](https://calendar.google.com/calendar/ical/df27dbb6e42cc1d73ea68a0b347d01045e0f675bed503de0d9398a553fdfef04%40group.calendar.google.com/public/basic.ics)
- [DPS - K12 School Afterschool Snack Menu](https://calendar.google.com/calendar/embed?src=bcfd3480f426a8d1990bd619f4a888aa2188047795925985e4bf9cc50080ac0d%40group.calendar.google.com&ctz=America%2FNew_York) [ical](https://calendar.google.com/calendar/ical/bcfd3480f426a8d1990bd619f4a888aa2188047795925985e4bf9cc50080ac0d%40group.calendar.google.com/public/basic.ics)
- [DPS - K12 School Breakfast Menu](https://calendar.google.com/calendar/embed?src=7cda9ed521242ca7f784e4be49659ea7bd0e111254d624a484856d393a46185d%40group.calendar.google.com&ctz=America%2FNew_York) [ical](https://calendar.google.com/calendar/ical/7cda9ed521242ca7f784e4be49659ea7bd0e111254d624a484856d393a46185d%40group.calendar.google.com/public/basic.ics)
- [DPS - PreK School Breakfast Menu](https://calendar.google.com/calendar/embed?src=49070180e250dc55fc9b9fb50f8af587ca8f0d185d0071b0f8a0a165795fa47a%40group.calendar.google.com&ctz=America%2FNew_York) [ical](https://calendar.google.com/calendar/ical/49070180e250dc55fc9b9fb50f8af587ca8f0d185d0071b0f8a0a165795fa47a%40group.calendar.google.com/public/basic.ics)
- [DPS - PreK School Lunch Menu](https://calendar.google.com/calendar/embed?src=f549af9de7f100ae4ffae580797d614a77e69ac66ebb022d4813a6c96de91b50%40group.calendar.google.com&ctz=America%2FNew_York) [ical](https://calendar.google.com/calendar/ical/f549af9de7f100ae4ffae580797d614a77e69ac66ebb022d4813a6c96de91b50%40group.calendar.google.com/public/basic.ics)
- [DPS - PreK School Snack Menu](https://calendar.google.com/calendar/embed?src=fe8ad901d2cf0c82cd5c432977a0fe373e5c636dcdc63c330e95c79953d703d6%40group.calendar.google.com&ctz=America%2FNew_York) [ical](https://calendar.google.com/calendar/ical/fe8ad901d2cf0c82cd5c432977a0fe373e5c636dcdc63c330e95c79953d703d6%40group.calendar.google.com/public/basic.ics)
- [DPS - Menú Desayuno Escuela Desayuno en el Aula](https://calendar.google.com/calendar/embed?src=9f5ac2b3a512255654fc0c989b0e9f9cf2d01b0aaaa1a6ed0d476345d716fa72%40group.calendar.google.com&ctz=America%2FNew_York) [ical](https://calendar.google.com/calendar/ical/9f5ac2b3a512255654fc0c989b0e9f9cf2d01b0aaaa1a6ed0d476345d716fa72%40group.calendar.google.com/public/basic.ics)
- [DPS - Menú Meriendas Después de Clases Escuela K12](https://calendar.google.com/calendar/embed?src=79e83fe767d41b79f70f4166a2da3e2268fc08afef2054a24da82810ef4aa9e4%40group.calendar.google.com&ctz=America%2FNew_York) [ical](https://calendar.google.com/calendar/ical/79e83fe767d41b79f70f4166a2da3e2268fc08afef2054a24da82810ef4aa9e4%40group.calendar.google.com/public/basic.ics)
- [DPS - Menú Desayuno Escuela K12](https://calendar.google.com/calendar/embed?src=239a570eb9534fb421707056c2a6d66c9eceb64fa75d187f56b344759cf4e0da%40group.calendar.google.com&ctz=America%2FNew_York) [ical](https://calendar.google.com/calendar/ical/239a570eb9534fb421707056c2a6d66c9eceb64fa75d187f56b344759cf4e0da%40group.calendar.google.com/public/basic.ics)
- [DPS - Menú Desayuno Escuela PreK](https://calendar.google.com/calendar/embed?src=70397351d0ae781bdf4f70a2829c38dbf926fdd7d4878ff06537801710ee36ac%40group.calendar.google.com&ctz=America%2FNew_York) [ical](https://calendar.google.com/calendar/ical/70397351d0ae781bdf4f70a2829c38dbf926fdd7d4878ff06537801710ee36ac%40group.calendar.google.com/public/basic.ics)
- [DPS - Menú Almuerzo Escuela PreK](https://calendar.google.com/calendar/embed?src=ab6c50f1b38abeafeaa860eecbc3bef1c838cb5849c8c7b2ed0ba5b61aa84635%40group.calendar.google.com&ctz=America%2FNew_York) [ical](https://calendar.google.com/calendar/ical/ab6c50f1b38abeafeaa860eecbc3bef1c838cb5849c8c7b2ed0ba5b61aa84635%40group.calendar.google.com/public/basic.ics)
- [DPS - Menú Merienda En la Escuela Escuela PreK](https://calendar.google.com/calendar/embed?src=588c0960558a35ba62c2e521cd0d648f54d09d67ea16d52f6625c67484745117%40group.calendar.google.com&ctz=America%2FNew_York) [ical](https://calendar.google.com/calendar/ical/588c0960558a35ba62c2e521cd0d648f54d09d67ea16d52f6625c67484745117%40group.calendar.google.com/public/basic.ics)
