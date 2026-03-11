/**
 * Hexo plugin: hide "Life" category posts from the homepage index.
 * Life-category posts remain accessible via /categories/Life/, /archives/,
 * direct URL, and the sidebar widget.
 *
 * Works by wrapping the built-in index generator to exclude Life posts
 * before pagination.
 */
'use strict';

var pagination = require('hexo-pagination');

// Remove the default index generator so we can replace it
hexo.extend.generator.register('index', function (locals) {
  var config = this.config;
  var indexConfig = config.index_generator || {};
  var perPage = indexConfig.per_page != null ? indexConfig.per_page : config.per_page || 10;
  var orderBy = indexConfig.order_by || '-date';
  var basePath = indexConfig.path || '';

  // Filter out Life-category posts
  var posts = locals.posts.sort(orderBy).filter(function (post) {
    var isLife = false;
    post.categories.forEach(function (cat) {
      if (cat.name === 'Life') {
        isLife = true;
      }
    });
    return !isLife;
  });

  return pagination(basePath, posts, {
    perPage: perPage,
    layout: ['index', 'archive'],
    format: perPage ? 'page/%d/' : '',
    data: {
      __index: true
    }
  });
});
