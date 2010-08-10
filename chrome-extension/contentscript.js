

function showBooks(responseText) {
  parser=new DOMParser();
  responseXML=parser.parseFromString(responseText,"text/xml");
  var books = responseXML.getElementsByTagName("book");

  for (var i = 0, book; (book = books[i]) && i < 5; i++) {
    var a = document.createElement("a");
    a.innerText = book.getAttribute("price") + ' TL, ' + book.getAttribute("name");
    a.href = book.getAttribute("link");
    document.body.appendChild(a);
    document.body.appendChild(document.createElement("br"));
    alert(a.innerText);
  }
  
}

function myfunction() {
    selectedText = document.getSelection().toString();
    chrome.extension.sendRequest({'action' : 'fetchBooks', 'selectedText' : selectedText}, showBooks);
}

var re = new RegExp('ISBN:([0-9]+)');
document.ondblclick = myfunction;

