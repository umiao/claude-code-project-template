/**
 * Hexo filter plugin: Series Navigation
 * Injects prev/next navigation links into posts that belong to a series.
 * Uses `series` and `series_index` front matter fields to determine order.
 *
 * Strategy: Use after_post_render filter with a pre-built series index.
 * The series index is built on first invocation (all posts are in the
 * database by then, even if not all rendered yet).
 */
'use strict';

var seriesMap = null;

function buildSeriesMap(hexoInstance) {
  if (seriesMap) return;
  seriesMap = {};

  // Access all posts from the database (available before rendering)
  hexoInstance.model('Post').forEach(function (post) {
    if (!post.series || post.series_index == null) return;
    var name = post.series;
    if (!seriesMap[name]) seriesMap[name] = [];
    seriesMap[name].push({
      title: post.title,
      path: post.path,
      series_index: parseInt(post.series_index, 10)
    });
  });

  // Sort each series by index
  Object.keys(seriesMap).forEach(function (name) {
    seriesMap[name].sort(function (a, b) {
      return a.series_index - b.series_index;
    });
  });
}

hexo.extend.filter.register('after_post_render', function (data) {
  if (!data.series || data.series_index == null) return data;

  // Build series map from database on first call
  buildSeriesMap(hexo);

  var list = seriesMap[data.series];
  if (!list) return data;

  var currentIndex = parseInt(data.series_index, 10);
  var prev = null;
  var next = null;
  for (var i = 0; i < list.length; i++) {
    if (list[i].series_index === currentIndex) {
      if (i > 0) prev = list[i - 1];
      if (i < list.length - 1) next = list[i + 1];
      break;
    }
  }

  if (!prev && !next) return data;

  // Build navigation HTML
  var nav = '\n<div class="series-nav">\n';
  nav += '<hr>\n';
  nav += '<p class="series-nav-title"><strong>' + data.series + ' Series</strong>';
  nav += ' (Part ' + currentIndex + ' of ' + list.length + ')</p>\n';
  nav += '<div class="series-nav-links">\n';

  if (prev) {
    nav += '  <span class="series-nav-prev">';
    nav += '&larr; <a href="/' + prev.path + '">Part ' + prev.series_index + ': ' + prev.title + '</a>';
    nav += '</span>\n';
  } else {
    nav += '  <span class="series-nav-prev"></span>\n';
  }

  if (next) {
    nav += '  <span class="series-nav-next">';
    nav += '<a href="/' + next.path + '">Part ' + next.series_index + ': ' + next.title + '</a> &rarr;';
    nav += '</span>\n';
  } else {
    nav += '  <span class="series-nav-next"></span>\n';
  }

  nav += '</div>\n</div>\n';

  // Inline styles
  var style = '<style>\n';
  style += '.series-nav { margin: 2em 0 1em; }\n';
  style += '.series-nav-title { margin-bottom: 0.5em; }\n';
  style += '.series-nav-links { display: flex; justify-content: space-between; flex-wrap: wrap; gap: 0.5em; }\n';
  style += '.series-nav-prev, .series-nav-next { max-width: 48%; }\n';
  style += '.series-nav-next { text-align: right; margin-left: auto; }\n';
  style += '</style>\n';

  data.content += style + nav;

  return data;
});

// Reset cache between runs (e.g., hexo server with watch)
hexo.extend.filter.register('before_generate', function () {
  seriesMap = null;
});
