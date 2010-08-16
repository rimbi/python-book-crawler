
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

function showBooks(responseText) {
    parser=new DOMParser();
    responseXML=parser.parseFromString(responseText,"text/xml");
    var books = responseXML.getElementsByTagName("book");
    
    //alert(responseText);
    book = books[0];
    if (book) {
        notification = createRootElement("deneme");
        var a = document.createElement("a");
        price = book.getAttribute("price");
        name = book.getAttribute("name");
        store = book.getAttribute("store");
        link = book.getAttribute("link");
        if (store == "1") {
            storeName = "Imge.com.tr";
        } else if (store == "2") {
            storeName = "Idefix.com";
        } else if (store == "3") {
            storeName = "Kitapyurdu.com";
        }
        notification.innerHTML = "<p>Bu ürünü <b>" + price + " TL</b>'ye <b><a href='" + link + "'>" + storeName + "</a></b> sitesinden alabilirsiniz.</p>";
    }
}

var re = /ISBN.*[0-9]{10}/g;
isbn = document.body.innerHTML.match(re)[0].slice(-10)
//alert(isbn);
chrome.extension.sendRequest({'action' : 'fetchBooks', 'selectedText' : isbn}, showBooks);

