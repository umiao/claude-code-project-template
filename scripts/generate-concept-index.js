/**
 * Hexo generator plugin: Concept Index
 * Reads key_concepts from all post front matter and generates an alphabetical
 * index page at /concepts/ linking each concept to its referencing posts.
 */
'use strict';

hexo.extend.generator.register('concept-index', function (locals) {
  var conceptMap = {};

  locals.posts.forEach(function (post) {
    var concepts = post.key_concepts;
    if (!concepts || !concepts.length) return;

    concepts.forEach(function (concept) {
      if (!concept) return;
      var key = concept.trim();
      if (!conceptMap[key]) {
        conceptMap[key] = [];
      }
      conceptMap[key].push({
        title: post.title,
        path: post.path
      });
    });
  });

  // Sort concepts alphabetically (case-insensitive)
  var sortedConcepts = Object.keys(conceptMap).sort(function (a, b) {
    return a.toLowerCase().localeCompare(b.toLowerCase());
  });

  // Group by first letter
  var grouped = {};
  sortedConcepts.forEach(function (concept) {
    var letter = concept.charAt(0).toUpperCase();
    if (!/[A-Z]/.test(letter)) {
      letter = '#';
    }
    if (!grouped[letter]) {
      grouped[letter] = [];
    }
    grouped[letter].push(concept);
  });

  var sortedLetters = Object.keys(grouped).sort();

  // Build HTML content
  var html = '<div class="concept-index">\n';
  html += '<h1>Concept Index</h1>\n';
  html += '<p>Browse all concepts covered across blog posts. Click a concept to see related articles.</p>\n';

  // Letter navigation
  html += '<div class="concept-nav">\n';
  sortedLetters.forEach(function (letter) {
    html += '<a href="#letter-' + letter + '">' + letter + '</a> ';
  });
  html += '\n</div>\n\n';

  // Concept listings
  sortedLetters.forEach(function (letter) {
    html += '<h2 id="letter-' + letter + '">' + letter + '</h2>\n';
    html += '<dl>\n';
    grouped[letter].forEach(function (concept) {
      html += '  <dt><strong>' + concept + '</strong></dt>\n';
      html += '  <dd>\n    <ul>\n';
      // Sort posts by title within each concept
      conceptMap[concept].sort(function (a, b) {
        return a.title.localeCompare(b.title);
      });
      conceptMap[concept].forEach(function (post) {
        html += '      <li><a href="/' + post.path + '">' + post.title + '</a></li>\n';
      });
      html += '    </ul>\n  </dd>\n';
    });
    html += '</dl>\n\n';
  });

  html += '</div>\n';

  // Add some inline styling for the concept index
  var style = '<style>\n';
  style += '.concept-index .concept-nav { margin: 1em 0 2em; font-size: 1.1em; }\n';
  style += '.concept-index .concept-nav a { margin-right: 0.5em; text-decoration: none; }\n';
  style += '.concept-index dl { margin-left: 0; }\n';
  style += '.concept-index dt { margin-top: 0.8em; font-size: 1.05em; }\n';
  style += '.concept-index dd { margin-left: 1.5em; }\n';
  style += '.concept-index dd ul { list-style: disc; padding-left: 1em; }\n';
  style += '.concept-index dd li { margin: 0.2em 0; }\n';
  style += '</style>\n';

  return {
    path: 'concepts/index.html',
    layout: ['page'],
    data: {
      title: 'Concept Index',
      content: style + html,
      slug: 'concepts',
      comments: false
    }
  };
});
