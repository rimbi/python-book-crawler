var bookStoreList = new Array("imge.com.tr", "idefix.com", "kitapyurdu.com", "pandora.com.tr", "netkitap.com", "ilknokta.com");

function GetDomain() {

	// Lets check first if url is what we need
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
			Firebug.Console.log("valid domain is " + domain);
			return domain;
		}
	}

	return null;
};

//
// notify()
// This function notifies the user about available books with using NotificationBox.
// Extra work here is done to make a link in NotificationBox. Naturally NotificationBox does not
// allow you to change string format. We do "Anonymous Content" trick here, in order to do that.
//
function notify(responseText) {
	parser=new DOMParser();
	responseXML=parser.parseFromString(responseText,"text/xml");
	var bookList = responseXML.getElementsByTagName("book");
	var fragment = document.createDocumentFragment();
	var link = new Array(bookList.length);
	var domain = GetDomain();
	var message = "";

	fragment.appendChild(document.createTextNode("Bu kitabi "));
	for (var i = 0, book; book = bookList[i]; i++) {
		var bookStore = book.getAttribute("store");
		var bookPrice = book.getAttribute("price");
		var bookLink = book.getAttribute("link");
		var storeName = bookStoreList[bookStore - 1];
		Firebug.Console.log("store name is " + storeName);
		if (domain == storeName) {
			Firebug.Console.log("Same domain!, it means the site has one of the cheapest");
			return;
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
	Firebug.Console.log("booklist length " + bookList.length);
	if (bookList.length == 0) {
		return;
	} else if (bookList.length == 1) {
		message = " sitesinden ";
	} else {
		message = " sitelerinden ";
	}
	message = message + "satin alabilirsiniz!";
	fragment.appendChild(document.createTextNode(message));

	var nb = gBrowser.getNotificationBox();
	var notification = nb.appendNotification('', 'kitapsever-notification', 'chrome://KitapSever/skin/kitapsever.png');
	var messageText = document.getAnonymousElementByAttribute(notification, "anonid", "messageText");
	messageText.removeChild(messageText.firstChild);
	messageText.appendChild(fragment);

};


var KitapSever = function () {
	var prefManager = Components.classes["@mozilla.org/preferences-service;1"].getService(Components.interfaces.nsIPrefBranch);
	return {
		init : function (event) {
			if (event.originalTarget instanceof HTMLDocument) {
				var win = event.originalTarget.defaultView;
				if (win.frameElement) {
					// Lets check, if we support what is being browsed.
					var ret = GetDomain();
					if (ret) {
						Firebug.Console.log("This site should be queried");
						KitapSever.run();
					}
				}
			}
		},

		run : function () {
			var pageBody = content.document.documentElement;
			var reIsbn = /ISBN[:\s]*([X0-9\\-]*)/g; 
			var bookIsbnRaw = pageBody.textContent.match(reIsbn)[0];
			var bookIsbnNum = bookIsbnRaw.split(":")[1];
			bookIsbnNum = bookIsbnNum.trim().slice(-10, -1);

			var req = new XMLHttpRequest();
			req.open("GET", "http://rimbiskitapsever.appspot.com/bookbyisbn?isbn=" + bookIsbnNum, "true");
			req.channel.loadFlags |= Components.interfaces.nsIRequest.LOAD_BYPASS_CACHE;
			req.onload = function (asyncEvent) {
				notify(req.responseText);
			};
			req.send(null);
		}
	};
}();

window.addEventListener("load", function () {
		// Callback runs every time a document loads.
		// This piece of code is copied from;
		// https://developer.mozilla.org/en/Code_snippets/Tabbed_browser
		gBrowser.addEventListener("load", KitapSever.init, true);
	}, false);