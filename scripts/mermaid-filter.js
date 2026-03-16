'use strict';

// Custom mermaid filter — fully self-contained, bypasses NexT's mermaid handler.
//
// NexT's mermaid handler copies innerHTML through DOM elements which can
// mangle content. Instead, we:
// 1. Extract ```mermaid blocks before markdown rendering (placeholder pattern)
// 2. Restore them after rendering as <pre class="mermaid"> (mermaid v11 native)
// 3. Inject a loader script that loads local mermaid.js and calls mermaid.run()

var defined = /^```mermaid\s*$/;
var defined_end = /^```\s*$/;
var mermaidStore = {};

function extractMermaidBlocks(content, key) {
  var result = '';
  var lines = content.split('\n');
  var inside = false;
  var buf = [];
  var blocks = [];
  var index = 0;

  for (var i = 0; i < lines.length; i++) {
    var line = lines[i];
    if (!inside && defined.test(line.trim())) {
      inside = true;
      buf = [];
    } else if (inside && defined_end.test(line.trim())) {
      inside = false;
      blocks.push(buf.join('\n'));
      result += '<!--mermaid-placeholder-' + index + '-->\n';
      index++;
    } else if (inside) {
      buf.push(line);
    } else {
      result += line + '\n';
    }
  }

  if (blocks.length > 0) {
    mermaidStore[key] = blocks;
  }
  return result;
}

function restoreMermaidBlocks(content, key) {
  var blocks = mermaidStore[key];
  if (!blocks) return content;

  for (var i = 0; i < blocks.length; i++) {
    var placeholder = '<!--mermaid-placeholder-' + i + '-->';
    // Only encode < and & (required for valid HTML).
    // Leave > and " raw — they're valid in HTML text content and
    // avoids any entity decoding issues with mermaid's parser.
    var encoded = blocks[i]
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;');
    var html = '<div class="mermaid-container">'
      + '<pre class="mermaid">'
      + encoded
      + '</pre>'
      + '</div>';
    content = content.replace(placeholder, html);
  }

  delete mermaidStore[key];
  return content;
}

hexo.extend.filter.register('before_post_render', function(data) {
  if (data.content && data.content.indexOf('```mermaid') !== -1) {
    var key = data.source || data._id || data.slug;
    data.content = extractMermaidBlocks(data.content, key);
  }
  return data;
}, 9);

hexo.extend.filter.register('after_post_render', function(data) {
  var key = data.source || data._id || data.slug;
  if (mermaidStore[key]) {
    data.content = restoreMermaidBlocks(data.content, key);
  }
  return data;
}, 9);

// Inject mermaid loader script on pages that have mermaid content.
// This replaces NexT's mermaid handler (which is now disabled).
hexo.extend.injector.register('body_end', function() {
  return '<script>'
    + '(function() {'
    + '  var els = document.querySelectorAll("pre.mermaid");'
    + '  if (!els.length) return;'
    + '  var script = document.createElement("script");'
    + '  script.src = "/lib/mermaid/dist/mermaid.min.js";'
    + '  script.onload = function() {'
    + '    var isDark = window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;'
    + '    mermaid.initialize({'
    + '      startOnLoad: false,'
    + '      theme: isDark ? "dark" : "default",'
    + '      logLevel: 4,'
    + '      flowchart: { curve: "linear" },'
    + '      gantt: { axisFormat: "%m/%d/%Y" },'
    + '      sequence: { actorMargin: 50 }'
    + '    });'
    + '    mermaid.run({ querySelector: "pre.mermaid" });'
    + '  };'
    + '  document.body.appendChild(script);'
    + '})();'
    + '</script>';
}, 'default');
