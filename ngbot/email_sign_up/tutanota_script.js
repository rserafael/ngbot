let divs = document.getElementsByClassName("dialog-header");
let freeDiv = null;
for (var div of divs){
	if( div.innerText.search("Free") !== -1){
		freeDiv = div;
		break;
    }
}
if(freeDiv !== null){
    let selectDiv = null;
    let bigBox = freeDiv.parentElement;
    for(var div of bigBox.children){
        if(div.innerText.search("Select") !== -1){
            selectDiv = div;
            break;
        }
    }
    if(selectDiv !== null){
        selectDiv.children[0].click();
        // window.confirm("Sumiu ? ");
        console.log(`sumiu ? `);
    }
}
else{
    console.log("Não foi possível achar o botão de free account");
}