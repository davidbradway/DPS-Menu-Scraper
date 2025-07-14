const calendars = [
    {
        name: "DPS - Elementary School Lunch Menu",
        embed_url: "https://calendar.google.com/calendar/embed?src=e033ace1eabc7f445f279e48c1492cd0e5db67aef703ca0c93acb5d980d6ba84%40group.calendar.google.com&ctz=America%2FNew_York",
        ical_url: "https://calendar.google.com/calendar/ical/e033ace1eabc7f445f279e48c1492cd0e5db67aef703ca0c93acb5d980d6ba84%40group.calendar.google.com/public/basic.ics"
    },
    {
        name: "DPS - Menú Almuerzo Escuela Elemental",
        embed_url: "https://calendar.google.com/calendar/embed?src=9d2d4085f41a4590166d8ffc53ddad4dda719e774d4d33199bc7a074c3644955%40group.calendar.google.com&ctz=America%2FNew_York",
        ical_url: "https://calendar.google.com/calendar/ical/9d2d4085f41a4590166d8ffc53ddad4dda719e774d4d33199bc7a074c3644955%40group.calendar.google.com/public/basic.ics"
    },
    {
        name: "DPS - Middle School Lunch Menu",
        embed_url: "https://calendar.google.com/calendar/embed?src=aa6e7d0349a33681b17ed1dcaeec77de4dd48c5c4cb3b88e5248d6970f974ea5%40group.calendar.google.com&ctz=America%2FNew_York",
        ical_url: "https://calendar.google.com/calendar/ical/aa6e7d0349a33681b17ed1dcaeec77de4dd48c5c4cb3b88e5248d6970f974ea5%40group.calendar.google.com/public/basic.ics"
    },
    {
        name: "DPS - Menú Almuerzo Escuela Secundaria",
        embed_url: "https://calendar.google.com/calendar/embed?src=2bb8971f94aec9f659533e827184663b3a997a669f4fbe4c3d6251d664545c4d%40group.calendar.google.com&ctz=America%2FNew_York",
        ical_url: "https://calendar.google.com/calendar/ical/2bb8971f94aec9f659533e827184663b3a997a669f4fbe4c3d6251d664545c4d%40group.calendar.google.com/public/basic.ics"
    },
    {
        name: "DPS - Menú Almuerzo Escuela Intermedia",
        embed_url: "https://calendar.google.com/calendar/embed?src=25481c7e9c55e194b3a403147b08a60ebb7c172ed806fa1f415006ee4279e848%40group.calendar.google.com&ctz=America%2FNew_York",
        ical_url: "https://calendar.google.com/calendar/ical/25481c7e9c55e194b3a403147b08a60ebb7c172ed806fa1f415006ee4279e848%40group.calendar.google.com/public/basic.ics"
    },
    {
        name: "DPS - High School Lunch Menu",
        embed_url: "https://calendar.google.com/calendar/embed?src=f43adf5cc404f764f1117c696a46822123284ddd9fb29787fa24987307c6ce66%40group.calendar.google.com&ctz=America%2FNew_York",
        ical_url: "https://calendar.google.com/calendar/ical/f43adf5cc404f764f1117c696a46822123284ddd9fb29787fa24987307c6ce66%40group.calendar.google.com/public/basic.ics"
    },
    {
        name: "DPS - Breakfast in Classroom School Breakfast Menu",
        embed_url: "https://calendar.google.com/calendar/embed?src=df27dbb6e42cc1d73ea68a0b347d01045e0f675bed503de0d9398a553fdfef04%40group.calendar.google.com&ctz=America%2FNew_York",
        ical_url: "https://calendar.google.com/calendar/ical/df27dbb6e42cc1d73ea68a0b347d01045e0f675bed503de0d9398a553fdfef04%40group.calendar.google.com/public/basic.ics"
    },
    {
        name: "DPS - K12 School Afterschool Snack Menu",
        embed_url: "https://calendar.google.com/calendar/embed?src=bcfd3480f426a8d1990bd619f4a888aa2188047795925985e4bf9cc50080ac0d%40group.calendar.google.com&ctz=America%2FNew_York",
        ical_url: "https://calendar.google.com/calendar/ical/bcfd3480f426a8d1990bd619f4a888aa2188047795925985e4bf9cc50080ac0d%40group.calendar.google.com/public/basic.ics"
    },
    {
        name: "DPS - K12 School Breakfast Menu",
        embed_url: "https://calendar.google.com/calendar/embed?src=7cda9ed521242ca7f784e4be49659ea7bd0e111254d624a484856d393a46185d%40group.calendar.google.com&ctz=America%2FNew_York",
        ical_url: "https://calendar.google.com/calendar/ical/7cda9ed521242ca7f784e4be49659ea7bd0e111254d624a484856d393a46185d%40group.calendar.google.com/public/basic.ics"
    },
    {
        name: "DPS - PreK School Breakfast Menu",
        embed_url: "https://calendar.google.com/calendar/embed?src=49070180e250dc55fc9b9fb50f8af587ca8f0d185d0071b0f8a0a165795fa47a%40group.calendar.google.com&ctz=America%2FNew_York",
        ical_url: "https://calendar.google.com/calendar/ical/49070180e250dc55fc9b9fb50f8af587ca8f0d185d0071b0f8a0a165795fa47a%40group.calendar.google.com/public/basic.ics"
    },
    {
        name: "DPS - PreK School Lunch Menu",
        embed_url: "https://calendar.google.com/calendar/embed?src=f549af9de7f100ae4ffae580797d614a77e69ac66ebb022d4813a6c96de91b50%40group.calendar.google.com&ctz=America%2FNew_York",
        ical_url: "https://calendar.google.com/calendar/ical/f549af9de7f100ae4ffae580797d614a77e69ac66ebb022d4813a6c96de91b50%40group.calendar.google.com/public/basic.ics"
    },
    {
        name: "DPS - PreK School Snack Menu",
        embed_url: "https://calendar.google.com/calendar/embed?src=fe8ad901d2cf0c82cd5c432977a0fe373e5c636dcdc63c330e95c79953d703d6%40group.calendar.google.com&ctz=America%2FNew_York",
        ical_url: "https://calendar.google.com/calendar/ical/fe8ad901d2cf0c82cd5c432977a0fe373e5c636dcdc63c330e95c79953d703d6%40group.calendar.google.com/public/basic.ics"
    },
    {
        name: "DPS - Menú Desayuno Escuela Desayuno en el Aula",
        embed_url: "https://calendar.google.com/calendar/embed?src=9f5ac2b3a512255654fc0c989b0e9f9cf2d01b0aaaa1a6ed0d476345d716fa72%40group.calendar.google.com&ctz=America%2FNew_York",
        ical_url: "https://calendar.google.com/calendar/ical/9f5ac2b3a512255654fc0c989b0e9f9cf2d01b0aaaa1a6ed0d476345d716fa72%40group.calendar.google.com/public/basic.ics"
    },
    {
        name: "DPS - Menú Meriendas Después de Clases Escuela K12",
        embed_url: "https://calendar.google.com/calendar/embed?src=79e83fe767d41b79f70f4166a2da3e2268fc08afef2054a24da82810ef4aa9e4%40group.calendar.google.com&ctz=America%2FNew_York",
        ical_url: "https://calendar.google.com/calendar/ical/79e83fe767d41b79f70f4166a2da3e2268fc08afef2054a24da82810ef4aa9e4%40group.calendar.google.com/public/basic.ics"
    },
    {
        name: "DPS - Menú Desayuno Escuela K12",
        embed_url: "https://calendar.google.com/calendar/embed?src=239a570eb9534fb421707056c2a6d66c9eceb64fa75d187f56b344759cf4e0da%40group.calendar.google.com&ctz=America%2FNew_York",
        ical_url: "https://calendar.google.com/calendar/ical/239a570eb9534fb421707056c2a6d66c9eceb64fa75d187f56b344759cf4e0da%40group.calendar.google.com/public/basic.ics"
    },
    {
        name: "DPS - Menú Desayuno Escuela PreK",
        embed_url: "https://calendar.google.com/calendar/embed?src=70397351d0ae781bdf4f70a2829c38dbf926fdd7d4878ff06537801710ee36ac%40group.calendar.google.com&ctz=America%2FNew_York",
        ical_url: "https://calendar.google.com/calendar/ical/70397351d0ae781bdf4f70a2829c38dbf926fdd7d4878ff06537801710ee36ac%40group.calendar.google.com/public/basic.ics"
    },
    {
        name: "DPS - Menú Almuerzo Escuela PreK",
        embed_url: "https://calendar.google.com/calendar/embed?src=ab6c50f1b38abeafeaa860eecbc3bef1c838cb5849c8c7b2ed0ba5b61aa84635%40group.calendar.google.com&ctz=America%2FNew_York",
        ical_url: "https://calendar.google.com/calendar/ical/ab6c50f1b38abeafeaa860eecbc3bef1c838cb5849c8c7b2ed0ba5b61aa84635%40group.calendar.google.com/public/basic.ics"
    },
    {
        name: "DPS - Menú Merienda En la Escuela Escuela PreK",
        embed_url: "https://calendar.google.com/calendar/embed?src=588c0960558a35ba62c2e521cd0d648f54d09d67ea16d52f6625c67484745117%40group.calendar.google.com&ctz=America%2FNew_York",
        ical_url: "https://calendar.google.com/calendar/ical/588c0960558a35ba62c2e521cd0d648f54d09d67ea16d52f6625c67484745117%40group.calendar.google.com/public/basic.ics"
    }
];

const calendarContainer = document.getElementById('calendars');
const calendarList = document.createElement('ul');

calendars.forEach(calendar => {
    const listItem = document.createElement('li');
    listItem.innerHTML = `<a href="${calendar.embed_url}">${calendar.name}</a> [<a href="${calendar.ical_url}">ical</a>]`;
    calendarList.appendChild(listItem);
});

calendarContainer.appendChild(calendarList);

const references = [
    {
        name: "Google API Setup",
        url: "Google_API.md"
    },
    {
        name: "Google Workspace Get Started",
        url: "https://developers.google.com/workspace/guides/get-started"
    },
    {
        name: "Google Calendar API Quickstart",
        url: "https://developers.google.com/calendar/api/quickstart/python"
    },
    {
        name: "EK Powe PTA",
        url: "http://ekpowe.org/"
    }
];

const referenceContainer = document.getElementById('references');
const referenceList = document.createElement('ul');

references.forEach(reference => {
    const listItem = document.createElement('li');
    listItem.innerHTML = `<a href="${reference.url}">${reference.name}</a>`;
    referenceList.appendChild(listItem);
});

referenceContainer.appendChild(referenceList);
