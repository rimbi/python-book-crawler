
function HTMLParser(aHTMLString){
	var html = document.implementation.createDocument("http://www.w3.org/1999/xhtml", "html", null),
		body = document.createElementNS("http://www.w3.org/1999/xhtml", "body");
	html.documentElement.appendChild(body);

	body.appendChild(Components.classes["@mozilla.org/feed-unescapehtml;1"]
			 .getService(Components.interfaces.nsIScriptableUnescapeHTML)
			 .parseFragment(aHTMLString, false, null, body));
	
	return body;
};

var KitapSever = function () {
	var prefManager = Components.classes["@mozilla.org/preferences-service;1"].getService(Components.interfaces.nsIPrefBranch);
	return {
		init : function () {
			gBrowser.addEventListener("load", function () {
				var autoRun = prefManager.getBoolPref("extensions.kitapsever.autorun");
				if (autoRun) {
					KitapSever.run();
				}
			}, false);
		},

		run : function () {
			var pageBody = content.document.documentElement;
			var reIsbn = /ISBN[:\s]*([0-9\\-]*)/g; 
			var bookIsbnRaw = pageBody.textContent.match(reIsbn)[0];
			var bookIsbnNum = bookIsbnRaw.split(":")[1];
			bookIsbnNum = bookIsbnNum.trim().slice(-10);
			alert("ISBN No : '" + bookIsbnNum + "'");

			var req = new XMLHttpRequest();
			req.open("GET", "http://127.0.0.1:8000/myapp/default/query.xml?column_name=isbn&query_string=" + bookIsbnNum, "true");
			req.onreadystatechange = function (asyncEvent) {
				if (req.readyState == 4) {
					if (req.status == 200) {
						alert("Incoming resp " + req.responseXML);
						// var respBody = HTMLParser(req.responseText);
						// var bookClass = respBody.getElementsByTagName("books");
						// alert("book Name " + bookClass + ", length " + bookClass.length);
//						var bookName = bookClass.

					} else {
						alert("Invalid response");
					}
				}
			};
			req.send(null);
		}
	};
}();
window.addEventListener("load", KitapSever.init, false);