
var re = /ISBN[:\s]*([X0-9\\-]*)/g;
rawISBN = document.body.innerText.match(re)[0];
isbn = rawISBN.replace(/-/g, "").slice(-10, -1)

function  createRootElement(id) {
	root = document.createElement("div");
	root.id = id;
	root.style.backgroundColor = "#00FF00";
	root.style.height = "25px";
	root.style.fontFamily = "Trebuchet MS";
	root.style.fontSize = "12px";
	root.style.verticalAlign = "middle";
	root.style.textAlign = "center";
	document.body.insertBefore(root, document.body.firstChild);
	return root;
}

var options = "height=400,width=600,titlebar=no,status=no,toolbar=no,menubar=no,location=no,resizable=no,scrollbars=1";
var server_addr = "http://rimbiskitapsever.appspot.com"
var addToBasket_link = "<a href=\"javascript:window.open(\'" + server_addr + "/addtobasket?isbn=" + isbn + "\',\'_blank\',\'" + options + "\');\">Sepete At</a>";
function showBooks(responseText) {
	parser=new DOMParser();
	responseXML=parser.parseFromString(responseText,"text/xml");
	var books = responseXML.getElementsByTagName("book");
	
	//alert(responseText);
	book = books[0];
	if (book) {
		notification = createRootElement("deneme");
		link = book.getAttribute("link");
		if (link == document.URL) {
			notification.innerHTML = "<p><b>En iyi fiyat :</b> Bu üründe en iyi fiyat bu sitede." + "&nbsp;&nbsp;&nbsp;&nbsp;" + addToBasket_link + "</p>";
			return;
		}
		price = book.getAttribute("price");
		name = book.getAttribute("name");
		store = book.getAttribute("store");
		if (store == "1") {
			storeName = "İmge.com.tr";
		} else if (store == "2") {
			storeName = "İdefix.com";
		} else if (store == "3") {
			storeName = "Kitapyurdu.com";
		} else if (store == "4") {
			storeName = "Pandora.com.tr";
		} else if (store == "5") {
			storeName = "Netkitap.com";
		} else if (store == "6") {
			storeName = "İlknokta.com";
		}
		notification.innerHTML = "<p>Bu ürünü <b>" + price + " TL</b>'ye <b><a href='" + link + "'>" + storeName + "</a></b> sitesinden alabilirsiniz." + "&nbsp;&nbsp;&nbsp;&nbsp;" + addToBasket_link + "</p>";
	}
}

//alert(isbn);
chrome.extension.sendRequest({'action' : 'fetchBooks', 'selectedText' : isbn}, showBooks);

