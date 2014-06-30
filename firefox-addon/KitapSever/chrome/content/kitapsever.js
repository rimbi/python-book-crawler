<<<<<<< HEAD

function HTMLParser(aHTMLString){
	var html = document.implementation.createDocument("http://www.w3.org/1999/xhtml", "html", null),
		body = document.createElementNS("http://www.w3.org/1999/xhtml", "body");
	html.documentElement.appendChild(body);

	body.appendChild(Components.classes["@mozilla.org/feed-unescapehtml;1"]
			 .getService(Components.interfaces.nsIScriptableUnescapeHTML)
			 .parseFragment(aHTMLString, false, null, body));
	
	return body;
};

//
// notify()
// This function notifies the user about available books with using NotificationBox.
// Extra work here is done to make a link in NotificationBox. Naturally NotificationBox does not
// allow you to change string format. We do "Anonymous Content" trick here, in order to do that.
//
function notify(bookList) {
	var nb = gBrowser.getNotificationBox();
	var notification = nb.appendNotification('', 'kitapsever-notification', 'chrome://KitapSever/skin/kitapsever.png');
	var messageText = document.getAnonymousElementByAttribute(notification, "anonid", "messageText");
	var fragment = document.createDocumentFragment();
	var link = new Array(bookList.length);

	var message = "";

	fragment.appendChild(document.createTextNode("Bu kitabi "));
	for (var i = 0, book; book = bookList[i]; i++) {
		var bookStore = book.getAttribute("store");
		var storeName;
		var bookPrice = book.getAttribute("price");
		var bookLink = book.getAttribute("link");
		if (bookStore == "1") {
			storeName = "imge.com.tr";
		} else if (bookStore == "2") {
			storeName = "idefix.com";
		} else if (bookStore == "3") {
			storeName = "kitapyurdu.com";
		} else if (bookStore == "4") {
			storeName = "pandora.com.tr";
		} else if (bookStore == "5") {
			storeName = "netkitap.com";
		} else if (bookStore == "6") {
			storeName = "ilknokta.com";
=======
var bookStoreList = new Array("imge.com.tr", "idefix.com", "kitapyurdu.com", "pandora.com.tr", "netkitap.com", "ilknokta.com");

/*
 * GetDomain()
 * Returns domain name of the site currently being browsed.
 */
function GetDomain() {

	/* Lets check first if url is what we need. */
	var valid = null;
	var url;
	var re;
	var domain;
	for (var i = 0; i < bookStoreList.length; i++) {
		domain = bookStoreList[i];
		url = content.document.location.href;
		re = new RegExp("www\." + domain + ".*", "g");
		valid = url.match(re);
		if (valid) {
			return domain;
		}
	}

	return null;
};

/*
 * notify()
 * This function notifies the user about available books with using NotificationBox.
 * Extra work here is done to make a link in NotificationBox. Naturally NotificationBox does not
 * allow you to change string format. We do "Anonymous Content" trick here, in order to do that.
 */
function notify(responseText) {
	parser=new DOMParser();
	responseXML=parser.parseFromString(responseText,"text/xml");
	var bookList = responseXML.getElementsByTagName("book");
	var fragment = document.createDocumentFragment();
	var link = new Array(bookList.length);
	var domain = GetDomain();
	var message = "";
	var nb = gBrowser.getNotificationBox();

	if (nb.currentNotification) {
		/* Check if we are already displaying notification box. */
		return;
	}

	fragment.appendChild(document.createTextNode("Bu kitabı, "));
	for (var i = 0, book; book = bookList[i]; i++) {
		var bookStore = book.getAttribute("store");
		var bookPrice = book.getAttribute("price");
		var bookLink = book.getAttribute("link");
		var storeName = bookStoreList[bookStore - 1];

		if (domain == storeName) {
			return;
>>>>>>> zaknafein/master
		}

		link[i] = document.createElementNS("http://www.w3.org/1999/xhtml", "link");
		link[i].setAttribute("target", "_blank");
		link[i].href = bookLink;
		linkTextArea = document.createElementNS("http://www.w3.org/1999/xhtml", "u");
		linkTextArea.innerHTML = "<b>" + storeName + " (" + bookPrice + " TL)" + "</b>";
		link[i].appendChild(linkTextArea);
		fragment.appendChild(link[i]);

		if (i == (bookList.length - 1)) {
			fragment.appendChild(document.createTextNode(" "));
		} else {
			fragment.appendChild(document.createTextNode(", "));
		}
	}
<<<<<<< HEAD
	if (bookList.length == 1) {
=======

	if (bookList.length == 0) {
		return;
	} else if (bookList.length == 1) {
>>>>>>> zaknafein/master
		message = " sitesinden ";
	} else {
		message = " sitelerinden ";
	}
<<<<<<< HEAD
	message = message + "satin alabilirsiniz!";
	fragment.appendChild(document.createTextNode(message));

	messageText.removeChild(messageText.firstChild);
	messageText.appendChild(fragment);

};

var KitapSever = function () {
	var prefManager = Components.classes["@mozilla.org/preferences-service;1"].getService(Components.interfaces.nsIPrefBranch);
	return {
		init : function () {
			gBrowser.addEventListener("load", function () {
				var autoRun = prefManager.getBoolPref("extensions.kitapsever.autorun");
//				if (autoRun) {
//					KitapSever.run();
//				}
			}, false);
=======
	message = message + "satın alabilirsiniz!";
	fragment.appendChild(document.createTextNode(message));

	var notification = nb.appendNotification('', 'kitapsever-notification', 'chrome://KitapSever/skin/kitapsever.png');
	var messageText = document.getAnonymousElementByAttribute(notification, "anonid", "messageText");
	messageText.removeChild(messageText.firstChild);
	messageText.appendChild(fragment);
};


var KitapSever = function () {
	return {
		init : function (event) {
			if (event.originalTarget instanceof HTMLDocument) {
				var win = event.originalTarget.defaultView;
				if (win.frameElement) {
					/* Lets check, if we support what is being browsed. */
					var ret = GetDomain();
					if (!ret) {
						return;
					}

					KitapSever.run();
				}
			}
>>>>>>> zaknafein/master
		},

		run : function () {
			var pageBody = content.document.documentElement;
<<<<<<< HEAD
			var reIsbn = /ISBN[:\s]*([0-9\\-]*)/g; 
			var bookIsbnRaw = pageBody.textContent.match(reIsbn)[0];
			var bookIsbnNum = bookIsbnRaw.split(":")[1];
			bookIsbnNum = bookIsbnNum.trim().slice(-10);
			alert("ISBN No : '" + bookIsbnNum + "'");

			var req = new XMLHttpRequest();
			req.open("GET", "http://127.0.0.1:8000/myapp/default/query.xml?column_name=isbn&query_string=" + bookIsbnNum, "true");
			req.channel.loadFlags |= Components.interfaces.nsIRequest.LOAD_BYPASS_CACHE;
			req.onreadystatechange = function (asyncEvent) {
				if (req.readyState == 4) {
					if (req.status == 200) {
						var books = req.responseXML.getElementsByTagName("book");
						notify(books);
					} else {
						alert("Invalid response");
					}
				}
=======
			var reIsbn = /ISBN[:\s]*([X0-9\\-]*)/g; 
			var bookIsbnRaw = pageBody.textContent.match(reIsbn)[0];
			var bookIsbnNum = bookIsbnRaw.split(":")[1];
			bookIsbnNum = bookIsbnNum.trim().slice(-10, -1);

			var req = new XMLHttpRequest();
			req.open("GET", "http://rimbiskitapsever.appspot.com/bookbyisbn?isbn=" + bookIsbnNum, "true");
			req.channel.loadFlags |= Components.interfaces.nsIRequest.LOAD_BYPASS_CACHE;
			req.onload = function (asyncEvent) {
				notify(req.responseText);
>>>>>>> zaknafein/master
			};
			req.send(null);
		}
	};
}();
<<<<<<< HEAD
window.addEventListener("load", KitapSever.init, false);
=======

window.addEventListener("load", function () {
		/*
		 * Callback runs every time a document loads.
		 * This piece of code is copied from;
		 * https://developer.mozilla.org/en/Code_snippets/Tabbed_browser
		 */
		gBrowser.addEventListener("load", KitapSever.init, true);
	}, false);
>>>>>>> zaknafein/master
