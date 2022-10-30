String.prototype.toProperCase = function () {
    return this.replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
};
async function request(method, url, data) {
    var settings = {
        method: method,
        headers: {
            "Content-Type":"application/json"
        }
    };
    if (data) {
        settings.body = JSON.stringify(data)
    }
    response = await fetch(url, settings)
    return await response.json()
}
function isEmoji(str) {
    var ranges = [
        '(?:[\u2700-\u27bf]|(?:\ud83c[\udde6-\uddff]){2}|[\ud800-\udbff][\udc00-\udfff]|[\u0023-\u0039]\ufe0f?\u20e3|\u3299|\u3297|\u303d|\u3030|\u24c2|\ud83c[\udd70-\udd71]|\ud83c[\udd7e-\udd7f]|\ud83c\udd8e|\ud83c[\udd91-\udd9a]|\ud83c[\udde6-\uddff]|[\ud83c[\ude01-\ude02]|\ud83c\ude1a|\ud83c\ude2f|[\ud83c[\ude32-\ude3a]|[\ud83c[\ude50-\ude51]|\u203c|\u2049|[\u25aa-\u25ab]|\u25b6|\u25c0|[\u25fb-\u25fe]|\u00a9|\u00ae|\u2122|\u2139|\ud83c\udc04|[\u2600-\u26FF]|\u2b05|\u2b06|\u2b07|\u2b1b|\u2b1c|\u2b50|\u2b55|\u231a|\u231b|\u2328|\u23cf|[\u23e9-\u23f3]|[\u23f8-\u23fa]|\ud83c\udccf|\u2934|\u2935|[\u2190-\u21ff])' // U+1F680 to U+1F6FF
    ];
    if (str.match(ranges.join('|'))) {
        return true;
    } else {
        return false;
    }
}

profile_data = {}

emojis = undefined
creatures = undefined
var usr;

if (location.search.includes("instant")) {
    //document.body.style.backgroundColor = "#36393F"
    document.body.style.backgroundColor = "rgb(0, 0, 0, 0)"
    document.getElementById("profile").style.transition = "all 0s"
    document.getElementById("profile").style.opacity = 1
    document.getElementById("profile").style.marginTop = "10px"
    document.getElementById("edit").style.display = "none"
    document.getElementById("profile").style.height = "500px";
    document.getElementById("profile").style.overflowY = "hidden"
    document.getElementById("profile-user").style.top = "100px"
    document.getElementsByClassName("background-container")[0].style.top = "125px"
    document.getElementsByClassName("background-container")[0].style.height = "calc(100% - 125px)"

    document.querySelectorAll("field-name").forEach(el => {
        el.style.fontSize = "50px;"
    })
}

