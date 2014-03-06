var system = require('system');
var fs = require('fs');
var page = require('webpage').create();

var infile = system.args[1];

/*
var outfile = null;
var out = outfile ? fs.open(outfile, 'w') : system.stdout;
*/

var c  = parseInt(system.args[2]);
var r  = parseInt(system.args[3]);
var sx = parseInt(system.args[4]);
var sy = parseInt(system.args[5]);
var w  = parseInt(system.args[6]);
var h  = parseInt(system.args[7]);

// bridge page's console to our stderr
page.onConsoleMessage = function(msg) {
  system.stderr.writeLine(msg);
};

page.open(infile, svg_loaded);

function svg_loaded(status) {
  try {
    if (status != 'success') {
      throw new Error('failed to load ' + infile);
    }

    for (var x = sx; x < sx+c*w; x += w) {
      for (var y = sy; y < sy+r*h; y += h) {
        var out = null;
        try {
          console.log('writing ' + x + ',' + y); 
          out = fs.open(x + '-' + y + '.svg', 'w');
          out.write(page.evaluate(process, x, y, w, h));
        }
        finally {
          if (out) {
            out.close();
          }
        }
      }
    }
  }
  catch (err) {
    console.log(err);
  }
  finally {
    page.close();
    phantom.exit();
  }
}

function process(c, r, sx, sy, w, h) {
  for (var x = sx; x < sx+c*w; x += w) {
    for (var y = sy; y < sy+r*h; y += h) {
      process_one(x, y, w, h);
    }
  }
}

function process(x, y, w, h) {
  // create a dst document
  var impl = document.implementation;
  var doctype = document.doctype ? 
    impl.createDocumentType(
      document.doctype.name,
      document.doctype.publicId,
      document.doctype.systemId
    ) : null;

  var doc = impl.createDocument(
    document.namespaceURI,
    'dummy', 
    doctype
  );

  // dummy root exists so we have an element into which to copy
  var droot = doc.documentElement;

  // set up the AoI
  var aoi = document.documentElement.createSVGRect();
  aoi.x = x;
  aoi.y = y;
  aoi.width = w;
  aoi.height = h;

  function chomp_whitespace(node) {
    if (node.lastChild &&
        node.lastChild.nodeType == Node.TEXT_NODE &&
        !/\S/.test(node.lastChild.nodeValue))
    {
      node.removeChild(node.lastChild);
    }
  }

  function copy_tree(src, dst) {
    return dst.appendChild(dst.ownerDocument.importNode(src, true));
  }

  function copy(src, dst) {
    return dst.appendChild(dst.ownerDocument.importNode(src, false));
  }

  function copy_intersecting(node, aoi, dst) {
    if (node.nodeName == 'defs') {
      copy_tree(node, dst);
      return dst;
    }
    else if (typeof node.getBoundingClientRect == 'function') {
      var bb = node.getBoundingClientRect();
      console.log(node.nodeName + " bb == " + JSON.stringify(bb));

      if ((bb.width > 0 || bb.height > 0) &&
          (bb.right < aoi.x || aoi.x + aoi.width < bb.left ||
           bb.bottom < aoi.y || aoi.y + aoi.height < bb.top)) {
        // nonempty box and empty intersection, skip the subtree
        console.log("skipping " + node);
        chomp_whitespace(dst);
        return dst;
      }
      else {
        console.log("keeping " + node);
      }
    }
    else {
      console.log("no getBoundingClientRect for " + node);
    }

    return copy(node, dst);
  }

  function remove_empty_groups(node) {
    if (node.nodeName == 'g') {
      var children = node.childNodes;
      for (var i = 0; i < children.length; ++i) {
        if (children[i].nodeType != Node.TEXT_NODE) {
          return;
        }
      }

      var p = node.parentNode;
      p.removeChild(node);
      chomp_whitespace(p);
    }
  }

  function walk(node, pre, arg, post) {
    var narg = pre(node, arg);
    if (narg != arg) {
      var children = [].slice.call(node.childNodes);
      for (var i = 0; i < children.length; ++i) {
        walk(children[i], pre, narg, post);
      }
      post(narg);
    }
  }

  // crop away nodes wholly outside the AoI
  console.log("starting tree walk");
  walk(
    document.documentElement,
    function(node, dst) { return copy_intersecting(node, aoi, dst); },
    droot,
    remove_empty_groups
  );
  console.log("done walking");

  // splice out the dummy root
  var svg = droot.firstChild;
  doc.removeChild(droot);
  doc.appendChild(svg); 

  // adjust the SVG bounds
  var svg = doc.documentElement;
  svg.setAttribute("viewBox", x + ' ' + y + ' ' + w + ' ' + h);
  svg.setAttribute("x", x + 'px');
  svg.setAttribute("y", y + 'px');
  svg.setAttribute("height", w + 'px');
  svg.setAttribute("width", h + 'px');

  // cleanup
  doc.normalize();

  // dump the cropped SVG
  return new XMLSerializer().serializeToString(doc);
}
