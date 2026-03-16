/* Fix sticky post sorting for hexo-generator-index.
 *
 * The built-in generator mutates posts.data with timsort, but
 * hexo-pagination calls posts.slice() on the Query object which
 * ignores the in-place mutation. This script replaces the index
 * generator with one that wraps arrays with toArray() for NexT
 * template compatibility.
 */

'use strict';

var pagination = require('hexo-pagination');

// Wrap a plain array so it behaves like a Query (has .toArray, .length, etc.)
function wrapArray(arr) {
  arr.toArray = function() { return arr; };
  return arr;
}

hexo.extend.generator.register('index', function(locals) {
  var config = this.config;
  var indexConfig = config.index_generator || {};
  var orderBy = indexConfig.order_by || '-date';
  var perPage = indexConfig.per_page != null ? indexConfig.per_page : 10;
  var paginationDir = config.pagination_dir || 'page';
  var basePath = indexConfig.path || '';

  // Sort by date first, then stable-sort by sticky (higher first)
  var posts = locals.posts.sort(orderBy).toArray();
  posts.sort(function(a, b) {
    return (b.sticky || 0) - (a.sticky || 0);
  });

  // Build pagination with plain arrays wrapped for template compatibility
  var length = posts.length;
  var total = perPage ? Math.ceil(length / perPage) : 1;
  var result = [];

  function formatURL(i) {
    var url = basePath;
    if (url && url[url.length - 1] !== '/') url += '/';
    if (i > 1) url += paginationDir + '/' + i + '/';
    return url;
  }

  function makeData(i) {
    var start = perPage * (i - 1);
    var end = perPage * i;
    return {
      base: basePath,
      total: total,
      current: i,
      current_url: formatURL(i),
      posts: wrapArray(perPage ? posts.slice(start, end) : posts.slice()),
      prev: i > 1 ? i - 1 : 0,
      prev_link: i > 1 ? formatURL(i - 1) : '',
      next: i < total ? i + 1 : 0,
      next_link: i < total ? formatURL(i + 1) : '',
      __index: true
    };
  }

  if (perPage) {
    for (var i = 1; i <= total; i++) {
      result.push({
        path: formatURL(i),
        layout: ['index', 'archive'],
        data: makeData(i)
      });
    }
  } else {
    result.push({
      path: basePath,
      layout: ['index', 'archive'],
      data: makeData(1)
    });
  }

  return result;
});
