'use strict';

// Inject a client-side script that attaches click handlers to mermaid SVG
// nodes after rendering. Each node navigates to /concepts/#<slug> where
// the slug is derived from the node's label text.
//
// Uses MutationObserver to detect when mermaid replaces <pre> with <svg>.

hexo.extend.injector.register('body_end', function() {
  return '<script>'
    + '(function() {'
    + '  function slugify(text) {'
    + '    return text.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/(^-|-$)/g, "");'
    + '  }'
    + '  function attachClickHandlers() {'
    + '    var nodes = document.querySelectorAll(".mermaid svg .node, svg[id^=mermaid] .node");'
    + '    if (!nodes.length) return;'
    + '    nodes.forEach(function(node) {'
    + '      var label = node.querySelector(".nodeLabel");'
    + '      if (!label) return;'
    + '      var text = label.textContent.trim();'
    + '      if (!text) return;'
    + '      node.style.cursor = "pointer";'
    + '      node.addEventListener("click", function() {'
    + '        window.location.href = "/concepts/#" + slugify(text);'
    + '      });'
    + '    });'
    + '  }'
    + '  var observer = new MutationObserver(function(mutations) {'
    + '    for (var i = 0; i < mutations.length; i++) {'
    + '      if (mutations[i].addedNodes.length) {'
    + '        var svg = document.querySelector("svg[id^=mermaid]");'
    + '        if (svg) {'
    + '          observer.disconnect();'
    + '          setTimeout(attachClickHandlers, 300);'
    + '          return;'
    + '        }'
    + '      }'
    + '    }'
    + '  });'
    + '  if (document.readyState === "loading") {'
    + '    document.addEventListener("DOMContentLoaded", function() {'
    + '      observer.observe(document.body, { childList: true, subtree: true });'
    + '    });'
    + '  } else {'
    + '    observer.observe(document.body, { childList: true, subtree: true });'
    + '  }'
    + '})();'
    + '</script>';
}, 'default');
