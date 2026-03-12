/**
 * Hexo filter plugin: Related Posts
 * Injects a "Related Reading" section at the bottom of each post.
 * Scoring: tag overlap + key_concepts overlap (weighted 2x higher than tags).
 * Shows top 3-5 related posts with titles and links.
 *
 * Uses after_post_render filter with a pre-built index for performance.
 */
'use strict';

var postIndex = null;

function buildPostIndex(hexoInstance) {
  if (postIndex) return;
  postIndex = [];

  hexoInstance.model('Post').forEach(function (post) {
    var tags = [];
    if (post.tags && post.tags.length) {
      post.tags.forEach(function (tag) {
        tags.push(tag.name.toLowerCase());
      });
    }

    var concepts = [];
    if (post.key_concepts && post.key_concepts.length) {
      post.key_concepts.forEach(function (c) {
        if (c) concepts.push(c.toLowerCase().trim());
      });
    }

    postIndex.push({
      _id: post._id,
      title: post.title,
      path: post.path,
      tags: tags,
      concepts: concepts
    });
  });
}

function getRelatedPosts(currentPost, maxResults) {
  var currentTags = [];
  if (currentPost.tags && currentPost.tags.length) {
    currentPost.tags.forEach(function (tag) {
      currentTags.push(tag.name.toLowerCase());
    });
  }

  var currentConcepts = [];
  if (currentPost.key_concepts && currentPost.key_concepts.length) {
    currentPost.key_concepts.forEach(function (c) {
      if (c) currentConcepts.push(c.toLowerCase().trim());
    });
  }

  // No tags or concepts means we cannot score relevance
  if (currentTags.length === 0 && currentConcepts.length === 0) {
    return [];
  }

  var scored = [];

  for (var i = 0; i < postIndex.length; i++) {
    var candidate = postIndex[i];
    if (candidate._id === currentPost._id) continue;

    var tagOverlap = 0;
    for (var t = 0; t < candidate.tags.length; t++) {
      if (currentTags.indexOf(candidate.tags[t]) !== -1) {
        tagOverlap++;
      }
    }

    var conceptOverlap = 0;
    for (var c = 0; c < candidate.concepts.length; c++) {
      if (currentConcepts.indexOf(candidate.concepts[c]) !== -1) {
        conceptOverlap++;
      }
    }

    var score = tagOverlap + (conceptOverlap * 2);
    if (score > 0) {
      scored.push({ post: candidate, score: score });
    }
  }

  // Sort by score descending, then by title for stability
  scored.sort(function (a, b) {
    if (b.score !== a.score) return b.score - a.score;
    return a.post.title.localeCompare(b.post.title);
  });

  // Return top N (3-5: use 5 if available, minimum 3 to show section)
  var results = [];
  var limit = Math.min(scored.length, maxResults);
  for (var j = 0; j < limit; j++) {
    results.push(scored[j].post);
  }
  return results;
}

hexo.extend.filter.register('after_post_render', function (data) {
  buildPostIndex(hexo);

  var related = getRelatedPosts(data, 5);
  if (related.length < 1) return data;

  // Build Related Reading HTML
  var html = '\n<div class="related-posts">\n';
  html += '<hr>\n';
  html += '<h3>Related Reading</h3>\n';
  html += '<ul>\n';

  for (var i = 0; i < related.length; i++) {
    html += '  <li><a href="/' + related[i].path + '">' + related[i].title + '</a></li>\n';
  }

  html += '</ul>\n';
  html += '</div>\n';

  // Inline styles
  var style = '<style>\n';
  style += '.related-posts { margin: 2em 0 1em; }\n';
  style += '.related-posts h3 { margin-bottom: 0.5em; }\n';
  style += '.related-posts ul { list-style: disc; padding-left: 1.5em; }\n';
  style += '.related-posts li { margin: 0.3em 0; }\n';
  style += '</style>\n';

  data.content += style + html;

  return data;
});

// Reset cache between runs (e.g., hexo server with watch)
hexo.extend.filter.register('before_generate', function () {
  postIndex = null;
});
