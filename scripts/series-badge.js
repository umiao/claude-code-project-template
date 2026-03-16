/**
 * Hexo theme_inject plugin: Series Badge
 * Adds a series name and position badge to post-meta on index and post pages.
 * Uses `series` and `series_index` front matter fields.
 */
'use strict';

hexo.extend.filter.register('theme_inject', function (injects) {
  injects.postMeta.raw('series-badge', `
  {% if post.series %}
    <span class="post-meta-item post-meta-series">
      <span class="post-meta-item-icon">
        <i class="fa fa-book"></i>
      </span>
      <span class="post-meta-item-text">Series:</span>
      <a href="/series/" class="series-badge" title="{{ post.series }} series{% if post.series_index %} (#{{ post.series_index }}){% endif %}">
        {{ post.series }}{% if post.series_index %} #{{ post.series_index }}{% endif %}
      </a>
    </span>
  {% endif %}
  `, {}, {});
});