async function load(pDataPre) {
    if (!usr) {
        r = await fetch("/api/user")
        usr = await r.json()
    }
    if (!usr.error) {
        document.getElementById("user-name").innerText = `${usr.username}#${usr.discriminator}: `
        document.getElementById("user-avatar").src = `https://cdn.discordapp.com/avatars/${usr.id}/${usr.avatar}.webp?size=96`
        setTimeout(function() {
            document.getElementById("user").style.opacity = 1;
            document.getElementById("user-logout").onclick = async function() {window.open(`/logout?to=${location.pathname.replace('edit', '')}`, "_self")}
        }, 1000)
    }
    
    if (!pDataPre) {
        r = await fetch(`/api/profile/${location.pathname.split("/")[2]}`)
        data = await r.json()
        profile_data = data
    } else {
        data = pDataPre
    }

    if (!usr.error && usr.id != data.user.id) {
        document.getElementById("edit").style.display = "none"
    }
    

    document.getElementById("creatures-name").innerText = `Creatures (${data.creatures.length})`

    counter = 0
    document.getElementById("creatures").innerHTML = ""
    for (creature of data.creatures.slice(0, 10)) {

        if (isEmoji(creature.emoji)) {
            src = `https://twemoji.maxcdn.com/v/14.0.2/72x72/${twemoji.convert.toCodePoint(creature.emoji)}.png`
        } else {
            src = `https://cdn.discordapp.com/emojis/${creature.emoji.split(':')[2].replace('>', '')}.png?size=48&quality=lossless`
        }

        if (counter % 5 == 0) {
            document.getElementById("creatures").innerHTML += "<br>"
        }
        counter += 1
        document.getElementById("creatures").innerHTML += `<span aria-label="${creature.name.toProperCase()}" data-balloon-pos="down" class="creature"><img class="creature-image" src=${src}></span>`
    }
    if (data.creatures.length > 10) {
        document.getElementById("creatures").innerHTML += `...And ${data.creatures.length - 10} more!`
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
    for (el of document.querySelectorAll("#quest_xp_currency")) {
        el.src = data.quest_xp_currency
    }
    for (el of document.querySelectorAll("#shards_currency")) {
        el.src = data.shards_currency
    }

    // badges
    document.getElementById("badges").innerHTML = ""
    document.getElementById("edit-pinned-badges").innerHTML = ""
    badges_added = 0
    for (pinned_badge of data.pinned_badges) {
        for (badge of data.badges) {
            if (badge.raw_name == pinned_badge) {
                fr = fromNameLength(badge.name)

                badges_added += 1
                if (badge.image) {
                    badgeReplaced = `<span class="badge-image" data-balloon-length="medium" aria-label="${badge.name}: ${badge.description}" data-balloon-pos="down"><img class="badge-image-image" src="/static/images/badges/${badge.image}"></span>`
                } else {
                    badgeReplaced = `<div class="badge" data-balloon-length="medium" style="${fr.style}" aria-label="${badge.name}: ${badge.description}" data-balloon-pos="down"><div class="all-center">${badge.name.substring(0, 1)}</div></div>`
                }
                document.getElementById("badges").innerHTML += badgeReplaced
            }
        }
    }
    for (badge of data.badges) {
        fr = fromNameLength(badge.name)
        ispinned = ""
        if (data.pinned_badges.includes(badge.raw_name)) {
            ispinned = "edit-pinned-badge-ispinned"
        }

        if (badge.image) {
            badgeReplaced = `<span class="badge-image" data-balloon-length="medium" aria-label="${badge.name}: ${badge.description}" data-balloon-pos="down"><img class="badge-image-image" src="/static/images/badges/${badge.image}"></span>`
            editBadge = `<img src="/static/images/badges/${badge.image}" class="edit-pinned-badge-inner">`
        } else {
            badgeReplaced = `<div style="${fr.style}" class="badge" aria-label="${badge.name}: ${badge.description}" data-balloon-pos="down"><div class="all-center">${badge.name.substring(0, 1)}</div></div>`
            editBadge = `<div style="${fr.style}" class="badge edit-pinned-badge-inner"><div class="all-center">${badge.name.substring(0, 1)}</div></div>`
        }

        document.getElementById("edit-pinned-badges").innerHTML += `<div class="edit-pinned-badge ${ispinned}" onclick="togglePinnedBadge('${badge.raw_name}')" 
            data-balloon-length="medium" aria-label="${badge.name}: ${badge.description}" data-balloon-pos="up">${editBadge}</div>`
        if (badges_added < 5 && !data.pinned_badges.includes(badge.raw_name)) {
            document.getElementById("badges").innerHTML += badgeReplaced
            badges_added += 1
        }
        
        
    }

    document.getElementById("edit-background-image").innerHTML = ""
    document.getElementById("edit-banner-image").innerHTML = ""
    document.getElementById("profile-banner").style.backgroundImage = ``
    document.getElementById("background").style.backgroundImage = ``
    document.getElementById("profile-banner").style.backgroundColor = data.color 
    document.getElementById("edit-banner-color").value = data.color
    for (art of data.profile_art) {
        if (art.file.includes("background")) {
            disabled = "-disabled"
            csr = "cursor:not-allowed;"
            onc = ``
            if (art.owned) {
                disabled = ""
                csr = ""
                onc = `onclick="toggleArt('${art.raw_name}')"`
            }
            if (art.equipped) {
                disabled = "-equipped"
                document.getElementById("background").style.backgroundImage = `url(/static/images/profile/${art.file})`
            }
            document.getElementById("edit-background-image").innerHTML += `<span data-balloon-length="fit" aria-label="${art.name}: ${art.unlock}" ${onc} 
                data-balloon-pos="up" class="edit-picker-container${disabled}"><div class="edit-picker-image${disabled}" style="${csr}background-image:url(/static/images/profile/${art.file})"></div></span>`
        }
        if (art.file.includes("banner")) {
            disabled = "-disabled"
            csr = "cursor:not-allowed;"
            onc = ``
            if (art.owned) {
                disabled = ""
                csr = ""
                onc = `onclick="toggleArt('${art.raw_name}')"`
            }
            if (art.equipped) {
                disabled = "-equipped"
                document.getElementById("profile-banner").style.backgroundImage = `url(/static/images/profile/${art.file})`
            }
            document.getElementById("edit-banner-image").innerHTML += `<span aria-label="${art.name}: ${art.unlock}" class="edit-picker-container${disabled}" ${onc}
            data-balloon-length="fit" data-balloon-pos="down"><div class="edit-picker-image${disabled}" style="${csr}background-image:url(/static/images/profile/${art.file})"></div></span>`
        }
    }

    document.getElementById("edit").onclick = edit
    if (location.pathname.includes("edit")) {
        edit()
    }

    if (!location.search.includes("instant")) {
        document.getElementById("profile").style.opacity = 1
        document.getElementById("profile").style.marginTop = "100px"
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

async function toggleArt(art_name) {
    d = {}

    for (art of profile_data.profile_art) {
        if (art_name.includes("background") && art.raw_name.includes("background") && art.owned) {
            d[art.raw_name] = "owned"
        }
        if (art_name.includes("banner") && art.raw_name.includes("banner") && art.owned) {
            d[art.raw_name] = "owned"
        }
        
    }

    for (art of profile_data.profile_art) {
        if (art.raw_name == art_name && art.owned) {
            
            if (art.equipped) {
                d[art.raw_name] = "owned"
            } else {
                d[art.raw_name] = "equipped"
            }
            
        }
    }

    profile_data = await request("POST", "/api/profile/art", d)
    await load(profile_data)
}

async function togglePinnedBadge(badge_name) {
    b = profile_data.pinned_badges 

    if (b.includes(badge_name)) {
        b.splice(b.indexOf(badge_name), 1);
    } else {
        b.push(badge_name)
        if (b.length > 5) {b.shift()}
    }

    

    profile_data = await request("POST", "/api/profile/pinned_badges", b)
    await load(profile_data)
}

async function edit() {
    if (!usr) {
        r = await fetch("/api/user")
        usr = await r.json()
    }

    if (usr.error) {
        return window.open(`/login?to=/profile/${profile_data.user.id}/edit`, "_self")
    }

    if (usr.id == profile_data.user.id) {
        MicroModal.show('modal-1');
    }

    window.history.pushState("", "", location.href.replace("edit", ""))
}


var timer;
document.getElementById("edit-banner-color").oninput = async function(e) {
    val = e.target.value 
    
    if (timer) {clearTimeout(timer);}
    timer = setTimeout(async () => {
        profile_data = await request("POST", "/api/profile/color", val)
        await load(profile_data)
    }, 200)
}

function fromNameLength(name) {
    colors = ["#ff0000", "#ff7300", "#ffd000", "#c3ff00", "#59ff00", "#00ff8c", "#00fff7", "#0073ff", "#6f00ff", "#dd00ff", "#ff0084"]
    colors_bw = ["white", "black", "black", "black", "black", "black", "black", "white", "black", "white", "white"]
    size = name.length + (name.split("e").length - 1 )
    if (size > 11) {
        size -= 11
    }

    color = colors[size]
    bw = colors_bw[size]
    console.log(name.length)
    console.log(color)
    return {color:color, size:size, style:`background-color:${color};border-radius:${size}px;color:${bw}`}
}

