String.prototype.toProperCase = function () {
    return this.replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
};

profile_data = {}

async function load() {

    r = await fetch(`/api/emojis`)
    emojis = await r.json()

    r = await fetch(`/api/creatures`)
    creatures = await r.json()

    r = await fetch(`/api/profile/${location.pathname.split("/")[2]}`)
    data = await r.json()
    profile_data = data

    document.getElementById("creatures-name").innerText = `Creatures (${data.creatures.length})`

    counter = 0
    for (creature of data.creatures.slice(0, 10)) {
        emoji = creatures[creature].emoji

        if (!emoji.includes("<")) {
            src = `https://twemoji.maxcdn.com/v/14.0.2/72x72/${twemoji.convert.toCodePoint(emojis[emoji.split(":").join("")])}.png`
        } else {
            src = `https://cdn.discordapp.com/emojis/${emoji.split(':')[2].replace('>', '')}.png?size=48&quality=lossless`
        }

        if (counter % 5 == 0) {
            document.getElementById("creatures").innerHTML += "<br>"
        }
        counter += 1
        document.getElementById("creatures").innerHTML += `<span aria-label="${creature.split('_').join(' ').toProperCase()}" data-balloon-pos="down" class="creature"><img class="creature-image" src=${src}></span>`
    }
    if (data.creatures.length > 10) {
        document.getElementById("creatures").innerHTML += "...And more!"
    }

    document.getElementById("avatar").src = data.user.avatar_url
    document.getElementById("name").innerText = data.user.name
    document.getElementById("discriminator").innerText = `#${data.user.discriminator}`

    document.getElementById("cash").innerText = data.balances.ub.cash.toLocaleString()
    document.getElementById("bank").innerText = data.balances.ub.bank.toLocaleString()
    document.getElementById("total").innerText = data.balances.ub.total.toLocaleString()
    document.getElementById("quest_xp").innerText = data.balances.quest_xp.toLocaleString()
    document.getElementById("shards").innerText = data.balances.shards.toLocaleString()

    for (el of document.querySelectorAll("#currency")) {
        el.src = data.currency
    }

    // badges
    for (badge of data.badges) {
        document.getElementById("badges").innerHTML += `<div class="badge hex" aria-label="${badge.description}" data-balloon-pos="down"><div class="all-center">${badge.name.substring(0, 1)}</div></div>`
    }

    for (art of data.profile_art) {
        if (art.file.includes("background")) {
            disabled = "-disabled"
            if (art.owned) {
                disabled = ""
            }
            if (art.equipped) {
                disabled = "-equipped"
                document.getElementById("background").style.backgroundImage = `url(/static/images/profile/${art.file})`
            }
            document.getElementById("edit-background-image").innerHTML += `<div class="edit-picker-image${disabled}" style="background-image:url(/static/images/profile/${art.file})"></div>`
        }
        if (art.file.includes("banner")) {
            disabled = "-disabled"
            if (art.owned) {
                disabled = ""
            }
            if (art.equipped) {
                disabled = "-equipped"
                document.getElementById("profile-banner").style.backgroundImage = `url(/static/images/profile/${art.file})`
            }
            document.getElementById("edit-banner-image").innerHTML += `<div class="edit-picker-image${disabled}" style="background-image:url(/static/images/profile/${art.file})"></div>`
        }
    }

    document.getElementById("edit").onclick = edit
    console.log(location.pathname)
    if (location.pathname.includes("edit")) {
        edit()
    }

}

load()
MicroModal.init({
    onShow: modal => console.info(`${modal.id} is shown`), // [1]
    onClose: modal => console.info(`${modal.id} is hidden`), // [2]
    openTrigger: 'data-custom-open', // [3]
    closeTrigger: 'data-custom-close', // [4]
    disableScroll: true, // [5]
    disableFocus: false, // [6]
    awaitCloseAnimation: false, // [7]
    debugMode: true // [8]
});

async function edit() {
    r = await fetch("/api/user")
    usr = await r.json()

    if (usr.error) {
        return window.open(`/login?to=/profile/${profile_data.user.id}/edit`, "_self")
    }

    MicroModal.show('modal-1'); // [1]
   // MicroModal.close('modal-id'); // [2]
}

